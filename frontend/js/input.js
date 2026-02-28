/**
 * Input bar: textarea auto-expand, file attachment, send
 */
import { $ } from './utils.js';

let attachedFile = null;
let onSend = null;

export function initInput(sendCallback) {
  onSend = sendCallback;

  const textarea = $('.input-bar__textarea');
  const sendBtn = $('.input-bar__btn--send');
  const attachBtn = $('.input-bar__btn--attach');
  const fileInput = $('.input-bar__file-input');
  const filePreview = $('.input-bar__file-preview');
  const fileRemoveBtn = $('.input-bar__file-remove');
  const fileName = $('.input-bar__file-name');

  // Auto-expand textarea
  textarea.addEventListener('input', () => {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 150) + 'px';
    updateSendBtn();
  });

  // Enter to send, Shift+Enter for newline
  // e.isComposing: 한글/중국어/일본어 IME 조합 중 Enter 이중 발생 방지
  textarea.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) {
      e.preventDefault();
      doSend();
    }
  });

  // Send button click
  sendBtn.addEventListener('click', doSend);

  // Attach file
  attachBtn.addEventListener('click', () => fileInput.click());

  fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];
    if (!file) return;
    attachedFile = file;
    fileName.textContent = file.name;
    filePreview.classList.add('active');
    updateSendBtn();
  });

  // Remove attachment
  fileRemoveBtn.addEventListener('click', () => {
    clearFile();
  });

  updateSendBtn();
}

function doSend() {
  const textarea = $('.input-bar__textarea');
  const text = textarea.value.trim();
  const model = $('.input-bar__model-select').value;

  if (!text && !attachedFile) return;

  if (onSend) {
    onSend({ text, file: attachedFile, model });
  }

  // Reset
  textarea.value = '';
  textarea.style.height = 'auto';
  clearFile();
  updateSendBtn();
}

function clearFile() {
  attachedFile = null;
  const fileInput = $('.input-bar__file-input');
  const filePreview = $('.input-bar__file-preview');
  fileInput.value = '';
  filePreview.classList.remove('active');
  updateSendBtn();
}

function updateSendBtn() {
  const textarea = $('.input-bar__textarea');
  const sendBtn = $('.input-bar__btn--send');
  const hasContent = textarea.value.trim() || attachedFile;
  sendBtn.disabled = !hasContent;
}

/** Set input text programmatically (for suggestion chips) */
export function setInputText(text) {
  const textarea = $('.input-bar__textarea');
  textarea.value = text;
  textarea.style.height = 'auto';
  textarea.style.height = Math.min(textarea.scrollHeight, 150) + 'px';
  textarea.focus();
  updateSendBtn();
}
