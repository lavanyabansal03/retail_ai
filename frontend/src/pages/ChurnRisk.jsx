import { useState, useEffect } from "react";
import { fetchChurn } from "../api";
import SegmentBadge from "../components/SegmentBadge";

function RiskBadge({ level }) {
  const styles = {
    High:   { background: "#fee2e2", color: "#dc2626" },
    Medium: { background: "#fef3c7", color: "#d97706" },
    Low:    { background: "#dcfce7", color: "#15803d" },
  };
  return (
    <span className="badge" style={styles[level] || styles.Low}>
      {level}
    </span>
  );
}

const fmt = (n) => n?.toLocaleString("en-GB") ?? "—";

export default function ChurnRisk() {
  const [data, setData] = useState(null);
  const [filter, setFilter] = useState("All");
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchChurn()
      .then(setData)
      .catch((e) => setError(e.message));
  }, []);

  if (error)
    return (
      <div>
        <div className="page-title">Churn risk leaderboard</div>
        <div className="error-banner">Could not reach API: {error}</div>
      </div>
    );

  if (!data) return <div className="loading">Loading churn predictions…</div>;

  const { customers, summary } = data;

  const visible = customers
    .filter((c) => filter === "All" || c.risk_level === filter)
    .slice(0, 100);

  return (
    <div>
      <div className="page-title">Churn risk leaderboard</div>
      <div className="page-subtitle">
        DNN model — customers most likely to stop buying, ranked by probability
      </div>

      {/* Summary cards */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3, 1fr)",
          gap: 14,
          marginBottom: 20,
        }}
      >
        <div className="card" style={{ borderTop: "3px solid #ef4444" }}>
          <div style={{ fontSize: 12, color: "#6b7280" }}>High risk customers</div>
          <div style={{ fontSize: 32, fontWeight: 700, color: "#ef4444", margin: "4px 0" }}>
            {fmt(summary.high_count)}
          </div>
          <div style={{ fontSize: 11, color: "#9ca3af" }}>churn prob above 70%</div>
        </div>
        <div className="card" style={{ borderTop: "3px solid #f59e0b" }}>
          <div style={{ fontSize: 12, color: "#6b7280" }}>Medium risk</div>
          <div style={{ fontSize: 32, fontWeight: 700, color: "#f59e0b", margin: "4px 0" }}>
            {fmt(summary.medium_count)}
          </div>
          <div style={{ fontSize: 11, color: "#9ca3af" }}>churn prob 40–70%</div>
        </div>
        <div className="card" style={{ borderTop: "3px solid #22c55e" }}>
          <div style={{ fontSize: 12, color: "#6b7280" }}>Low risk</div>
          <div style={{ fontSize: 32, fontWeight: 700, color: "#22c55e", margin: "4px 0" }}>
            {fmt(summary.low_count)}
          </div>
          <div style={{ fontSize: 11, color: "#9ca3af" }}>churn prob below 40%</div>
        </div>
      </div>

      {/* Table */}
      <div className="card">
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            marginBottom: 16,
          }}
        >
          <div style={{ fontSize: 14, fontWeight: 600 }}>
            Top customers at risk right now
          </div>
          {/* Filter buttons */}
          <div style={{ display: "flex", gap: 6 }}>
            {["All", "High", "Medium", "Low"].map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                style={{
                  padding: "4px 12px",
                  border: "1px solid #e5e7eb",
                  borderRadius: 6,
                  background: filter === f ? "#111827" : "#fff",
                  color: filter === f ? "#fff" : "#374151",
                  fontSize: 12,
                  cursor: "pointer",
                  fontWeight: filter === f ? 600 : 400,
                }}
              >
                {f}
              </button>
            ))}
          </div>
        </div>
        <table>
          <thead>
            <tr>
              <th>Customer ID</th>
              <th>Segment</th>
              <th>Last purchase</th>
              <th>Churn probability</th>
              <th>Risk</th>
            </tr>
          </thead>
          <tbody>
            {visible.map((c) => (
              <tr key={c.customer_id}>
                <td style={{ fontWeight: 500 }}>{c.customer_id}</td>
                <td>
                  <SegmentBadge segment={c.segment} />
                </td>
                <td style={{ color: "#6b7280" }}>{c.recency}</td>
                <td style={{ fontWeight: 600 }}>
                  {(c.churn_probability * 100).toFixed(1)}%
                </td>
                <td>
                  <RiskBadge level={c.risk_level} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
