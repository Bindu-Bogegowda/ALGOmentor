import sys
import os
import unittest
from fastapi.testclient import TestClient

# Ensure backend directory is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app
from app.database import Base, engine, SessionLocal
from app.services.seed_data import seed_database

class TestAlgoMentorAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        seed_database(db)
        db.close()
        cls.client = TestClient(app)

    def test_01_root_health(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["platform"], "AlgoMentor")
        self.assertEqual(data["status"], "operational")

    def test_02_demo_login(self):
        res = self.client.post("/api/v1/auth/login", json={
            "username_or_email": "demo@algomentor.dev",
            "password": "algomentor123"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("access_token", data)
        self.assertEqual(data["user"]["email"], "demo@algomentor.dev")
        self.__class__.token = data["access_token"]

    def test_03_dashboard_stats(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        res = self.client.get("/api/v1/dashboard/stats", headers=headers)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("welcome_message", data)
        self.assertGreaterEqual(data["concepts_completed"], 1)
        self.assertGreaterEqual(data["problems_solved"], 1)
        self.assertGreaterEqual(data["current_streak"], 1)

    def test_04_roadmaps(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        res = self.client.get("/api/v1/roadmaps", headers=headers)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreaterEqual(len(data), 7) # All 7 streams present
        stream_ids = [s["id"] for s in data]
        self.assertIn("dsa", stream_ids)
        self.assertIn("aiml", stream_ids)
        self.assertIn("graph", stream_ids)

    def test_05_concept_lessons(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        res = self.client.get("/api/v1/lessons", headers=headers)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreaterEqual(len(data), 1)

        # Detail of bubble sort lesson
        res_detail = self.client.get("/api/v1/lessons/lesson_bubble_sort", headers=headers)
        self.assertEqual(res_detail.status_code, 200)
        detail = res_detail.json()
        self.assertIn("fundamental_explanation", detail)
        self.assertIn("pseudocode", detail)
        self.assertIn("video_url", detail)

    def test_06_code_execution_run(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        python_code = """
def solve():
    print(3)
solve()
"""
        res = self.client.post("/api/v1/execution/run", json={
            "language": "python",
            "code": python_code,
            "custom_input": "hello"
        }, headers=headers)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["stdout"], "3")

    def test_07_code_execution_submission(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        valid_solution = """def count_vowels(s: str) -> int:
    vowels = set("aeiouAEIOU")
    return sum(1 for c in s if c in vowels)

if __name__ == '__main__':
    import sys
    inp = sys.stdin.read().strip()
    print(count_vowels(inp))"""
        
        # Get problem 1 (count vowels)
        res = self.client.post("/api/v1/execution/submit", json={
            "problem_id": 1,
            "language": "python",
            "code": valid_solution
        }, headers=headers)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "Accepted")
        self.assertEqual(data["passed_tests"], data["total_tests"])

    def test_08_progressive_hints(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        for level in [1, 2, 3]:
            res = self.client.post("/api/v1/hints", json={
                "problem_id": 1,
                "level": level
            }, headers=headers)
            self.assertEqual(res.status_code, 200)
            data = res.json()
            self.assertEqual(data["level"], level)
            self.assertTrue(len(data["content"]) > 0)

    def test_09_intelligent_debugger(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        res = self.client.post("/api/v1/debugger/analyze", json={
            "language": "python",
            "code": "def test():\n    for i in range(10)\n        print(i)",
            "runtime_error": "SyntaxError: expected ':'"
        }, headers=headers)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("Syntax", data["error_type"])
        self.assertTrue(len(data["how_to_fix"]) > 0)

    def test_10_ai_tutor_chat(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        res = self.client.post("/api/v1/ai-tutor/chat", json={
            "message": "What is the time complexity of Quick Sort?",
            "context_page": "general"
        }, headers=headers)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(len(data["reply"]) > 0)

    def test_11_project_builder(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        res = self.client.post("/api/v1/projects/generate", json={
            "prompt": "Create an interactive Dijkstra grid visualizer",
            "project_type": "web_interactive"
        }, headers=headers)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(len(data["files"]) >= 1)

    def test_12_streaks_and_analytics(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        res_streak = self.client.get("/api/v1/streaks/calendar", headers=headers)
        self.assertEqual(res_streak.status_code, 200)
        streak_data = res_streak.json()
        self.assertGreaterEqual(len(streak_data["calendar_days"]), 100)

        res_analytics = self.client.get("/api/v1/analytics/weekly", headers=headers)
        self.assertEqual(res_analytics.status_code, 200)
        analytics_data = res_analytics.json()
        self.assertEqual(len(analytics_data["daily_breakdown"]), 7)

    def test_13_daily_review(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        res = self.client.get("/api/v1/reviews/today", headers=headers)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(len(data["overall_summary"]) > 0)
        self.assertTrue(len(data["strengths"]) > 0)
        self.assertTrue(len(data["common_mistakes"]) > 0)

if __name__ == "__main__":
    unittest.main()
