import React from 'react';
import './HistoryPanel.css';

const HistoryPanel = ({ sessions, onSelectSession, onClearHistory }) => {
  return (
    <div className="history-panel-container">
      <div className="history-header">
        <h3 className="history-title">SESSION_ARCHIVES</h3>
        <button className="clear-history-btn" onClick={onClearHistory}>PURGE_ALL</button>
      </div>
      <div className="history-list">
        {sessions.length === 0 ? (
          <p className="no-history">No archives found, Sir.</p>
        ) : (
          sessions.map((session) => (
            <div 
              key={session.id} 
              className="history-item" 
              onClick={() => onSelectSession(session)}
            >
              <div className="history-item-meta">
                <span className="session-id">ID_{session.id.toString().slice(-6)}</span>
                <span className="session-date">{new Date(session.id).toLocaleTimeString()}</span>
              </div>
              <p className="session-preview">
                {session.messages[session.messages.length - 1]?.text.slice(0, 40)}...
              </p>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default HistoryPanel;
