const DEFAULT_API_BASE_URL = "http://localhost:8000";

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? DEFAULT_API_BASE_URL;

export async function apiFetch(path: string, init?: RequestInit) {
  const url = `${API_BASE_URL}${path}`;
  const response = await fetch(url, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {})
    },
    cache: "no-store"
  });

  return response;
}

export async function postFormData(path: string, form: FormData, init?: Omit<RequestInit, "body" | "headers">) {
  const url = `${API_BASE_URL}${path}`;
  // Do NOT set Content-Type; the browser will set multipart boundary
  const response = await fetch(url, {
    method: "POST",
    body: form,
    cache: "no-store",
    ...init
  });
  return response;
}

export async function submitAssessment(form: FormData) {
  const res = await postFormData("/api/v1/assess/pronunciation", form);
  if (!res.ok) {
    let detail: any = undefined;
    try {
      detail = await res.json();
    } catch {}
    const err = new Error(`Assessment failed: ${res.status}`) as any;
    err.detail = detail;
    throw err;
  }
  return res.json();
}
