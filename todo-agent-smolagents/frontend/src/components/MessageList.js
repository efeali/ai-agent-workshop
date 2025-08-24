import React, { useEffect, useRef } from 'react';
import './MessageList.css';

const MessageList = ({ messages, isLoading }) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="message-list">
      {messages.map((message) => (
        <div
          key={message.id}
          className={`message ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}
        >
          <div className="message-content">
            <div className="message-text">{message.text}</div>
            <div className="message-time">{formatTime(message.timestamp)}</div>
          </div>
        </div>
      ))}
      {isLoading && (
        <div className="message bot-message">
          <div className="message-content">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      )}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;
