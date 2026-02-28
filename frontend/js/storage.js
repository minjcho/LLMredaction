/**
 * localStorage conversation history management
 */

const STORAGE_KEY = 'llmredaction_conversations';

/** Get all conversations */
export function getConversations() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
  } catch {
    return [];
  }
}

/** Save all conversations */
function saveConversations(convs) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(convs));
}

/** Create a new conversation, returns its id */
export function createConversation() {
  const convs = getConversations();
  const conv = {
    id: crypto.randomUUID(),
    title: 'New Chat',
    messages: [],
    createdAt: Date.now(),
    updatedAt: Date.now(),
  };
  convs.unshift(conv);
  saveConversations(convs);
  return conv.id;
}

/** Get a single conversation by id */
export function getConversation(id) {
  return getConversations().find(c => c.id === id) || null;
}

/** Add a message to a conversation */
export function addMessage(convId, role, content, meta = {}) {
  const convs = getConversations();
  const conv = convs.find(c => c.id === convId);
  if (!conv) return;

  conv.messages.push({ role, content, meta, ts: Date.now() });
  conv.updatedAt = Date.now();

  // Auto-title from first user message
  if (conv.title === 'New Chat' && role === 'user') {
    conv.title = content.slice(0, 40) + (content.length > 40 ? '...' : '');
  }

  saveConversations(convs);
}

/** Update conversation title */
export function updateTitle(convId, title) {
  const convs = getConversations();
  const conv = convs.find(c => c.id === convId);
  if (!conv) return;
  conv.title = title;
  saveConversations(convs);
}

/** Delete a conversation */
export function deleteConversation(id) {
  const convs = getConversations().filter(c => c.id !== id);
  saveConversations(convs);
}

/** Get chat history in API format for a conversation */
export function getChatHistory(convId) {
  const conv = getConversation(convId);
  if (!conv) return [];
  return conv.messages
    .filter(m => m.role === 'user' || m.role === 'model')
    .map(m => ({ role: m.role, content: m.content }));
}
