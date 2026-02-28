/**
 * API client for LLM Redaction backend
 */

const BASE = '';  // same origin

/** Health check */
export async function healthCheck() {
  const res = await fetch(`${BASE}/health`);
  return res.json();
}

/**
 * Redact a file
 * @param {File} file - uploaded file
 * @param {string} model - backend detector (hybrid|regex|ner|gemini)
 * @returns {Promise<{doc_id, masked_text, audit, envelope}>}
 */
export async function redact(file, model = 'hybrid') {
  const form = new FormData();
  form.append('file', file);
  const res = await fetch(
    `${BASE}/redaction/${model}?store_envelope=true&include_envelope=false`,
    { method: 'POST', body: form }
  );
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `Redaction failed (${res.status})`);
  }
  return res.json();
}

/**
 * Download masked text or audit JSON
 * @param {string} docId
 * @param {'masked'|'audit'} format
 */
export async function download(docId, format = 'masked') {
  const res = await fetch(`${BASE}/download/${docId}?format=${format}`);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `Download failed (${res.status})`);
  }
  const blob = await res.blob();
  const ext = format === 'audit' ? 'json' : 'txt';
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${docId}_${format}.${ext}`;
  a.click();
  URL.revokeObjectURL(url);
}

/**
 * Restore original text
 * @param {string} docId
 * @param {string} adminKey
 * @returns {Promise<{doc_id, restored_text}>}
 */
export async function restore(docId, adminKey) {
  const res = await fetch(`${BASE}/restore/${docId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-ADMIN-KEY': adminKey,
    },
    body: JSON.stringify({}),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `Restore failed (${res.status})`);
  }
  return res.json();
}

/**
 * Chat with LLM
 * @param {string} message
 * @param {Array<{role:string, content:string}>} history
 * @returns {Promise<{reply: string}>}
 */
export async function chat(message, history = [], docId = null) {
  const body = { message, history };
  if (docId) body.doc_id = docId;
  const res = await fetch(`${BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `Chat failed (${res.status})`);
  }
  return res.json();
}
