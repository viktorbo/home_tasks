import allure
import pytest

from framework.helpers.checker import Checker as check


@allure.epic("FUNCTIONAL")
@allure.feature("GET")
@allure.story("CHARACTERS")
class TestGetCharacters:

    @allure.title("Check response structure")
    @allure.description("Test for 'GET /characters' method. Check response structure, data types and response time")
    def test_response_structure_get_all_characters(self, api):
        response = api.get_all_characters()
        # "хороший" статус код может быть не один, в таком случае надо доработать (в тестах ниже аналогично)
        check.status_code(response.status_code, 200)
        # время выбрано в среднем с учетом возможных задержек (в тестах ниже аналогично)
        check.request_exec_time(response.time, 1)
        check.object_schema(
            {"result": {
                "type": ["dict"],
                "schema": {
                    "education": {"type": "string"},
                    "height": {"type": "integer"},
                    "weight": {"type": "float"},
                    "identity": {"type": "string"},
                    "name": {"type": "string"},
                    "other_aliases": {"type": "string"},
                    "universe": {"type": "string"}
                }
            }}, response.content)


@allure.epic("FUNCTIONAL")
@allure.feature("GET")
@allure.story("CHARACTER BY NAME")
class TestGetCharacterByName:

    @allure.description("Test for 'GET /character?name=...' method. "
                        "Check response structure, data types and response time for request with "
                        "correct name")
    @pytest.mark.parametrize("character_name", ["Nomad", "Mary Jane Watson"])
    def test_correct_name_get_character_by_name(self, api, character_name):
        allure.dynamic.title(f"Request with correct name: '{character_name}'")
        response = api.get_character_by_name(character_name)
        check.status_code(response.status_code, 200)
        check.request_exec_time(response.time, 1.5)
        check.object_schema(
            {"result": {
                "type": "dict",
                "schema": {
                    "education": {"type": "string"},
                    "height": {"type": "integer"},
                    "weight": {"type": "float"},
                    "identity": {"type": "string"},
                    "name": {"type": "string"},
                    "other_aliases": {"type": "string"},
                    "universe": {"type": "string"}
                }
            }}, response.content)