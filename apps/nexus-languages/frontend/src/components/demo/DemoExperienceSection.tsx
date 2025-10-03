"use client";

import {useTranslations} from "next-intl";
import {type ChangeEvent, useEffect, useMemo, useState} from "react";

import {apiFetch} from "@/lib/api";
import {PracticePanel} from "@/components/demo/PracticePanel";
import type {AzureLocale, RateLimitRuleResult} from "@/types/azure";

type QuotaStatus =
  | {type: "idle"}
  | {type: "ok"; remaining: number}
  | {type: "blocked"; minutes: number}
  | {type: "daily"}
  | {type: "error"};

const PHRASE_LIBRARY: Record<string, string[]> = {
  "en-US": [
    "Can you recommend a family-friendly restaurant?",
    "I practiced this sentence three times today.",
    "Let's explore the museum this afternoon."
  ],
  "es-ES": [
    "Hoy practiqué mi pronunciación frente al espejo.",
    "¿Puedes repetirlo un poco más despacio, por favor?",
    "Me gustaría ordenar un café con leche y una tostada."
  ],
  "es-MX": [
    "¿Cómo te fue en tu clase de conversación hoy?",
    "Voy a practicar diez minutos antes de dormir.",
    "¿Podrías indicarme dónde está el metro más cercano?"
  ],
  "fr-FR": [
    "Je voudrais réserver une table pour quatre personnes.",
    "Nous répétons cette phrase ensemble tous les matins.",
    "Peux-tu parler un peu plus lentement, s'il te plaît ?"
  ],
  "de-DE": [
    "Können Sie mir bitte den Weg zum Bahnhof erklären?",
    "Ich übe diese Sätze vor dem Spiegel jeden Abend.",
    "Lass uns heute eine neue Redewendung lernen."
  ],
  default: [
    "How was your pronunciation practice today?",
    "I feel more confident after repeating this sentence.",
    "Could you say that again a little slower, please?"
  ]
};

function pickRandomPhrase(locale: string) {
  const candidates = PHRASE_LIBRARY[locale] ?? PHRASE_LIBRARY.default;
  return candidates[Math.floor(Math.random() * candidates.length)];
}

