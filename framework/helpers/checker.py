import allure
from cerberus import Validator
from hamcrest import assert_that, equal_to, less_than_or_equal_to


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