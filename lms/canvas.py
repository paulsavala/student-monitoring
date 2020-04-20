from canvasapi import Canvas
from lms.generic import GenericApi


class CanvasApi(GenericApi):
    def get_courses(self, instructor=None, course=None):
        raise NotImplementedError

    def get_grades(self, course=None, student=None):
        raise NotImplementedError

    def get_assignments(self, course=None, student=None):
        raise NotImplementedError
