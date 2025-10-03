"use client";

import type {Route} from "next";
import {usePathname, useRouter} from "next/navigation";
import {useTransition} from "react";

import {Locale, locales} from "@/i18n/locales";

type Props = {
  currentLocale: Locale;
};

export function LanguageSwitcher({currentLocale}: Props) {
  const pathname = usePathname();
  const router = useRouter();
  const [isPending, startTransition] = useTransition();

  const buildTargetPath = (locale: Locale) => {
    const segments = pathname.split("/").filter(Boolean);
    const hasLocale = locales.includes(segments[0] as Locale);
    const restSegments = hasLocale ? segments.slice(1) : segments;
    const restPath = restSegments.length > 0 ? `/${restSegments.join("/")}` : "";
    return `/${locale}${restPath}`;
  };

  return (
    <div className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-3 py-1 text-sm shadow-sm">
      {locales.map((locale) => {
        const isActive = locale === currentLocale;

        return (
          <button
            key={locale}
            type="button"
            onClick={() => {
              if (isActive) return;
              startTransition(() => {
                router.replace(buildTargetPath(locale) as Route);
              });
            }}
            className={`rounded-full px-3 py-1 transition ${
              isActive
                ? "bg-nexus-navy text-white"
                : "text-slate-500 hover:bg-slate-100"
            } ${isPending ? "opacity-70" : ""}`}
            aria-pressed={isActive}
          >
            {locale.toUpperCase()}
          </button>
        );
      })}
    </div>
  );
}
