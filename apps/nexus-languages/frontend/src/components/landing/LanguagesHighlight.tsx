"use client";

import {useTranslations} from "next-intl";

const sampleLocales = [
  {code: "es-ES", name: "Español (España)"},
  {code: "en-US", name: "English (United States)"},
  {code: "pt-BR", name: "Português (Brasil)"},
  {code: "fr-FR", name: "Français (France)"},
  {code: "de-DE", name: "Deutsch (Deutschland)"}
];

export function LanguagesHighlight() {
  const t = useTranslations("landing.languages");

  return (
    <section className="rounded-3xl border border-nexus-navy/10 bg-nexus-navy/5 p-8 shadow-inner">
      <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
        <div className="max-w-2xl space-y-3">
          <h2 className="text-2xl font-semibold text-nexus-navy">{t("title")}</h2>
          <p className="text-sm text-slate-600">{t("description")}</p>
          <p className="text-sm font-medium text-nexus-navy/80">{t("highlight")}</p>
        </div>
        <div className="flex flex-wrap gap-3">
          {sampleLocales.map((locale) => (
            <span
              key={locale.code}
              className="inline-flex min-w-[150px] items-center justify-between rounded-full bg-white px-4 py-2 text-sm font-medium text-slate-700 shadow-sm"
            >
              <span>{locale.name}</span>
              <span className="text-xs text-slate-400">{locale.code}</span>
            </span>
          ))}
        </div>
      </div>
    </section>
  );
}
