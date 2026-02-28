/**
 * App entry point: initialize modules and wire events
 */
import { $ } from './utils.js';
import { initSidebar, setCurrentConvId, getCurrentConvId, renderList } from './sidebar.js';
import { initInput, setInputText } from './input.js';
import { renderMessages, appendMessage, showTyping, removeTyping } from './chat.js';
import { getConversation, createConversation, addMessage, getChatHistory, getLastDocId, getConversations } from './storage.js';
import * as api from './api.js';

function init() {
  // Ensure at least one conversation exists
  let convs = getConversations();
  let activeId;
  if (convs.length === 0) {
    activeId = createConversation();
  } else {
    activeId = convs[0].id;
  }

  // Initialize sidebar
  initSidebar(switchConversation);
  setCurrentConvId(activeId);

  // Load current conversation
  loadConversation(activeId);

  // Initialize input bar
  initInput(handleSend);

  // Welcome chips
  document.querySelectorAll('.welcome__chip').forEach(chip => {
    chip.addEventListener('click', () => {
      setInputText(chip.textContent);
    });
  });
}

function switchConversation(id) {
  loadConversation(id);
}

function loadConversation(id) {
  setCurrentConvId(id);
  const conv = getConversation(id);
  renderMessages(conv ? conv.messages : []);
}

async function handleSend({ text, file, mode }) {
  const convId = getCurrentConvId();
  if (!convId) return;

  if (mode === 'masking') {
    if (!file) return;
    await handleRedaction(convId, file);
    return;
  }

  if (!text) return;
  await handleChat(convId, text);
}

async function handleRedaction(convId, file) {
  // Show user message with file info
  const userContent = `Redacting file: ${file.name}`;
  addMessage(convId, 'user', userContent, { fileName: file.name });
  appendMessage({ role: 'user', content: userContent, meta: { fileName: file.name } });
  renderList();

  // Show typing
  showTyping();

  try {
    const result = await api.redact(file, 'hybrid');

    // Store as assistant message with redaction metadata
    addMessage(convId, 'model', `Redaction complete (${result.audit.total_found} PII found)`, { redaction: result });
    removeTyping();
    appendMessage({
      role: 'model',
      content: '',
      meta: { redaction: result },
    });
  } catch (err) {
    removeTyping();
    const errorMsg = `Error: ${err.message}`;
    addMessage(convId, 'model', errorMsg);
    appendMessage({ role: 'model', content: errorMsg, meta: {} });
  }
}

async function handleChat(convId, text) {
  // Show user message
  addMessage(convId, 'user', text);
  appendMessage({ role: 'user', content: text, meta: {} });
  renderList();

  // Show typing
  showTyping();

  try {
    const history = getChatHistory(convId);
    // Remove the last user message from history since it's included in the "message" param
    const pastHistory = history.slice(0, -1);
    const docId = getLastDocId(convId);
    const result = await api.chat(text, pastHistory, docId);

    removeTyping();
    const reply = result.reply || 'No response received.';
    const meta = {};
    if (result.reply_masked) {
      meta.replyMasked = result.reply_masked;
    }
    addMessage(convId, 'model', reply, meta);
    appendMessage({ role: 'model', content: reply, meta });
  } catch (err) {
    removeTyping();
    const errorMsg = `Error: ${err.message}`;
    addMessage(convId, 'model', errorMsg);
    appendMessage({ role: 'model', content: errorMsg, meta: {} });
  }
}

// Boot
document.addEventListener('DOMContentLoaded', init);
