"use client";
import { Entities } from "@/lib/types";

const CHIP_CONFIG = {
  disease: {
    label: "Disease",
    dot: "bg-rose-400",
    chip: "chip-disease",
    icon: "🔴",
  },
  drug: {
    label: "Drug",
    dot: "bg-blue-400",
    chip: "chip-drug",
    icon: "🔵",
  },
  symptom: {
    label: "Symptom",
    dot: "bg-yellow-400",
    chip: "chip-symptom",
    icon: "🟡",
  },
};

export default function EntityChips({ entities }: { entities: Entities }) {
  const total =
    entities.disease.length + entities.drug.length + entities.symptom.length;

  if (total === 0) {
    return (
      <p className="text-xs text-slate-400 italic">No entities detected.</p>
    );
  }

  return (
    <div className="space-y-3">
      {/* Summary counts */}
      <div className="flex gap-3 flex-wrap">
        {(["disease", "drug", "symptom"] as const).map((type) => {
          const count = entities[type].length;
          if (count === 0) return null;
          const cfg = CHIP_CONFIG[type];
          return (
            <span
              key={type}
              className="text-xs font-medium text-slate-500 flex items-center gap-1"
            >
              <span className={`w-2 h-2 rounded-full inline-block ${cfg.dot}`} />
              {count} {cfg.label}
              {count > 1 ? "s" : ""}
            </span>
          );
        })}
      </div>

      {/* Chips by category */}
      {(["disease", "drug", "symptom"] as const).map((type) => {
        if (entities[type].length === 0) return null;
        const cfg = CHIP_CONFIG[type];
        return (
          <div key={type}>
            <p className="text-[10px] uppercase tracking-widest text-slate-400 mb-1.5 font-semibold">
              {cfg.icon} {cfg.label}s
            </p>
            <div className="flex flex-wrap gap-1.5">
              {entities[type].map((item, i) => (
                <span
                  key={i}
                  className={`${cfg.chip} text-xs font-medium px-2.5 py-1 rounded-full capitalize`}
                >
                  {item}
                </span>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}
