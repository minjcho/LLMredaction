/**
 * Minimal markdown renderer for assistant messages.
 * Escapes all raw text first and only injects known-safe tags.
 */
import { escapeHtml } from './utils.js';

const ORDERED_LIST_RE = /^\d+\.\s+/;
const UNORDERED_LIST_RE = /^[-*+]\s+/;

export function renderMarkdown(markdown) {
  const source = String(markdown ?? '').replace(/\r\n?/g, '\n');
  if (!source.trim()) return '';

  const lines = source.split('\n');
  const html = [];

  let index = 0;
  while (index < lines.length) {
    const line = lines[index];

    if (!line.trim()) {
      index += 1;
      continue;
    }

    const fenceMatch = line.match(/^```([a-zA-Z0-9_-]+)?\s*$/);
    if (fenceMatch) {
      const lang = fenceMatch[1] ? ` class="language-${escapeHtml(fenceMatch[1])}"` : '';
      const codeLines = [];
      index += 1;
      while (index < lines.length && !/^```/.test(lines[index])) {
        codeLines.push(lines[index]);
        index += 1;
      }
      if (index < lines.length && /^```/.test(lines[index])) {
        index += 1;
      }
      html.push(`<pre><code${lang}>${escapeHtml(codeLines.join('\n'))}</code></pre>`);
      continue;
    }

    const headingMatch = line.match(/^(#{1,6})\s+(.+)$/);
    if (headingMatch) {
      const level = headingMatch[1].length;
      html.push(`<h${level}>${renderInline(headingMatch[2])}</h${level}>`);
      index += 1;
      continue;
    }

    if (/^>\s?/.test(line)) {
      const quoteLines = [];
      while (index < lines.length && /^>\s?/.test(lines[index])) {
        quoteLines.push(lines[index].replace(/^>\s?/, ''));
        index += 1;
      }
      html.push(`<blockquote>${renderInline(quoteLines.join('\n')).replace(/\n/g, '<br>')}</blockquote>`);
      continue;
    }

    if (UNORDERED_LIST_RE.test(line) || ORDERED_LIST_RE.test(line)) {
      const ordered = ORDERED_LIST_RE.test(line);
      const listTag = ordered ? 'ol' : 'ul';
      const items = [];

      while (index < lines.length) {
        const current = lines[index];
        const isListLine = ordered ? ORDERED_LIST_RE.test(current) : UNORDERED_LIST_RE.test(current);
        if (!isListLine) break;
        const itemText = current.replace(ordered ? ORDERED_LIST_RE : UNORDERED_LIST_RE, '');
        items.push(`<li>${renderInline(itemText)}</li>`);
        index += 1;
      }

      html.push(`<${listTag}>${items.join('')}</${listTag}>`);
      continue;
    }

    const paragraphLines = [];
    while (index < lines.length) {
      const current = lines[index];
      if (!current.trim()) break;
      if (
        /^```/.test(current) ||
        /^(#{1,6})\s+/.test(current) ||
        /^>\s?/.test(current) ||
        UNORDERED_LIST_RE.test(current) ||
        ORDERED_LIST_RE.test(current)
      ) {
        break;
      }
      paragraphLines.push(current);
      index += 1;
    }
    html.push(`<p>${renderInline(paragraphLines.join('\n')).replace(/\n/g, '<br>')}</p>`);
  }

  return html.join('');
}

function renderInline(text) {
  const tokenStore = [];
  const stash = html => {
    const key = `@@MD${tokenStore.length}@@`;
    tokenStore.push(html);
    return key;
  };

  let value = String(text ?? '');

  value = value.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (match, label, href) => {
    const safeHref = sanitizeUrl(href);
    if (!safeHref) return match;
    return stash(
      `<a href="${escapeHtml(safeHref)}" target="_blank" rel="noopener noreferrer">${escapeHtml(label)}</a>`
    );
  });

  value = value.replace(/`([^`\n]+)`/g, (_, code) => stash(`<code>${escapeHtml(code)}</code>`));
  value = escapeHtml(value);

  value = value.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  value = value.replace(/(^|[^\*])\*([^*\n]+)\*(?!\*)/g, '$1<em>$2</em>');
  value = value.replace(/(^|[^_])_([^_\n]+)_(?!_)/g, '$1<em>$2</em>');
  value = value.replace(/~~([^~]+)~~/g, '<del>$1</del>');

  for (let i = 0; i < tokenStore.length; i += 1) {
    value = value.replaceAll(`@@MD${i}@@`, tokenStore[i]);
  }

  return value;
}

function sanitizeUrl(url) {
  try {
    const parsed = new URL(url, window.location.origin);
    if (parsed.protocol === 'http:' || parsed.protocol === 'https:' || parsed.protocol === 'mailto:') {
      return parsed.href;
    }
    return null;
  } catch {
    return null;
  }
}
