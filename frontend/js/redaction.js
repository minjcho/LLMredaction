/**
 * PII token highlighting, audit panel, download/restore UI
 */
import { escapeHtml, el } from './utils.js';
import { download, restore } from './api.js';

const ICON_DOWNLOAD = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>`;
const ICON_SHIELD = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>`;
const ICON_RESTORE = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 4v6h6M23 20v-6h-6"/><path d="M20.49 9A9 9 0 005.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 013.51 15"/></svg>`;

/**
 * Parse masked_text and replace [[PII:TYPE:id]] tokens with highlighted spans
 */
export function highlightPiiTokens(maskedText) {
  const escaped = escapeHtml(maskedText);
  return escaped.replace(
    /\[\[PII:([A-Z_]+):([a-f0-9]+)\]\]/g,
    (match, type, id) =>
      `<span class="pii-token" data-type="${type}" title="${type} (${id})">${type}</span>`
  );
}

/**
 * Build the full redaction result block (highlighted text + audit + actions)
 */
export function buildRedactionBlock(data) {
  const { doc_id, masked_text, audit } = data;

  const container = el('div', { class: 'redaction-result' });

  // Highlighted masked text
  const textBlock = el('div', { class: 'message__redacted-text' });
  textBlock.innerHTML = highlightPiiTokens(masked_text);
  textBlock.style.whiteSpace = 'pre-wrap';
  textBlock.style.lineHeight = '1.8';
  container.appendChild(textBlock);

  // Audit summary
  const auditPanel = buildAuditSummary(audit);
  container.appendChild(auditPanel);

  // Action buttons
  const actions = buildActions(doc_id);
  container.appendChild(actions);

  // Restore panel (hidden by default)
  const restorePanel = buildRestorePanel(doc_id);
  container.appendChild(restorePanel);

  return container;
}

function buildAuditSummary(audit) {
  const panel = el('div', { class: 'audit-summary' });

  const title = el('div', { class: 'audit-summary__title' });
  title.innerHTML = `${ICON_SHIELD} Audit Summary`;
  panel.appendChild(title);

  const stats = el('div', { class: 'audit-summary__stats' });

  // Total count
  stats.appendChild(buildStat('Total PII Found', audit.total_found));

  // Sources used
  stats.appendChild(buildStat('Sources', audit.sources_used.join(', ')));

  // Count by type
  const typeCounts = {};
  for (const span of audit.spans) {
    typeCounts[span.type] = (typeCounts[span.type] || 0) + 1;
  }
  for (const [type, count] of Object.entries(typeCounts)) {
    stats.appendChild(buildStat(type, count));
  }

  panel.appendChild(stats);
  return panel;
}

function buildStat(label, value) {
  return el('div', { class: 'audit-summary__stat' },
    el('span', {}, `${label}: `),
    el('span', { class: 'audit-summary__stat-value' }, String(value))
  );
}

function buildActions(docId) {
  const row = el('div', { class: 'redaction-actions' });

  // Download masked text
  const dlMasked = el('button', { class: 'redaction-actions__btn' });
  dlMasked.innerHTML = `${ICON_DOWNLOAD} Download Masked`;
  dlMasked.addEventListener('click', () => download(docId, 'masked'));
  row.appendChild(dlMasked);

  // Download audit JSON
  const dlAudit = el('button', { class: 'redaction-actions__btn' });
  dlAudit.innerHTML = `${ICON_DOWNLOAD} Download Audit`;
  dlAudit.addEventListener('click', () => download(docId, 'audit'));
  row.appendChild(dlAudit);

  // Restore button
  const restoreBtn = el('button', { class: 'redaction-actions__btn redaction-actions__btn--restore' });
  restoreBtn.innerHTML = `${ICON_RESTORE} Restore Original`;
  restoreBtn.addEventListener('click', () => {
    const panel = restoreBtn.closest('.redaction-result').querySelector('.restore-panel');
    panel.classList.toggle('active');
  });
  row.appendChild(restoreBtn);

  return row;
}

function buildRestorePanel(docId) {
  const panel = el('div', { class: 'restore-panel' });

  const title = el('div', { class: 'restore-panel__title' }, 'Enter Admin Key to restore original text');

  const inputRow = el('div', { class: 'restore-panel__input-row' });
  const input = el('input', {
    class: 'restore-panel__input',
    type: 'password',
    placeholder: 'Admin Key',
  });
  const submitBtn = el('button', { class: 'restore-panel__submit' }, 'Restore');
  inputRow.appendChild(input);
  inputRow.appendChild(submitBtn);

  const resultDiv = el('div', { class: 'restore-panel__result' });
  resultDiv.style.display = 'none';

  const errorDiv = el('div', { class: 'restore-panel__error' });

  submitBtn.addEventListener('click', async () => {
    const key = input.value.trim();
    if (!key) return;

    errorDiv.textContent = '';
    resultDiv.style.display = 'none';
    submitBtn.textContent = 'Restoring...';
    submitBtn.disabled = true;

    try {
      const data = await restore(docId, key);
      resultDiv.textContent = data.restored_text;
      resultDiv.style.display = 'block';
    } catch (err) {
      errorDiv.textContent = err.message;
    } finally {
      submitBtn.textContent = 'Restore';
      submitBtn.disabled = false;
    }
  });

  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') submitBtn.click();
  });

  panel.appendChild(title);
  panel.appendChild(inputRow);
  panel.appendChild(errorDiv);
  panel.appendChild(resultDiv);
  return panel;
}
