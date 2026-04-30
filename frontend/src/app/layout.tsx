import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "MedAI — Clinical Report Assistant",
  description: "AI-powered medical report summarizer with clinical NER",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
