#!/usr/bin/env python
import unittest
from datetime import datetime
import os

from config import StEdwardsTestConfig
from models.assignment import Assignment
from models.course import Course
from models.enrollment import Enrollment
from models.grade import Grade
from models.instructor import Instructor
from models.student import Student

from bootstrap.db import bootstrap
from utils import db, email, models


class UtilsModelsCase(unittest.TestCase):
    @classmethod
    def add_to_list(cls):
        # Simple case
        result1 = models.add_to_list([1, 2, 3], [4, 5, 6])
        expected1 = [1, 2, 3, 4, 5, 6]
        cls.assertEqual(result1, expected1)

        # Duplicate values
        result2 = models.add_to_list([1, 2, 3], [1, 5, 6])
        expected2 = [1, 2, 3, 5, 6]
        cls.assertEqual(result2, expected2)

        # Out of order
        result3 = models.add_to_list([5, 4, 3], [1, 2])
        expected3 = [5, 4, 3, 1, 2]
        cls.assertEqual(result3, expected3)

        # Append single item to list
        result4 = models.add_to_list([5, 4, 3], 1)
        expected4 = [5, 4, 3, 1]
        cls.assertEqual(result4, expected4)

        # Append list to single item
        result5 = models.add_to_list(1, [2, 3, 4])
        expected5 = [1, 2, 3, 4]
        cls.assertEqual(result5, expected5)

        # Append single item to single item
        result6 = models.add_to_list(1, 2)
        expected6 = [1, 2]
        cls.assertEqual(result6, expected6)

        # Empty append list
        result7 = models.add_to_list([5, 4, 3], [])
        expected7 = [5, 4, 3]
        cls.assertEqual(result7, expected7)

        # Empty source list
        result8 = models.add_to_list([], [1, 2, 3])
        expected8 = [1, 2, 3]
        cls.assertEqual(result8, expected8)

        # None append list
        result9 = models.add_to_list([1, 2, 3], None)
        expected9 = [1, 2, 3]
        cls.assertEqual(result9, expected9)

        # None source list
        result10 = models.add_to_list(None, [1, 2, 3])
        expected10 = [1, 2, 3]
        cls.assertEqual(result10, expected10)

    @classmethod
    def remove_from_list(cls):
        # Simple case
        result1 = models.remove_from_list([1, 2, 3, 4, 5, 6], [4, 5, 6])
        expected1 = [1, 2, 3]
        cls.assertEqual(result1, expected1)

        # Duplicate values
        result2 = models.remove_from_list([1, 1, 2, 3], [1])
        expected2 = [2, 3]
        cls.assertEqual(result2, expected2)

        # Items to be removed don't exist in orig
        result1 = models.remove_from_list([1, 2, 3], [4, 5, 6])
        expected1 = [1, 2, 3]
        cls.assertEqual(result1, expected1)

        # Remove single item to list
        result4 = models.remove_from_list([1, 2, 3], 1)
        expected4 = [2, 3]
        cls.assertEqual(result4, expected4)

        # Remove list from single item
        result5 = models.remove_from_list(1, [1, 2, 3])
        expected5 = []
        cls.assertEqual(result5, expected5)

        # Remove single item from single item
        result6 = models.remove_from_list(1, 1)
        expected6 = []
        cls.assertEqual(result6, expected6)

        # Empty remove list
        result7 = models.remove_from_list([1, 2, 3], [])
        expected7 = [1, 2, 3]
        cls.assertEqual(result7, expected7)

        # Empty source list
        result8 = models.remove_from_list([], [1, 2, 3])
        expected8 = []
        cls.assertEqual(result8, expected8)

        # None remove list
        result9 = models.remove_from_list([1, 2, 3], None)
        expected9 = [1, 2, 3]
        cls.assertEqual(result9, expected9)

        # None source list
        result10 = models.remove_from_list(None, [1, 2, 3])
        expected10 = None
        cls.assertEqual(result10, expected10)


class DatabaseCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.db_endpoint = StEdwardsTestConfig.DB_ENDPOINT
        cls.conn = db.create_connection(cls.db_endpoint)
        cls.cursor = db.create_cursor(cls.conn)

    @classmethod
    def tearDown(cls):
        cls.conn.close()
        os.remove(cls.db_endpoint)

    @classmethod
    def run_query(cls):
        # No params
        result1 = db.run_query('SELECT 1;', cls.cursor)
        cls.assertTrue(len(result1) > 0)

        # With params
        result2 = db.run_query('SELECT 1 FROM schools WHERE id=%s;', cls.cursor, (1,))
        cls.assertTrue(len(result2) > 0)

    @classmethod
    def bootstrap(cls):
        cls.conn, cls.cursor = bootstrap(cls.db_endpoint, db)
        cls.assertTrue(os.path.isfile(cls.db_endpoint), msg="Sqlite test db doesn't exist")

        # Check that all expected tables exist
        result1 = db.run_query('SELECT 1 FROM schools;', cls.cursor)
        result2 = db.run_query('SELECT 1 FROM college_of;', cls.cursor)
        result3 = db.run_query('SELECT 1 FROM departments;', cls.cursor)
        result4 = db.run_query('SELECT 1 FROM instructors;', cls.cursor)
        result5 = db.run_query('SELECT 1 FROM courses;', cls.cursor)
        result6 = db.run_query('SELECT 1 FROM outliers;', cls.cursor)

        cls.assertTrue(len(result1) == 1)
        cls.assertTrue(result1[0] == 1)
        cls.assertTrue(len(result2) == 1)
        cls.assertTrue(result2[0] == 1)
        cls.assertTrue(len(result3) == 1)
        cls.assertTrue(result3[0] == 1)
        cls.assertTrue(len(result4) == 1)
        cls.assertTrue(result4[0] == 1)
        cls.assertTrue(len(result5) == 1)
        cls.assertTrue(result5[0] == 1)
        cls.assertTrue(len(result6) == 1)
        cls.assertTrue(result6[0] == 1)


class AssignmentModelCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        datetime_format = '%Y-%m-%dT%H:%M:%SZ'
        cls.assignment1 = Assignment(1, 'hw1', '2018-01-02T23:59:00', None, datetime_format)

    @classmethod
    def valid_date_format(cls):
        cls.assertIsInstance(cls.assignment1.due_date, datetime)


class CourseModelCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        # Course with alias
        cls.course1 = Course(1, 'TEST123')
        # Course without alias
        cls.course2 = Course(2, 'TEST123', 'My test course')

    @classmethod
    def add_students(cls):
        pass

    @classmethod
    def remove_students(cls):
        pass

    @classmethod
    def add_assignments(cls):
        pass

    @classmethod
    def remove_assignments(cls):
        pass

    @classmethod
    def create_context_dict(cls):
        pass


class EnrollmentModelCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        pass

    @classmethod
    def add_grades(cls):
        pass

    @classmethod
    def remove_grades(cls):
        pass

    @classmethod
    def get_grades(cls):
        pass

    @classmethod
    def form_ci(cls):
        pass

    @classmethod
    def set_ci(cls):
        pass

    @classmethod
    def get_outliers(cls):
        pass

    @classmethod
    def commit_outliers_to_db(cls):
        pass


class GradeModelCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        pass

    @classmethod
    def is_outlier(cls):
        pass


class InstructorModelCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        pass

    @classmethod
    def add_courses(cls):
        pass

    @classmethod
    def remove_courses(cls):
        pass

    @classmethod
    def render_email(cls):
        pass

    @classmethod
    def send_email(cls):
        pass


class StudentModelCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        pass

    @classmethod
    def add_enrollments(cls):
        pass

    @classmethod
    def remove_enrollments(cls):
        pass

    @classmethod
    def get_enrollments_by_course(cls):
        pass


class AppCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        pass

    @classmethod
    def tearDown(cls):
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
