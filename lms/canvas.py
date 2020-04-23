from canvasapi import Canvas
from lms.generic import GenericApi
from models.course import Course
from models.instructor import Instructor
from models.assignment import Assignment, AssignmentCollection
from models.student import Student

from collections import defaultdict


class CanvasApi(GenericApi):
    def _connect_to_lms(self):
        return Canvas(self.api_url, self.api_token)

    def get_instructor(self):
        # Get Canvas user associated with this api key ('self' is a magic keyword to get the current user)
        instructor_obj = self.lms.get_user(user='self')
        email = instructor_obj.get_profile()['primary_email']
        instructor = Instructor(name=instructor_obj.name, email=email, lms_id=instructor_obj.id)
        return instructor

    def get_courses(self, instructor):
        instructor_obj = self.lms.get_user(user=instructor.lms_id)
        all_courses = instructor_obj.get_course(enrollment_type='teacher',
                                                include=['term'])
        # todo: Is there a better way to get the current term than hard-coding it?
        # todo: Trying to pull this from the Config gives a circular import
        current_courses = [c for c in all_courses if c.term['name'] == 'Spring 2020']
        courses = [Course(c.id, c.name) for c in current_courses]
        return courses

    def get_students_in_course(self, course):
        course_obj = self.lms.get_course(course.course_id)
        enrollments_obj = course_obj.get_enrollments(type=['StudentEnrollment'])
        students = [Student(name=e.user['name'], lms_id=e.user['id']) for e in enrollments_obj]
        return students

    def get_course_grades(self, course):
        all_assignments = self.lms.get_assignments(bucket='past', order_by='due_at')
        graded_assignments = [a for a in all_assignments if a.points_possible > 0]
        students = self.get_students_in_course(course)
        students_by_id = {s.lms_id: s for s in students}

        # Store all the Assignments for a single student
        student_assignments = defaultdict(list)

        for assignment in graded_assignments:
            submissions = assignment.get_submissions()
            for submission in submissions:
                student_assignments[submission.user_id].append(
                    Assignment(students_by_id[submission.user_id],
                               assignment.name,
                               assignment.due_at,
                               submission.score / assignment.points_possible
                               )
                )

        return [AssignmentCollection(s, course, student_assignments[s.lms_id]) for s in students]

    def get_student_grades(self, student, course):
        all_assignments = student.lms_obj.get_assignments(bucket='past', order_by='due_at')
        graded_assignments = [a for a in all_assignments if a.points_possible > 0]
        student_assignments = []

        for assignment in graded_assignments:
            for submission in assignment.get_submission(student.lms_id):
                student_assignments.append(Assignment(student.lms_id,
                                                      assignment.name,
                                                      assignment.due_at,
                                                      submission.score / assignment.points_possible)
                                           )

        return [AssignmentCollection(student, course, student_assignments)]
