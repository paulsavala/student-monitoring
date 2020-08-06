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
    def test_add_to_list(self):
        # Simple case
        result1 = models.add_to_list([1, 2, 3], [4, 5, 6])
        expected1 = [1, 2, 3, 4, 5, 6]
        self.assertEqual(result1, expected1)

        # Duplicate values
        result2 = models.add_to_list([1, 2, 3], [1, 5, 6])
        expected2 = [1, 2, 3, 1, 5, 6]
        self.assertEqual(result2, expected2)

        # Out of order
        result3 = models.add_to_list([5, 4, 3], [1, 2])
        expected3 = [5, 4, 3, 1, 2]
        self.assertEqual(result3, expected3)

        # Append single item to list
        result4 = models.add_to_list([5, 4, 3], 1)
        expected4 = [5, 4, 3, 1]
        self.assertEqual(result4, expected4)

        # Append list to single item
        result5 = models.add_to_list(1, [2, 3, 4])
        expected5 = [1, 2, 3, 4]
        self.assertEqual(result5, expected5)

        # Append single item to single item
        result6 = models.add_to_list(1, 2)
        expected6 = [1, 2]
        self.assertEqual(result6, expected6)

        # Empty append list
        result7 = models.add_to_list([5, 4, 3], [])
        expected7 = [5, 4, 3]
        self.assertEqual(result7, expected7)

        # Empty source list
        result8 = models.add_to_list([], [1, 2, 3])
        expected8 = [1, 2, 3]
        self.assertEqual(result8, expected8)

        # None append list
        result9 = models.add_to_list([1, 2, 3], None)
        expected9 = [1, 2, 3, None]
        self.assertEqual(result9, expected9)

        # None source list
        result10 = models.add_to_list(None, [1, 2, 3])
        expected10 = [1, 2, 3]
        self.assertEqual(result10, expected10)

    def test_remove_from_list(self):
        # Simple case
        result1 = models.remove_from_list([1, 2, 3, 4, 5, 6], [4, 5, 6])
        expected1 = [1, 2, 3]
        self.assertEqual(result1, expected1)

        # Duplicate values
        result2 = models.remove_from_list([1, 1, 2, 3], [1])
        expected2 = [2, 3]
        self.assertEqual(result2, expected2)

        # Items to be removed don't exist in orig (want it to throw an exception)
        try:
            result3 = models.remove_from_list([1, 2, 3], [4, 5, 6])
            # Really just checking if it goes past the previous line without throwing an exception
            self.assertTrue(False)
        except AssertionError:
            # It's supposed to throw an error, so affirming that it did
            self.assertTrue(True)

        # Ignore warnings about item not existing in list
        result3 = models.remove_from_list([1, 2, 3], [4, 5, 6], ignore_warnings=True)
        # Really just checking if it goes past the previous line without throwing an exception
        expected3 = [1, 2, 3]
        self.assertEqual(result3, expected3)

        # Remove single item to list
        result4 = models.remove_from_list([1, 2, 3], 1)
        expected4 = [2, 3]
        self.assertEqual(result4, expected4)

        # Remove list from single item
        result5 = models.remove_from_list(1, [1, 2, 3], ignore_warnings=True)
        expected5 = []
        self.assertEqual(result5, expected5)

        # Remove single item from single item
        result6 = models.remove_from_list(1, 1)
        expected6 = []
        self.assertEqual(result6, expected6)

        # Empty remove list
        result7 = models.remove_from_list([1, 2, 3], [])
        expected7 = [1, 2, 3]
        self.assertEqual(result7, expected7)

        # Empty source list
        result8 = models.remove_from_list([], [1, 2, 3], ignore_warnings=True)
        expected8 = []
        self.assertEqual(result8, expected8)

        # None remove list
        result9 = models.remove_from_list([1, 2, 3], None, ignore_warnings=True)
        expected9 = [1, 2, 3]
        self.assertEqual(result9, expected9)

        # None source list
        result10 = models.remove_from_list(None, [1, 2, 3], ignore_warnings=True)
        expected10 = [None]
        self.assertEqual(result10, expected10)


