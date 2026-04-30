const BASE = "/api";

async function get(path) {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

export const fetchDashboard = () => get("/dashboard");
export const fetchSegments = () => get("/segments");
export const fetchChurn = () => get("/churn");
export const fetchNextPurchase = () => get("/next-purchase");
export const fetchRecommendations = () => get("/recommendations");
export const fetchRFM = () => get("/rfm");
