import createMiddleware from "next-intl/middleware";

import {locales, defaultLocale} from "@/i18n/locales";

export default createMiddleware({
  // List of all supported locales
  locales,
  
  // Default locale to use when none is matched
  defaultLocale,
  
  // Don't use locale prefix for default locale (optional)
  // Set to 'always' if you want /es even for default
  localePrefix: "always"
});

export const config = {
  // Match all pathnames except for
  // - API routes
  // - Static files (_next/static)
  // - Image optimization files (_next/image)
  // - Favicon, etc
  matcher: ["/((?!api|_next|_vercel|.*\\..*).*)"]
};
