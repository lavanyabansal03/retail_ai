import { useState, useEffect } from "react";
import { fetchChurn, fetchNextPurchase } from "../api";
import SegmentBadge from "../components/SegmentBadge";

const OFFER = {
  Champions:
    "You're one of our best customers! Here's an exclusive loyalty reward just for you...",
  "At Risk":
    "We miss you! Here's a special win-back offer just for you — don't let it expire.",
  "Lost Customers":
    "It's been a while. Come back with 30% off your next order. We'd love to see you again.",
  "Loyal Customers":
    "As a valued customer, get early access to our new collection before anyone else.",
};

const OFFER_COLOR = {
  Champions:        { bg: "#eff6ff", border: "#bfdbfe", text: "#1d4ed8" },
  "Loyal Customers": { bg: "#f0fdf4", border: "#bbf7d0", text: "#15803d" },
  "At Risk":         { bg: "#fffbeb", border: "#fde68a", text: "#b45309" },
  "Lost Customers":  { bg: "#fef2f2", border: "#fecaca", text: "#dc2626" },
};

function RiskPill({ level }) {
  const styles = {
    High:   { background: "#fee2e2", color: "#dc2626" },
    Medium: { background: "#fef3c7", color: "#d97706" },
    Low:    { background: "#dcfce7", color: "#15803d" },
  };
  return (
    <span className="badge" style={styles[level] || styles.Low}>
      {level} risk
    </span>
  );
}

export default function PersonalizedOffers() {
  const [offers, setOffers] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([fetchChurn(), fetchNextPurchase()])
      .then(([churnData, purchaseData]) => {
        const purchaseMap = {};
        [...(purchaseData.upcoming || [])].forEach((c) => {
          purchaseMap[c.customer_id] = c.predicted_days;
        });

        const top15 = churnData.customers.slice(0, 15).map((c) => ({
          ...c,
          predicted_days: purchaseMap[c.customer_id] ?? null,
          offer: OFFER[c.segment] || OFFER["At Risk"],
        }));

        setOffers(top15);
      })
      .catch((e) => setError(e.message));
  }, []);

  if (error)
    return (
      <div>
        <div className="page-title">Personalized offers</div>
        <div className="error-banner">Could not reach API: {error}</div>
      </div>
    );

  if (!offers.length)
    return <div className="loading">Building personalized offers…</div>;

  return (
    <div>
      <div className="page-title">Personalized offers</div>
      <div className="page-subtitle">
        Top 15 highest-risk customers — AI-generated offers based on segment + churn probability
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        {offers.map((c) => {
          const theme = OFFER_COLOR[c.segment] || OFFER_COLOR["At Risk"];
          return (
            <div key={c.customer_id} className="card">
              {/* Header row */}
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 10,
                  marginBottom: 8,
                  flexWrap: "wrap",
                }}
              >
                <span style={{ fontSize: 15, fontWeight: 700 }}>
                  Customer {c.customer_id}
                </span>
                <SegmentBadge segment={c.segment} />
                <RiskPill level={c.risk_level} />
              </div>

              {/* Stats row */}
              <div
                style={{
                  fontSize: 12,
                  color: "#6b7280",
                  marginBottom: 12,
                  display: "flex",
                  gap: 20,
                  flexWrap: "wrap",
                }}
              >
                <span>Last purchase: {c.recency}</span>
                <span>
                  Churn prob:{" "}
                  <strong style={{ color: "#ef4444" }}>
                    {(c.churn_probability * 100).toFixed(1)}%
                  </strong>
                </span>
                {c.predicted_days !== null && (
                  <span>
                    Next purchase in:{" "}
                    <strong style={{ color: "#374151" }}>
                      {Math.round(c.predicted_days)} days
                    </strong>
                  </span>
                )}
              </div>

              {/* Offer message */}
              <div
                style={{
                  background: theme.bg,
                  border: `1px solid ${theme.border}`,
                  borderRadius: 8,
                  padding: "10px 14px",
                  fontSize: 13,
                  color: theme.text,
                  fontStyle: "italic",
                  lineHeight: 1.5,
                }}
              >
                "{c.offer}"
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
