import type {Metadata} from "next";
import "./globals.css";

import {defaultLocale} from "@/i18n/locales";

export const metadata: Metadata = {
  title: "Nexus Languages",
  description: "Demo de pronunciación con Azure Speech y feedback inteligente"
};

export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang={defaultLocale} suppressHydrationWarning>
      <body className="bg-nexus-cream text-slate-900">
        {children}
      </body>
    </html>
  );
}
