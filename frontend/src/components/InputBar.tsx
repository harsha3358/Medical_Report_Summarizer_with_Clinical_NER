"use client";
import { useRef, useState, KeyboardEvent } from "react";
import { Send, Paperclip, X, FileText } from "lucide-react";
import clsx from "clsx";

interface InputBarProps {
  onSend: (text: string, file?: File) => void;
  disabled?: boolean;
}

export default function InputBar({ onSend, disabled }: InputBarProps) {
  const [text, setText] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const canSend = (text.trim().length > 0 || file !== null) && !disabled;

  const handleSend = () => {
    if (!canSend) return;
    onSend(text.trim(), file || undefined);
    setText("");
    setFile(null);
    if (textareaRef.current) textareaRef.current.style.height = "auto";
  };

  const handleKey = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (f) setFile(f);
    e.target.value = "";
  };

  return (
    <div className="p-3 md:p-4">
      <div
        className={clsx(
          "glass rounded-2xl focus-ring transition-all",
          disabled && "opacity-60"
        )}
      >
        {/* File preview */}
        {file && (
          <div className="flex items-center gap-2 px-4 pt-3">
            <div className="flex items-center gap-1.5 bg-blue-50 border border-blue-100 rounded-lg px-2.5 py-1">
              <FileText size={12} className="text-blue-500" />
              <span className="text-xs text-blue-600 font-medium max-w-[180px] truncate">
                {file.name}
              </span>
              <button
                onClick={() => setFile(null)}
                className="text-blue-400 hover:text-blue-600 ml-1"
              >
                <X size={11} />
              </button>
            </div>
          </div>
        )}

        <div className="flex items-end gap-2 px-3 py-2">
          {/* File upload */}
          <button
            onClick={() => fileInputRef.current?.click()}
            disabled={disabled}
            className="text-slate-400 hover:text-blue-500 transition-colors p-1.5 rounded-xl hover:bg-blue-50 flex-shrink-0 mb-0.5"
            title="Upload file"
          >
            <Paperclip size={17} />
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept=".txt,.pdf,.png,.jpg,.jpeg"
            onChange={handleFileChange}
            className="hidden"
          />

          {/* Textarea */}
          <textarea
            ref={textareaRef}
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={handleKey}
            disabled={disabled}
            placeholder="Paste a medical report or describe a case…"
            className="flex-1 bg-transparent resize-none text-sm text-slate-700 placeholder:text-slate-400 focus:outline-none leading-relaxed py-1.5"
            rows={1}
            style={{ maxHeight: 180 }}
          />

          {/* Send */}
          <button
            onClick={handleSend}
            disabled={!canSend}
            className={clsx(
              "flex-shrink-0 w-9 h-9 rounded-xl flex items-center justify-center mb-0.5",
              canSend ? "btn-water" : "bg-slate-100 text-slate-400 cursor-not-allowed"
            )}
          >
            <Send size={15} />
          </button>
        </div>
      </div>
      <p className="text-center text-[10px] text-slate-400 mt-2">
        Press <kbd className="bg-slate-100 px-1 py-0.5 rounded text-[9px]">Enter</kbd> to send
        &nbsp;·&nbsp;
        <kbd className="bg-slate-100 px-1 py-0.5 rounded text-[9px]">Shift+Enter</kbd> for new line
      </p>
    </div>
  );
}
