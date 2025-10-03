import {NextIntlClientProvider} from "next-intl";
import {getMessages} from "next-intl/server";
import type {ReactNode} from "react";

import {SiteHeader} from "@/components/layout/SiteHeader";
import {Locale, locales} from "@/i18n/locales";

type Props = {
  children: ReactNode;
  params: {locale: Locale};
};

export function generateStaticParams() {
  return locales.map((value) => ({locale: value}));
}

export default async function LocaleLayout({children, params}: Props) {
  const {locale} = params;
  
  // Get messages from the request config
  const messages = await getMessages();

  return (
    <NextIntlClientProvider locale={locale} messages={messages}>
      <SiteHeader currentLocale={locale} />
      {children}
    </NextIntlClientProvider>
  );
}
