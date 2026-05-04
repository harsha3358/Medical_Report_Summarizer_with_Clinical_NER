"use client";
import { useState } from "react";
import { ChatMessage, HistoryItem } from "@/lib/types";
import { analyzeText, analyzeFile } from "@/lib/api";
import Sidebar from "@/components/Sidebar";
import ChatWindow from "@/components/ChatWindow";
import InputBar from "@/components/InputBar";
import { Trash2 } from "lucide-react";

export default function Home() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [historyRefreshKey, setHistoryRefreshKey] = useState(0);

  const addMessage = (msg: ChatMessage) => {
    setMessages((prev) => [...prev, msg]);
  };

  const handleSend = async (text: string, file?: File) => {
    if (loading) return;

    // User message
    const userMsg: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: text,
      timestamp: new Date(),
      isFile: !!file,
      fileName: file?.name,
    };
    addMessage(userMsg);

    // Loading indicator
    const loadingId = crypto.randomUUID();
    addMessage({ id: loadingId, role: "loading", timestamp: new Date() });
    setLoading(true);

    try {
      const result = file
        ? await analyzeFile(file)
        : await analyzeText(text);
      setHistoryRefreshKey((key) => key + 1);

      // Remove loading, add result
      setMessages((prev) => {
        const without = prev.filter((m) => m.id !== loadingId);
        const aiMsg: ChatMessage = {
          id: crypto.randomUUID(),
          role: "assistant",
          content: text,
          result,
          timestamp: new Date(),
        };
        return [...without, aiMsg];
      });
    } catch (err) {
      setMessages((prev) => {
        const without = prev.filter((m) => m.id !== loadingId);
        const errMsg: ChatMessage = {
          id: crypto.randomUUID(),
          role: "assistant",
          content: "⚠️ Could not reach the backend. Make sure it's running at the configured API URL.",
          timestamp: new Date(),
        };
        return [...without, errMsg];
      });
    }

    setLoading(false);
  };

  const handleHistorySelect = (item: HistoryItem) => {
    let parsedEntities = { disease: [], drug: [], symptom: [], treatment: [] };
    try {
      parsedEntities = { ...parsedEntities, ...JSON.parse(item.entities) };
    } catch {}

    const userMsg: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: item.input_text,
      timestamp: new Date(item.created_at),
    };
    const aiMsg: ChatMessage = {
      id: crypto.randomUUID(),
      role: "assistant",
      content: item.input_text,
      result: {
        clinical_summary: item.summary,
        entities: parsedEntities,
        confidence: 0,
        disclaimer: "AI-generated summary. Not a medical diagnosis.",
      },
      timestamp: new Date(item.created_at),
    };
    setMessages([userMsg, aiMsg]);
  };

  return (
    <div className="relative z-10 flex h-screen overflow-hidden">
      {/* Sidebar */}
      <Sidebar
        onSelectHistory={handleHistorySelect}
        collapsed={sidebarCollapsed}
        onToggle={() => setSidebarCollapsed((v) => !v)}
        refreshKey={historyRefreshKey}
      />

      {/* Main chat area */}
      <main className="flex flex-col flex-1 min-w-0 h-full">
        {/* Top bar */}
        <header
          className="flex items-center justify-between px-5 py-3 flex-shrink-0"
          style={{
            background: "rgba(255,255,255,0.6)",
            backdropFilter: "blur(12px)",
            borderBottom: "1px solid rgba(255,255,255,0.9)",
          }}
        >
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-[#7dd3fc] to-[#38bdf8] flex items-center justify-center shadow-sm">
              <span className="text-white text-[11px] font-bold">M</span>
            </div>
            <div>
              <h1 className="text-sm font-bold text-slate-700 leading-none">
                MedAI
              </h1>
              <p className="text-[10px] text-slate-400 leading-none mt-0.5">
                Clinical Report Assistant
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            {messages.length > 0 && (
              <button
                onClick={() => setMessages([])}
                className="btn-ghost-water flex items-center gap-1.5 px-3 py-1.5"
              >
                <Trash2 size={12} />
                Clear chat
              </button>
            )}
            <div className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl bg-emerald-50 border border-emerald-100">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              <span className="text-[10px] font-medium text-emerald-600">
                distilbart-cnn
              </span>
            </div>
          </div>
        </header>

        {/* Chat window */}
        <ChatWindow
          messages={messages}
          onSuggestion={(text) => handleSend(text)}
        />

        {/* Input bar */}
        <div className="flex-shrink-0">
          <InputBar onSend={handleSend} disabled={loading} />
        </div>
      </main>
    </div>
  );
}
