import config from "../../config.json";
import { analyzer_option } from "../../types/RestultSet";

export async function fetchAnalyzers(): Promise<analyzer_option[]> {
  const response = await fetch(config.SERVER_URL + "/api/analyzers/", {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });
  if (!response.ok) {
    throw new Error(`Failed to fetch analyzers: ${response.status}`);
  }
  return response.json();
}
