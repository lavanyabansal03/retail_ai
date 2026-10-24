import { useState, useEffect } from "react";
import { fetchSegments } from "../api";
import SegmentBadge from "../components/SegmentBadge";

const ORDER = ["Champions", "Loyal Customers", "At Risk", "Lost Customers"];

const CARD_THEME = {
  Champions:        { bg: "#eff6ff", border: "#bfdbfe", nameColor: "#1d4ed8" },
  "Loyal Customers": { bg: "#f0fdf4", border: "#bbf7d0", nameColor: "#15803d" },
  "At Risk":         { bg: "#fffbeb", border: "#fde68a", nameColor: "#d97706" },
  "Lost Customers":  { bg: "#fef2f2", border: "#fecaca", nameColor: "#dc2626" },
};

const ACTION_COLOR = {
  Champions:        "#1d4ed8",
  "Loyal Customers": "#15803d",
  "At Risk":         "#d97706",
  "Lost Customers":  "#dc2626",
};

const fmt = (n) => n?.toLocaleString("en-GB") ?? "—";

export default function Segments() {
  const [segments, setSegments] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchSegments()
      .then(setSegments)
      .catch((e) => setError(e.message));
  }, []);

  if (error)
    return (
      <div>
        <div className="page-title">Customer segments</div>
        <div className="error-banner">Could not reach API: {error}</div>
      </div>
    );

  if (!segments.length) return <div className="loading">Loading segments…</div>;

  const sorted = [...segments].sort(
    (a, b) => ORDER.indexOf(a.segment) - ORDER.indexOf(b.segment)
  );

  return (
    <div>
      <div className="page-title">Customer segments</div>
      <div className="page-subtitle">
        KMeans clustering on RFM scores — who are your customers?
      </div>

      {/* 2 × 2 cards */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: 14,
          marginBottom: 20,
        }}
      >
        {sorted.map((seg) => {
          const theme = CARD_THEME[seg.segment] || CARD_THEME.Champions;
          return (
            <div
              key={seg.segment}
              style={{
                background: theme.bg,
                border: `1px solid ${theme.border}`,
                borderRadius: 12,
                padding: "20px 24px",
              }}
            >
              <div
                style={{
                  color: theme.nameColor,
                  fontWeight: 600,
                  fontSize: 14,
                  marginBottom: 8,
                }}
              >
                {seg.segment}
              </div>
              <div
                style={{
                  fontSize: 38,
                  fontWeight: 700,
                  color: "#111827",
                  lineHeight: 1,
                  marginBottom: 10,
                }}
              >
                {fmt(seg.count)}
              </div>
              <div style={{ fontSize: 12, color: "#6b7280" }}>
                {seg.pct_of_total}% · Recency avg {Math.round(seg.avg_recency)} days · Spend avg £
                {fmt(Math.round(seg.avg_monetary))}
              </div>
            </div>
          );
        })}
      </div>

      {/* Breakdown table */}
      <div className="card">
        <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 16 }}>
          Segment breakdown with recommended actions
        </div>
        <table>
          <thead>
            <tr>
              <th>Segment</th>
              <th>Customers</th>
              <th>Avg recency</th>
              <th>Avg spend</th>
              <th>Recommended action</th>
            </tr>
          </thead>
          <tbody>
            {sorted.map((seg) => (
              <tr key={seg.segment}>
                <td>
                  <SegmentBadge segment={seg.segment} />
                </td>
                <td>{fmt(seg.count)}</td>
                <td>{Math.round(seg.avg_recency)} days</td>
                <td>£{fmt(Math.round(seg.avg_monetary))}</td>
                <td
                  style={{
                    color: ACTION_COLOR[seg.segment],
                    fontWeight: 500,
                  }}
                >
                  {seg.recommended_action}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
