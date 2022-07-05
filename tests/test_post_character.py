import allure
import pytest

from framework.helpers.checker import Checker as check
from framework.helpers.utils import transform_to_float, update_dictionary_single_val, change_field_name, pop_field


@allure.feature("POST")
@allure.story("CHARACTER")
class TestPostCharacter:

    @allure.description("Test for 'POST /character' method with correct data. "
                        "Check response structure, data types and response time."
                        "Expected status code 200. New character must be added to collection")
    @pytest.mark.parametrize("name, universe, education, weight, height, identity, other_aliases", [
        ("TestName", "Test Universe", "TestEducation", 1, 2.2, "Test Identity", "TestAlias1"),
        ("Test Name", "TestUniverse", "Test Education", 3.3, 4, "TestIdentity", "Test Alias1"),
        ("TestName", "TestUniverse", "TestEducation", 0, -5, "TestIdentity", "TestAlias1, TestAlias2"),
        ("TestName", "TestUniverse", "TestEducation", -5, 0, "TestIdentity", "Test Alias1, Test Alias2"),
        ("ТестИмя", "Тест Вселенная", "ТестОбразование", "11", "-22.22", "ТестИзвестность",
         "ТестПрозвище1, ТестПрозвище2"),
        ("Тест Имя", "ТестВселенная", "Тест Образование", "-11.11", "22", "ТестИзвестность",
         "Тест Прозвище1, Тест Прозвище2")
    ])
    def test_correct_data(self, api, fake, name, universe, education, weight, height, identity, other_aliases):
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
                          "identity": identity,
                          "other_aliases": other_aliases}
        allure.dynamic.title(f"Add character: {character_data}")
        response = api.post_character(character_data)
        check.base_complex_check(response, 200, schema=schema)
        character_data.update({"weight": transform_to_float(character_data["weight"]),
                               "height": transform_to_float(character_data["height"])})
        check.matching_data(api.get_character_by_name(character_data.get('name')).content.get('result'), character_data)

    @allure.description("Test for 'POST /character' method with empty input field in json. "
                        "Check response structure, data types and response time."
                        "Expected status code 400. Error message will not be checked. "
                        "New character will not be added to collection")
    @pytest.mark.parametrize("empty_field_names", [
        ("name",),
        ("other_aliases",),
        ("name", "universe", "education"),
        ("weight", "height", "identity")])
    def test_empty_field(self, api, fake, empty_field_names):
        allure.dynamic.title(f"Check add character with empty fields: {empty_field_names}")
        character_data = {"name": "TestName" + str(fake.random_number()),
                          "universe": "TestUniverse",
                          "education": "TestEducation",
                          "weight": 1,
                          "height": 2,
                          "identity": "TestIdentity",
                          "other_aliases": "TestAliases"}
        update_dictionary_single_val(character_data, empty_field_names, "")
        response = api.post_character(character_data)
        check.base_complex_check(response, 400, schema={"error": {"type": "string"}})
        for field_name in empty_field_names:
            check.data_contain_str(response.content["error"], field_name)

    @allure.description("Test for 'POST /character' method with null input field in json. "
                        "Check response structure, data types and response time."
                        "Expected status code 400.  Error message will not be checked. "
                        "New character will not be added to collection")
    @pytest.mark.parametrize("null_field_names", [
        ("name",),
        ("other_aliases", ),
        ("name", "universe", "education"),
        ("weight", "height", "identity")])
    def test_null_field(self, api, fake, null_field_names):
        allure.dynamic.title(f"Check add character with null field: {null_field_names}")
        character_data = {"name": "TestName" + str(fake.random_number()),
                          "universe": "TestUniverse",
                          "education": "TestEducation",
                          "weight": 1,
                          "height": 2,
                          "identity": "TestIdentity",
                          "other_aliases": "TestAliases"}
        update_dictionary_single_val(character_data, null_field_names, None)
        response = api.post_character(character_data)
        check.base_complex_check(response, 400, schema={"error": {"type": "string"}})
        for field_name in null_field_names:
            check.data_contain_str(response.content["error"], field_name)

    @allure.description("Test for 'POST /character' method with bad input json (string fields)"
                        "Check response structure, data types and response time."
                        "Expected status code 400.  Error message will not be checked. "
                        "New character will not be added to collection")
    @pytest.mark.parametrize("bad_field_names", [
        ("name",),
        ("other_aliases", ),
        ("name", "universe"),
        ("education", "identity")
    ])
    @pytest.mark.parametrize("bad_value", [
        'A' * (2 ** 10),
        123,
        -10,
        "!?;:/|@#$%^&*_-+=~<>±§"  # сомнительный кейс
    ])
    def test_bad_field_str(self, api, fake, bad_field_names, bad_value):
        allure.dynamic.title(f"Check add character with bad string fields {bad_field_names}, value: {bad_value}")
        character_data = {"name": "TestName" + str(fake.random_number()),
                          "universe": "TestUniverse",
                          "education": "TestEducation",
                          "weight": 1,
                          "height": 2,
                          "identity": "TestIdentity",
                          "other_aliases": "TestAliases"}
        update_dictionary_single_val(character_data, bad_field_names, bad_value)
        if ("name" in bad_field_names) and (bad_value == "!?;:/|@#$%^&*_-+=~<>±§"):
            update_dictionary_single_val(character_data, ["name", ], f"{character_data['name']}{fake.random_number()}")
        response = api.post_character(character_data)
        check.base_complex_check(response, 400, schema={"error": {"type": "string"}})
        for field_name in bad_field_names:
            check.data_contain_str(response.content["error"], field_name)

    @allure.description("Test for 'POST /character' method with bad input json (numeric fields)"
                        "Check response structure, data types and response time."
                        "Expected status code 400.  Error message will not be checked. "
                        "New character will not be added to collection")
    @pytest.mark.parametrize("bad_field_names", [
        ("weight",),
        ("height",),
        ("weight", "height")
    ])
    @pytest.mark.parametrize("bad_value", [
        'A' * (2 ** 10),
        "!?;:/|@#$%^&*_-+=~<>±§",
        "1 2",
        "123.1a2b3"
    ])
    def test_bad_field_numeric(self, api, fake, bad_field_names, bad_value):
        allure.dynamic.title(f"Check add character with bad numeric fields {bad_field_names}, value: {bad_value}")
        character_data = {"name": "TestName" + str(fake.random_number()),
                          "universe": "TestUniverse",
                          "education": "TestEducation",
                          "weight": 1,
                          "height": 2,
                          "identity": "TestIdentity",
                          "other_aliases": "TestAliases"}
        update_dictionary_single_val(character_data, bad_field_names, bad_value)
        response = api.post_character(character_data)
        check.base_complex_check(response, 400, schema={"error": {"type": "string"}})
        for field_name in bad_field_names:
            check.data_contain_str(response.content["error"], field_name)

    @allure.description("Test for 'POST /character' method with 'wrong' field names. "
                        "Check response structure, data types and response time."
                        "Expected status code 400. New character will not be added to collection")
    @pytest.mark.parametrize("field_names", [
        ["name", ],
        ["other_aliases", ],
        ["name", "education", "height"],
        ["universe", "weight", "identity"],
    ])
    def test_wrong_fields_name(self, api, fake, field_names):
        character_data = {"name": "TestName" + str(fake.random_number()),
                          "universe": "TestUniverse",
                          "education": "TestEducation",
                          "weight": 1,
                          "height": 2,
                          "identity": "TestIdentity",
                          "other_aliases": "TestAliases"}
        allure.dynamic.title(f"Add character with wrong fields ({field_names}). Data: {character_data}")
        for field_name in field_names:
            change_field_name(character_data, field_name, f"wrong_{field_name}")
        response = api.post_character(character_data)
        check.base_complex_check(response, 400, schema={"error": {"type": "string"}})

    @allure.description("Test for 'POST /character' method without some fields. "
                        "Check response structure, data types and response time."
                        "Expected status code 400. New character will not be added to collection")
    @pytest.mark.parametrize("field_names", [
        ["name", ],
        ["other_aliases", ],
        ["name", "education", "height"],
        ["universe", "weight", "identity"],
    ])
    def test_pop_fields(self, api, fake, field_names):
        character_data = {"name": "TestName" + str(fake.random_number()),
                          "universe": "TestUniverse",
                          "education": "TestEducation",
                          "weight": 1,
                          "height": 2,
                          "identity": "TestIdentity",
                          "other_aliases": "TestAliases"}
        allure.dynamic.title(f"Add character without fields ({field_names}). Data: {character_data}")
        for field_name in field_names:
            pop_field(character_data, field_name)
        response = api.post_character(character_data)
        check.base_complex_check(response, 400, schema= {"error": {"type": "string"}})

    @allure.description("Test for 'POST /character' method for duplicate character"
                        "Check response structure, data types and response time."
                        "Expected status code 400.  Error message will not be checked. "
                        "Duplicated character will not be added to collection")
    def test_duplicate_character(self, api, fake):
        character_name = "TestName" + str(fake.random_number())
        character_data = {"name": character_name,
                          "universe": "TestUniverse",
                          "education": "TestEducation",
                          "weight": 1,
                          "height": 2,
                          "identity": "TestIdentity",
                          "other_aliases": "TestAliases"}
        allure.dynamic.title(f"Check adding duplicate character. Name '{character_name}'")
        first_response = api.post_character(character_data)
        check.base_complex_check(first_response, 200)
        second_response = api.post_character(character_data)
        check.base_complex_check(second_response, 400, schema={"error": {"type": "string"}})
        check.data_contain_str(second_response.content["error"], character_name)

    @allure.description("Test for 'POST /character' method for too many characters (more than DB limit)"
                        "Check response structure, data types and response time."
                        "Expected status code 400.  Error message will not be checked. "
                        "Duplicated character will not be added to collection")
    def test_characters_limit(self, api, fake):
        limit = 500
        allure.dynamic.title(f"Check adding characters more than DB limit ({limit})")
        for i in range(limit + 1):
            character_data = {"name": f"{i + 1}_TestName_{fake.random_number()}",
                              "universe": "TestUniverse",
                              "education": "TestEducation",
                              "weight": 1,
                              "height": 2,
                              "identity": "TestIdentity",
                              "other_aliases": "TestAliases"}
            response = api.post_character(character_data)
            try:
                check.base_complex_check(response, 200)
            except AssertionError:
                check.base_complex_check(response, 400, schema={"error": {"type": "string"}})
                check.data_contain_str(response.content["error"], str(limit))
                break
