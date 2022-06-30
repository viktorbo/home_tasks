import allure
import pytest

from framework.helpers.checker import Checker as check
from framework.helpers.utils import get_first_duplicate_name, transform_to_float


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


@allure.feature("GET")
@allure.story("CHARACTER BY NAME")
class TestGetCharacterByName:

    @allure.description("Test for 'GET /character?name=...' method. "
                        "Check response structure, data types and response time for request with "
                        "correct name")
    @pytest.mark.parametrize("character_name", ["Nomad", "Mary Jane Watson"])
    def test_correct_name(self, api, character_name):
        allure.dynamic.title(f"Request with correct name: '{character_name}'")
        response = api.get_character_by_name(character_name)
        check.status_code(response.status_code, 200)
        check.request_exec_time(response.time, 1.5)
        check.object_schema(
            {"result": {
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
            }}, response.content)

    @allure.description("Test for 'GET /character?name=...' method for duplicate records. "
                        "Check response structure and data types. "
                        "Expected only one record")
    def test_duplicate_name_single(self, api):
        collection = api.get_all_characters().content.get("result")
        duplicate_name, count = get_first_duplicate_name(collection)
        allure.dynamic.title(f"Request with duplicate name (expect one record): '{duplicate_name}' ({count} times)")
        response = api.get_character_by_name(duplicate_name)
        check.object_schema(
            {"result": {
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
            }}, response.content)

    @allure.description("Test for 'GET /character?name=...' method for duplicate records. "
                        "Check response structure and data types. "
                        "Expected many records")
    def test_duplicate_name_many(self, api):
        """
        Данный кейс падает ожидаемо, так как нет информации о том сколько должно возвращаться записей в таком случае.
        Таким образом мы контролируем информацию об возвращаемых данных. Намеренно не стал скипать тест,
        потому что это потенциальный баг
        """
        collection = api.get_all_characters().content.get("result")
        duplicate_name, count = get_first_duplicate_name(collection)
        allure.dynamic.title(f"Request with duplicate name (expect many records): '{duplicate_name}' ({count} times)")
        response = api.get_character_by_name(duplicate_name)
        check.obj_type(response.content['result'], dict, negative=True)

    @allure.description("Test for 'GET /character?name=...' method with bad names. "
                        "Check request time and status code. Also check error messages in some cases."
                        "Expected status code 400 or 414")
    @pytest.mark.parametrize("bad_name, reason, expected_status_code, check_msg", [
        ("alksfnlaknsvkla", "Non-existent name", 400, True),
        ('', "Empty name", 400, True),
        ("    ", "Some whitespaces", 400, True),
        ('A' * (2 ** 16), "Too long name", 414, False),
        ("!@#$%^&*_-+=<>/?~`", "Special symbols (Can be read but character will not found)", 400, True)
    ])
    def test_bad_name(self, api, bad_name, reason, expected_status_code, check_msg):
        allure.dynamic.title(f"Request with bad name '{bad_name}' ({reason}, status code {expected_status_code})")
        response = api.get_character_by_name(bad_name)
        check.status_code(response.status_code, expected_status_code)
        check.request_exec_time(response.time, 1.5)
        if check_msg:
            check.object_schema({"error": {"type": "string", "regex": "name"}}, response.content)


