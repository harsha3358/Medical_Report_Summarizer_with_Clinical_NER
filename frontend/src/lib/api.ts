import { AnalyzeResponse, HistoryItem } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:10000";

export async function analyzeText(text: string): Promise<AnalyzeResponse> {
  const form = new FormData();
  form.append("text", text);
  const res = await fetch(`${API_URL}/analyze`, { method: "POST", body: form });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function analyzeFile(file: File): Promise<AnalyzeResponse> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API_URL}/analyze`, { method: "POST", body: form });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getHistory(): Promise<HistoryItem[]> {
  const res = await fetch(`${API_URL}/history`);
  if (!res.ok) throw new Error("Failed to fetch history");
  const data = await res.json();
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.value)) return data.value;
  return [];
}

export async function clearHistory(): Promise<void> {
  const res = await fetch(`${API_URL}/history/clear`, { method: "DELETE" });
  if (!res.ok) throw new Error("Failed to clear history");
}
