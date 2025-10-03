"use client";

import {useTranslations} from "next-intl";

const featureIds = ["visualFeedback", "metrics", "coaching", "plans"] as const;

export function UpcomingFeaturesSection() {
  const t = useTranslations("landing.upcoming");

  return (
    <section className="space-y-8 rounded-3xl bg-white p-10 shadow-xl">
      <div className="space-y-3">
        <h2 className="text-3xl font-semibold text-slate-900">{t("title")}</h2>
      </div>
      <div className="grid gap-6 md:grid-cols-2">
        {featureIds.map((id) => (
          <div
            key={id}
            className="rounded-3xl border border-slate-100 bg-nexus-cream/50 p-6 shadow-sm"
          >
            <h3 className="text-lg font-semibold text-slate-900">{t(`items.${id}.title`)}</h3>
            <p className="mt-3 text-sm text-slate-600">{t(`items.${id}.description`)}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
