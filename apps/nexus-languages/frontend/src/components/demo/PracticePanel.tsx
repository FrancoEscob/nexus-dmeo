"use client";

import {useLocale, useTranslations} from "next-intl";
import {useMemo, useState} from "react";
import {useRecorder} from "@/hooks/useRecorder";
import {submitAssessment} from "@/lib/api";
import type {AssessmentResponse} from "@/types/assessment";

type Props = {
  targetLocale: string;
  nativeLanguage?: string;
  phrase: string;
  onClose?: () => void;
};

export function PracticePanel({targetLocale, nativeLanguage, phrase, onClose}: Props) {
  const t = useTranslations("landing.demoExperience");
  const uiLocale = useLocale();
  const {state, blob, durationMs, start, stop, reset} = useRecorder(10);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AssessmentResponse | null>(null);

  const canRecord = useMemo(() => state === "idle" || state === "ready", [state]);

  const handleSend = async () => {
    if (!blob) return;
    setSubmitting(true);
    setError(null);
    try {
      const fd = new FormData();
      fd.append("audio", blob, "audio.webm");
      fd.append("targetLocale", targetLocale);
      fd.append("referenceText", phrase);
      fd.append("uiLocale", uiLocale);
      if (nativeLanguage) fd.append("nativeLanguage", nativeLanguage);
      if (durationMs) fd.append("durationMs", String(durationMs));
      const payload: AssessmentResponse = await submitAssessment(fd);
      setResult(payload);
    } catch (e: any) {
      const msg = e?.detail?.detail?.message || e?.detail?.error?.message || e?.message || "Failed";
      setError(String(msg));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-lg font-semibold text-slate-900">{t("controls.start")} – {targetLocale}</h3>
        {onClose && (
          <button onClick={onClose} className="rounded-full px-3 py-1 text-sm text-slate-600 hover:bg-slate-200">✕</button>
        )}
      </div>

      {!result && (
        <div className="space-y-4">
          <p className="text-sm text-slate-600">{phrase}</p>
          <div className="flex gap-3">
            <button
              type="button"
              onClick={() => (state === "recording" ? stop() : start())}
              className="rounded-full bg-nexus-navy px-4 py-2 text-sm font-semibold text-white disabled:opacity-60"
              disabled={!canRecord && state !== "recording"}
            >
              {state === "recording" ? "Stop" : "Record (≤10s)"}
            </button>
            {blob && (
              <button
                type="button"
                onClick={handleSend}
                className="rounded-full bg-nexus-mint/20 px-4 py-2 text-sm font-semibold text-nexus-navy disabled:opacity-60"
                disabled={submitting}
              >
                {submitting ? "Sending..." : "Analyze"}
              </button>
            )}
            {blob && (
              <button type="button" onClick={reset} className="rounded-full border px-4 py-2 text-sm">
                Reset
              </button>
            )}
          </div>
          <div className="text-xs text-slate-500">{state === "recording" ? "Recording..." : blob ? `Ready (${Math.round(durationMs / 1000)}s)` : "Idle"}</div>
          {blob && (
            <audio controls src={URL.createObjectURL(blob)} className="mt-2 w-full" />
          )}
          {error && <div className="rounded-md bg-rose-100 p-2 text-sm text-rose-700">{error}</div>}
        </div>
      )}

      {result && (
        <div className="space-y-6">
          <div className="grid grid-cols-2 gap-3 md:grid-cols-5">
            {Object.entries(result.scores).map(([k, v]) => (
              <div key={k} className="rounded-xl bg-white p-3 text-center shadow-sm">
                <div className="text-xs uppercase text-slate-500">{k}</div>
                <div className="text-2xl font-semibold text-slate-900">{v}</div>
              </div>
            ))}
          </div>
          <div className="space-y-2">
            <h4 className="text-sm font-medium text-slate-700">Feedback</h4>
            <div className="grid gap-3 md:grid-cols-2">
              {result.feedback.map((f, i) => (
                <div key={i} className="rounded-xl bg-white p-4 shadow-sm">
                  <div className="text-sm font-semibold text-slate-900">{f.title}</div>
                  <div className="mt-1 text-sm text-slate-600">{f.body}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
