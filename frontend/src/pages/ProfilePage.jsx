import React, { useState, useEffect } from 'react';
import { User, Save, Key, Shield, Sparkles, Check, Globe } from 'lucide-react';
import { api } from '../services/api';

export default function ProfilePage({ user, onProfileUpdated, theme, setTheme }) {
  const [fullName, setFullName] = useState(user?.full_name || '');
  const [bio, setBio] = useState(user?.bio || '');
  const [language, setLanguage] = useState(user?.preferred_language || 'python');
  const [level, setLevel] = useState(user?.difficulty_level || 'Beginner');
  const [apiKey, setApiKey] = useState('');
  const [saving, setSaving] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');

  useEffect(() => {
    if (user) {
      setFullName(user.full_name || '');
      setBio(user.bio || '');
      setLanguage(user.preferred_language || 'python');
      setLevel(user.difficulty_level || 'Beginner');
    }
  }, [user]);

  async function handleSave(e) {
    e.preventDefault();
    setSaving(true);
    setSuccessMsg('');
    try {
      const updated = await api.updateProfile({
        full_name: fullName,
        bio: bio,
        preferred_language: language,
        difficulty_level: level,
        theme: theme
      });
      if (onProfileUpdated) onProfileUpdated(updated);
      setSuccessMsg('Profile settings saved successfully!');
      setTimeout(() => setSuccessMsg(''), 2500);
    } catch (err) {
      console.error('Failed to update profile:', err);
    } finally {
      setSaving(false);
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem', maxWidth: '850px', margin: '0 auto' }}>
      {/* Header */}
      <div>
        <h1 style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '0.35rem' }}>
          Student Profile & Configuration
        </h1>
        <p style={{ fontSize: '0.92rem', color: 'var(--text-secondary)' }}>
          Manage your learning preferences, coding language, curriculum tiers, and external AI keys.
        </p>
      </div>

      {successMsg && (
        <div style={{
          backgroundColor: 'rgba(16, 185, 129, 0.12)',
          border: '1px solid rgba(16, 185, 129, 0.3)',
          borderRadius: '10px',
          padding: '0.75rem 1rem',
          color: 'var(--accent-emerald)',
          fontSize: '0.88rem',
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem'
        }}>
          <Check size={16} /> {successMsg}
        </div>
      )}

      {/* Main Profile Form */}
      <form onSubmit={handleSave} className="card-glass" style={{ padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        {/* Avatar & Identifiers */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem', paddingBottom: '1.5rem', borderBottom: '1px solid var(--border-subtle)' }}>
          <img
            src={user?.avatar || 'https://api.dicebear.com/7.x/bottts/svg?seed=algomentor'}
            alt="Profile Avatar"
            style={{
              width: '72px',
              height: '72px',
              borderRadius: '50%',
              border: '3px solid var(--accent-cyan)',
              backgroundColor: 'var(--bg-primary)'
            }}
          />
          <div>
            <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-primary)' }}>
              {user?.full_name || user?.username || 'Alex Mercer'}
            </h3>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
              {user?.email || 'demo@algomentor.dev'} • Account Active
            </p>
          </div>
        </div>

        {/* Inputs */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1.25rem' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '0.4rem' }}>
              Full Name
            </label>
            <input
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              style={{
                width: '100%',
                padding: '0.65rem 0.85rem',
                borderRadius: '8px',
                border: '1px solid var(--border-subtle)',
                backgroundColor: 'var(--bg-primary)',
                color: 'var(--text-primary)',
                fontSize: '0.9rem',
                outline: 'none'
              }}
            />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '0.4rem' }}>
              Preferred Programming Language
            </label>
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              style={{
                width: '100%',
                padding: '0.65rem 0.85rem',
                borderRadius: '8px',
                border: '1px solid var(--border-subtle)',
                backgroundColor: 'var(--bg-primary)',
                color: 'var(--text-primary)',
                fontSize: '0.9rem',
                outline: 'none'
              }}
            >
              <option value="python">Python 3</option>
              <option value="java">Java (JDK)</option>
            </select>
          </div>
        </div>

        <div>
          <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '0.4rem' }}>
            Current Difficulty Level
          </label>
          <div style={{ display: 'flex', gap: '0.75rem' }}>
            {['Beginner', 'Intermediate', 'Advanced', 'Master'].map(lvl => (
              <button
                key={lvl}
                type="button"
                onClick={() => setLevel(lvl)}
                style={{
                  flex: 1,
                  padding: '0.65rem',
                  borderRadius: '8px',
                  border: level === lvl ? '1px solid var(--accent-cyan)' : '1px solid var(--border-subtle)',
                  backgroundColor: level === lvl ? 'rgba(56, 189, 248, 0.15)' : 'var(--bg-primary)',
                  color: level === lvl ? 'var(--accent-cyan)' : 'var(--text-secondary)',
                  fontWeight: 600,
                  fontSize: '0.85rem',
                  cursor: 'pointer'
                }}
              >
                {lvl}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '0.4rem' }}>
            Bio / Learning Objective
          </label>
          <textarea
            value={bio}
            onChange={(e) => setBio(e.target.value)}
            rows={3}
            style={{
              width: '100%',
              padding: '0.75rem',
              borderRadius: '8px',
              border: '1px solid var(--border-subtle)',
              backgroundColor: 'var(--bg-primary)',
              color: 'var(--text-primary)',
              fontSize: '0.9rem',
              outline: 'none',
              resize: 'vertical'
            }}
          />
        </div>

        {/* External AI Provider API Keys Section */}
        <div style={{
          padding: '1.25rem',
          borderRadius: '10px',
          backgroundColor: 'rgba(168, 85, 247, 0.08)',
          border: '1px solid rgba(168, 85, 247, 0.25)',
          display: 'flex',
          flexDirection: 'column',
          gap: '0.75rem'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Key size={18} color="var(--accent-purple)" />
            <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--text-primary)' }}>
              External LLM API Key (Optional)
            </h4>
          </div>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
            AlgoMentor includes an offline high-fidelity algorithmic intelligence engine by default. If you wish to connect your own Gemini or OpenAI API key for live external LLM queries, you may configure it in <code>backend/.env</code> or enter it below:
          </p>
          <input
            type="password"
            placeholder="AIzaSy... or sk-..."
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            style={{
              width: '100%',
              padding: '0.65rem 0.85rem',
              borderRadius: '8px',
              border: '1px solid var(--border-subtle)',
              backgroundColor: 'var(--bg-primary)',
              color: 'var(--text-primary)',
              fontSize: '0.85rem',
              fontFamily: 'Consolas, monospace',
              outline: 'none'
            }}
          />
        </div>

        <button
          type="submit"
          disabled={saving}
          className="btn-primary"
          style={{ justifyContent: 'center', padding: '0.75rem' }}
        >
          <Save size={16} /> {saving ? 'Saving...' : 'Save Settings'}
        </button>
      </form>
    </div>
  );
}
