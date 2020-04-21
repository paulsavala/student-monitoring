from canvasapi import Canvas
from lms.generic import GenericApi
from models.course import Course

import pandas as pd


class CanvasApi(GenericApi):
    def _connect_to_lms(self):
        return Canvas(self.api_url, self.api_token)

    def get_courses(self, instructor):
        # Get Canvas id associated to the instructor
        canvas_course = self.lms.get_course()
        course = Course(canvas_course.id, canvas_course.name, canvas_course)
        return course

    def get_course_grades(self, course):
        assignments = course.lms_obj.get_assignments()

    def get_student_grades(self, student):
        assignments = student.lms_obj.get_assignments()
