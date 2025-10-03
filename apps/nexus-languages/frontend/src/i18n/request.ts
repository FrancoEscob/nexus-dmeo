import {getRequestConfig} from "next-intl/server";
import {notFound} from "next/navigation";

import type {AbstractIntlMessages} from "next-intl";
import {locales, type Locale} from "./locales";

async function loadMessages(locale: Locale): Promise<AbstractIntlMessages> {
  const loaders: Record<Locale, () => Promise<{default: AbstractIntlMessages}>> = {
    en: () => import("@/i18n/messages/en.json"),
    es: () => import("@/i18n/messages/es.json")
  };

  const loader = loaders[locale];
  if (!loader) {
    return {};
  }

  const messages = (await loader()).default;
  return messages || {};
}

export default getRequestConfig(async ({locale}) => {
  // Validate that the incoming `locale` parameter is valid
  if (!locales.includes(locale as Locale)) {
    notFound();
  }

  return {
    messages: await loadMessages(locale as Locale),
    timeZone: "UTC",
    now: new Date()
  };
});
