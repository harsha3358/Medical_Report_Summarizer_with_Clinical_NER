"use client";
import { useEffect, useState } from "react";
import { HistoryItem } from "@/lib/types";
import { getHistory, clearHistory } from "@/lib/api";
import { Clock, Trash2, Search, X, ChevronLeft, ChevronRight } from "lucide-react";
import clsx from "clsx";

export default function Sidebar({
  onSelectHistory,
  collapsed,
  onToggle,
  refreshKey,
}: {
  onSelectHistory: (item: HistoryItem) => void;
  collapsed: boolean;
  onToggle: () => void;
  refreshKey: number;
}) {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchHistory = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await getHistory();
      setHistory(data);
    } catch {
      setError("History unavailable");
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchHistory();
  }, [refreshKey]);

  const handleClear = async () => {
    if (!confirm("Clear all history?")) return;
    try {
      await clearHistory();
      setHistory([]);
    } catch {
      setError("Could not clear history");
    }
  };

  const filtered = history.filter(
    (h) =>
      h.input_text.toLowerCase().includes(search.toLowerCase()) ||
      h.summary.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <aside
      className={clsx(
        "flex flex-col h-full transition-all duration-300 relative",
        collapsed ? "w-12" : "w-64"
      )}
      style={{
        background: "rgba(240,244,255,0.85)",
        backdropFilter: "blur(16px)",
        borderRight: "1px solid rgba(255,255,255,0.9)",
      }}
    >
      {/* Toggle button */}
      <button
        onClick={onToggle}
        className="absolute -right-3 top-6 z-10 w-6 h-6 rounded-full bg-white shadow-md flex items-center justify-center text-slate-500 hover:text-blue-500 transition-colors"
      >
        {collapsed ? <ChevronRight size={12} /> : <ChevronLeft size={12} />}
      </button>

      {collapsed ? (
        <div className="flex flex-col items-center pt-4 gap-4">
          <Clock size={16} className="text-slate-400" />
        </div>
      ) : (
        <>
          {/* Header */}
          <div className="p-4 pb-3">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-xs font-bold uppercase tracking-widest text-slate-500">
                History
              </h2>
              <div className="flex items-center gap-1">
                <button
                  onClick={fetchHistory}
                  className="text-slate-400 hover:text-blue-500 transition-colors p-1"
                  title="Refresh"
                >
                  <Clock size={12} />
                </button>
                {history.length > 0 && (
                  <button
                    onClick={handleClear}
                    className="text-slate-400 hover:text-rose-500 transition-colors p-1"
                    title="Clear all"
                  >
                    <Trash2 size={12} />
                  </button>
                )}
              </div>
            </div>

            {/* Search */}
            <div className="relative">
              <Search
                size={11}
                className="absolute left-2.5 top-1/2 -translate-y-1/2 text-slate-400"
              />
              <input
                type="text"
                placeholder="Search..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="w-full pl-7 pr-6 py-1.5 text-xs rounded-xl bg-white/70 border border-slate-200 focus:outline-none focus:border-blue-300 text-slate-600 placeholder:text-slate-400"
              />
              {search && (
                <button
                  onClick={() => setSearch("")}
                  className="absolute right-2 top-1/2 -translate-y-1/2 text-slate-400"
                >
                  <X size={10} />
                </button>
              )}
            </div>
          </div>

          {/* List */}
          <div className="flex-1 overflow-y-auto px-3 pb-4 space-y-2">
            {loading && (
              <p className="text-xs text-slate-400 text-center py-4">
                Loading...
              </p>
            )}
            {!loading && error && (
              <p className="text-xs text-rose-400 text-center py-4">
                {error}
              </p>
            )}
            {!loading && !error && filtered.length === 0 && (
              <p className="text-xs text-slate-400 text-center py-8">
                {history.length === 0 ? "No history yet" : "No results"}
              </p>
            )}
            {filtered.map((item) => (
              <button
                key={item.id}
                onClick={() => onSelectHistory(item)}
                className="w-full text-left p-2.5 rounded-xl bg-white/60 hover:bg-white/90 border border-transparent hover:border-blue-100 transition-all group"
              >
                <p className="text-xs font-medium text-slate-600 truncate group-hover:text-blue-600">
                  {item.input_text.slice(0, 50)}
                  {item.input_text.length > 50 ? "…" : ""}
                </p>
                <p className="text-[10px] text-slate-400 mt-0.5 truncate">
                  {item.summary.slice(0, 40)}…
                </p>
                <p className="text-[9px] text-slate-300 mt-1">
                  {new Date(item.created_at).toLocaleDateString()}
                </p>
              </button>
            ))}
          </div>
        </>
      )}
    </aside>
  );
}
