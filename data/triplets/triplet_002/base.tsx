import React from 'react';
import './chatlist.css';

type ChatType = 'PRIVATE' | 'GROUP';

interface Chat {
  chatId: number;
  type: ChatType;
  title: string;
  partnerId?: number;
  lastMessage: string;
  lastMessageTime: number;
  unreadCount: number;
}

interface ChatListProps {
  chats: Chat[];
  onChatSelect?: (chatId: number) => void;
  selectedChatId?: number;
}

const ChatList: React.FC<ChatListProps> = ({ chats, onChatSelect, selectedChatId }) => {
  const handleChatClick = (chatId: number) => {
    if (onChatSelect) {
      onChatSelect(chatId);
    }
  };

  const formatTime = (timestamp: number): string => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

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
                <span className="chat-time">{formatTime(chat.lastMessageTime)}</span>
              </div>
              <div className="chat-preview">
                <p className="chat-message">{chat.lastMessage}</p>
                {chat.unreadCount > 0 && (
                  <span className="unread-count">{chat.unreadCount}</span>
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