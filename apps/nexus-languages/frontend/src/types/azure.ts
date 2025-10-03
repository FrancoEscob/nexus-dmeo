export type NativeLocale = {
  locale: string;
  display_name: string;
};

export type VoiceSample = {
  short_name: string;
  display_name: string;
  gender?: string | null;
};

export type AzureLocale = {
  target_locale: string;
  target_language: string;
  target_display_name: string;
  native_locales: NativeLocale[];
  voices: VoiceSample[];
};

export type RateLimitRuleResult = {
  name: string;
  limit: number;
  window_seconds: number;
  remaining: number;
  retry_after_seconds: number;
};
