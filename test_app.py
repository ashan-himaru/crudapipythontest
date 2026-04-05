import unittest
import json
from app import app, write_users

class FlaskCRUDTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.headers = {"Content-Type": "application/json"}
        # Clear JSON file before each test
        write_users([])

    def test_create_user(self):
        data = {"name": "Alice", "email": "alice@example.com"}
        response = self.app.post("/users", headers=self.headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data)
        self.assertEqual(result["name"], "Alice")
        self.assertEqual(result["email"], "alice@example.com")
        self.assertEqual(result["id"], 1)

    def test_get_all_users(self):
        self.test_create_user()
        response = self.app.get("/users", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Alice")

    def test_get_single_user(self):
        self.test_create_user()
        response = self.app.get("/users/1", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "Alice")

    def test_update_user(self):
        self.test_create_user()
        data = {"name": "Alice Smith"}
        response = self.app.put("/users/1", headers=self.headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result["name"], "Alice Smith")

    def test_delete_user(self):
        self.test_create_user()
        response = self.app.delete("/users/1", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertIn("message", result)
        self.assertEqual(result["message"], "User deleted successfully")

if __name__ == "__main__":
    unittest.main()


