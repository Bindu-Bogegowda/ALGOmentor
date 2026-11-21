# AlgoMentor
> **Learn Algorithms. Master Logic. Build Anything.**

AlgoMentor is a professional, AI-powered multi-disciplinary algorithm learning, coding practice, interactive algorithm visualization, student performance analytics, and project development platform.

---

## 🌟 Key Modules & Features

1. **Modern UI/UX Design & Branding**
   - Glassmorphic dark/light design system with customizable accent glows.
   - Fully responsive for desktop, laptop, tablet, and mobile screens.
   - Consistent AlgoMentor brand identity.

2. **Secure Authentication & Individual Accounts**
   - PBKDF2/HMAC-SHA256 hashed passwords (no plain-text storage).
   - JWT token-based authentication with expiration handling.
   - Sign up, Login, Logout, Forgot Password, and Password Reset workflows.
   - 1-Click Instant Demo Login (`demo@algomentor.dev` / `algomentor123`).

3. **Personalized Main Dashboard**
   - Telemetry welcome banner with current roadmap and student tier.
   - Quantitative counters: Concepts Completed, Weekly Hours, Problems Solved, Active Streak.
   - Interactive Hours Spent bar chart and Circular Mastery Performance gauge.
   - Daily Learning Goals checklist.
   - Ongoing roadmaps with progress bars and recent activity feed.
   - Daily AI performance review summary preview.

4. **Multi-Disciplinary Algorithm Roadmaps (7 Streams)**
   - Data Structures & Algorithms (DSA)
   - Artificial Intelligence & Machine Learning (AI/ML)
   - Deep Learning & Neural Networks (DL)
   - Design & Analysis of Algorithms (DAA)
   - Graph Algorithms & Network Theory
   - Optimization Algorithms
   - Computational & Domain-Specific Algorithms
   - Beginner, Intermediate, Advanced, and Master level milestone progressions.

5. **Concept Learning Module**
   - Searchable lesson library with topic filters.
   - Fundamental explanations from first principles.
   - Step-by-step execution sequence.
   - Real-world applications and code illustrations.
   - Pseudocode with copy actions and Big-O time/space complexity cards.
   - In-app embedded video lesson player.
   - Interactive algorithm visualization launcher.
   - "Mark Complete" tracking progress in the database.

6. **Interactive Algorithm Visualization Workspace**
   - Step-by-step stepper with Play, Pause, Next, Previous, Reset, and Speed controls (0.5x, 1x, 2x).
   - Live animations for:
     - Sorting: Bubble Sort, Selection Sort, Insertion Sort, Merge Sort, Quick Sort (active comparisons, swaps, sorted highlights).
     - Searching: Binary Search & Linear Search (low/mid/high pointers and target match).
     - Linear Data Structures: Arrays, Linked Lists (pointer mutations), Stacks (LIFO), Queues (FIFO).
     - Trees & Binary Search Trees (BST node insertions and traversals).
     - Graph Traversals: BFS and DFS (node network with visited states, active queue/stack).
     - Shortest Paths: Dijkstra's Algorithm (priority relaxation table and distance updates).
     - Dynamic Programming: Fibonacci memoization tree.
   - Side-by-side pseudocode line highlighter and variable watch-table.

7. **Coding Practice Bank & In-App Editor**
   - Searchable problem bank with filters for difficulty, topic, pattern, and status.
   - Python and Java language selection.
   - Split-screen workspace: problem statement & examples on left, code editor on right.
   - Isolated sandboxed execution engine with strict timeouts and memory safeguards.
   - Sample test cases, hidden test cases, and custom input runner.
   - Test execution results showing runtime in ms, stdout, stderr, and pass/fail badges.
   - Bookmarking and revision list support.

