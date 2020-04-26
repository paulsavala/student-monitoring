from canvasapi import Canvas
from lms.generic import GenericApi
from models.course import Course
from models.instructor import Instructor
from models.assignment import Assignment, AssignmentCollection
from models.student import Student

from collections import defaultdict
import numpy as np


class CanvasApi(GenericApi):
    def _connect_to_lms(self):
        """
        Connects to the Canvas API
        :return: Canvas object (API connection)
        """
        return Canvas(self.api_url, self.api_token)

    def get_instructor(self, populate=False):
        """
        Get Canvas user associated with this api key ('self' is a magic keyword to get the current user)
        :param: populate: Bool, defaults to True. Whether or not to run populate_instructor upon creation.
        :return: Instructor object
        """
        instructor_obj = self.lms.get_user(user='self')
        email = instructor_obj.get_profile()['primary_email']
        instructor = Instructor(name=instructor_obj.name, email=email, lms_id=instructor_obj.id)
        if populate:
            instructor = self.populate_instructor(instructor)
        return instructor

    def populate_instructor(self, instructor):
        """
        Get all courses for the instructor, along with all students and grades in those courses
        :param: instructor: Instructor object
        :return: Instructor object
        """
        courses = self.get_courses(instructor)
        instructor.courses = courses
        for c in courses:
            c.students = self.get_students_in_course(c)
            course_grades = self.get_course_grades(c)
            course_grades_by_student = {ac.student.lms_id: ac for ac in course_grades}
            for s in c.students:
                s.set_assignments(course_grades_by_student[s.lms_id])
        return instructor

    def get_courses(self, instructor):
        """
        Get all courses from Canvas for an instructor
        :param instructor: Instructor object
        :return: List of Course objects
        """
        instructor_obj = self.lms.get_user(user=instructor.lms_id)
        all_courses = instructor_obj.get_courses(enrollment_type='teacher', include=['term', 'total_students'])
        # todo: Is there a better way to get the current term than hard-coding it?
        current_courses = [c for c in all_courses if c.term['name'] == 'Spring 2020']
        # Filter out courses with no students
        current_courses = [c for c in current_courses if c.total_students > 0]
        courses = [Course(c.id, c.name, instructor) for c in current_courses]
        return courses

    def get_students_in_course(self, course):
        """
        Get all students in a course
        :param course: Course object
        :return: List of Student objects
        """
        course_obj = self.lms.get_course(course.course_id)
        enrollments_obj = course_obj.get_enrollments(type=['StudentEnrollment'])
        students = [Student(name=e.user['name'], lms_id=e.user['id']) for e in enrollments_obj]
        return students

    def get_course_grade_summary(self, course, summary_stat, last_week=False):
        assert summary_stat.lower() == 'mean' or summary_stat.lower() == 'median', \
            'summary_stat must be either "mean" or "median"'
        course_obj = self.lms.get_course(course.course_id)
        enrollments_obj = course_obj.get_enrollments(type=['StudentEnrollment'])
        current_scores = [e.grades['current_score'] for e in enrollments_obj if e.grades['current_score'] > 0]

        if summary_stat == 'mean':
            summary_stat = np.mean(current_scores)
        elif summary_stat == 'median':
            summary_stat = np.median(current_scores)

        return summary_stat

    def get_course_grades(self, course):
        """
        Get all grades for all students in the given course
        :param course: Course object
        :return: List of AssignmentCollection objects (one per student)
        """
        course_obj = self.lms.get_course(course.course_id)
        all_assignments = course_obj.get_assignments(bucket='past', order_by='due_at')
        graded_assignments = [a for a in all_assignments if getattr(a, 'points_possible') and a.points_possible > 0]
        students = self.get_students_in_course(course)
        students_by_id = {s.lms_id: s for s in students}

        # Store all the Assignments for a single student, keys = student LMS id
        student_assignments = defaultdict(list)

        for a in graded_assignments:
            submissions = a.get_submissions()
            for s in submissions:
                # The test student is not included in the course students, but their submissions are still returned
                if s.user_id not in students_by_id:
                    continue
                # Make sure the assignment has actually been graded, so ungraded assignments aren't treated as zeros
                if s.graded_at is None:
                    continue
                # Fill missing scores with a zero
                if not s.score:
                    s.score = 0
                student_assignments[s.user_id].append(
                    Assignment(students_by_id[s.user_id],
                               a.name,
                               a.due_at,
                               s.score / a.points_possible
                               )
                )

        return [AssignmentCollection(s, course, student_assignments[s.lms_id]) for s in students]

    def get_student_grades(self, student, course):
        """
        Get all grades for a single student in the given course. If you need all grades for all students in a course,
        use get_course_grades instead to reduce the number of API calls.
        :param student: Student object
        :param course: Course object
        :return: AssignmentCollection object
        """
        all_assignments = student.lms_obj.get_assignments(bucket='past', order_by='due_at')
        graded_assignments = [a for a in all_assignments if a.points_possible > 0]
        student_assignments = []

        for a in graded_assignments:
            for s in a.get_submission(student.lms_id):
                student_assignments.append(Assignment(student.lms_id,
                                                      a.name,
                                                      a.due_at,
                                                      s.score / a.points_possible)
                                           )

        return AssignmentCollection(student, course, student_assignments)
