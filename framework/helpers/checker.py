import allure
from cerberus import Validator
from hamcrest import assert_that, equal_to, less_than_or_equal_to, is_not, is_, contains_string, is_in, not_


class Checker:
    """
    Класс для работы с проверками различных объектов и логирования эттго процесса
    """

    @staticmethod
    def headers(headers: dict, expected_headers: dict):
        with allure.step("Check headers"):
            with allure.step("Allowed headers"):
                for header in expected_headers.items():
                    assert_that(header, is_in(list(headers.items())), f"Wrong header: {header}")
            with allure.step("Check deprecated headers"):
                deprecated_headers_list = ["X-Powered-By", ]
                for deprecated_header in deprecated_headers_list:
                    assert_that(deprecated_header, not_(is_in(list(headers.keys()))),
                                f"Headers contain deprecated header '{deprecated_header}'")

    @staticmethod
    def status_code(current_status_code, expected_status_code):
        with allure.step(f"Check status code (expect [{expected_status_code}])"):
            assert_that(current_status_code, equal_to(expected_status_code), "Wrong status code!")

    @staticmethod
    def object_schema(checking_object, schema):
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

    @staticmethod
    def data_contain_str(data, substring):
        with allure.step(f"Check that data '{data}' contain '{substring}'"):
            assert_that(data, contains_string(substring), "Data don't contain substring")

    @staticmethod
    def base_complex_check(response, status_code, exec_time=1.5, schema=None):
        with allure.step(f"Base check response: status code = {status_code}, execution time = {exec_time}, "
                         f"schema = {schema}"):
            Checker.status_code(response.status_code, status_code)
            Checker.request_exec_time(response.time, exec_time)
            if schema:
                Checker.object_schema(response.content, schema)
            Checker.headers(response.headers, {"Connection": "keep-alive"})
