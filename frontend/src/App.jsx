import { useState } from "react";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import Segments from "./pages/Segments";
import ChurnRisk from "./pages/ChurnRisk";
import NextPurchase from "./pages/NextPurchase";
import Recommendations from "./pages/Recommendations";
import PersonalizedOffers from "./pages/PersonalizedOffers";

function AnomalyPlaceholder() {
  return (
    <div>
      <div className="page-title">Anomaly alerts</div>
      <div className="page-subtitle">Autoencoder-based anomaly detection</div>
      <div className="card" style={{ textAlign: "center", padding: 60, color: "#9ca3af" }}>
        Coming soon — autoencoder model integration
      </div>
    </div>
  );
}

const PAGES = {
  dashboard: Dashboard,
  segments: Segments,
  churn: ChurnRisk,
  nextPurchase: NextPurchase,
  recommendations: Recommendations,
  offers: PersonalizedOffers,
  anomaly: AnomalyPlaceholder,
};

export default function App() {
  const [active, setActive] = useState("dashboard");
  const Page = PAGES[active] || Dashboard;

  return (
    <div style={{ display: "flex", minHeight: "100vh", width: "100%" }}>
      <Sidebar active={active} onNav={setActive} />
      <main
        style={{
          flex: 1,
          padding: "28px 32px",
          overflowY: "auto",
          minWidth: 0,
        }}
      >
        <Page />
      </main>
    </div>
  );
}
