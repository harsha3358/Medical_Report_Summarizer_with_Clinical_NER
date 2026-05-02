"use client";
import { AnalyzeResponse } from "@/lib/types";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";

const COLORS = ["#fb7185", "#4f8ef7", "#fbbf24"];

function StatCard({
  label,
  value,
  sub,
}: {
  label: string;
  value: string | number;
  sub?: string;
}) {
  return (
    <div className="glass rounded-2xl p-3 text-center">
      <p className="text-[10px] uppercase tracking-widest text-slate-400 mb-1">
        {label}
      </p>
      <p className="text-xl font-bold text-slate-700">{value}</p>
      {sub && <p className="text-[10px] text-slate-400 mt-0.5">{sub}</p>}
    </div>
  );
}

export default function AnalyticsPanel({
  result,
  inputText,
}: {
  result: AnalyzeResponse;
  inputText: string;
}) {
  const inputLen = inputText.length;
  const summaryLen = result.bart_summary.length;
  const compressionRatio =
    inputLen > 0 ? ((1 - summaryLen / inputLen) * 100).toFixed(0) : "0";
  const entityCount =
    result.entities.disease.length +
    result.entities.drug.length +
    result.entities.symptom.length +
    (result.entities.treatment?.length ?? 0);

  const pieData = [
    { name: "Disease",   value: result.entities.disease.length },
    { name: "Drug",      value: result.entities.drug.length },
    { name: "Symptom",   value: result.entities.symptom.length },
    { name: "Treatment", value: result.entities.treatment?.length ?? 0 },
  ].filter((d) => d.value > 0);

  const barData = [
    { name: "BART", length: summaryLen, fill: "#4f8ef7" },
    { name: "LSTM", length: result.lstm_summary.length, fill: "#a78bfa" },
  ];

  return (
    <div className="space-y-4">
      {/* Stat row */}
      <div className="grid grid-cols-2 gap-2">
        <StatCard label="Input" value={inputLen} sub="chars" />
        <StatCard label="Summary" value={summaryLen} sub="chars" />
        <StatCard label="Compressed" value={`${compressionRatio}%`} sub="reduction" />
        <StatCard label="Entities" value={entityCount} sub="detected" />
      </div>

      {/* Bar chart — model comparison */}
      {summaryLen > 0 && (
        <div className="glass rounded-2xl p-3">
          <p className="text-[10px] uppercase tracking-widest text-slate-400 mb-3 font-semibold">
            📊 Model Output Length
          </p>
          <ResponsiveContainer width="100%" height={100}>
            <BarChart data={barData} margin={{ top: 0, right: 0, bottom: 0, left: -20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="name" tick={{ fontSize: 11, fill: "#94a3b8" }} />
              <YAxis tick={{ fontSize: 10, fill: "#94a3b8" }} />
              <Tooltip
                contentStyle={{
                  background: "rgba(255,255,255,0.9)",
                  border: "none",
                  borderRadius: 8,
                  fontSize: 11,
                }}
              />
              <Bar dataKey="length" radius={[4, 4, 0, 0]}>
                {barData.map((entry, i) => (
                  <Cell key={i} fill={entry.fill} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Pie chart — entity distribution */}
      {pieData.length > 0 && (
        <div className="glass rounded-2xl p-3">
          <p className="text-[10px] uppercase tracking-widest text-slate-400 mb-3 font-semibold">
            🧬 Entity Distribution
          </p>
          <ResponsiveContainer width="100%" height={120}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                innerRadius={30}
                outerRadius={50}
                paddingAngle={3}
                dataKey="value"
              >
                {pieData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  background: "rgba(255,255,255,0.9)",
                  border: "none",
                  borderRadius: 8,
                  fontSize: 11,
                }}
              />
            </PieChart>
          </ResponsiveContainer>
          <div className="flex justify-center gap-4 flex-wrap mt-1">
            {pieData.map((d, i) => (
              <span key={i} className="flex items-center gap-1 text-[10px] text-slate-500">
                <span
                  className="w-2 h-2 rounded-full"
                  style={{ background: COLORS[i] }}
                />
                {d.name} ({d.value})
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
