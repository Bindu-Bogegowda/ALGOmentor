import React, { useState, useEffect, useRef } from 'react';
import { X, Send, Bot, Sparkles, Code, Check, Terminal } from 'lucide-react';
import { api } from '../services/api';

export default function AIChatDrawer({ isOpen, onClose, contextData = {} }) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: 'Hello! I am your AlgoMentor AI Personal Tutor. I can explain algorithms, review code line by line, unpack tricky Big-O complexities, or suggest guided hints.',
      code_snippet: null
    }
  ]);
  const [inputMsg, setInputMsg] = useState('');
  const [loading, setLoading] = useState(false);
  const [copiedId, setCopiedId] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  async function handleSend(e) {
    e?.preventDefault();
    if (!inputMsg.trim() || loading) return;

    const userText = inputMsg.trim();
    setInputMsg('');
    const userMsgObj = {
      id: Date.now(),
      role: 'user',
      content: userText
    };
    setMessages(prev => [...prev, userMsgObj]);
    setLoading(true);

    try {
      const res = await api.sendTutorMessage({
        message: userText,
        context_page: contextData.page || 'general',
        current_code: contextData.code || null,
        problem_title: contextData.problemTitle || null,
        error_message: contextData.error || null
      });

      const asstMsgObj = {
        id: Date.now() + 1,
        role: 'assistant',
        content: res.reply,
        code_snippet: res.code_suggestion
      };
      setMessages(prev => [...prev, asstMsgObj]);
    } catch (err) {
      setMessages(prev => [
        ...prev,
        {
          id: Date.now() + 1,
          role: 'assistant',
          content: 'Sorry, I encountered an issue analyzing this query. Please try again.',
          code_snippet: null
        }
      ]);
    } finally {
      setLoading(false);
    }
  }

  function copyCode(snippet, id) {
    navigator.clipboard.writeText(snippet);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  }

  if (!isOpen) return null;

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      right: 0,
      bottom: 0,
      width: '100%',
      maxWidth: '430px',
      backgroundColor: 'var(--bg-secondary)',
      borderLeft: '1px solid var(--border-subtle)',
      boxShadow: '-8px 0 25px rgba(0,0,0,0.4)',
      zIndex: 90,
      display: 'flex',
      flexDirection: 'column'
    }}>
      {/* Header */}
      <div style={{
        padding: '1.1rem 1.25rem',
        borderBottom: '1px solid var(--border-subtle)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        backgroundColor: 'var(--bg-card)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
          <div style={{
            width: '32px',
            height: '32px',
            borderRadius: '8px',
            background: 'linear-gradient(135deg, #9333ea 0%, #c084fc 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#fff'
          }}>
            <Bot size={18} />
          </div>
          <div>
            <div style={{ fontWeight: 700, fontSize: '0.95rem', color: 'var(--text-primary)' }}>
              AI Assistant
            </div>
            <div style={{ fontSize: '0.72rem', color: 'var(--accent-emerald)', display: 'flex', alignItems: 'center', gap: '4px' }}>
              <span style={{ width: '6px', height: '6px', borderRadius: '50%', backgroundColor: 'var(--accent-emerald)', display: 'inline-block' }} />
              Ready & Pedagogically Active
            </div>
          </div>
        </div>

        <button
          onClick={onClose}
          style={{
            background: 'none',
            border: 'none',
            color: 'var(--text-muted)',
            cursor: 'pointer',
            padding: '4px'
          }}
        >
          <X size={20} />
        </button>
      </div>

      {/* Context Banner if on problem/lesson */}
      {contextData.problemTitle && (
        <div style={{
          padding: '0.5rem 1rem',
          backgroundColor: 'rgba(56, 189, 248, 0.08)',
          borderBottom: '1px solid rgba(56, 189, 248, 0.2)',
          fontSize: '0.78rem',
          color: 'var(--accent-cyan)',
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem'
        }}>
          <Sparkles size={14} />
          <span>Context: <strong>{contextData.problemTitle}</strong></span>
        </div>
      )}

      {/* Messages stream */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: '1rem',
        display: 'flex',
        flexDirection: 'column',
        gap: '1rem'
      }}>
        {messages.map((m) => (
          <div
            key={m.id}
            style={{
              alignSelf: m.role === 'user' ? 'flex-end' : 'flex-start',
              maxWidth: '88%',
              backgroundColor: m.role === 'user' ? 'var(--accent-cyan)' : 'var(--bg-card)',
              color: m.role === 'user' ? '#000000' : 'var(--text-primary)',
              padding: '0.75rem 1rem',
              borderRadius: m.role === 'user' ? '14px 14px 2px 14px' : '14px 14px 14px 2px',
              border: m.role === 'user' ? 'none' : '1px solid var(--border-subtle)',
              fontSize: '0.88rem',
              lineHeight: 1.5,
              wordBreak: 'break-word',
              boxShadow: 'var(--shadow-sm)'
            }}
          >
            <div style={{ whiteSpace: 'pre-wrap' }}>{m.content}</div>

            {m.code_snippet && (
              <div style={{
                marginTop: '0.75rem',
                backgroundColor: 'rgba(0,0,0,0.5)',
                borderRadius: '8px',
                border: '1px solid rgba(255,255,255,0.1)',
                overflow: 'hidden'
              }}>
                <div style={{
                  padding: '0.35rem 0.65rem',
                  backgroundColor: 'rgba(255,255,255,0.05)',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  fontSize: '0.72rem',
                  color: '#94a3b8'
                }}>
                  <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <Code size={12} /> Code Guide
                  </span>
                  <button
                    onClick={() => copyCode(m.code_snippet, m.id)}
                    style={{
                      background: 'none',
                      border: 'none',
                      color: copiedId === m.id ? '#10b981' : '#94a3b8',
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '4px',
                      fontSize: '0.72rem'
                    }}
                  >
                    {copiedId === m.id ? <Check size={12} /> : null}
                    {copiedId === m.id ? 'Copied' : 'Copy'}
                  </button>
                </div>
                <pre style={{
                  padding: '0.65rem',
                  fontSize: '0.78rem',
                  fontFamily: 'Consolas, monospace',
                  overflowX: 'auto',
                  color: '#e2e8f0',
                  margin: 0
                }}>
                  {m.code_snippet}
                </pre>
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div style={{
            alignSelf: 'flex-start',
            backgroundColor: 'var(--bg-card)',
            padding: '0.75rem 1rem',
            borderRadius: '14px 14px 14px 2px',
            border: '1px solid var(--border-subtle)',
            fontSize: '0.85rem',
            color: 'var(--text-muted)',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            <Sparkles size={14} className="pulse-glow" /> Thinking algorithmically...
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Prompts */}
      <div style={{
        padding: '0.5rem 1rem',
        borderTop: '1px solid var(--border-subtle)',
        display: 'flex',
        gap: '0.5rem',
        overflowX: 'auto'
      }}>
        {[
          'Explain Time Complexity',
          'Give me a hint',
          'Check for edge cases'
        ].map((prompt, i) => (
          <button
            key={i}
            onClick={() => setInputMsg(prompt)}
            style={{
              padding: '0.3rem 0.65rem',
              borderRadius: '999px',
              backgroundColor: 'var(--bg-primary)',
              border: '1px solid var(--border-subtle)',
              color: 'var(--text-secondary)',
              fontSize: '0.75rem',
              cursor: 'pointer',
              whiteSpace: 'nowrap'
            }}
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* Input box */}
      <form onSubmit={handleSend} style={{
        padding: '0.85rem 1rem',
        borderTop: '1px solid var(--border-subtle)',
        display: 'flex',
        gap: '0.5rem',
        backgroundColor: 'var(--bg-card)'
      }}>
        <input
          type="text"
          placeholder="Ask me anything..."
          value={inputMsg}
          onChange={(e) => setInputMsg(e.target.value)}
          style={{
            flex: 1,
            padding: '0.65rem 0.85rem',
            borderRadius: '10px',
            border: '1px solid var(--border-subtle)',
            backgroundColor: 'var(--bg-primary)',
            color: 'var(--text-primary)',
            fontSize: '0.88rem',
            outline: 'none'
          }}
        />
        <button
          type="submit"
          disabled={!inputMsg.trim() || loading}
          style={{
            padding: '0.65rem 1rem',
            borderRadius: '10px',
            border: 'none',
            background: 'linear-gradient(135deg, #0284c7 0%, #38bdf8 100%)',
            color: '#fff',
            cursor: (!inputMsg.trim() || loading) ? 'not-allowed' : 'pointer',
            opacity: (!inputMsg.trim() || loading) ? 0.6 : 1,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
        >
          <Send size={16} />
        </button>
      </form>
    </div>
  );
}
