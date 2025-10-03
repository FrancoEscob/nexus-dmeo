"use client";

import Link from "next/link";
import {useTranslations} from "next-intl";

import {LanguageSwitcher} from "@/components/layout/LanguageSwitcher";
import type {Locale} from "@/i18n/locales";

type Props = {
  currentLocale: Locale;
};

export function SiteHeader({currentLocale}: Props) {
  const t = useTranslations("landing.hero");

  return (
    <header className="sticky top-0 z-20 border-b border-white/40 bg-nexus-cream/80 backdrop-blur">
      <div className="mx-auto flex max-w-5xl items-center justify-between gap-6 px-6 py-4">
        <Link href={`/${currentLocale}`} prefetch={false} className="text-lg font-semibold text-nexus-navy">
          Nexus Languages
        </Link>
        <div className="flex items-center gap-4">
          <span className="hidden text-sm text-slate-500 md:inline">
            {t("badge")}
          </span>
          <LanguageSwitcher currentLocale={currentLocale} />
        </div>
      </div>
    </header>
  );
}
