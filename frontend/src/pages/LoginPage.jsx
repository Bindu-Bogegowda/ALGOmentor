import React, { useState } from 'react';
import { 
  Lock, 
  Mail, 
  User, 
  ArrowRight, 
  Sparkles, 
  ShieldCheck, 
  Eye, 
  EyeOff, 
  Code2, 
  BookOpen, 
  Flame, 
  CheckCircle2, 
  HelpCircle,
  Zap,
  ArrowLeft
} from 'lucide-react';
import { api } from '../services/api';

export default function LoginPage({ onAuthSuccess, onNavigate, theme = 'light' }) {
  const [tab, setTab] = useState('login'); // 'login' | 'register' | 'forgot' | 'reset'
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [preferredLanguage, setPreferredLanguage] = useState('java');
  const [resetToken, setResetToken] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  const isLight = theme === 'light';

  async function handleLogin(e) {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await api.login({ username_or_email: email || username, password });
      localStorage.setItem('algomentor_token', res.access_token);
      if (onAuthSuccess) onAuthSuccess(res.user);
      if (onNavigate) onNavigate('dashboard');
    } catch (err) {
      setError(err.message || 'Login failed. Please check your email and password.');
    } finally {
      setLoading(false);
    }
  }

  async function handleRegister(e) {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await api.register({
        email,
        username,
        password,
        full_name: fullName || username,
        preferred_language: preferredLanguage
      });
      localStorage.setItem('algomentor_token', res.access_token);
      if (onAuthSuccess) onAuthSuccess(res.user);
      if (onNavigate) onNavigate('dashboard');
    } catch (err) {
      setError(err.message || 'Registration failed. Please check your input.');
    } finally {
      setLoading(false);
    }
  }

  async function handleForgotPassword(e) {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await api.forgotPassword(email);
      setSuccessMsg(`Reset token created! Use demo token: ${res.demo_token}`);
      setTab('reset');
      setResetToken(res.demo_token || '');
    } catch (err) {
      setError(err.message || 'Error requesting password reset.');
    } finally {
      setLoading(false);
    }
  }

  async function handleResetPassword(e) {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await api.resetPassword({ email, reset_token: resetToken, new_password: newPassword });
      setSuccessMsg('Password successfully reset! You can now sign in.');
      setTab('login');
      setPassword(newPassword);
    } catch (err) {
      setError(err.message || 'Password reset failed.');
    } finally {
      setLoading(false);
    }
  }

  function handleDemoLogin() {
    setError('');
    setLoading(true);
    api.login({ username_or_email: 'demo@algomentor.dev', password: 'algomentor123' })
      .then(res => {
        localStorage.setItem('algomentor_token', res.access_token);
        if (onAuthSuccess) onAuthSuccess(res.user);
        if (onNavigate) onNavigate('dashboard');
      })
      .catch(err => {
        setError(err.message || 'Demo login failed. Make sure backend is running.');
      })
      .finally(() => setLoading(false));
  }

  return (
    <div style={{
      minHeight: '85vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '2rem 1rem'
    }}>
      <div style={{
        width: '100%',
        maxWidth: '1050px',
        backgroundColor: isLight ? '#FFFFFF' : '#0B1120',
        borderRadius: '24px',
        border: isLight ? '1px solid #E2E8F0' : '1px solid #1E293B',
        boxShadow: isLight ? '0 12px 40px rgba(0, 0, 0, 0.08)' : '0 12px 40px rgba(0, 0, 0, 0.5)',
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
        overflow: 'hidden'
      }}>
        
        {/* Left Side: Brand & Visual Showcase */}
        <div style={{
          padding: '3rem 2.5rem',
          background: isLight 
            ? 'linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 50%, #DBEAFE 100%)' 
            : 'linear-gradient(135deg, #1E1B4B 0%, #0F172A 100%)',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          borderRight: isLight ? '1px solid #E0E7FF' : '1px solid #1E293B'
        }}>
          <div>
            {/* Logo */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.75rem' }}>
              <div style={{
                width: '42px',
                height: '42px',
                borderRadius: '12px',
                background: 'linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#ffffff',
                fontWeight: 800,
                fontSize: '1.15rem',
                boxShadow: '0 4px 14px rgba(79, 70, 229, 0.4)'
              }}>
                &lt;/&gt;
              </div>
              <div>
                <h2 style={{ fontSize: '1.4rem', fontWeight: 800, color: isLight ? '#1E1B4B' : '#FFFFFF', margin: 0, letterSpacing: '-0.02em' }}>
                  AlgoMentor
                </h2>
                <div style={{ fontSize: '0.75rem', fontWeight: 700, color: '#4F46E5', letterSpacing: '0.05em' }}>
                  LEARN • PRACTICE • EXCEL
                </div>
              </div>
            </div>

            <h1 style={{
              fontSize: '1.75rem',
              fontWeight: 800,
              color: isLight ? '#1E1B4B' : '#F8FAFC',
              lineHeight: 1.3,
              margin: '0 0 1rem 0'
            }}>
              Master Algorithms Visually & Ace Technical Interviews
            </h1>

            <p style={{
              fontSize: '0.92rem',
              color: isLight ? '#475569' : '#94A3B8',
              lineHeight: 1.6,
              margin: '0 0 2rem 0'
            }}>
              Interactive step-by-step visualizations, Java-first code execution, AI mentorship hints, and continuous streak tracking based on the roadmap.sh curriculum.
            </p>

            {/* Feature Highlights */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <div style={{ width: '28px', height: '28px', borderRadius: '50%', backgroundColor: '#DCFCE7', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <CheckCircle2 size={16} color="#16A34A" />
                </div>
                <span style={{ fontSize: '0.88rem', fontWeight: 600, color: isLight ? '#1E1B4B' : '#F1F5F9' }}>
                  87 Interconnected DSA Concepts & Visualizations
                </span>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <div style={{ width: '28px', height: '28px', borderRadius: '50%', backgroundColor: '#DBEAFE', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Code2 size={16} color="#2563EB" />
                </div>
                <span style={{ fontSize: '0.88rem', fontWeight: 600, color: isLight ? '#1E1B4B' : '#F1F5F9' }}>
                  ☕ Java-First Code Sandbox & Line Synchronizer
                </span>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <div style={{ width: '28px', height: '28px', borderRadius: '50%', backgroundColor: '#FEF3C7', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Flame size={16} color="#D97706" />
                </div>
                <span style={{ fontSize: '0.88rem', fontWeight: 600, color: isLight ? '#1E1B4B' : '#F1F5F9' }}>
                  GitHub & LeetCode 365-Day Activity Heatmap
                </span>
              </div>
            </div>
          </div>

          {/* Quick Guest Link */}
          <div style={{ marginTop: '2.5rem', paddingTop: '1.25rem', borderTop: isLight ? '1px solid #CBD5E1' : '1px solid #334155' }}>
            <button
              onClick={() => onNavigate && onNavigate('dashboard')}
              style={{
                background: 'none',
                border: 'none',
                color: '#4F46E5',
                fontSize: '0.84rem',
                fontWeight: 700,
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                cursor: 'pointer',
                padding: 0
              }}
            >
              <ArrowLeft size={14} />
              <span>Continue exploring as Guest</span>
            </button>
          </div>
        </div>

        {/* Right Side: Auth Forms */}
        <div style={{ padding: '3rem 2.5rem', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          
          {/* 1-Click Instant Demo Login Banner */}
          <div style={{
            marginBottom: '1.75rem',
            padding: '1rem 1.25rem',
            borderRadius: '14px',
            background: 'linear-gradient(135deg, rgba(79, 70, 229, 0.1) 0%, rgba(124, 58, 237, 0.08) 100%)',
            border: '1.5px dashed #818CF8',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '1rem',
            flexWrap: 'wrap'
          }}>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.82rem', fontWeight: 800, color: '#4F46E5' }}>
                <Sparkles size={15} /> Instant 1-Click Demo Access
              </div>
              <div style={{ fontSize: '0.74rem', color: isLight ? '#64748B' : '#94A3B8', marginTop: '2px' }}>
                Preloaded with 7-day streak & solved problems
              </div>
            </div>

            <button
              onClick={handleDemoLogin}
              disabled={loading}
              style={{
                padding: '0.5rem 1rem',
                borderRadius: '999px',
                border: 'none',
                backgroundColor: '#4F46E5',
                color: '#ffffff',
                fontSize: '0.78rem',
                fontWeight: 700,
                display: 'flex',
                alignItems: 'center',
                gap: '5px',
                cursor: 'pointer',
                boxShadow: '0 3px 8px rgba(79, 70, 229, 0.3)',
                whiteSpace: 'nowrap'
              }}
            >
              <span>Login as Demo</span>
              <ArrowRight size={13} />
            </button>
          </div>

          {/* Form Tabs */}
          <div style={{
            display: 'flex',
            borderBottom: isLight ? '1px solid #E2E8F0' : '1px solid #1E293B',
            marginBottom: '1.5rem',
            gap: '1.5rem'
          }}>
            <button
              onClick={() => { setTab('login'); setError(''); setSuccessMsg(''); }}
              style={{
                padding: '0.6rem 0',
                background: 'none',
                border: 'none',
                borderBottom: tab === 'login' ? '2.5px solid #4F46E5' : '2.5px solid transparent',
                color: tab === 'login' ? '#4F46E5' : isLight ? '#64748B' : '#94A3B8',
                fontWeight: tab === 'login' ? 800 : 600,
                fontSize: '0.94rem',
                cursor: 'pointer'
              }}
            >
              Sign In
            </button>

            <button
              onClick={() => { setTab('register'); setError(''); setSuccessMsg(''); }}
              style={{
                padding: '0.6rem 0',
                background: 'none',
                border: 'none',
                borderBottom: tab === 'register' ? '2.5px solid #4F46E5' : '2.5px solid transparent',
                color: tab === 'register' ? '#4F46E5' : isLight ? '#64748B' : '#94A3B8',
                fontWeight: tab === 'register' ? 800 : 600,
                fontSize: '0.94rem',
                cursor: 'pointer'
              }}
            >
              Create Account
            </button>

            <button
              onClick={() => { setTab('forgot'); setError(''); setSuccessMsg(''); }}
              style={{
                padding: '0.6rem 0',
                background: 'none',
                border: 'none',
                borderBottom: tab === 'forgot' || tab === 'reset' ? '2.5px solid #4F46E5' : '2.5px solid transparent',
                color: tab === 'forgot' || tab === 'reset' ? '#4F46E5' : isLight ? '#64748B' : '#94A3B8',
                fontWeight: tab === 'forgot' || tab === 'reset' ? 800 : 600,
                fontSize: '0.94rem',
                cursor: 'pointer'
              }}
            >
              Reset Password
            </button>
          </div>

          {/* Feedback Alerts */}
          {error && (
            <div style={{
              padding: '0.75rem 1rem',
              borderRadius: '10px',
              backgroundColor: '#FEE2E2',
              border: '1px solid #FCA5A5',
              color: '#991B1B',
              fontSize: '0.82rem',
              fontWeight: 600,
              marginBottom: '1.25rem'
            }}>
              {error}
            </div>
          )}

          {successMsg && (
            <div style={{
              padding: '0.75rem 1rem',
              borderRadius: '10px',
              backgroundColor: '#DCFCE7',
              border: '1px solid #86EFAC',
              color: '#166534',
              fontSize: '0.82rem',
              fontWeight: 600,
              marginBottom: '1.25rem'
            }}>
              {successMsg}
            </div>
          )}

          {/* TAB 1: SIGN IN */}
          {tab === 'login' && (
            <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '1.1rem' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 700, color: isLight ? '#334155' : '#CBD5E1', marginBottom: '0.4rem' }}>
                  Email or Username
                </label>
                <div style={{ position: 'relative' }}>
                  <Mail size={16} style={{ position: 'absolute', left: '12px', top: '12px', color: '#94A3B8' }} />
                  <input
                    type="text"
                    required
                    placeholder="learner@algomentor.dev or username"
                    value={email || username}
                    onChange={(e) => {
                      setEmail(e.target.value);
                      setUsername(e.target.value);
                    }}
                    style={{
                      width: '100%',
                      padding: '0.65rem 1rem 0.65rem 2.4rem',
                      borderRadius: '10px',
                      border: isLight ? '1px solid #CBD5E1' : '1px solid #334155',
                      backgroundColor: isLight ? '#F8FAFC' : '#0F172A',
                      color: isLight ? '#1E1B4B' : '#F8FAFC',
                      fontSize: '0.88rem',
                      outline: 'none',
                      boxSizing: 'border-box'
                    }}
                  />
                </div>
              </div>

              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
                  <label style={{ fontSize: '0.78rem', fontWeight: 700, color: isLight ? '#334155' : '#CBD5E1' }}>
                    Password
                  </label>
                  <button
                    type="button"
                    onClick={() => setTab('forgot')}
                    style={{ background: 'none', border: 'none', color: '#4F46E5', fontSize: '0.75rem', fontWeight: 700, cursor: 'pointer', padding: 0 }}
                  >
                    Forgot password?
                  </button>
                </div>
                <div style={{ position: 'relative' }}>
                  <Lock size={16} style={{ position: 'absolute', left: '12px', top: '12px', color: '#94A3B8' }} />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    required
                    placeholder="••••••••"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    style={{
                      width: '100%',
                      padding: '0.65rem 2.4rem 0.65rem 2.4rem',
                      borderRadius: '10px',
                      border: isLight ? '1px solid #CBD5E1' : '1px solid #334155',
                      backgroundColor: isLight ? '#F8FAFC' : '#0F172A',
                      color: isLight ? '#1E1B4B' : '#F8FAFC',
                      fontSize: '0.88rem',
                      outline: 'none',
                      boxSizing: 'border-box'
                    }}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    style={{
                      position: 'absolute',
                      right: '12px',
                      top: '12px',
                      background: 'none',
                      border: 'none',
                      color: '#94A3B8',
                      cursor: 'pointer',
                      padding: 0
                    }}
                  >
                    {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                  </button>
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                style={{
                  marginTop: '0.5rem',
                  padding: '0.75rem',
                  borderRadius: '10px',
                  border: 'none',
                  backgroundColor: '#4F46E5',
                  color: '#ffffff',
                  fontSize: '0.92rem',
                  fontWeight: 700,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '8px',
                  cursor: loading ? 'not-allowed' : 'pointer',
                  boxShadow: '0 4px 14px rgba(79, 70, 229, 0.4)',
                  transition: 'transform 0.15s ease'
                }}
              >
                <span>{loading ? 'Signing In...' : 'Sign In to AlgoMentor'}</span>
                <ArrowRight size={16} />
              </button>
            </form>
          )}

          {/* TAB 2: REGISTER */}
          {tab === 'register' && (
            <form onSubmit={handleRegister} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 700, color: isLight ? '#334155' : '#CBD5E1', marginBottom: '0.35rem' }}>
                  Full Name
                </label>
                <div style={{ position: 'relative' }}>
                  <User size={16} style={{ position: 'absolute', left: '12px', top: '12px', color: '#94A3B8' }} />
                  <input
                    type="text"
                    required
                    placeholder="Alex Morgan"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    style={{
                      width: '100%',
                      padding: '0.65rem 1rem 0.65rem 2.4rem',
                      borderRadius: '10px',
                      border: isLight ? '1px solid #CBD5E1' : '1px solid #334155',
                      backgroundColor: isLight ? '#F8FAFC' : '#0F172A',
                      color: isLight ? '#1E1B4B' : '#F8FAFC',
                      fontSize: '0.88rem',
                      outline: 'none',
                      boxSizing: 'border-box'
                    }}
                  />
                </div>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 700, color: isLight ? '#334155' : '#CBD5E1', marginBottom: '0.35rem' }}>
                  Email Address
                </label>
                <div style={{ position: 'relative' }}>
                  <Mail size={16} style={{ position: 'absolute', left: '12px', top: '12px', color: '#94A3B8' }} />
                  <input
                    type="email"
                    required
                    placeholder="alex@example.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    style={{
                      width: '100%',
                      padding: '0.65rem 1rem 0.65rem 2.4rem',
                      borderRadius: '10px',
                      border: isLight ? '1px solid #CBD5E1' : '1px solid #334155',
                      backgroundColor: isLight ? '#F8FAFC' : '#0F172A',
                      color: isLight ? '#1E1B4B' : '#F8FAFC',
                      fontSize: '0.88rem',
                      outline: 'none',
                      boxSizing: 'border-box'
                    }}
                  />
                </div>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 700, color: isLight ? '#334155' : '#CBD5E1', marginBottom: '0.35rem' }}>
                  Username
                </label>
                <input
                  type="text"
                  required
                  placeholder="alex_coder"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '0.65rem 1rem',
                    borderRadius: '10px',
                    border: isLight ? '1px solid #CBD5E1' : '1px solid #334155',
                    backgroundColor: isLight ? '#F8FAFC' : '#0F172A',
                    color: isLight ? '#1E1B4B' : '#F8FAFC',
                    fontSize: '0.88rem',
                    outline: 'none',
                    boxSizing: 'border-box'
                  }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 700, color: isLight ? '#334155' : '#CBD5E1', marginBottom: '0.35rem' }}>
                  Preferred Programming Language
                </label>
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                  {[
                    { id: 'java', label: '☕ Java (Primary)' },
                    { id: 'python', label: '🐍 Python' },
                    { id: 'cpp', label: '⚡ C++' }
                  ].map(lang => (
                    <button
                      key={lang.id}
                      type="button"
                      onClick={() => setPreferredLanguage(lang.id)}
                      style={{
                        flex: 1,
                        padding: '0.5rem',
                        borderRadius: '8px',
                        border: preferredLanguage === lang.id ? '2px solid #4F46E5' : '1px solid #CBD5E1',
                        backgroundColor: preferredLanguage === lang.id ? (isLight ? '#EEF2FF' : 'rgba(79, 70, 229, 0.2)') : 'transparent',
                        color: preferredLanguage === lang.id ? '#4F46E5' : isLight ? '#64748B' : '#94A3B8',
                        fontWeight: preferredLanguage === lang.id ? 700 : 500,
                        fontSize: '0.78rem',
                        cursor: 'pointer'
                      }}
                    >
                      {lang.label}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 700, color: isLight ? '#334155' : '#CBD5E1', marginBottom: '0.35rem' }}>
                  Create Password
                </label>
                <div style={{ position: 'relative' }}>
                  <Lock size={16} style={{ position: 'absolute', left: '12px', top: '12px', color: '#94A3B8' }} />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    required
                    placeholder="At least 6 characters"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    style={{
                      width: '100%',
                      padding: '0.65rem 2.4rem 0.65rem 2.4rem',
                      borderRadius: '10px',
                      border: isLight ? '1px solid #CBD5E1' : '1px solid #334155',
                      backgroundColor: isLight ? '#F8FAFC' : '#0F172A',
                      color: isLight ? '#1E1B4B' : '#F8FAFC',
                      fontSize: '0.88rem',
                      outline: 'none',
                      boxSizing: 'border-box'
                    }}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    style={{
                      position: 'absolute',
                      right: '12px',
                      top: '12px',
                      background: 'none',
                      border: 'none',
                      color: '#94A3B8',
                      cursor: 'pointer',
                      padding: 0
                    }}
                  >
                    {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                  </button>
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                style={{
                  marginTop: '0.5rem',
                  padding: '0.75rem',
                  borderRadius: '10px',
                  border: 'none',
                  backgroundColor: '#4F46E5',
                  color: '#ffffff',
                  fontSize: '0.92rem',
                  fontWeight: 700,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '8px',
                  cursor: loading ? 'not-allowed' : 'pointer',
                  boxShadow: '0 4px 14px rgba(79, 70, 229, 0.4)'
                }}
              >
                <span>{loading ? 'Creating Account...' : 'Create Account'}</span>
                <ArrowRight size={16} />
              </button>
            </form>
          )}

          {/* TAB 3: FORGOT PASSWORD */}
          {tab === 'forgot' && (
            <form onSubmit={handleForgotPassword} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
              <p style={{ fontSize: '0.86rem', color: isLight ? '#64748B' : '#94A3B8', margin: 0, lineHeight: 1.5 }}>
                Enter the email address registered with your AlgoMentor account to generate a reset security token.
              </p>

              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 700, color: isLight ? '#334155' : '#CBD5E1', marginBottom: '0.4rem' }}>
                  Email Address
                </label>
                <div style={{ position: 'relative' }}>
                  <Mail size={16} style={{ position: 'absolute', left: '12px', top: '12px', color: '#94A3B8' }} />
                  <input
                    type="email"
                    required
                    placeholder="learner@algomentor.dev"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    style={{
                      width: '100%',
                      padding: '0.65rem 1rem 0.65rem 2.4rem',
                      borderRadius: '10px',
                      border: isLight ? '1px solid #CBD5E1' : '1px solid #334155',
                      backgroundColor: isLight ? '#F8FAFC' : '#0F172A',
                      color: isLight ? '#1E1B4B' : '#F8FAFC',
                      fontSize: '0.88rem',
                      outline: 'none',
                      boxSizing: 'border-box'
                    }}
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                style={{
                  padding: '0.75rem',
                  borderRadius: '10px',
                  border: 'none',
                  backgroundColor: '#4F46E5',
                  color: '#ffffff',
                  fontSize: '0.92rem',
                  fontWeight: 700,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '8px',
                  cursor: loading ? 'not-allowed' : 'pointer'
                }}
              >
                <span>{loading ? 'Sending...' : 'Generate Reset Token'}</span>
                <ArrowRight size={16} />
              </button>
            </form>
          )}

          {/* TAB 4: RESET PASSWORD */}
          {tab === 'reset' && (
            <form onSubmit={handleResetPassword} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 700, color: isLight ? '#334155' : '#CBD5E1', marginBottom: '0.35rem' }}>
                  Reset Token
                </label>
                <input
                  type="text"
                  required
                  placeholder="Paste security token"
                  value={resetToken}
                  onChange={(e) => setResetToken(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '0.65rem 1rem',
                    borderRadius: '10px',
                    border: isLight ? '1px solid #CBD5E1' : '1px solid #334155',
                    backgroundColor: isLight ? '#F8FAFC' : '#0F172A',
                    color: isLight ? '#1E1B4B' : '#F8FAFC',
                    fontSize: '0.88rem',
                    outline: 'none',
                    boxSizing: 'border-box'
                  }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 700, color: isLight ? '#334155' : '#CBD5E1', marginBottom: '0.35rem' }}>
                  New Password
                </label>
                <input
                  type="password"
                  required
                  placeholder="Enter new password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '0.65rem 1rem',
                    borderRadius: '10px',
                    border: isLight ? '1px solid #CBD5E1' : '1px solid #334155',
                    backgroundColor: isLight ? '#F8FAFC' : '#0F172A',
                    color: isLight ? '#1E1B4B' : '#F8FAFC',
                    fontSize: '0.88rem',
                    outline: 'none',
                    boxSizing: 'border-box'
                  }}
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                style={{
                  padding: '0.75rem',
                  borderRadius: '10px',
                  border: 'none',
                  backgroundColor: '#4F46E5',
                  color: '#ffffff',
                  fontSize: '0.92rem',
                  fontWeight: 700,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '8px',
                  cursor: loading ? 'not-allowed' : 'pointer'
                }}
              >
                <span>{loading ? 'Updating...' : 'Set New Password'}</span>
                <ArrowRight size={16} />
              </button>
            </form>
          )}

        </div>
      </div>
    </div>
  );
}
