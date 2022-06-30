from copy import deepcopy

import allure
from cerberus import Validator
from hamcrest import assert_that, equal_to, less_than_or_equal_to, is_not, is_


class Checker:
    """
    Класс для работы с проверками различных объектов и логирования эттго процесса
    """

    @staticmethod
    def status_code(current_status_code, expected_status_code):
        with allure.step(f"Check status code (expect [{expected_status_code}])"):
            assert_that(current_status_code, equal_to(expected_status_code), "Wrong status code!")

    @staticmethod
    def object_schema(schema, checking_object):
        with allure.step(f"Validate object schema: {schema}"):
            validator = Validator()
            validator.validate(checking_object, schema)

    @staticmethod
    def request_exec_time(curr_time, expected_time):
        with allure.step(f"Check request execution time ({curr_time} <= {expected_time})"):
            assert_that(curr_time, less_than_or_equal_to(expected_time), "Too long request execution")

    @staticmethod
    def obj_type(obj, expected_type: type, negative: bool = False):
        with allure.step(f"Check object type (expect {expected_type})"):
            assert_that(obj, is_not(expected_type), f"Wrong type ({type(obj)} but expect not {expected_type})") \
                if negative else \
                assert_that(obj, is_(expected_type), f"Wrong type ({type(obj)} but expect {expected_type})")

    @staticmethod
    def matching_data(curr_data, expected_data):
        with allure.step(f"Check that data matched"):
            assert_that(curr_data, equal_to(expected_data), "Data aren't equal")
