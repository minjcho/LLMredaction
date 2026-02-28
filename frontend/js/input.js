/**
 * Input bar: textarea auto-expand, file attachment, send
 */
import { $ } from './utils.js';

let attachedFile = null;
let onSend = null;
let applyModeUi = null;
let currentMode = 'chat';

export function initInput(sendCallback) {
  onSend = sendCallback;

  const textarea = $('.input-bar__textarea');
  const sendBtn = $('.input-bar__btn--send');
  const attachBtn = $('.input-bar__btn--attach');
  const fileInput = $('.input-bar__file-input');
  const filePreview = $('.input-bar__file-preview');
  const fileRemoveBtn = $('.input-bar__file-remove');
  const fileName = $('.input-bar__file-name');
  const modeButtons = [...document.querySelectorAll('.input-bar__mode-btn')];
  const hint = $('.input-bar__hint');
  const activeModeBtn = modeButtons.find(btn => btn.classList.contains('is-active'));
  if (activeModeBtn && activeModeBtn.dataset.mode) {
    currentMode = activeModeBtn.dataset.mode;
  }

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

  applyModeUi = () => {
    const isMasking = currentMode === 'masking';

    if (isMasking) {
      textarea.value = '';
      textarea.style.height = 'auto';
      textarea.disabled = true;
      textarea.placeholder = 'Masking mode: upload a file to redact PII';
      attachBtn.disabled = false;
      fileInput.disabled = false;
      if (hint) hint.textContent = 'Upload a file, then press Send';
    } else {
      textarea.disabled = false;
      textarea.placeholder = 'Type a message...';
      attachBtn.disabled = true;
      fileInput.disabled = true;
      if (attachedFile) clearFile();
      if (hint) hint.textContent = 'Enter to send, Shift+Enter for newline';
    }

    updateSendBtn();
  };

  for (const btn of modeButtons) {
    btn.addEventListener('click', () => {
      setMode(btn.dataset.mode, modeButtons);
      if (applyModeUi) applyModeUi();
    });
  }

  setMode(currentMode, modeButtons);
  applyModeUi();
  updateSendBtn();
}

function doSend() {
  const textarea = $('.input-bar__textarea');
  const text = textarea.value.trim();

  if (currentMode === 'masking' && !attachedFile) return;
  if (currentMode === 'chat' && !text) return;

  if (onSend) {
    onSend({ text, file: attachedFile, mode: currentMode });
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
  const hasContent = currentMode === 'masking' ? Boolean(attachedFile) : Boolean(textarea.value.trim());
  sendBtn.disabled = !hasContent;
}

/** Set input text programmatically (for suggestion chips) */
export function setInputText(text) {
  const modeButtons = [...document.querySelectorAll('.input-bar__mode-btn')];
  if (currentMode === 'masking') {
    setMode('chat', modeButtons);
    if (applyModeUi) applyModeUi();
  }

  const textarea = $('.input-bar__textarea');
  textarea.value = text;
  textarea.style.height = 'auto';
  textarea.style.height = Math.min(textarea.scrollHeight, 150) + 'px';
  textarea.focus();
  updateSendBtn();
}

function setMode(mode, modeButtons) {
  if (mode !== 'chat' && mode !== 'masking') return;
  currentMode = mode;
  for (const btn of modeButtons) {
    const active = btn.dataset.mode === mode;
    btn.classList.toggle('is-active', active);
    btn.setAttribute('aria-pressed', String(active));
  }
}