8. **AI Personal Tutor**
   - Persistent assistant drawer and full-page chat interface.
   - Explains concepts in simple language, answers doubts, and derives time and space complexity.
   - Context-aware: receives current problem, active code, and error tracebacks.
   - Multi-turn conversation history.
   - Configurable LLM adapter (Gemini, OpenAI, Groq) with built-in pedagogical algorithmic intelligence engine fallback.

9. **Intelligent Code Debugger**
   - Analyzes student code, syntax errors, and runtime tracebacks.
   - Classifies error types (Syntax, Boundary/Index, Logical, Time Limit Exceeded).
   - Explains what went wrong, why it happened, and how to fix it without revealing the full solution.

10. **3-Level Progressive Hint System**
    - Level 1: Conceptual clue (identifies the needed concept).
    - Level 2: Algorithmic direction (explains the logical strategy).
    - Level 3: Pseudocode blueprint (shows code structure without giving away the answer).
    - Tracks hint level usage to encourage independent problem-solving.

11. **AI Project Builder / Creative Workspace**
    - Natural language prompt generator ("Create a Pathfinding Visualizer in HTML/JS").
    - Multi-file project structure generator (HTML, CSS, JS, Python).
    - In-browser code editor with multi-file tree.
    - Live interactive sandbox preview (sandboxed iframe).
    - Save, reload, and revisit projects.

12. **Progress & Mastery Tracker**
    - Real database statistics for total concepts completed, problems solved, and accuracy.
    - Topic-wise competency progress bars.

13. **Streaks & Heatmap Calendar**
    - GitHub/LeetCode-style 180-to-365 day activity calendar heatmap (levels 0-4).
    - Current streak, longest streak, and active days telemetry.

14. **Weekly Learning Analytics**
    - Stacked daily hours chart (Concepts vs Coding vs Visualizations).
    - Active days density, time allocation ratios, and week-over-week comparisons.

15. **Daily AI Performance Review**
    - Real activity analysis across 7 required pillars:
      1. Overall summary
      2. High performance & strengths
      3. Common mistakes detected
      4. Concepts to improve
      5. Recommended revisions
      6. Actionable next day plan
      7. Achievable daily targets

16. **Student Profile & Settings**
    - Edit full name, bio, preferred language (Python/Java), difficulty level.
    - Dark/Light mode theme toggle.
    - External LLM API key configuration.

---

## 🛠️ Technology Stack

- **Frontend**: React 19, Vite, Tailwind CSS / Custom Design System, Lucide React icons.
- **Backend**: Python 3.13, FastAPI, Uvicorn, SQLAlchemy 2.0, Pydantic v2.
- **Database**: SQLite (out-of-the-box zero setup) or PostgreSQL via `DATABASE_URL`.
- **Authentication**: JWT (JSON Web Tokens) with PBKDF2/HMAC-SHA256 password hashing.
- **Code Execution**: Sandboxed isolated execution runner with timeout and memory enforcement.

---

## 🚀 Quick Start Guide

### 1. Start the Backend API Server
```powershell
# Navigate to the backend directory
cd backend

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Start FastAPI server
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
The backend will automatically create all database tables and seed the rich multi-disciplinary curriculum on first run.
- **API URL**: `http://127.0.0.1:8000`
- **Swagger Documentation**: `http://127.0.0.1:8000/docs`

### 2. Start the Frontend Development Server
```powershell
# In a new terminal, navigate to the frontend directory
cd frontend

# Start the Vite development server
npm run dev
```
- **Frontend URL**: `http://localhost:5173`

---

## 🔑 Demo Account Credentials
For instant testing and evaluation:
- **Email**: `demo@algomentor.dev`
- **Password**: `algomentor123`
*(Or click the "1-Click Instant Demo Login" button in the sign-in modal)*

---

## 🧪 Running Automated Tests
```powershell
cd backend
python -m unittest tests/test_backend.py
```
This runs 10 test suites verifying authentication, dashboard metrics, 7 roadmap streams, concept lessons, practice bank, code execution sandbox, 3-level progressive hints, intelligent debugger, AI project builder, and streaks/analytics.
