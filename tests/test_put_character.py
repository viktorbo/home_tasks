import allure
import pytest

from framework.helpers.checker import Checker as check
from framework.helpers.utils import transform_to_float, pop_field, update_dictionary_single_val, \
    get_first_duplicate_name, get_duplicated_records


@allure.feature("PUT")
@allure.story("CHARACTER")
class TestPutCharacter:
    """
    В некоторых кейсах специально берется уже сущетсвующая запись. При из мнении данных в БД тест упадет,
    зато при тестировании исключено влияние других методов API
    """

    @allure.description("Test for 'PUT /character' method with correct data. "
                        "Check response structure, data types and response time."
                        "Expected status code 200. Character must be updated")
    @pytest.mark.parametrize("name, universe, education, weight, height, identity, other_aliases", [
        ("Dracula", "Test Universe", "TestEducation", 1, 2.2, "Test Identity", "TestAlias"),
        ("Dracula", "TestUniverse", "Test Education", 3.3, 4, "TestIdentity", "TestAlias1, TestAlias2"),
        ("Dracula", "TestUniverse", "TestEducation", 0, -5, "TestIdentity", "Test Alias"),
        ("Dracula", "TestUniverse", "TestEducation", -5, 0, "TestIdentity", "TestAlias"),
        ("Dracula", "Тест Вселенная", "ТестОбразование", "11", "-22.22", "Тест Известность", "Тест Прозвище"),
        ("Dracula", "ТестВселенная", "Тест Образование", "-11.11", "22", "ТестИзвестность",
         "Тест Прозвище1, Тест Прозвище2")
    ])
    def test_correct_data_full(self, api, name, universe, education, weight, height, identity, other_aliases):
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
        character_data = {"name": name,
                          "universe": universe,
                          "education": education,
                          "weight": weight,
                          "height": height,
                          "identity": identity,
                          "other_aliases": other_aliases}
        allure.dynamic.title(f"Update character: {character_data}")
        response = api.put_character(character_data)
        check.base_complex_check(response, 200, schema=schema)
        character_data.update({"weight": transform_to_float(character_data["weight"]),
                               "height": transform_to_float(character_data["height"])})
        curr_data = api.get_character_by_name(name).content.get("result")
        check.matching_data(curr_data, character_data)

    @allure.description("Test for 'PUT /character' method with correct data (partially). "
                        "Check response structure, data types and response time."
                        "Expected status code 200. Character must be updated")
    @pytest.mark.parametrize("field_names", [
        ["education", ],
        ["height", ],
        ["weight", ],
        ["identity", ],
        ["other_aliases", ],
        ["universe", ],
        ["education", "weight", "other_aliases"],
        ["height", "identity", "universe"]
    ])
    def test_correct_data_partially(self, api, field_names):
        allure.dynamic.title(f"Update character with fields: {field_names}")
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
        name = "Dracula"
        character_data = {"universe": "TestUniverse",
                          "education": "TestEducation",
                          "weight": 1,
                          "height": 2,
                          "identity": "TestIdentity",
                          "other_aliases": "TestAliases"
                          }
        for field in field_names:
            pop_field(character_data, field)
        expected_data = api.get_character_by_name(name).content.get("result")
        expected_data.update(character_data)
        response = api.put_character({"name": name, **character_data})
        check.base_complex_check(response, 200, schema=schema)
        check.matching_data(api.get_character_by_name(name).content.get("result"), expected_data)

    @allure.title("Update character with empty data (without 'name')")
    @allure.description("Check PUT CHARACTER with empty data (empty json)."
                        "Expected status code 400 and error message. "
                        "Message must contain information about field 'name'")
    def test_empty_data_without_name(self, api):
        character_data = {}
        response = api.put_character(character_data)
        check.base_complex_check(response, 400, schema={"error": {"type": "string"}})
        check.data_contain_str(response.content["error"], "name")

    @allure.title("Update character with empty data (with 'name')")
    @allure.description("Check PUT CHARACTER with empty data (json contain only 'name' field)."
                        "Expected status code 400 and error message.")
    def test_empty_data_with_name(self, api):
        character_data = {"name": "Dracula"}
        response = api.put_character(character_data)
        check.base_complex_check(response, 400, schema={"error": {"type": "string"}})

    @allure.description("Check PUT CHARACTER with nonexistent name. "
                        "Expected status code 400 and error message")
    def test_nonexistent_name(self, api):
        name = "asfadvavgawfa"
        allure.dynamic.title(f"Update character with nonexistent name '{name}'")
        character_data = {"universe": "TestUniverse",
                          "education": "TestEducation",
                          "weight": 1,
                          "height": 2,
                          "identity": "TestIdentity",
                          "other_aliases": "TestAliases"
                          }
        response = api.put_character({"name": name, **character_data})
        check.base_complex_check(response, 400, schema={"error": {"type": "string"}})

    @allure.description("Check PUT CHARACTER method with some null fields. "
                        "Expect status code 400 and error message")
    @pytest.mark.parametrize("null_field_names", [
        ["education", ],
        ["height", ],
        ["weight", ],
        ["identity", ],
        ["other_aliases", ],
        ["universe", ],
        ["education", "weight", "other_aliases"],
        ["height", "identity", "universe"],
        "all"
    ])
    def test_null_fields(self, api, fake, null_field_names):
        name = "Dracula"
        allure.dynamic.title(f"Update character '{name}' with null fields {null_field_names}")
        character_data = {"universe": "TestUniverse",
                          "education": "TestEducation",
                          "weight": 1,
                          "height": 2,
                          "identity": "TestIdentity",
                          "other_aliases": "TestAliases"
                          }
        fields_list = character_data.keys() if null_field_names == "all" else null_field_names
        update_dictionary_single_val(character_data, fields_list, None)
        response = api.put_character({"name": name, **character_data})
        check.base_complex_check(response, 400, schema={"error": {"type": "string"}})

    @allure.description("Check PUT CHARACTER method with some empty fields. "
                        "Expect status code 400 and error message")
    @pytest.mark.parametrize("empty_field_names", [
        ["education", ],
        ["height", ],
        ["weight", ],
        ["identity", ],
        ["other_aliases", ],
        ["universe", ],
        ["education", "weight", "other_aliases"],
        ["height", "identity", "universe"],
        "all"
    ])
    def test_empty_fields(self, api, fake, empty_field_names):
        name = "Dracula"
        allure.dynamic.title(f"Update character '{name}' with empty fields {empty_field_names}")
        character_data = {"universe": "TestUniverse",
                          "education": "TestEducation",
                          "weight": 1,
                          "height": 2,
                          "identity": "TestIdentity",
                          "other_aliases": "TestAliases"
                          }
        fields_list = character_data.keys() if empty_field_names == "all" else empty_field_names
        update_dictionary_single_val(character_data, fields_list, "")
        response = api.put_character({"name": name, **character_data})
        check.base_complex_check(response, 400, schema={"error": {"type": "string"}})

    @allure.description("Check PUT CHARACTER when the number of characters has reached the limit. "
                        "Expected status code 200 and updated character")
    def test_update_character_with_limit(self, api, fake):
        limit = 500
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
        for i in range(limit + 1):
            character_data = {"name": f"PUT_{i + 1}_TestName_{fake.random_number()}",
                              "universe": "TestUniverse",
                              "education": "TestEducation",
                              "weight": 1,
                              "height": 2,
                              "identity": "TestIdentity",
                              "other_aliases": "TestAliases"}
            response = api.post_character(character_data)
            try:
                check.status_code(response.status_code, 200)
            except AssertionError:
                check.base_complex_check(response, 400, schema={"error": {"type": "string"}})
                check.data_contain_str(response.content["error"], str(limit))
                break
        upd_name = "Dracula"
        upd_data = {"name": upd_name, "other_aliases": "UPD by PUT test"}
        allure.dynamic.title(f"Update character '{upd_name}' (PUT) with DB limit ({limit})")
        data_before = api.get_character_by_name(upd_name).content.get("result")
        data_before.update(upd_data)
        response = api.put_character(upd_data)
        check.base_complex_check(response, 200, schema=schema)
        curr_data = api.get_character_by_name(upd_name).content.get("result")
        check.matching_data(curr_data, data_before)

    @allure.description("Check PUT CHARACTER with double update the same fields. "
                        "Expect status code 200 and correct response")
    def test_double_update(self, api, fake):
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
        upd_name = "Dracula"
        allure.dynamic.title(f"Double update character '{upd_name}'")
        character_data = {"name": upd_name, "universe": "UPD by PUT test"}
        response = api.put_character(character_data)
        check.base_complex_check(response, 200, schema=schema)
        response = api.put_character(character_data)
        check.base_complex_check(response, 200, schema=schema)

    @allure.description("Test for PUT CHARACTER method for duplicate characters"
                        "Check response structure, data types and response time."
                        "Expected status code 200. All records must be updated")
    def test_update_duplicate_character(self, api, fake):
        collection = api.get_all_characters().content.get("result")
        duplicate_name, count = get_first_duplicate_name(collection)
        allure.dynamic.title(f"Update duplicate character with name '{duplicate_name}' ({count} times)")

        upd_education = "UPD by PUT test (duplicate)"
        response = api.put_character({"name": duplicate_name, "education": upd_education})
        check.base_complex_check(response, 200)

        collection = api.get_all_characters().content.get("result")
        duplicated_records = get_duplicated_records(collection, duplicate_name)
        for record in duplicated_records:
            check.matching_data(curr_data={"name": record["name"], "education": record["education"]},
                                expected_data={"name": duplicate_name, "education": upd_education})

    @allure.description("Test for PUT CHARACTER method with bad input json (string fields)"
                        "Check response structure, data types and response time."
                        "Expected status code 400")
    @pytest.mark.parametrize("bad_field_names", [
        ("other_aliases",),
        ("universe",),
        ("education",),
        ("identity",),
        ("universe", "other_aliases", "education", "identity")
    ])
    @pytest.mark.parametrize("bad_value", [
        'A' * (2 ** 10),
        123,
        -10,
        "!?;:/|@#$%^&*_-+=~<>±§"
    ])
    def test_bad_field_str(self, api, fake, bad_field_names, bad_value):
        upd_name = "Dracula"
        allure.dynamic.title(f"Check update character '{upd_name}' "
                             f"with bad string fields {bad_field_names}, value: {bad_value}")
        character_data = {"name": upd_name,
                          "universe": "TestUniverse",
                          "education": "TestEducation",
                          "weight": 1,
                          "height": 2,
                          "identity": "TestIdentity",
                          "other_aliases": "TestAliases"}
        update_dictionary_single_val(character_data, bad_field_names, bad_value)
        response = api.put_character(character_data)
        check.base_complex_check(response, 400, schema={"error": {"type": "string"}})
        for field_name in bad_field_names:
            check.data_contain_str(response.content["error"], field_name)

    @allure.description("Test for PUT CHARACTER method with bad input json (numeric fields)"
                        "Check response structure, data types and response time."
                        "Expected status code 400")
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
        upd_name = "Dracula"
        allure.dynamic.title(f"Check add character '{upd_name}' "
                             f"with bad numeric fields {bad_field_names}, value: {bad_value}")
        character_data = {"name": upd_name,
                          "universe": "TestUniverse",
                          "education": "TestEducation",
                          "weight": 1,
                          "height": 2,
                          "identity": "TestIdentity",
                          "other_aliases": "TestAliases"}
        update_dictionary_single_val(character_data, bad_field_names, bad_value)
        response = api.put_character(character_data)
        check.base_complex_check(response, 400, schema={"error": {"type": "string"}})
        for field_name in bad_field_names:
            check.data_contain_str(response.content["error"], field_name)
