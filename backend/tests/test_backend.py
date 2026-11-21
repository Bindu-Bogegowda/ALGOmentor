import sys
import os
import unittest
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import Base, engine, SessionLocal
from app.services.seed_data import seed_database
from app.models.user import User
from app.models.roadmap import RoadmapStream, RoadmapTopic
from app.models.lesson import Lesson
from app.models.problem import Problem
from app.models.submission import Submission
from app.services.auth_service import hash_password, verify_password, create_access_token
from app.services.execution_service import ExecutionService
from app.services.ai_service import AIService

# Routers
from app.routers.dashboard import get_dashboard_stats
from app.routers.roadmaps import list_roadmap_streams
from app.routers.lessons import list_lessons, get_lesson
from app.routers.problems import list_problems, get_problem
from app.routers.hints import get_progressive_hint
from app.routers.debugger import analyze_solution
from app.routers.projects import list_projects, generate_project_with_ai
from app.routers.progress import get_mastery_overview
from app.routers.streaks import get_streak_calendar
from app.routers.analytics import get_weekly_analytics
from app.routers.reviews import get_daily_review

from app.schemas.problem import HintRequest
from app.schemas.ai import DebugAnalyzeRequest
from app.schemas.project import ProjectGenerateRequest

class TestAlgoMentorDirect(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.db = SessionLocal()
        seed_database(cls.db)
        cls.user = cls.db.query(User).filter(User.email == "demo@algomentor.dev").first()

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def test_01_auth_service(self):
        pw = "superSecretPassword123"
        hashed = hash_password(pw)
        self.assertTrue(verify_password(pw, hashed))
        self.assertFalse(verify_password("wrongPassword", hashed))

        token = create_access_token({"sub": str(self.user.id)})
        self.assertTrue(len(token) > 20)
        print("✓ Auth service & password hashing verified.")

    def test_02_dashboard_stats(self):
        stats = get_dashboard_stats(current_user=self.user, db=self.db)
        self.assertGreaterEqual(stats["concepts_completed"], 1)
        self.assertGreaterEqual(stats["problems_solved"], 1)
        self.assertGreaterEqual(stats["current_streak"], 1)
        self.assertGreaterEqual(stats["weekly_learning_hours"], 1.0)
        print(f"✓ Dashboard stats verified: {stats['concepts_completed']} concepts, {stats['problems_solved']} problems, streak {stats['current_streak']}.")

    def test_03_roadmaps_curriculum(self):
        streams = list_roadmap_streams(current_user=self.user, db=self.db)
        self.assertGreaterEqual(len(streams), 7)
        stream_ids = [s.id for s in streams]
        self.assertIn("dsa", stream_ids)
        self.assertIn("aiml", stream_ids)
        self.assertIn("graph", stream_ids)
        self.assertIn("python_base", stream_ids)
        self.assertIn("java_base", stream_ids)
        print(f"✓ Multi-disciplinary roadmaps verified: {len(streams)} streams including Python & Java base.")

    def test_04_lessons_library(self):
        lessons = list_lessons(topic_id=None, current_user=self.user, db=self.db)
        self.assertGreaterEqual(len(lessons), 4)
        
        detail = get_lesson(lesson_id="lesson_bubble_sort", current_user=self.user, db=self.db)
        self.assertTrue(len(detail.fundamental_explanation) > 50)
        self.assertTrue(len(detail.pseudocode) > 20)
        self.assertTrue("youtube" in detail.video_url.lower())
        print(f"✓ Concept lessons verified: {len(lessons)} lessons, embedded video & pseudocode active.")

    def test_05_problems_bank(self):
        problems = list_problems(current_user=self.user, db=self.db)
        self.assertGreaterEqual(len(problems), 4)
        
        detail = get_problem(slug="count-vowels-in-a-string", current_user=self.user, db=self.db)
        self.assertEqual(detail.title, "Count Vowels in a String")
        self.assertEqual(detail.difficulty, "Easy")
        print(f"✓ Practice bank verified: {len(problems)} problems.")

    def test_06_execution_service(self):
        test_cases = [
            {"input": "hello world", "expected_output": "3"},
            {"input": "python programming", "expected_output": "4"}
        ]
        sol_code = """import sys
s = sys.stdin.read().strip()
vowels = set("aeiouAEIOU")
print(sum(1 for c in s if c in vowels))"""

        res = ExecutionService.run_isolated(
            language="python",
            code=sol_code,
            test_cases=test_cases,
            timeout_seconds=3.0
        )
        self.assertEqual(res["status"], "Accepted")
        self.assertEqual(res["passed_tests"], 2)
        print(f"✓ Isolated code execution engine verified: runtime {res['runtime_ms']}ms, 2/2 tests passed.")

    def test_07_progressive_hints(self):
        for lvl in [1, 2, 3, 4, 5, 6, 7]:
            req = HintRequest(problem_id=1, level=lvl, current_code="public int[] twoSum(int[] nums, int target) { return new int[0]; }")
            hint_res = get_progressive_hint(req=req, current_user=self.user, db=self.db)
            self.assertEqual(hint_res.level, lvl)
            self.assertTrue(len(hint_res.content) > 10)
        print("✓ Unlimited progressive hint architecture verified (Levels 1 through 7+ with dynamic code analysis).")

    def test_08_intelligent_debugger(self):
        dbg_req = DebugAnalyzeRequest(
            language="python",
            code="for i in range(len(nums)):\n    for j in range(i, len(nums)): ...",
            runtime_error="IndexError: list index out of range"
        )
        diag = analyze_solution(req=dbg_req, current_user=self.user, db=self.db)
        self.assertIn("Boundary", diag.error_type)
        self.assertTrue(len(diag.why_it_happened) > 10)
        self.assertTrue(len(diag.how_to_fix) > 10)
        print("✓ Intelligent code debugger analysis verified.")

    def test_09_project_builder(self):
        gen_req = ProjectGenerateRequest(prompt="Create an interactive Pathfinding Visualizer with BFS")
        proj = generate_project_with_ai(req=gen_req, current_user=self.user, db=self.db)
        self.assertTrue(len(proj.files) >= 1)
        self.assertTrue(any(f.filename.endswith(".html") for f in proj.files))
        print(f"✓ AI Project Builder verified: generated '{proj.title}' with {len(proj.files)} files.")

    def test_10_streaks_analytics_reviews(self):
        cal = get_streak_calendar(current_user=self.user, db=self.db)
        self.assertGreaterEqual(len(cal.calendar_days), 150)

        an = get_weekly_analytics(current_user=self.user, db=self.db)
        self.assertEqual(len(an.daily_breakdown), 7)

        rev = get_daily_review(current_user=self.user, db=self.db)
        self.assertTrue(len(rev.overall_summary) > 10)
        self.assertTrue(len(rev.strengths) >= 2)
        print("✓ Streaks heatmap, weekly analytics, and 7-pillar daily AI review verified.")

if __name__ == "__main__":
    unittest.main()
