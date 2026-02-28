/**
 * Sidebar toggle and conversation list management
 */
import { $, el } from './utils.js';
import { getConversations, createConversation, deleteConversation } from './storage.js';

let onSwitchConversation = null;
let currentConvId = null;

const ICON_DELETE = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M8 6V4a2 2 0 012-2h4a2 2 0 012 2v2m3 0v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6h14"/></svg>`;

export function initSidebar(switchCallback) {
  onSwitchConversation = switchCallback;

  const sidebar = $('.sidebar');
  const menuBtn = $('.header__menu-btn');
  const overlay = $('.sidebar-overlay');
  const newChatBtn = $('.sidebar__new-chat');

  // Toggle sidebar
  menuBtn.addEventListener('click', () => {
    const isMobile = window.innerWidth <= 768;
    if (isMobile) {
      sidebar.classList.toggle('open');
      overlay.classList.toggle('active', sidebar.classList.contains('open'));
    } else {
      sidebar.classList.toggle('collapsed');
    }
  });

  // Close sidebar on overlay click (mobile)
  overlay.addEventListener('click', () => {
    sidebar.classList.remove('open');
    overlay.classList.remove('active');
  });

  // New chat
  newChatBtn.addEventListener('click', () => {
    const id = createConversation();
    switchTo(id);
    closeMobileSidebar();
  });

  renderList();
}

/** Render the conversation list */
export function renderList() {
  const list = $('.sidebar__conversations');
  const convs = getConversations();
  list.innerHTML = '';

  if (convs.length === 0) {
    list.appendChild(el('div', { class: 'sidebar__empty' }, 'No conversations yet'));
    return;
  }

  for (const conv of convs) {
    const item = el('div', {
      class: `sidebar__conv-item${conv.id === currentConvId ? ' active' : ''}`,
      dataset: { id: conv.id },
    });

    const title = el('span', { class: 'sidebar__conv-title' }, conv.title);
    const deleteBtn = el('button', { class: 'sidebar__conv-delete' });
    deleteBtn.innerHTML = ICON_DELETE;

    deleteBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      deleteConversation(conv.id);
      if (conv.id === currentConvId) {
        const remaining = getConversations();
        if (remaining.length > 0) {
          switchTo(remaining[0].id);
        } else {
          const newId = createConversation();
          switchTo(newId);
        }
      } else {
        renderList();
      }
    });

    item.addEventListener('click', () => {
      switchTo(conv.id);
      closeMobileSidebar();
    });

    item.appendChild(title);
    item.appendChild(deleteBtn);
    list.appendChild(item);
  }
}

function switchTo(id) {
  currentConvId = id;
  renderList();
  if (onSwitchConversation) onSwitchConversation(id);
}

function closeMobileSidebar() {
  if (window.innerWidth <= 768) {
    $('.sidebar').classList.remove('open');
    $('.sidebar-overlay').classList.remove('active');
  }
}

export function setCurrentConvId(id) {
  currentConvId = id;
  renderList();
}

export function getCurrentConvId() {
  return currentConvId;
}
