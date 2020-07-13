import requests
import json


class GenericLMS:
    def __init__(self, lms_url, lms_token, api_url):
        self.lms_url = lms_url
        self.lms_token = lms_token
        self.api_url = api_url

    def _form_endpoint(self, resource):
        resource = resource.strip('/')
        url = f'{self.api_url}/{resource}'
        return url

    def do_post(self, resource, params, data):
        raise NotImplementedError

    def test_api(self):
        url = self.form_endpoint('lms_api')
        resp = requests.get(url).json()
        return resp

    def get_instructor(self):
        raise NotImplementedError

    def get_courses_by_instructor(self, semester, instructor_id):
        raise NotImplementedError

    def get_students_in_course(self, course_id):
        raise NotImplementedError

    def get_course_assignments(self, course_id):
        raise NotImplementedError

    def get_course_grades(self, course_id, student_ids, assignment_ids=None):
        raise NotImplementedError

    def get_current_scores(self, course_id):
        raise NotImplementedError

    def get_student_grades(self, course_id, student_id):
        raise NotImplementedError

    def get_course_grade_summary(self, course_id, summary_stat):
        raise NotImplementedError


class Canvas(GenericLMS):
    def do_post(self, resource, params=None, data=None):
        # Send the appropriate lms url and token, along with requested params/data
        url = self._form_endpoint(resource)
        if not params:
            params = dict()
        if not data:
            data = dict()
        params.update({'lms': 'CANVAS'})
        data.update({'lms_url': self.lms_url, 'lms_token': self.lms_token})
        data = json.dumps(data)
        resp = requests.post(url, params=params, data=data)
        return resp

    def get_instructor(self):
        resp = self.do_post('get_instructor')
        return resp

    def get_courses_by_instructor(self, semester, instructor_id):
        assert isinstance(semester, str), 'semester must be a string'
        assert isinstance(instructor_id, int) or isinstance(instructor_id, str), \
            'instructor_id must be an integer or string'
        data = {'semester': semester, 'instructor_id': instructor_id}
        resp = self.do_post('get_courses_by_instructor', data=data)
        return resp

    def get_students_in_course(self, course_id):
        assert isinstance(course_id, int) or isinstance(course_id, str), 'course_id must be an integer or string'
        data = {'course_id': course_id}
        resp = self.do_post('get_students_in_course', data=data)
        return resp

    def get_course_assignments(self, course_id):
        assert isinstance(course_id, int) or isinstance(course_id, str), 'course_id must be an integer or string'
        data = {'course_id': course_id}
        resp = self.do_post('get_course_assignments', data=data)
        return resp

    def get_course_grades(self, course_id, student_ids, assignment_ids=None):
        assert isinstance(course_id, int) or isinstance(course_id, str), 'course_id must be an integer or string'
        assert isinstance(student_ids, list), 'student_ids must be a list'

        data = {'course_id': course_id, 'student_ids': student_ids}
        if assignment_ids is not None:
            assert isinstance(assignment_ids, list), 'assignment_ids must be a list'
            data.update({'assignment_ids': assignment_ids})
        resp = self.do_post('get_course_grades', data=data)
        return resp

    def get_current_scores(self, course_id):
        assert isinstance(course_id, int) or isinstance(course_id, str), 'course_id must be an integer or string'

        data = {'course_id': course_id}
        resp = self.do_post('get_current_scores', data=data)
        return resp

    def get_student_grades(self, course_id, student_id):
        assert isinstance(course_id, int) or isinstance(course_id, str), 'course_id must be an integer or string'
        assert isinstance(student_id, int) or isinstance(student_id, str), 'student_id must be an integer or string'

        data = {'course_id': course_id, 'student_id': student_id}
        resp = self.do_post('get_student_grades', data=data)
        return resp

    def get_course_grade_summary(self, course_id, summary_stat):
        assert isinstance(course_id, int) or isinstance(course_id, str), 'course_id must be an integer or string'
        assert isinstance(summary_stat, str) and summary_stat.lower() in ['mean', 'median'], \
            'summary_stat must be one of "mean" or "median"'

        data = {'course_id': course_id, 'summary_stat': summary_stat}
        resp = self.do_post('get_course_grade_summary', data=data)
        return resp
