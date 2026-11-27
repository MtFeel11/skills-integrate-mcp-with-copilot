import unittest
from unittest.mock import patch

from fastapi import HTTPException

from src.app import activities, signup_for_activity


class SignupCapacityTests(unittest.TestCase):
    def test_signup_succeeds_when_one_spot_remains(self):
        test_activity = {
            "max_participants": 2,
            "participants": ["existing@mergington.edu"],
        }

        with patch.dict(activities, {"Test Activity": test_activity}):
            result = signup_for_activity("Test Activity", "new@mergington.edu")

        self.assertEqual(
            result,
            {"message": "Signed up new@mergington.edu for Test Activity"},
        )
        self.assertEqual(len(test_activity["participants"]), 2)

    def test_signup_is_rejected_when_activity_is_full(self):
        test_activity = {
            "max_participants": 1,
            "participants": ["existing@mergington.edu"],
        }

        with patch.dict(activities, {"Test Activity": test_activity}):
            with self.assertRaises(HTTPException) as raised:
                signup_for_activity("Test Activity", "new@mergington.edu")

        self.assertEqual(raised.exception.status_code, 409)
        self.assertEqual(raised.exception.detail, "Activity is full")
        self.assertEqual(test_activity["participants"], ["existing@mergington.edu"])

    def test_duplicate_signup_is_rejected_even_when_activity_is_full(self):
        test_activity = {
            "max_participants": 1,
            "participants": ["existing@mergington.edu"],
        }

        with patch.dict(activities, {"Test Activity": test_activity}):
            with self.assertRaises(HTTPException) as raised:
                signup_for_activity("Test Activity", "existing@mergington.edu")

        self.assertEqual(raised.exception.status_code, 400)
        self.assertEqual(raised.exception.detail, "Student is already signed up")


if __name__ == "__main__":
    unittest.main()
