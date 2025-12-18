import React, { useEffect, useState } from 'react';
import { fetchChats, type Chat } from './chat.service.ts';
import './chatlist.css';

interface ChatListProps {
  onChatSelect?: (chatId: number) => void;
  selectedChatId?: number;
}

const ChatList: React.FC<ChatListProps> = ({ onChatSelect, selectedChatId }) => {
  const [chats, setChats] = useState<Chat[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadChats = async () => {
      try {
        const { chats } = await fetchChats();
        setChats(chats);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load chats');
      } finally {
        setLoading(false);
      }
    };

    loadChats();
  }, []);

  const handleChatClick = (chatId: number) => {
    onChatSelect?.(chatId);
  };

  const formatTime = (timestamp?: number): string => {
    if (!timestamp) return '';
    return new Date(timestamp).toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
        <div className="chat-list-container">
          <div style={{ padding: '20px', textAlign: 'center' }}>Загрузка чатов...</div>
        </div>
    );
  }

  if (error) {
    return (
        <div className="chat-list-container">
          <div style={{
            padding: '20px',
            textAlign: 'center',
            color: '#ff3333',
            fontFamily: '"Monomakh", system-ui'
          }}>
            {error}
          </div>
        </div>
    );
  }

  return (
      <div className="chat-list-container">
        <div className="chat-list-scrollable">
          {chats.map((chat) => (
              <div
                  key={chat.chatId}
                  className={`chat-item ${selectedChatId === chat.chatId ? 'selected' : ''}`}
                  onClick={() => handleChatClick(chat.chatId)}
              >
                <div className="chat-avatar">
                  {chat.type === 'PRIVATE' ? (
                      <span className="avatar-private">P</span>
                  ) : (
                      <span className="avatar-group">G</span>
                  )}
                </div>
                <div className="chat-content">
                  <div className="chat-header">
                    <span className="chat-title">{chat.title}</span>
                    {chat.lastMessageTime && (
                        <span className="chat-time">{formatTime(chat.lastMessageTime)}</span>
                    )}
                  </div>
                  <div className="chat-preview">
                    {chat.lastMessage && (
                        <p className="chat-message">{chat.lastMessage}</p>
                    )}
                    {chat.unreadCount > 0 && (
                        <span className="unread-count">
                    {chat.unreadCount > 99 ? '99+' : chat.unreadCount}
                  </span>
                    )}
                  </div>
                </div>
              </div>
          ))}
        </div>
      </div>
  );
};

export default ChatList;