@allure.feature("POST")
@allure.story("CHARACTER")
class TestPostCharacter:

    @allure.description("Test for 'POST /character' method with correct data. "
                        "Check response structure, data types and response time."
                        "Expected status code 200. New character must be added to collection")
    @pytest.mark.parametrize("name, universe, education, weight, height, identity", [
        ("TestName", "Test Universe", "TestEducation", 1, 2.2, "Test Identity"),
        ("Test Name", "TestUniverse", "Test Education", 3.3, 4, "TestIdentity"),
        ("TestName", "TestUniverse", "TestEducation", 0, -5, "TestIdentity"),
        ("TestName", "TestUniverse", "TestEducation", -5, 0, "TestIdentity"),
        ("ТестИмя", "Тест Вселенная", "ТестОбразование", "11", "-22.22", "ТестИзвестность"),
        ("Тест Имя", "ТестВселенная", "Тест Образование", "-11.11", "22", "ТестИзвестность")
    ])
    def test_correct_data(self, api, fake, name, universe, education, weight, height, identity):
        schema = {
            "result": {
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
        character_data = {"name": name + str(fake.random_number()),
                          "universe": universe,
                          "education": education,
                          "weight": weight,
                          "height": height,
                          "identity": identity}
        allure.dynamic.title(f"Add character: {character_data}")
        response = api.post_character(character_data)
        check.status_code(response.status_code, 200)
        check.request_exec_time(response.time, 1.5)
        check.object_schema(schema, response.content)
        character_data.update({"weight": transform_to_float(character_data["weight"]),
                               "height": transform_to_float(character_data["height"])})
        check.matching_data(api.get_character_by_name(character_data.get('name')).content.get('result'), character_data)

    @allure.description("Test for 'POST /character' method with empty input field in json. "
                        "Check response structure, data types and response time."
                        "Expected status code 400. Error message will not be checked. "
                        "New character will not be added to collection")
    @pytest.mark.parametrize("empty_field_names", [
        ("name",),
        ("name", "universe", "education"),
        ("weight", "height", "identity")])
    def test_empty_field(self, api, fake, empty_field_names):
        allure.dynamic.title(f"Check add character with empty fields: {empty_field_names}")
        character_data = {"name": "TestName" + str(fake.random_number()),
                          "universe": "TestUniverse",
                          "education": "TestEducation",
                          "weight": 1,
                          "height": 2,
                          "identity": "TestIdentity"}
        for field_name in empty_field_names:
            character_data.update({field_name: ""})
        response = api.post_character(character_data)
        check.status_code(response.status_code, 400)
        check.request_exec_time(response.time, 1.5)
        check.object_schema({"error": {"type": "string"}}, response.content)
        for field_name in empty_field_names:
            check.data_contain_str(response.content["error"], field_name)

    @allure.description("Test for 'POST /character' method with null input field in json. "
                        "Check response structure, data types and response time."
                        "Expected status code 400.  Error message will not be checked. "
                        "New character will not be added to collection")
    @pytest.mark.parametrize("null_field_names", [
        ("name",),
        ("name", "universe", "education"),
        ("weight", "height", "identity")])
    def test_null_field(self, api, fake, null_field_names):
        allure.dynamic.title(f"Check add character with null field: {null_field_names}")
        character_data = {"name": "TestName" + str(fake.random_number()),
                          "universe": "TestUniverse",
                          "education": "TestEducation",
                          "weight": 1,
                          "height": 2,
                          "identity": "TestIdentity"}
        for field_name in null_field_names:
            character_data.update({field_name: None})
        response = api.post_character(character_data)
        check.status_code(response.status_code, 400)
        check.request_exec_time(response.time, 1.5)
        check.object_schema({"error": {"type": "string"}}, response.content)
        for field_name in null_field_names:
            check.data_contain_str(response.content["error"], field_name)

    @allure.description("Test for 'POST /character' method with bad input json (string type)"
                        "Check response structure, data types and response time."
                        "Expected status code 400.  Error message will not be checked. "
                        "New character will not be added to collection")
    @pytest.mark.parametrize("bad_field_names", [
        ("name",),
        ("name", "universe"),
        ("education", "identity")
    ])
    @pytest.mark.parametrize("bad_value", [
        'A' * (2 ** 10),
        123,
        -10,
        "!?;:/|\@#$%^&*_-+=~<>"  # сомнительный кейс
    ])
    def test_bad_field_str(self, api, fake, bad_field_names, bad_value):
        allure.dynamic.title(f"Check add character with bad string fields '{bad_field_names}', value: {bad_value}")
        character_data = {"name": "TestName" + str(fake.random_number()),
                          "universe": "TestUniverse",
                          "education": "TestEducation",
                          "weight": 1,
                          "height": 2,
                          "identity": "TestIdentity"}
        for field_name in bad_field_names:
            character_data.update({field_name: bad_value})
        response = api.post_character(character_data)
        check.status_code(response.status_code, 400)
        check.request_exec_time(response.time, 1.5)
        check.object_schema({"error": {"type": "string"}}, response.content)
        for field_name in bad_field_names:
            check.data_contain_str(response.content["error"], field_name)
