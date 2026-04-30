"use client";
import { useState } from "react";
import { ChatMessage } from "@/lib/types";
import EntityChips from "./EntityChips";
import AnalyticsPanel from "./AnalyticsPanel";
import { Download, ChevronDown, ChevronUp, FileText } from "lucide-react";

function TypingDots() {
  return (
    <div className="flex items-center gap-1.5 px-4 py-3">
      <span className="typing-dot" />
      <span className="typing-dot" />
      <span className="typing-dot" />
    </div>
  );
}

function downloadText(content: string, filename: string) {
  const blob = new Blob([content], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

export default function MessageBubble({ message }: { message: ChatMessage }) {
  const [showLSTM, setShowLSTM] = useState(false);
  const [showAnalytics, setShowAnalytics] = useState(false);

  // Loading bubble
  if (message.role === "loading") {
    return (
      <div className="chat-message flex items-end gap-2 mb-4">
        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#7dd3fc] to-[#38bdf8] shadow-sm flex items-center justify-center text-white text-xs font-bold flex-shrink-0">
          AI
        </div>
        <div className="glass rounded-2xl rounded-bl-sm max-w-[80px]">
          <TypingDots />
        </div>
      </div>
    );
  }

  // User bubble
  if (message.role === "user") {
    return (
      <div className="chat-message flex justify-end mb-4">
        <div className="max-w-[75%]">
          {message.isFile ? (
            <div className="bg-gradient-to-br from-[#38bdf8] to-[#0ea5e9] text-white rounded-2xl rounded-br-sm px-4 py-3 flex items-center gap-2 shadow-md">
              <FileText size={16} />
              <span className="text-sm font-medium">{message.fileName}</span>
            </div>
          ) : (
            <div className="bg-gradient-to-br from-[#38bdf8] to-[#0ea5e9] text-white rounded-2xl rounded-br-sm px-4 py-3 shadow-md">
              <p className="text-sm leading-relaxed whitespace-pre-wrap break-words">
                {message.content}
              </p>
            </div>
          )}
          <p className="text-[10px] text-slate-400 text-right mt-1 mr-1">
            {message.timestamp.toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            })}
          </p>
        </div>
      </div>
    );
  }

  // AI result bubble
  const { result } = message;
  if (!result) return null;

  const inputText = message.content || "";
  const entities = typeof result.entities === "string"
    ? JSON.parse(result.entities)
    : result.entities;
  const safeEntities = {
    disease: entities?.disease ?? [],
    drug: entities?.drug ?? [],
    symptom: entities?.symptom ?? [],
  };
  const entityCount =
    safeEntities.disease.length +
    safeEntities.drug.length +
    safeEntities.symptom.length;

  return (
    <div className="chat-message flex items-start gap-2 mb-4">
      {/* Avatar */}
      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#7dd3fc] to-[#38bdf8] shadow-sm flex items-center justify-center text-white text-xs font-bold flex-shrink-0 mt-1">
        AI
      </div>

      <div className="flex-1 min-w-0 space-y-3 max-w-[90%]">
        {/* BART Summary card */}
        <div className="glass rounded-2xl rounded-tl-sm p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[10px] uppercase tracking-widest font-semibold text-blue-500">
              🧠 AI Summary
            </span>
            <button
              onClick={() =>
                downloadText(result.bart_summary, "summary.txt")
              }
              className="text-slate-400 hover:text-blue-500 transition-colors"
              title="Download summary"
            >
              <Download size={13} />
            </button>
          </div>
          <p className="text-sm text-slate-700 leading-relaxed">
            {result.bart_summary || (
              <span className="italic text-slate-400">No summary generated.</span>
            )}
          </p>
        </div>

        {/* LSTM baseline — collapsible */}
        {result.lstm_summary && (
          <div className="glass rounded-2xl p-3">
            <button
              onClick={() => setShowLSTM(!showLSTM)}
              className="w-full flex items-center justify-between text-left"
            >
              <span className="text-[10px] uppercase tracking-widest font-semibold text-purple-500">
                ⚡ LSTM Baseline
              </span>
              {showLSTM ? (
                <ChevronUp size={13} className="text-slate-400" />
              ) : (
                <ChevronDown size={13} className="text-slate-400" />
              )}
            </button>
            {showLSTM && (
              <p className="text-xs text-slate-500 leading-relaxed mt-2 pt-2 border-t border-slate-100">
                {result.lstm_summary}
              </p>
            )}
          </div>
        )}

        {/* Entities card */}
        <div className="glass rounded-2xl p-4">
          <p className="text-[10px] uppercase tracking-widest font-semibold text-teal-500 mb-3">
            🧬 Clinical Entities
            {entityCount > 0 && (
              <span className="ml-2 bg-teal-100 text-teal-600 px-1.5 py-0.5 rounded-full text-[9px]">
                {entityCount}
              </span>
            )}
          </p>
          <EntityChips entities={safeEntities} />
        </div>

        {/* Analytics — collapsible */}
        <div className="glass rounded-2xl p-3">
          <button
            onClick={() => setShowAnalytics(!showAnalytics)}
            className="w-full flex items-center justify-between text-left"
          >
            <span className="text-[10px] uppercase tracking-widest font-semibold text-slate-500">
              📊 Analytics
            </span>
            {showAnalytics ? (
              <ChevronUp size={13} className="text-slate-400" />
            ) : (
              <ChevronDown size={13} className="text-slate-400" />
            )}
          </button>
          {showAnalytics && (
            <div className="mt-3">
              <AnalyticsPanel result={result} inputText={inputText} />
            </div>
          )}
        </div>

        <p className="text-[10px] text-slate-400 ml-1">
          {message.timestamp.toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </p>
      </div>
    </div>
  );
}
