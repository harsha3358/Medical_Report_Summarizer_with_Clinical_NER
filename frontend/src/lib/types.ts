export interface Entities {
  disease:   string[];
  drug:      string[];
  symptom:   string[];
  treatment: string[];   // added — NLP Objective requires TREATMENT extraction
}

export interface AnalyzeResponse {
  clinical_summary: string;
  lstm_summary?: string;
  entities: Entities;
  confidence: number;
  disclaimer: string;
  error?: string;
}

export interface HistoryItem {
  id: number;
  input_text: string;
  summary: string;
  entities: string; // JSON string
  created_at: string;
}

export type MessageRole = "user" | "assistant" | "loading";

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content?: string;
  inputText?: string;
  result?: AnalyzeResponse;
  timestamp: Date;
  isFile?: boolean;
  fileName?: string;
}
