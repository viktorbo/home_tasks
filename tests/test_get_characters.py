import allure

from framework.helpers.checker import Checker as check


@allure.feature("GET")
@allure.story("CHARACTERS")
class TestGetCharacters:

    @allure.title("Check correct response without params")
    @allure.description("Test for 'GET /characters' method. Expected status code 200. "
                        "Check response structure, data types and response time")
    def test_response_without_params(self, api):
        response = api.get_all_characters()
        expected_schema = {
            "result": {
                "type": "list",
                "schema": {
                    "type": "dict",
                    "schema": {
                        "education": {"type": "string"},
                        "height": {"type": "number"},
                        "weight": {"type": "number"},
                        "identity": {"type": "string"},
                        "name": {"type": "string"},
                        "other_aliases": {"type": "string"},
                        "universe": {"type": "string"}
                    }
                }
            }
        }
        check.base_complex_check(response, 200, schema=expected_schema)

    @allure.title("Check correct response with params")
    @allure.description("Test for 'GET /characters' method. Expected status code 200. "
                        "Check response structure, data types and response time. "
                        "Response should not be affected by request with params ")
    def test_response_with_params(self, api):
        expected_schema = {
            "result": {
                "type": "list",
                "schema": {
                    "type": "dict",
                    "schema": {
                        "education": {"type": "string"},
                        "height": {"type": "number"},
                        "weight": {"type": "number"},
                        "identity": {"type": "string"},
                        "name": {"type": "string"},
                        "other_aliases": {"type": "string"},
                        "universe": {"type": "string"}
                    }
                }
            }
        }
        response = api.get_all_characters()
        check.base_complex_check(response, 200)
        response_with_params = api.get_all_characters(params={"name": "Dracula"})
        check.base_complex_check(response_with_params, 200, schema=expected_schema)
        check.matching_data(response_with_params.content, response.content)
        check.matching_data(response_with_params.headers, response.headers)
