export const INTERNAL_API_BASE =
  process.env.INTERNAL_API_BASE || "http://127.0.0.1:5000";

export async function internalJson(path: string, init?: RequestInit) {
  const res = await fetch(`${INTERNAL_API_BASE}${path}`, {
    ...init,
    cache: "no-store",
  });

  const text = await res.text();
  let data: unknown;
  try {
    data = text ? JSON.parse(text) : {};
  } catch {
    data = { ok: false, error: "invalid_json", raw: text };
  }

  return { res, data };
}
