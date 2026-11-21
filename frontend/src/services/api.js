const API_BASE = '/api/v1';

async function request(endpoint, options = {}) {
  const token = localStorage.getItem('algomentor_token');
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    ...(options.headers || {})
  };

  const config = {
    ...options,
    headers
  };

  try {
    const response = await fetch(`${API_BASE}${endpoint}`, config);
    if (!response.ok) {
      const errData = await response.json().catch(() => ({ detail: 'Network response error' }));
      throw new Error(errData.detail || `Error ${response.status}: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`API Error on [${options.method || 'GET'}] ${endpoint}:`, error);
    throw error;
  }
}

export const api = {
  // Auth
  login: (credentials) => request('/auth/login', { method: 'POST', body: JSON.stringify(credentials) }),
  register: (userData) => request('/auth/register', { method: 'POST', body: JSON.stringify(userData) }),
  getMe: () => request('/auth/me'),
  forgotPassword: (email) => request('/auth/forgot-password', { method: 'POST', body: JSON.stringify({ email }) }),
  resetPassword: (data) => request('/auth/reset-password', { method: 'POST', body: JSON.stringify(data) }),

  // Dashboard
  getDashboardStats: () => request('/dashboard/stats'),

  // Roadmaps
  listRoadmaps: () => request('/roadmaps'),
  getRoadmapStream: (streamId) => request(`/roadmaps/${streamId}`),

  // Lessons
  listLessons: (filters = {}) => {
    const params = new URLSearchParams();
    if (typeof filters === 'string') {
      params.append('topic_id', filters);
    } else if (filters && typeof filters === 'object') {
      if (filters.topicId) params.append('topic_id', filters.topicId);
      if (filters.category && filters.category !== 'all' && filters.category !== 'All Categories') {
        params.append('category', filters.category);
      }
      if (filters.difficulty && filters.difficulty !== 'all' && filters.difficulty !== 'All Difficulties') {
        params.append('difficulty', filters.difficulty);
      }
      if (filters.search) params.append('search', filters.search);
    }
    const qs = params.toString();
    return request(`/lessons${qs ? `?${qs}` : ''}`);
  },
  getLesson: (lessonId) => request(`/lessons/${lessonId}`),
  updateLessonProgress: (lessonId, isCompleted, timeSpent = 60) => 
    request(`/lessons/${lessonId}/progress`, {
      method: 'POST',
      body: JSON.stringify({ is_completed: isCompleted, time_spent_seconds: timeSpent })
    }),
  submitLessonQuiz: (lessonId, answers) =>
    request(`/lessons/${lessonId}/quiz`, {
      method: 'POST',
      body: JSON.stringify({ answers })
    }),
  getDependencyGraph: () => request('/lessons/dependency-graph'),

  // Problems
  listProblems: (filters = {}) => {
    const params = new URLSearchParams();
    if (filters.topic) params.append('topic', filters.topic);
    if (filters.difficulty) params.append('difficulty', filters.difficulty);
    if (filters.pattern) params.append('pattern', filters.pattern);
    if (filters.search) params.append('search', filters.search);
    const qs = params.toString();
    return request(`/problems${qs ? `?${qs}` : ''}`);
  },
  getProblem: (slug) => request(`/problems/${slug}`),
  toggleBookmark: (slug) => request(`/problems/${slug}/bookmark`, { method: 'POST' }),

  // Code Execution
  runCode: (code, language, problemId = null, customInput = null) =>
    request('/execution/run', {
      method: 'POST',
      body: JSON.stringify({ code, language, problem_id: problemId, custom_input: customInput })
    }),
  submitCode: (code, language, problemId) =>
    request('/execution/submit', {
      method: 'POST',
      body: JSON.stringify({ code, language, problem_id: problemId })
    }),

  // Hints
  getHint: (problemId, level, currentCode = null) =>
    request('/hints', {
      method: 'POST',
      body: JSON.stringify({ problem_id: problemId, level, current_code: currentCode })
    }),

  // Debugger
  analyzeCode: (data) => request('/debugger/analyze', { method: 'POST', body: JSON.stringify(data) }),

  // AI Tutor
  sendTutorMessage: (data) => request('/ai-tutor/chat', { method: 'POST', body: JSON.stringify(data) }),
  getTutorHistory: (sessionId) => request(`/ai-tutor/history/${sessionId}`),

  // Projects
  listProjects: () => request('/projects'),
  getProject: (projectId) => request(`/projects/${projectId}`),
  generateProject: (prompt, projectType = 'web_interactive') =>
    request('/projects/generate', {
      method: 'POST',
      body: JSON.stringify({ prompt, project_type: projectType })
    }),
  updateProjectFile: (projectId, filename, fileData) =>
    request(`/projects/${projectId}/files/${encodeURIComponent(filename)}`, {
      method: 'PUT',
      body: JSON.stringify(fileData)
    }),

  // Progress, Streaks & Analytics
  getMastery: () => request('/progress/mastery'),
  getStreakCalendar: () => request('/streaks/calendar'),
  logActivity: (actionType, topic, activeSeconds = 120, metadata = {}) =>
    request('/streaks/log-activity', {
      method: 'POST',
      body: JSON.stringify({ action_type: actionType, topic, active_seconds: activeSeconds, metadata })
    }),
  getWeeklyAnalytics: () => request('/analytics/weekly'),
  getDailyReview: () => request('/reviews/today'),

  // Profile
  getProfile: () => request('/profile'),
  updateProfile: (profileData) => request('/profile', { method: 'PUT', body: JSON.stringify(profileData) })
};
