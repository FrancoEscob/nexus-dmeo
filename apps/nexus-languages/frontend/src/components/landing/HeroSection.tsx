"use client";

import {useTranslations} from "next-intl";

const metricKeys = ["accuracy", "fluency", "completeness", "prosody"] as const;

export function HeroSection() {
  const t = useTranslations("landing.hero");
  const badge = t("badge");

  return (
    <section className="grid gap-10 md:grid-cols-2 md:items-center">
      <div className="space-y-6">
        <span className="inline-flex items-center rounded-full bg-white px-3 py-1 text-sm font-semibold text-nexus-navy shadow-sm">
          {badge}
        </span>
        <h1 className="text-4xl font-semibold text-slate-900 md:text-5xl">
          {t("title")}
        </h1>
        <p className="text-lg text-slate-600">
          {t("description")}
        </p>
        <div className="flex flex-wrap gap-4">
          <button className="rounded-full bg-nexus-navy px-6 py-3 text-white shadow-lg shadow-nexus-navy/20 transition hover:bg-nexus-navy/90">
            {t("primaryCta")}
          </button>
          <button className="rounded-full border border-nexus-navy px-6 py-3 text-nexus-navy transition hover:bg-white">
            {t("secondaryCta")}
          </button>
        </div>
      </div>
      <div className="relative overflow-hidden rounded-3xl bg-white/90 p-8 shadow-xl">
        <div className="pointer-events-none absolute -right-12 -top-12 h-56 w-56 rounded-full bg-nexus-mint/30 blur-3xl" />
        <div className="pointer-events-none absolute -bottom-16 -left-16 h-48 w-48 rounded-full bg-nexus-navy/20 blur-3xl" />
        <div className="relative space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-slate-900">{t("preview.title")}</h2>
            <span className="rounded-full bg-nexus-mint/20 px-3 py-1 text-sm font-medium text-nexus-navy">
              {t("preview.tag")}
            </span>
          </div>
          <div className="grid gap-4 md:grid-cols-2">
            {metricKeys.map((key) => (
              <div
                key={key}
                className="rounded-2xl border border-slate-100 bg-slate-50 p-4 shadow-sm"
              >
                <p className="text-sm text-slate-500">{t(`preview.metrics.${key}`)}</p>
                <p className="mt-2 text-2xl font-semibold text-slate-900">82</p>
                <p className="text-xs text-slate-500">{t("preview.goalLabel")}</p>
              </div>
            ))}
          </div>
          <div className="rounded-2xl border border-slate-100 bg-white p-6 shadow-sm">
            <p className="text-sm font-medium text-nexus-navy">{t("preview.tipTitle")}</p>
            <p className="mt-2 text-sm text-slate-600">{t("preview.tipBody")}</p>
          </div>
        </div>
      </div>
    </section>
  );
}
