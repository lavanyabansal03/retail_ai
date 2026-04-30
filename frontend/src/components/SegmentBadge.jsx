const STYLES = {
  Champions:        { background: "#dbeafe", color: "#1d4ed8" },
  "Loyal Customers": { background: "#dcfce7", color: "#15803d" },
  "At Risk":         { background: "#fef3c7", color: "#d97706" },
  "Lost Customers":  { background: "#fee2e2", color: "#dc2626" },
};

export default function SegmentBadge({ segment }) {
  const s = STYLES[segment] || { background: "#f3f4f6", color: "#374151" };
  return (
    <span className="badge" style={s}>
      {segment}
    </span>
  );
}
