"use client";
import { useEffect, useRef } from "react";
import { ChatMessage } from "@/lib/types";
import MessageBubble from "./MessageBubble";
import { Stethoscope } from "lucide-react";

const SUGGESTIONS = [
  "Patient has fever, fatigue and is on aspirin and metformin.",
  "Diabetes patient with insulin resistance and frequent urination.",
  "Post-op cancer patient experiencing pain and fatigue.",
];

export default function ChatWindow({
  messages,
  onSuggestion,
}: {
  messages: ChatMessage[];
  onSuggestion: (text: string) => void;
}) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  if (messages.length === 0) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center px-6 py-12 overflow-y-auto">
        {/* Hero */}
        <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center shadow-lg mb-5">
          <Stethoscope size={28} className="text-white" />
        </div>
        <h1 className="text-2xl font-bold text-slate-700 mb-2">MedAI Assistant</h1>
        <p className="text-sm text-slate-500 text-center max-w-sm mb-8 leading-relaxed">
          Paste a clinical report or patient note to get an AI-powered summary,
          entity extraction, and insights.
        </p>

        {/* Suggestions */}
        <div className="w-full max-w-md space-y-2">
          <p className="text-[10px] uppercase tracking-widest text-slate-400 text-center mb-3">
            Try an example
          </p>
          {SUGGESTIONS.map((s, i) => (
            <button
              key={i}
              onClick={() => onSuggestion(s)}
              className="w-full text-left px-4 py-3 rounded-2xl glass text-sm text-slate-600 hover:text-blue-600 hover:border-blue-200 border border-transparent transition-all leading-relaxed"
            >
              {s}
            </button>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto px-4 md:px-8 py-6">
      <div className="max-w-2xl mx-auto">
        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}
