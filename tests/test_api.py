import allure

from framework.helpers.checker import Checker as check


@allure.epic("GET")
class TestGetCharacters:

    @allure.feature("CHARACTERS")
    @allure.title("Check response structure")
    @allure.description("Test for 'GET /characters' method. Check response structure, data types and response time")
    def test_response_structure_get_all_characters(self, api):
        response = api.get_all_characters()
        # "хороший" статус код может быть не один, в таком случае надо доработать
        check.status_code(response.status_code, 200)
        # время выбрано в среднем с учетом возможных задержек
        check.request_exec_time(response.time, 1)
        check.object_schema(
            {"result": {
                "type": ["dict"],
                "schema": {
                    "education": {"type": ["string"]},
                    "height": {"type": ["integer"]},
                    "weight": {"type": ["float"]},
                    "identity": {"type": ["string"]},
                    "name": {"type": ["string"]},
                    "other_aliases": {"type": ["string"]},
                    "universe": {"type": ["string"]}
                }
            }}, response.content)


@allure.epic("GET")
class TestGetCharacterByName:

    @allure.feature("CHARACTER BY NAME")
    @allure.title("Check response structure")
    @allure.description("Test for 'GET /character?name=...' method. "
                        "Check response structure, data types and response time")
    def test_response_structure_get_character_by_name(self, api):
        response = api.get_character_by_name('')
        # "хороший" статус код может быть не один, в таком случае надо доработать
        check.status_code(response.status_code, 200)
        # время выбрано в среднем с учетом возможных задержек
        check.request_exec_time(response.time, 1.5)
        check.object_schema(
            {"result": {
                "type": ["dict"],
                "schema": {
                    "education": {"type": ["string"]},
                    "height": {"type": ["integer"]},
                    "weight": {"type": ["float"]},
                    "identity": {"type": ["string"]},
                    "name": {"type": ["string"]},
                    "other_aliases": {"type": ["string"]},
                    "universe": {"type": ["string"]}
                }
            }}, response.content)