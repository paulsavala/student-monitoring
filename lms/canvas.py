from canvasapi import Canvas
from lms.generic import GenericApi

from collections import defaultdict
import numpy as np


class CanvasApi(GenericApi):
    def _connect_to_lms(self):
        """
        Connects to the Canvas API
        :return: Canvas object (API connection)
        """
        return Canvas(self.api_url, self.api_token)

    def get_instructor(self):
        """
        Get Canvas user associated with this api key ('self' is a magic keyword to get the current user)
        :return: Instructor object
        """
        instructor_obj = self.lms.get_user(user='self')
        email = instructor_obj.get_profile()['primary_email']
        instructor = dict(name=instructor_obj.name, email=email, lms_id=instructor_obj.id)
        return instructor

    def get_courses_by_instructor(self, instructor, semester):
        """
        Get all courses from Canvas for an instructor
        :param instructor: Instructor object
        :param semester: string like 'Spring 2020'
        :return: List of dictionaries containing course LMS id and name
        """
        instructor_obj = self.lms.get_user(user=instructor.lms_id)
        all_courses = instructor_obj.get_courses(enrollment_type='teacher', include=['term', 'total_students'])
        current_courses = [c for c in all_courses if c.term['name'] == semester]
        # Filter out courses with no students
        current_courses = [c for c in current_courses if c.total_students > 0]
        courses = [dict(id=c.id, name=c.name) for c in current_courses]
        return courses

    def get_students_in_course(self, course):
        """
        Get all students in a course
        :param course: Course object
        :return: List of dictionaries of the form {'name': student_name, 'lms_id': student_lms_id}
        """
        course_obj = self.lms.get_course(course.course_id)
        enrollments_obj = course_obj.get_enrollments(type=['StudentEnrollment'])
        students = [dict(name=e.user['name'], lms_id=e.user['id']) for e in enrollments_obj]
        return students

    def get_course_assignments(self, course):
        """
        Get all assignments for all students in the given course
        :param course: Course object
        :return: List of dictionaries of the form {student_lms_id: list of student assignments}. Student assignments
        are dictionaries of the form {'name': assignment_name, 'due_date': due_date, 'score': score}.
        """
        course_obj = self.lms.get_course(course.course_id)
        all_assignments = course_obj.get_assignments(bucket='past', order_by='due_at')
        graded_assignments = [a for a in all_assignments if getattr(a, 'points_possible') and a.points_possible > 0]
        return [dict(lms_id=a.id, name=a.name, due_date=a.due_at) for a in graded_assignments]

    def get_course_grades(self, course, students, assignments=None):
        """
        Get all grades for all students in the given course
        :param course: Course object
        :param students: List of Student objects
        :param assignments: (Optional) List of Assignment objects for which to get the grades
        :return: List of dictionaries of the form {student: list of student assignments}. Student assignments
        are dictionaries of the form {'name': assignment_name, 'due_date': due_date, 'score': score}.
        """
        course_obj = self.lms.get_course(course.course_id)
        if assignments is not None:
            assignment_objs = course_obj.get_assignments(assignment_ids=[a.lms_id for a in assignments])
        else:
            all_assignments = course_obj.get_assignments(bucket='past', order_by='due_at')
            assignment_objs = [a for a in all_assignments if getattr(a, 'points_possible') and a.points_possible > 0]
        students_by_id = {s.lms_id: s for s in students}

        # Store all the Assignments for a single student, keys = student LMS id
        student_assignments = defaultdict(list)

        for a in assignment_objs:
            # Submissions have the actual grades
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
                    dict(lms_id=a.id, name=a.name, due_date=a.due_at, score=s.score/a.points_possible))

        return {s: student_assignments[s.lms_id] for s in students}

    def get_current_scores(self, course):
        course_obj = self.lms.get_course(course.course_id)
        enrollments_obj = course_obj.get_enrollments(type=['StudentEnrollment'])
        current_scores = {e.user['id']: e.grades['current_score'] for e in enrollments_obj if
                          e.grades['current_score'] is not None and e.grades.get('current_score') > 0}
        return current_scores

    def get_student_grades(self, student, course):
        """
        Get all grades for a single student in the given course. If you need all grades for all students in a course,
        use get_course_grades instead to reduce the number of API calls.
        :param student: Student object
        :param course: Course object
        :return: List of assignments. Assignments are dictionaries of the form
        {'name': assignment_name, 'due_date': due_date, 'score': score}
        """
        all_assignments = self.lms.get_assignments(bucket='past', order_by='due_at')
        graded_assignments = [a for a in all_assignments if a.points_possible > 0]
        student_assignments = []

        for a in graded_assignments:
            for s in a.get_submission(student.lms_id):
                student_assignments.append(dict(name=a.name, due_date=a.due_at, score=s.score/a.points_possible))

        return student_assignments

    def get_course_grade_summary(self, course, summary_stat):
        """
        Create a summary of the course using the specified summary_stat
        :param course: Course object
        :param summary_stat: String. One of either 'mean' or 'median'
        :return: Float
        """
        summary_stat = summary_stat.lower()
        assert summary_stat == 'mean' or summary_stat == 'median', 'summary_stat must be either "mean" or "median"'
        course_obj = self.lms.get_course(course.course_id)
        enrollments_obj = course_obj.get_enrollments(type=['StudentEnrollment'])
        current_scores = [e.grades['current_score'] for e in enrollments_obj if
                          e.grades['current_score'] is not None and e.grades.get('current_score') > 0]

        if not current_scores:
            return None
        if summary_stat == 'mean':
            summary_stat = np.mean(current_scores)
        elif summary_stat == 'median':
            summary_stat = np.median(current_scores)

        return summary_stat
