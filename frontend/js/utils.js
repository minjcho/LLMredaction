/**
 * DOM helper & utility functions
 */

/** Shorthand for querySelector */
export const $ = (sel, root = document) => root.querySelector(sel);

/** Shorthand for querySelectorAll */
export const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

/** Create an element with optional attributes and children */
export function el(tag, attrs = {}, ...children) {
  const elem = document.createElement(tag);
  for (const [key, val] of Object.entries(attrs)) {
    if (key === 'class') {
      elem.className = val;
    } else if (key === 'dataset') {
      Object.assign(elem.dataset, val);
    } else if (key.startsWith('on')) {
      elem.addEventListener(key.slice(2).toLowerCase(), val);
    } else {
      elem.setAttribute(key, val);
    }
  }
  for (const child of children) {
    if (typeof child === 'string') {
      elem.appendChild(document.createTextNode(child));
    } else if (child) {
      elem.appendChild(child);
    }
  }
  return elem;
}

/** Generate a random hex ID */
export function uid(length = 8) {
  const arr = new Uint8Array(length);
  crypto.getRandomValues(arr);
  return Array.from(arr, b => b.toString(16).padStart(2, '0')).join('').slice(0, length);
}

/** Escape HTML to prevent XSS */
export function escapeHtml(str) {
  const div = document.createElement('div');
  div.appendChild(document.createTextNode(str));
  return div.innerHTML;
}

/** Debounce a function */
export function debounce(fn, ms = 300) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), ms);
  };
}
