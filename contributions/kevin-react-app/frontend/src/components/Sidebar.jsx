const NAV = [
  {
    section: "OVERVIEW",
    items: [
      { id: "dashboard",       label: "Dashboard",           icon: "⊞" },
      { id: "segments",        label: "Segments",             icon: "◎" },
    ],
  },
  {
    section: "PREDICTIONS",
    items: [
      { id: "churn",           label: "Churn risk",           icon: "⚠" },
      { id: "nextPurchase",    label: "Next purchase",        icon: "☰" },
      { id: "recommendations", label: "Recommendations",      icon: "◈" },
    ],
  },
  {
    section: "ACTIONS",
    items: [
      { id: "offers",          label: "Personalized offers",  icon: "✉" },
      { id: "anomaly",         label: "Anomaly alerts",       icon: "ⓘ" },
    ],
  },
];

export default function Sidebar({ active, onNav }) {
  return (
    <aside
      style={{
        width: 220,
        minHeight: "100vh",
        background: "#fff",
        borderRight: "1px solid #e5e7eb",
        display: "flex",
        flexDirection: "column",
        flexShrink: 0,
      }}
    >
      {/* Branding */}
      <div style={{ padding: "22px 20px 20px", borderBottom: "1px solid #f3f4f6" }}>
        <div style={{ fontWeight: 700, fontSize: 15, color: "#111827" }}>
          Customer Analyzer
        </div>
        <div style={{ fontSize: 12, color: "#6b7280", marginTop: 3 }}>
          UK Retail · 5,878 customers
        </div>
      </div>

      {/* Nav */}
      <nav style={{ flex: 1, paddingTop: 12 }}>
        {NAV.map(({ section, items }) => (
          <div key={section} style={{ marginBottom: 6 }}>
            <div
              style={{
                padding: "6px 20px 4px",
                fontSize: 10,
                fontWeight: 700,
                color: "#9ca3af",
                letterSpacing: "0.08em",
                textTransform: "uppercase",
              }}
            >
              {section}
            </div>
            {items.map(({ id, label, icon }) => {
              const isActive = active === id;
              return (
                <button
                  key={id}
                  onClick={() => onNav(id)}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 9,
                    width: "100%",
                    padding: "8px 20px",
                    border: "none",
                    borderLeft: isActive ? "3px solid #2563eb" : "3px solid transparent",
                    background: isActive ? "#eff6ff" : "transparent",
                    color: isActive ? "#2563eb" : "#374151",
                    fontWeight: isActive ? 600 : 400,
                    fontSize: 13,
                    cursor: "pointer",
                    textAlign: "left",
                    transition: "background 0.12s",
                  }}
                >
                  <span style={{ fontSize: 14, opacity: 0.8 }}>{icon}</span>
                  {label}
                </button>
              );
            })}
          </div>
        ))}
      </nav>
    </aside>
  );
}