# class DatabaseCase(unittest.TestCase):
#     def setUp(self):
#         self.db_endpoint = StEdwardsTestConfig.DB_ENDPOINT
#         self.conn = db.create_connection(self.db_endpoint)
#         self.cursor = db.create_cursor(self.conn)
#
#
#     def tearDown(self):
#         self.conn.close()
#         os.remove(self.db_endpoint)
#
#
#     def test_run_query(self):
#         # No params
#         result1 = db.run_query('SELECT 1;', self.cursor)
#         self.assertTrue(len(result1) > 0)
#
#         # With params
#         result2 = db.run_query('SELECT 1 FROM schools WHERE id=%s;', self.cursor, (1,))
#         self.assertTrue(len(result2) > 0)

    
    # def test_bootstrap(self):
    #     self.conn, self.cursor = bootstrap(self.db_endpoint, db)
    #     self.assertTrue(os.path.isfile(self.db_endpoint), msg="Sqlite test db doesn't exist")
    #
    #     # Check that all expected tables exist
    #     result1 = db.run_query('SELECT 1 FROM schools;', self.cursor)
    #     result2 = db.run_query('SELECT 1 FROM college_of;', self.cursor)
    #     result3 = db.run_query('SELECT 1 FROM departments;', self.cursor)
    #     result4 = db.run_query('SELECT 1 FROM instructors;', self.cursor)
    #     result5 = db.run_query('SELECT 1 FROM courses;', self.cursor)
    #     result6 = db.run_query('SELECT 1 FROM outliers;', self.cursor)
    #
    #     self.assertTrue(len(result1) == 1)
    #     self.assertTrue(result1[0] == 1)
    #     self.assertTrue(len(result2) == 1)
    #     self.assertTrue(result2[0] == 1)
    #     self.assertTrue(len(result3) == 1)
    #     self.assertTrue(result3[0] == 1)
    #     self.assertTrue(len(result4) == 1)
    #     self.assertTrue(result4[0] == 1)
    #     self.assertTrue(len(result5) == 1)
    #     self.assertTrue(result5[0] == 1)
    #     self.assertTrue(len(result6) == 1)
    #     self.assertTrue(result6[0] == 1)


class AssignmentModelCase(unittest.TestCase):
    def setUp(self):
        datetime_format = '%Y-%m-%dT%H:%M:%SZ'
        self.assignment1 = Assignment(1, 'hw1', '2018-01-02T23:59:00Z', None, datetime_format)

    
    def test_valid_date_format(self):
        self.assertIsInstance(self.assignment1.due_date, datetime)


