import { useState, useEffect } from "react";
import { fetchRecommendations } from "../api";

function ProductPill({ name }) {
  return (
    <span
      style={{
        display: "inline-block",
        background: "#dbeafe",
        color: "#1d4ed8",
        border: "1px solid #bfdbfe",
        borderRadius: 6,
        padding: "3px 10px",
        fontSize: 12,
        margin: "3px 4px 3px 0",
        fontWeight: 500,
      }}
    >
      {name}
    </span>
  );
}

export default function Recommendations() {
  const [rules, setRules] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchRecommendations()
      .then(setRules)
      .catch((e) => setError(e.message));
  }, []);

  if (error)
    return (
      <div>
        <div className="page-title">Product recommendations</div>
        <div className="error-banner">Could not reach API: {error}</div>
      </div>
    );

  if (!rules.length) return <div className="loading">Loading recommendations…</div>;

  return (
    <div>
      <div className="page-title">Product recommendations</div>
      <div className="page-subtitle">
        Apriori association rules — what each customer is likely to buy based on past purchases
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        {rules.map((rule, i) => (
          <div key={i} className="card">
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "flex-start",
                gap: 16,
              }}
            >
              {/* Left — products */}
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 11, color: "#9ca3af", marginBottom: 4, fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.05em" }}>
                  Usually bought together
                </div>
                <div style={{ marginBottom: 10 }}>
                  {rule.antecedents.map((p, j) => (
                    <span key={j} style={{ fontWeight: 500, color: "#374151", fontSize: 13 }}>
                      {j > 0 ? <span style={{ color: "#9ca3af", margin: "0 4px" }}>+</span> : null}
                      {p}
                    </span>
                  ))}
                </div>
                <div style={{ fontSize: 11, color: "#9ca3af", marginBottom: 6, fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.05em" }}>
                  Apriori recommends
                </div>
                <div>
                  {rule.consequents.map((p, j) => (
                    <ProductPill key={j} name={p} />
                  ))}
                </div>
              </div>

              {/* Right — metrics */}
              <div style={{ textAlign: "right", flexShrink: 0 }}>
                <div
                  style={{
                    background: "#f0fdf4",
                    color: "#15803d",
                    border: "1px solid #bbf7d0",
                    borderRadius: 6,
                    padding: "4px 12px",
                    fontSize: 13,
                    fontWeight: 700,
                    marginBottom: 6,
                  }}
                >
                  {rule.confidence}% confidence
                </div>
                <div style={{ fontSize: 11, color: "#9ca3af" }}>
                  lift {rule.lift}
                </div>
                <div style={{ fontSize: 11, color: "#9ca3af" }}>
                  support {rule.support}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