export function DemoExperienceSection() {
  const t = useTranslations("landing.demoExperience");

  const [locales, setLocales] = useState<AzureLocale[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState(false);

  const [targetLocale, setTargetLocale] = useState<string>("");
  const [nativeLocale, setNativeLocale] = useState<string>("");
  const [phrase, setPhrase] = useState<string>("");

  const [quotaStatus, setQuotaStatus] = useState<QuotaStatus>({type: "idle"});
  const [checkingQuota, setCheckingQuota] = useState(false);
  const [showPractice, setShowPractice] = useState(false);

  useEffect(() => {
    let active = true;

    async function loadLocales() {
      try {
        setLoading(true);
        setLoadError(false);
        const response = await apiFetch("/api/v1/locales");
        if (!response.ok) {
          throw new Error(`Failed with status ${response.status}`);
        }
        const payload = (await response.json()) as AzureLocale[];
        if (!active) return;

        setLocales(payload);
        if (payload.length > 0) {
          const first = payload[0];
          setTargetLocale(first.target_locale);
          const firstNative = first.native_locales[0]?.locale ?? "";
          setNativeLocale(firstNative);
          setPhrase(pickRandomPhrase(first.target_locale));
        } else {
          setLoadError(true);
        }
      } catch (error) {
        if (!active) return;
        console.warn("Failed to load locales", error);
        setLoadError(true);
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    loadLocales();

    return () => {
      active = false;
    };
  }, []);

  const targetOptions = locales;
  const selectedTarget = useMemo(
    () => targetOptions.find((item) => item.target_locale === targetLocale),
    [targetOptions, targetLocale]
  );

  const nativeOptions = selectedTarget?.native_locales ?? [];

  useEffect(() => {
    setQuotaStatus({type: "idle"});
  }, [targetLocale, nativeLocale]);

  const voices = useMemo(() => selectedTarget?.voices.slice(0, 3) ?? [], [selectedTarget]);

  const selectLabelClass = "block text-sm font-medium text-slate-600";
  const selectBaseClass =
    "mt-2 w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-slate-900 shadow-sm focus:border-nexus-navy focus:outline-none focus:ring-2 focus:ring-nexus-navy/20";

  const handleTargetChange = (event: ChangeEvent<HTMLSelectElement>) => {
    const value = event.target.value;
    setTargetLocale(value);
    const localeEntry = locales.find((item) => item.target_locale === value);
    const firstNative = localeEntry?.native_locales[0]?.locale ?? "";
    setNativeLocale(firstNative);
    setPhrase(pickRandomPhrase(value));
  };

  const handleNativeChange = (event: ChangeEvent<HTMLSelectElement>) => {
    setNativeLocale(event.target.value);
  };

  const handleRefreshPhrase = () => {
    if (!targetLocale) {
      setPhrase(pickRandomPhrase("default"));
      return;
    }
    setPhrase(pickRandomPhrase(targetLocale));
  };

  const handleCheckQuota = async () => {
    if (!targetLocale) {
      return;
    }

    const targetLanguage = selectedTarget?.target_language ?? null;
    setCheckingQuota(true);

    try {
      const response = await apiFetch("/api/v1/rate-limit/probe", {
        method: "POST",
        body: JSON.stringify({
          targetLocale,
          targetLanguage
        })
      });

      if (response.ok) {
        const data = (await response.json()) as {
          rules: RateLimitRuleResult[];
        };
        const hourly = data.rules.find((rule) => rule.name === "hourly");
        const remaining = hourly?.remaining ?? 0;
        setQuotaStatus({type: "ok", remaining});
        return;
      }

      if (response.status === 429) {
        const detail = await response.json();
        const retrySeconds = Number(detail?.detail?.retry_after_seconds ?? 0);
        const ruleName = detail?.detail?.rule as string | undefined;

        if (ruleName === "hourly") {
          const minutes = Math.max(1, Math.ceil(retrySeconds / 60));
          setQuotaStatus({type: "blocked", minutes});
        } else {
          setQuotaStatus({type: "daily"});
        }
        return;
      }

      throw new Error(`Unexpected status ${response.status}`);
    } catch (error) {
      console.error("Error probing rate limit", error);
      setQuotaStatus({type: "error"});
    } finally {
      setCheckingQuota(false);
    }
  };

  const quotaMessage = useMemo(() => {
    if (quotaStatus.type === "idle") return null;
    if (quotaStatus.type === "ok") {
      return {
        tone: "success" as const,
        text: t("status.quotaOk", {remaining: quotaStatus.remaining})
      };
    }
    if (quotaStatus.type === "blocked") {
      return {
        tone: "warning" as const,
        text: t("status.quotaBlocked", {minutes: quotaStatus.minutes})
      };
    }
    if (quotaStatus.type === "daily") {
      return {
        tone: "warning" as const,
        text: t("status.quotaDaily")
      };
    }
    return {
      tone: "error" as const,
      text: t("status.quotaError")
    };
  }, [quotaStatus, t]);

  const statusBadgeClass = useMemo(() => {
    if (!quotaMessage) return "";
    if (quotaMessage.tone === "success") return "bg-nexus-mint/15 text-nexus-navy";
    if (quotaMessage.tone === "warning") return "bg-amber-100 text-amber-800";
    return "bg-rose-100 text-rose-700";
  }, [quotaMessage]);

  return (
    <section className="space-y-10 rounded-3xl bg-white p-10 shadow-xl" aria-labelledby="demo-experience-heading">
      <div className="max-w-3xl space-y-4">
        <h2 id="demo-experience-heading" className="text-3xl font-semibold text-slate-900">
          {t("title")}
        </h2>
        <p className="text-slate-600">{t("subtitle")}</p>
      </div>

      {loading ? (
        <div className="rounded-2xl border border-dashed border-slate-200 bg-slate-50 p-8 text-center text-slate-500">
          {t("status.loadingLocales")}
        </div>
      ) : loadError ? (
        <div className="rounded-2xl border border-rose-200 bg-rose-50 p-6 text-sm text-rose-700">
          {t("status.noLocales")}
        </div>
      ) : (
        <div className="grid gap-8 md:grid-cols-2">
          <div className="space-y-6">
            <div>
              <label className={selectLabelClass} htmlFor="target-locale">
                {t("targetLabel")}
              </label>
              <select
                id="target-locale"
                className={selectBaseClass}
                value={targetLocale}
                onChange={handleTargetChange}
              >
                {targetOptions.map((option) => (
                  <option key={option.target_locale} value={option.target_locale}>
                    {option.target_display_name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className={selectLabelClass} htmlFor="native-locale">
                {t("nativeLabel")}
              </label>
              <select
                id="native-locale"
                className={selectBaseClass}
                value={nativeLocale}
                onChange={handleNativeChange}
              >
                {nativeOptions.map((option) => (
                  <option key={option.locale} value={option.locale}>
                    {option.display_name}
                  </option>
                ))}
              </select>
            </div>

            {voices.length > 0 && (
              <div className="space-y-2">
                <p className="text-sm font-medium text-slate-600">{t("voicesLabel")}</p>
                <div className="flex flex-wrap gap-2">
                  {voices.map((voice) => (
                    <span
                      key={voice.short_name}
                      className="inline-flex items-center rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600"
                    >
                      {voice.display_name}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="space-y-6">
            <div>
              <label className={selectLabelClass} htmlFor="sample-phrase">
                {t("sampleLabel")}
              </label>
              <textarea
                id="sample-phrase"
                className="mt-2 h-32 w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-slate-900 shadow-sm focus:border-nexus-navy focus:outline-none focus:ring-2 focus:ring-nexus-navy/20"
                value={phrase}
                placeholder={t("samplePlaceholder")}
                onChange={(event) => setPhrase(event.target.value)}
              />
              <p className="mt-2 text-xs text-slate-500">{t("sampleHint")}</p>
            </div>

            <div className="flex flex-wrap gap-3">
              <button
                type="button"
                onClick={handleRefreshPhrase}
                className="inline-flex items-center justify-center rounded-full border border-slate-200 px-5 py-2 text-sm font-medium text-slate-700 transition hover:border-nexus-navy hover:text-nexus-navy"
              >
                {t("controls.refresh")}
              </button>
              <button
                type="button"
                onClick={handleCheckQuota}
                className="inline-flex items-center justify-center rounded-full bg-nexus-navy px-5 py-2 text-sm font-semibold text-white shadow-md shadow-nexus-navy/20 transition hover:bg-nexus-navy/90 disabled:cursor-not-allowed disabled:opacity-70"
                disabled={checkingQuota}
              >
                {checkingQuota ? `${t("controls.checkQuota")}...` : t("controls.checkQuota")}
              </button>
              <button
                type="button"
                onClick={() => setShowPractice(true)}
                className="inline-flex items-center justify-center rounded-full bg-nexus-mint/20 px-5 py-2 text-sm font-semibold text-nexus-navy transition hover:bg-nexus-mint/30"
              >
                {t("controls.start")}
              </button>
            </div>

            {quotaMessage && (
              <div className={`rounded-2xl px-4 py-3 text-sm font-medium ${statusBadgeClass}`}>
                {quotaMessage.text}
              </div>
            )}

            {showPractice && (
              <div className="mt-6">
                <PracticePanel
                  targetLocale={targetLocale}
                  nativeLanguage={nativeLocale}
                  phrase={phrase}
                  onClose={() => setShowPractice(false)}
                />
              </div>
            )}
          </div>
        </div>
      )}
    </section>
  );
}