class CourseModelCase(unittest.TestCase):
    def setUp(self):
        # Course with alias
        self.course1 = Course(1, 'TEST123')
        # Course without alias
        self.course2 = Course(2, 'TEST123', 'My test course')

    def test_add_students(self):
        # Add single student
        self.course1.add_students(Student('test1', 1))
        self.assertEqual(len(self.course1.students), 1)

        # Add multiple students
        self.course1.add_students([Student('test2', 2), Student('test3', 3)])
        self.assertEqual(len(self.course1.students), 3)

    def test_remove_students(self):
        # Add single student
        self.course1.add_students(Student('test1', 1))
        self.assertEqual(len(self.course1.students), 1)

        # Add multiple students
        self.course1.add_students([Student('test2', 2), Student('test3', 3)])
        self.assertEqual(len(self.course1.students), 3)

        # Remove a single student
        self.course1.remove_students(Student('test1', 1), unique_attr='lms_id')
        self.assertEqual(len(self.course1.students), 2)

        # Remove multiple students
        self.course1.remove_students([Student('test2', 2), Student('test3', 3)], unique_attr='lms_id')
        self.assertEqual(len(self.course1.students), 0)

    def test_add_assignments(self):
        # Add a single assignment
        datetime_format = '%Y-%m-%dT%H:%M:%SZ'
        self.course1.add_assignments(Assignment(1, 'hw1', '2018-01-02T23:59:00Z', None, datetime_format))
        self.assertEqual(len(self.course1.assignments), 1)

        # Add multiple assignments (note that assignment added in previous test already exists, so three total)
        datetime_format = '%Y-%m-%dT%H:%M:%SZ'
        self.course1.add_assignments([Assignment(2, 'hw2', '2018-01-02T23:59:00Z', None, datetime_format),
                                     Assignment(3, 'hw3', '2018-02-03T23:59:00Z', None, datetime_format)])
        self.assertEqual(len(self.course1.assignments), 3)

    def test_remove_assignments(self):
        # Add assignments (so that you can remove them for testing)
        datetime_format = '%Y-%m-%dT%H:%M:%SZ'
        self.course1.add_assignments([Assignment(1, 'hw1', '2018-01-02T23:59:00Z', None, datetime_format),
                                     Assignment(2, 'hw2', '2018-02-03T23:59:00Z', None, datetime_format),
                                      Assignment(3, 'hw3', '2018-02-03T23:59:00Z', None, datetime_format)])
        self.assertEqual(len(self.course1.assignments), 3)

        # Remove a single assignment
        self.course1.remove_assignments(Assignment(1, 'hw1', '2018-01-02T23:59:00Z', None, datetime_format),
                                        unique_attr='lms_id')
        self.assertEqual(len(self.course1.assignments), 2)

        # Remove multiple assignments
        self.course1.remove_assignments([Assignment(2, 'hw2', '2018-01-02T23:59:00Z', None, datetime_format),
                                        Assignment(3, 'hw3', '2018-02-03T23:59:00Z', None, datetime_format)],
                                        unique_attr='lms_id')
        self.assertEqual(len(self.course1.assignments), 0)

    def test_create_context_dict(self):
        pass


class EnrollmentModelCase(unittest.TestCase):
    def setUp(self):
        student = Student('test', 1)
        course = Course(1, 'test_course')
        datetime_format = '%Y-%m-%dT%H:%M:%SZ'
        assignment1 = Assignment(1, 'hw1', '2018-01-02T23:59:00Z', course, datetime_format)
        assignment2 = Assignment(2, 'hw2', '2018-01-02T23:59:00Z', course, datetime_format)
        assignment3 = Assignment(3, 'hw3', '2018-01-02T23:59:00Z', course, datetime_format)
        assignment4 = Assignment(4, 'hw4', '2018-01-02T23:59:00Z', course, datetime_format)
        self.grade1 = Grade(student, course, assignment1, 0.85)
        self.grade2 = Grade(student, course, assignment2, 0.75)
        self.grade3 = Grade(student, course, assignment3, 0.65)
        self.grade4 = Grade(student, course, assignment4, 0.55)

        self.enrollment = Enrollment(student, course, [self.grade1], 0.75)

    def test_add_grades(self):
        # Add single grade
        self.enrollment.add_grades(self.grade2)
        self.assertEqual(len(self.enrollment.grades), 2)

        # Add multiple grades
        self.enrollment.add_grades([self.grade3, self.grade4])
        self.assertEqual(len(self.enrollment.grades), 4)

    def test_remove_grades(self):
        # Remove a single grade
        self.enrollment.remove_grades(self.grade4, unique_attr='assignment')
        self.assertEqual(len(self.enrollment.grades), 3)

        # Remove multiple grades
        self.enrollment.remove_grades([self.grade2, self.grade3], unique_attr='assignment')
        self.assertEqual(len(self.enrollment.grades), 1)

    def test_get_grades(self):
        pass

    def test_form_ci(self):
        pass

    def test_set_ci(self):
        pass

    def test_get_outliers(self):
        pass

    def test_commit_outliers_to_db(self):
        pass


