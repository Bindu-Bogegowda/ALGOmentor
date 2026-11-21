import React, { useState } from 'react';
import { Bot, Send, Sparkles, Code, Check, RefreshCw, BookOpen, Layers } from 'lucide-react';
import { api } from '../services/api';

export default function AITutorPage({ user }) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: `Hello ${user?.full_name || 'learner'}! I am your AlgoMentor AI Personal Tutor.\n\nI adapt to your current learning level (${user?.difficulty_level || 'Intermediate'}) to explain algorithms from first principles, derive asymptotic time and space complexities, and construct intuitive visual mental models.\n\nWhat concept or algorithmic challenge would you like to explore today?`,
      code_snippet: null
    }
  ]);
  const [inputMsg, setInputMsg] = useState('');
  const [loading, setLoading] = useState(false);
  const [copiedId, setCopiedId] = useState(null);

  const promptSuggestions = [
    "Explain Master's Theorem for Divide & Conquer recurrence",
    "How does Dijkstra's priority queue relaxation work?",
    "When should I use Two Pointers vs Sliding Window?",
    "Explain In-order vs Pre-order vs Post-order BST traversal",
    "What is the difference between BFS and DFS in unweighted graphs?"
  ];

  async function handleSend(promptText = null) {
    const textToSend = promptText || inputMsg;
    if (!textToSend.trim() || loading) return;

    setInputMsg('');
    const userMsg = { id: Date.now(), role: 'user', content: textToSend };
    setMessages(prev => [...prev, userMsg]);
    setLoading(true);

    try {
      const res = await api.sendTutorMessage({
        message: textToSend,
        context_page: 'ai_tutor_full'
      });
      setMessages(prev => [
        ...prev,
        {
          id: Date.now() + 1,
          role: 'assistant',
          content: res.reply,
          code_snippet: res.code_suggestion
        }
      ]);
    } catch (err) {
      setMessages(prev => [
        ...prev,
        {
          id: Date.now() + 1,
          role: 'assistant',
          content: 'Sorry, I encountered an issue generating an answer. Please verify network connectivity and try again.',
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

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', height: 'calc(100vh - 100px)' }}>
      {/* Header */}
      <div className="card-glass" style={{ padding: '1.25rem 1.75rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{
            width: '44px',
            height: '44px',
            borderRadius: '12px',
            background: 'linear-gradient(135deg, #9333ea 0%, #c084fc 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#fff',
            boxShadow: '0 4px 14px rgba(147, 51, 234, 0.4)'
          }}>
            <Bot size={24} />
          </div>
          <div>
            <h1 style={{ fontSize: '1.45rem', fontWeight: 800, color: 'var(--text-primary)' }}>
              AlgoMentor AI Personal Tutor
            </h1>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
              Pedagogically adapted algorithm instruction, complexity derivation & live code explanation
            </p>
          </div>
        </div>

        <button
          onClick={() => setMessages([messages[0]])}
          className="btn-secondary"
          style={{ fontSize: '0.8rem', padding: '0.45rem 0.8rem' }}
          title="Clear Conversation History"
        >
          <RefreshCw size={14} /> Clear Chat
        </button>
      </div>

      {/* Main Chat Box Area */}
      <div className="card-glass" style={{
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden'
      }}>
        {/* Messages Feed */}
        <div style={{
          flex: 1,
          overflowY: 'auto',
          padding: '1.5rem',
          display: 'flex',
          flexDirection: 'column',
          gap: '1.25rem'
        }}>
          {messages.map((m) => (
            <div
              key={m.id}
              style={{
                alignSelf: m.role === 'user' ? 'flex-end' : 'flex-start',
                maxWidth: m.role === 'user' ? '75%' : '85%',
                backgroundColor: m.role === 'user' ? 'var(--accent-cyan)' : 'var(--bg-primary)',
                color: m.role === 'user' ? '#000000' : 'var(--text-primary)',
                padding: '1rem 1.25rem',
                borderRadius: m.role === 'user' ? '16px 16px 2px 16px' : '16px 16px 16px 2px',
                border: m.role === 'user' ? 'none' : '1px solid var(--border-subtle)',
                fontSize: '0.92rem',
                lineHeight: 1.6,
                boxShadow: 'var(--shadow-sm)'
              }}
            >
              <div style={{ whiteSpace: 'pre-wrap' }}>{m.content}</div>

              {m.code_snippet && (
                <div style={{
                  marginTop: '1rem',
                  backgroundColor: '#050811',
                  borderRadius: '10px',
                  border: '1px solid rgba(255,255,255,0.1)',
                  overflow: 'hidden'
                }}>
                  <div style={{
                    padding: '0.45rem 0.85rem',
                    backgroundColor: 'rgba(255,255,255,0.05)',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    fontSize: '0.75rem',
                    color: '#94a3b8'
                  }}>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                      <Code size={14} /> Algorithmic Snippet
                    </span>
                    <button
                      onClick={() => copyCode(m.code_snippet, m.id)}
                      style={{
                        background: 'none',
                        border: 'none',
                        color: copiedId === m.id ? 'var(--accent-emerald)' : '#94a3b8',
                        cursor: 'pointer',
                        fontSize: '0.75rem',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '4px'
                      }}
                    >
                      {copiedId === m.id ? <Check size={13} /> : null}
                      {copiedId === m.id ? 'Copied' : 'Copy Code'}
                    </button>
                  </div>
                  <pre style={{
                    padding: '0.85rem',
                    color: '#38bdf8',
                    fontFamily: 'Consolas, monospace',
                    fontSize: '0.85rem',
                    margin: 0,
                    overflowX: 'auto',
                    lineHeight: 1.5
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
              backgroundColor: 'var(--bg-primary)',
              padding: '0.85rem 1.25rem',
              borderRadius: '16px 16px 16px 2px',
              border: '1px solid var(--border-subtle)',
              fontSize: '0.88rem',
              color: 'var(--accent-purple)',
              display: 'flex',
              alignItems: 'center',
              gap: '0.65rem'
            }}>
              <Sparkles size={16} className="pulse-glow" /> Synthesizing algorithmic derivation...
            </div>
          )}
        </div>

        {/* Suggested Prompts Pills */}
        <div style={{
          padding: '0.65rem 1.25rem',
          borderTop: '1px solid var(--border-subtle)',
          backgroundColor: 'var(--bg-card)',
          display: 'flex',
          gap: '0.5rem',
          overflowX: 'auto'
        }}>
          {promptSuggestions.map((p, idx) => (
            <button
              key={idx}
              onClick={() => handleSend(p)}
              style={{
                padding: '0.35rem 0.75rem',
                borderRadius: '999px',
                border: '1px solid var(--border-subtle)',
                backgroundColor: 'var(--bg-primary)',
                color: 'var(--text-secondary)',
                fontSize: '0.78rem',
                cursor: 'pointer',
                whiteSpace: 'nowrap'
              }}
            >
              {p}
            </button>
          ))}
        </div>

        {/* Input Bar */}
        <form
          onSubmit={(e) => { e.preventDefault(); handleSend(); }}
          style={{
            padding: '1rem 1.25rem',
            borderTop: '1px solid var(--border-subtle)',
            backgroundColor: 'var(--bg-secondary)',
            display: 'flex',
            gap: '0.75rem'
          }}
        >
          <input
            type="text"
            placeholder="Ask about dynamic programming, invariants, complexity proofs, or logic..."
            value={inputMsg}
            onChange={(e) => setInputMsg(e.target.value)}
            style={{
              flex: 1,
              padding: '0.75rem 1rem',
              borderRadius: '10px',
              border: '1px solid var(--border-subtle)',
              backgroundColor: 'var(--bg-primary)',
              color: 'var(--text-primary)',
              fontSize: '0.9rem',
              outline: 'none'
            }}
          />
          <button
            type="submit"
            disabled={!inputMsg.trim() || loading}
            className="btn-primary"
            style={{ padding: '0.75rem 1.25rem', opacity: (!inputMsg.trim() || loading) ? 0.6 : 1 }}
          >
            <Send size={16} /> Send
          </button>
        </form>
      </div>
    </div>
  );
}
