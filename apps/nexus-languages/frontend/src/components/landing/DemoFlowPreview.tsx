"use client";

import {useTranslations} from "next-intl";

const stepIds = [
  "selectLanguages",
  "pickSentence",
  "recordAudio",
  "reviewFeedback"
] as const;

export function DemoFlowPreview() {
  const t = useTranslations("landing.demoFlow");

  return (
    <section className="space-y-10 rounded-3xl bg-white p-10 shadow-xl">
      <div className="max-w-3xl space-y-4">
        <h2 className="text-3xl font-semibold text-slate-900">{t("title")}</h2>
        <p className="text-slate-600">{t("subtitle")}</p>
      </div>
      <div className="grid gap-6 md:grid-cols-2">
        {stepIds.map((id, index) => (
          <article
            key={id}
            className="group rounded-3xl border border-slate-100 bg-nexus-cream/60 p-6 shadow-sm transition duration-200 hover:-translate-y-1 hover:shadow-lg"
          >
            <span className="inline-flex items-center rounded-full bg-white px-3 py-1 text-xs font-semibold text-nexus-navy shadow-sm">
              {t(`steps.${id}.badge`)}
            </span>
            <h3 className="mt-4 text-xl font-semibold text-slate-900">
              {t(`steps.${id}.title`)}
            </h3>
            <p className="mt-3 text-sm text-slate-600">
              {t(`steps.${id}.description`)}
            </p>
            <div className="mt-6 flex items-center justify-end text-xs font-medium text-slate-400">
              {String(index + 1).padStart(2, "0")}
            </div>
          </article>
        ))}
      </div>
      <div className="text-sm font-medium text-nexus-navy">{t("cta")}</div>
    </section>
  );
}
