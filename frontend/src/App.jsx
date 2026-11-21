import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import TopBar from './components/TopBar';
import AuthModal from './components/AuthModal';
import AIChatDrawer from './components/AIChatDrawer';

// Pages
import DashboardPage from './pages/DashboardPage';
import RoadmapsPage from './pages/RoadmapsPage';
import ConceptsPage from './pages/ConceptsPage';
import VisualizerPage from './pages/VisualizerPage';
import PracticePage from './pages/PracticePage';
import AITutorPage from './pages/AITutorPage';
import DebuggerPage from './pages/DebuggerPage';
import ProjectBuilderPage from './pages/ProjectBuilderPage';
import ProgressPage from './pages/ProgressPage';
import StreaksPage from './pages/StreaksPage';
import AnalyticsPage from './pages/AnalyticsPage';
import ReviewPage from './pages/ReviewPage';
import ProfilePage from './pages/ProfilePage';

import { api } from './services/api';

export default function App() {
  const [theme, setTheme] = useState('light');
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [user, setUser] = useState(null);
  const [authModalOpen, setAuthModalOpen] = useState(false);
  const [aiDrawerOpen, setAiDrawerOpen] = useState(false);
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedLessonId, setSelectedLessonId] = useState(null);
  const [visualizerAlgorithm, setVisualizerAlgorithm] = useState(null);
  const [practiceOptions, setPracticeOptions] = useState({ problem: null, language: 'java' });

  // Apply theme to document element
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('algomentor_theme', theme);
  }, [theme]);

  // Load user profile on mount
  useEffect(() => {
    loadUser();
  }, []);

  async function loadUser() {
    try {
      const u = await api.getMe();
      setUser(u);
    } catch (err) {
      console.log('Using default guest/demo session');
    }
  }

  function handleLogout() {
    localStorage.removeItem('algomentor_token');
    setUser(null);
    setCurrentPage('dashboard');
  }

  function handleNavigate(page, options = {}) {
    const targetPage = page === 'visualizer' ? 'visualizations' : page;
    setCurrentPage(targetPage);
    if (options.lessonId) {
      setSelectedLessonId(options.lessonId);
    }
    if (options.algorithm) {
      setVisualizerAlgorithm(options.algorithm);
    }
    if (options.problem || options.language) {
      setPracticeOptions({
        problem: options.problem || null,
        language: options.language || 'java'
      });
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', backgroundColor: 'var(--bg-primary)' }}>
      {/* 1. Left Persistent Sidebar */}
      <Sidebar
        currentPage={currentPage}
        setCurrentPage={setCurrentPage}
        theme={theme}
        setTheme={setTheme}
        user={user}
        onOpenAuth={() => setAuthModalOpen(true)}
        onLogout={handleLogout}
        mobileOpen={mobileSidebarOpen}
        setMobileOpen={setMobileSidebarOpen}
      />

      {/* 2. Main Content Area */}
      <div style={{
        flex: 1,
        marginLeft: '270px',
        display: 'flex',
        flexDirection: 'column',
        minHeight: '100vh',
        width: 'calc(100% - 270px)'
      }}>
        {/* Top Navbar */}
        <TopBar
          user={user}
          streakCount={5}
          onTriggerAI={() => setAiDrawerOpen(true)}
          onOpenMobileSidebar={() => setMobileSidebarOpen(true)}
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
          onNavigate={handleNavigate}
        />

        {/* Dynamic Page Container */}
        <main style={{
          flex: 1,
          padding: '1.75rem 2rem',
          maxWidth: '1440px',
          width: '100%',
          margin: '0 auto',
          boxSizing: 'border-box'
        }}>
          {currentPage === 'dashboard' && (
            <DashboardPage 
              onNavigate={handleNavigate} 
              onTriggerAI={() => setAiDrawerOpen(true)} 
            />
          )}

          {currentPage === 'roadmaps' && (
            <RoadmapsPage 
              onNavigate={handleNavigate}
              onSelectLesson={(id) => handleNavigate('concepts', { lessonId: id })}
            />
          )}

          {currentPage === 'concepts' && (
            <ConceptsPage 
              onNavigate={handleNavigate}
              initialLessonId={selectedLessonId}
            />
          )}

          {currentPage === 'visualizations' && (
            <VisualizerPage 
              initialAlgorithm={visualizerAlgorithm}
              onNavigate={handleNavigate}
            />
          )}

          {currentPage === 'practice' && (
            <PracticePage 
              onTriggerAI={() => setAiDrawerOpen(true)} 
              initialProblemSlug={practiceOptions.problem}
              initialLanguage={practiceOptions.language || 'java'}
            />
          )}

          {currentPage === 'ai-tutor' && (
            <AITutorPage user={user} />
          )}

          {currentPage === 'debugger' && (
            <DebuggerPage onNavigate={handleNavigate} />
          )}

          {currentPage === 'projects' && (
            <ProjectBuilderPage />
          )}

          {currentPage === 'progress' && (
            <ProgressPage onNavigate={handleNavigate} />
          )}

          {currentPage === 'streaks' && (
            <StreaksPage />
          )}

          {currentPage === 'analytics' && (
            <AnalyticsPage />
          )}

          {currentPage === 'review' && (
            <ReviewPage onNavigate={handleNavigate} />
          )}

          {currentPage === 'profile' && (
            <ProfilePage 
              user={user} 
              onProfileUpdated={(updated) => setUser(updated)} 
              theme={theme}
              setTheme={setTheme}
            />
          )}
        </main>
      </div>

      {/* 3. Auth Modal */}
      <AuthModal
        isOpen={authModalOpen}
        onClose={() => setAuthModalOpen(false)}
        onAuthSuccess={(authUser) => {
          setUser(authUser);
          loadUser();
        }}
      />

      {/* 4. AI Assistant Floating / Sliding Drawer */}
      <AIChatDrawer
        isOpen={aiDrawerOpen}
        onClose={() => setAiDrawerOpen(false)}
        contextData={{
          page: currentPage
        }}
      />
    </div>
  );
}
