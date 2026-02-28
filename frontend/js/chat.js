/**
 * Chat message rendering and scroll management
 */
import { $, el, escapeHtml } from './utils.js';
import { buildRedactionBlock } from './redaction.js';

const ICON_FILE = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/></svg>`;

/**
 * Render all messages for a conversation
 */
export function renderMessages(messages) {
  const chatArea = $('.chat-area');
  const welcome = $('.welcome');
  const messagesContainer = getOrCreateMessages();

  messagesContainer.innerHTML = '';

  if (!messages || messages.length === 0) {
    welcome.style.display = 'flex';
    messagesContainer.style.display = 'none';
    return;
  }

  welcome.style.display = 'none';
  messagesContainer.style.display = 'flex';

  for (const msg of messages) {
    appendMessageEl(msg, messagesContainer);
  }

  // Scroll anchor
  const anchor = el('div', { class: 'scroll-anchor' });
  messagesContainer.appendChild(anchor);

  scrollToBottom();
}

/**
 * Append a single message to the chat
 */
export function appendMessage(msg) {
  const welcome = $('.welcome');
  const messagesContainer = getOrCreateMessages();

  welcome.style.display = 'none';
  messagesContainer.style.display = 'flex';

  appendMessageEl(msg, messagesContainer);
  scrollToBottom();
}

function appendMessageEl(msg, container) {
  const { role, content, meta } = msg;
  const isUser = role === 'user';

  const wrapper = el('div', {
    class: `message message--${isUser ? 'user' : 'assistant'}`,
  });

  // Avatar
  const avatar = el('div', { class: 'message__avatar' }, isUser ? 'U' : 'AI');
  wrapper.appendChild(avatar);

  // Content
  const contentDiv = el('div', { class: 'message__content' });

  // File indicator
  if (meta && meta.fileName) {
    const fileTag = el('div', { class: 'message__file' });
    fileTag.innerHTML = `${ICON_FILE} <span>${escapeHtml(meta.fileName)}</span>`;
    contentDiv.appendChild(fileTag);
  }

  // Redaction result
  if (meta && meta.redaction) {
    const redactionBlock = buildRedactionBlock(meta.redaction);
    contentDiv.appendChild(redactionBlock);
  } else {
    // Plain text - convert newlines to <br>
    const textNode = el('div');
    textNode.innerHTML = escapeHtml(content).replace(/\n/g, '<br>');
    contentDiv.appendChild(textNode);
  }

  wrapper.appendChild(contentDiv);
  container.appendChild(wrapper);
}

/**
 * Show typing indicator
 */
export function showTyping() {
  const container = getOrCreateMessages();
  removeTyping();

  const indicator = el('div', { class: 'typing-indicator', id: 'typing-indicator' });

  const avatar = el('div', { class: 'message__avatar' }, 'AI');
  avatar.style.background = 'linear-gradient(135deg, var(--accent), #8ab4f8)';
  avatar.style.color = '#fff';

  const dots = el('div', { class: 'typing-indicator__dots' },
    el('div', { class: 'typing-indicator__dot' }),
    el('div', { class: 'typing-indicator__dot' }),
    el('div', { class: 'typing-indicator__dot' })
  );

  indicator.appendChild(avatar);
  indicator.appendChild(dots);
  container.appendChild(indicator);
  scrollToBottom();
}

/**
 * Remove typing indicator
 */
export function removeTyping() {
  const existing = document.getElementById('typing-indicator');
  if (existing) existing.remove();
}

function getOrCreateMessages() {
  let container = $('.messages');
  if (!container) {
    container = el('div', { class: 'messages' });
    const chatArea = $('.chat-area');
    chatArea.appendChild(container);
  }
  return container;
}

function scrollToBottom() {
  const chatArea = $('.chat-area');
  requestAnimationFrame(() => {
    chatArea.scrollTop = chatArea.scrollHeight;
  });
}