class GradeModelCase(unittest.TestCase):
    def setUp(self):
        student = Student('test', 1)
        course = Course(1, 'test_course')
        datetime_format = '%Y-%m-%dT%H:%M:%SZ'
        assignment = Assignment(1, 'hw1', '2018-01-02T23:59:00Z', course, datetime_format)
        self.grade = Grade(student, course, assignment, 0.85)
    
    def test_is_outlier(self):
        # Not an outlier
        result = self.grade.is_outlier(0.5, 1)
        self.assertFalse(result)

        # Low outlier
        result = self.grade.is_outlier(0.9, 1)
        self.assertTrue(result)

        # High outlier
        result = self.grade.is_outlier(0.5, 0.6)
        self.assertTrue(result)


class InstructorModelCase(unittest.TestCase):
    def setUp(self):
        self.instructor = Instructor('john', 'smith', 'jsmith@stedwards.edu', 123)
        self.course1 = Course(1, 'test_course1')
        self.course2 = Course(2, 'test_course2')
        self.course3 = Course(3, 'test_course3')
    
    def test_add_courses(self):
        # Add a single course
        self.instructor.add_courses(self.course1)
        self.assertEqual(len(self.instructor.courses), 1)

        # Add multiple courses
        self.instructor.add_courses([self.course2, self.course3])
        self.assertEqual(len(self.instructor.courses), 3)
    
    def test_remove_courses(self):
        # Add a single course
        self.instructor.add_courses(self.course1)
        self.assertEqual(len(self.instructor.courses), 1)

        # Add multiple courses
        self.instructor.add_courses([self.course2, self.course3])
        self.assertEqual(len(self.instructor.courses), 3)
        
        # Remove a single course
        self.instructor.remove_courses(self.course1, unique_attr='lms_id')
        self.assertEqual(len(self.instructor.courses), 2)

        # Remove multiple courses
        self.instructor.remove_courses([self.course2, self.course3], unique_attr='lms_id')
        self.assertEqual(len(self.instructor.courses), 0)
    
    def test_render_email(self):
        pass

    def test_send_email(self):
        pass


class StudentModelCase(unittest.TestCase):
    def setUp(self):
        self.student = Student('test1', 123)
        self.course1 = Course(1, 'test_course1')
        self.course2 = Course(2, 'test_course2')
        self.course3 = Course(3, 'test_course3')
        self.course4 = Course(4, 'test_course4')
        self.enrollment1 = Enrollment(self.student, self.course1)
        self.enrollment2 = Enrollment(self.student, self.course2)
        self.enrollment3 = Enrollment(self.student, self.course3)
    
    def test_add_enrollments(self):
        # Add a single enrollment
        self.student.add_enrollments(self.enrollment1)
        self.assertEqual(len(self.student.enrollments), 1)

        # Add multiple enrollments
        self.student.add_enrollments([self.enrollment2, self.enrollment3])
        self.assertEqual(len(self.student.enrollments), 3)
    
    def test_remove_enrollments(self):
        # Remove a single enrollment
        self.student.remove_enrollments(self.enrollment1)
        self.assertEqual(len(self.student.enrollments), 2)

        # Remove multiple enrollments
        self.student.remove_enrollments([self.enrollment2, self.enrollment3])
        self.assertEqual(len(self.student.enrollments), 0)

    def test_get_enrollments_by_course(self):
        # Add the enrollments back
        self.test_add_enrollments()

        # Course with enrollments
        enrollments = self.student.get_enrollment_by_course(self.course1)
        self.assertEqual(enrollments.course.lms_id, 1)

        # Course with no enrollments (show throw an error)
        try:
            self.student.get_enrollment_by_course(self.course4)
            # Really just checking if it goes past the previous line without throwing an exception
            self.assertTrue(False)
        except AssertionError:
            # It's supposed to throw an error, so affirming that it did
            self.assertTrue(True)


class AppCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
