import allure

from framework.helpers.checker import Checker as check


@allure.feature("GET")
@allure.story("CHARACTERS")
class TestGetCharacters:

    @allure.title("Check response structure")
    @allure.description("Test for 'GET /characters' method. Check response structure, data types and response time")
    def test_response_structure(self, api):
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
