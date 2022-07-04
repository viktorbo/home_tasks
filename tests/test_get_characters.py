import allure

from framework.helpers.checker import Checker as check


@allure.feature("GET")
@allure.story("CHARACTERS")
class TestGetCharacters:

    @allure.title("Check response structure")
    @allure.description("Test for 'GET /characters' method. Check response structure, data types and response time")
    def test_response_structure(self, api):
        response = api.get_all_characters()
        # "хороший" статус код может быть не один, в таком случае надо доработать (в тестах ниже аналогично)
        check.status_code(response.status_code, 200)
        # время выбрано в среднем с учетом возможных задержек (в тестах ниже аналогично)
        check.request_exec_time(response.time, 1.5)
        check.object_schema(
            {"result": {
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
            }}, response.content)
