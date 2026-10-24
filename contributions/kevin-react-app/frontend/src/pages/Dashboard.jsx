import { useState, useEffect } from "react";
import {
  PieChart, Pie, Cell, BarChart, Bar,
  XAxis, YAxis, Tooltip, ResponsiveContainer, Legend,
} from "recharts";
import { fetchDashboard, fetchSegments, fetchRFM } from "../api";

const SEG_COLORS = {
  Champions: "#3b82f6",
  "Loyal Customers": "#22c55e",
  "At Risk": "#f59e0b",
  "Lost Customers": "#ef4444",
};

function KPICard({ title, value, subtitle, valueColor }) {
  return (
    <div className="card">
      <div style={{ fontSize: 12, color: "#6b7280", marginBottom: 6 }}>{title}</div>
      <div style={{ fontSize: 28, fontWeight: 700, color: valueColor || "#111827", lineHeight: 1.1 }}>
        {value}
      </div>
      <div style={{ fontSize: 11, color: "#9ca3af", marginTop: 5 }}>{subtitle}</div>
    </div>
  );
}

const fmt = (n) => n?.toLocaleString("en-GB") ?? "—";

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [segments, setSegments] = useState([]);
  const [rfm, setRfm] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([fetchDashboard(), fetchSegments(), fetchRFM()])
      .then(([s, segs, r]) => {
        setStats(s);
        setSegments(segs);
        setRfm(r);
      })
      .catch((e) => setError(e.message));
  }, []);

  if (error)
    return (
      <div>
        <div className="page-title">Dashboard</div>
        <div className="error-banner">Could not reach API: {error}</div>
      </div>
    );

  if (!stats) return <div className="loading">Loading dashboard…</div>;

  const pieData = segments.map((s) => ({ name: s.segment, value: s.count }));

  const rfmBarData = rfm
    ? Object.entries(rfm.total_score_dist).map(([k, v]) => ({ score: k, count: v }))
    : [];

  const churnCount = Math.round((stats.total_customers * stats.churn_rate) / 100);

  return (
    <div>
      <div className="page-title">Dashboard</div>
      <div className="page-subtitle">Business overview — UK Retail</div>

      {/* KPI cards */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(4, 1fr)",
          gap: 14,
          marginBottom: 20,
        }}
      >
        <KPICard
          title="Total customers"
          value={fmt(stats.total_customers)}
          subtitle="unique buyers"
        />
        <KPICard
          title="Total revenue"
          value={`£${(stats.total_revenue / 1e6).toFixed(1)}M`}
          subtitle="all transactions"
        />
        <KPICard
          title="Churn risk"
          value={`${stats.churn_rate}%`}
          subtitle={`${fmt(churnCount)} customers`}
          valueColor="#ef4444"
        />
        <KPICard
          title="Avg order value"
          value={`£${fmt(Math.round(stats.avg_order_value))}`}
          subtitle="per transaction"
        />
      </div>

      {/* Charts row */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
        {/* Segment donut */}
        <div className="card">
          <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 12 }}>
            Customer segments
          </div>
          <ResponsiveContainer width="100%" height={260}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                innerRadius={55}
                outerRadius={95}
                paddingAngle={3}
                dataKey="value"
              >
                {pieData.map((entry) => (
                  <Cell key={entry.name} fill={SEG_COLORS[entry.name] || "#8884d8"} />
                ))}
              </Pie>
              <Tooltip formatter={(v) => fmt(v)} />
              <Legend
                formatter={(val) => (
                  <span style={{ fontSize: 12, color: "#374151" }}>{val}</span>
                )}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* RFM score distribution */}
        <div className="card">
          <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 12 }}>
            RFM Total Score Distribution
          </div>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={rfmBarData} margin={{ left: -10 }}>
              <XAxis dataKey="score" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip formatter={(v) => [fmt(v), "Customers"]} />
              <Bar dataKey="count" fill="#6366f1" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Segment summary row */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(4, 1fr)",
          gap: 14,
          marginTop: 14,
        }}
      >
        {segments
          .sort(
            (a, b) =>
              ["Champions", "Loyal Customers", "At Risk", "Lost Customers"].indexOf(a.segment) -
              ["Champions", "Loyal Customers", "At Risk", "Lost Customers"].indexOf(b.segment)
          )
          .map((seg) => (
            <div
              key={seg.segment}
              className="card"
              style={{ borderTop: `3px solid ${SEG_COLORS[seg.segment] || "#9ca3af"}` }}
            >
              <div style={{ fontSize: 12, color: SEG_COLORS[seg.segment], fontWeight: 600 }}>
                {seg.segment}
              </div>
              <div style={{ fontSize: 22, fontWeight: 700, margin: "4px 0" }}>
                {fmt(seg.count)}
              </div>
              <div style={{ fontSize: 11, color: "#9ca3af" }}>
                {seg.pct_of_total}% of customers
              </div>
            </div>
          ))}
      </div>
    </div>
  );
}
