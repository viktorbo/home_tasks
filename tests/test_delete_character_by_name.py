import allure
import pytest

from framework.helpers.checker import Checker as check
from framework.helpers.utils import get_first_duplicate_name


@allure.feature("DELETE")
@allure.story("CHARACTER BY NAME")
class TestDeleteCharacterByName:

    @allure.description("Test for DELETE /character?name=...' method. "
                        "Check response structure, data types and response time for request with "
                        "correct name")
    @pytest.mark.parametrize("character_name", ["Nomad", "Mary Jane Watson"])
    def test_correct_name(self, api, character_name):
        allure.dynamic.title(f"Delete request with correct name: '{character_name}'")
        response = api.delete_character_by_name(character_name)
        check.base_complex_check(response, 200, schema={"result": {"type": "string"}})
        check.data_contain_str(response.content["result"], character_name)

        find_response = api.get_character_by_name(character_name)
        check.base_complex_check(find_response, 400, schema={"error": {"type": "string"}})

    @allure.description("Test for DELETE /character?name=... method for duplicate records. "
                        "Check response structure and data types. "
                        "Expected delete all duplicated records")
    def test_duplicate_name(self, api):
        collection = api.get_all_characters().content.get("result")
        duplicate_name, count = get_first_duplicate_name(collection)
        allure.dynamic.title(f"Delete request with duplicate name (one record): '{duplicate_name}' ({count} times)")
        response = api.delete_character_by_name(duplicate_name)
        check.base_complex_check(response, 200, schema={"result": {"type": "string"}})
        check.data_contain_str(response.content["result"], duplicate_name)
        duplicate_name_response = api.get_character_by_name(duplicate_name)
        check.base_complex_check(duplicate_name_response, 400, schema={"error": {"type": "string"}})

    @allure.description("Test for DELETE /character?name=... method with bad names. "
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
        allure.dynamic.title(f"Delete request with bad name '{bad_name}' ({reason}, status code {expected_status_code})")
        response = api.delete_character_by_name(bad_name)
        check.base_complex_check(response, expected_status_code)
        if check_msg:
            check.object_schema(response.content, {"error": {"type": "string", "regex": "name"}})

    @allure.title("Delete record with empty name")
    @allure.description("Check DELETE request with empty name. "
                        "Expected status code 400 and error message. "
                        "No one records will be deleted")
    def test_empty_name(self, api):
        response = api.delete_character_by_name("")
        check.base_complex_check(response, 400, schema={"error": {"type": "string"}})

    @allure.title("Delete record with null name")
    @allure.description("Check DELETE request with null name. "
                        "Expected status code 400 and error message. "
                        "No one records will be deleted")
    def test_null_name(self, api):
        response = api.delete_character_by_name(None)
        check.base_complex_check(response, 400, schema={"error": {"type": "string"}})

    @allure.title("Delete new record")
    @allure.description("Check DELETE request for new record. "
                        "Expected status code 200")
    def test_delete_new_record(self, api, fake):
        character_data = {"name": "TestName" + str(fake.random_number()),
                          "universe": "TestUniverse",
                          "education": "TestEducation",
                          "weight": 1,
                          "height": 2,
                          "identity": "TestIdentity",
                          "other_aliases": "TestAliases"}
        add_response = api.post_character(character_data)
        check.base_complex_check(add_response, 200)

        delete_response = api.delete_character_by_name(character_data["name"])
        check.base_complex_check(delete_response, 200, schema={"result": {"type": "string"}})
        check.data_contain_str(delete_response.content["result"], character_data["name"])

        find_response = api.get_character_by_name(character_data["name"])
        check.base_complex_check(find_response, 400, schema={"error": {"type": "string"}})

    @allure.description("Check double DELETE request. "
                        "Only one record will be deleted. "
                        "Expected status code 200 and 400 + error message")
    def test_double_delete(self, api):
        del_name = "Dracula"

        first_response = api.delete_character_by_name(del_name)
        check.base_complex_check(first_response, 200, schema={"result": {"type": "string"}})
        check.data_contain_str(first_response.content["result"], del_name)

        second_response = api.delete_character_by_name(del_name)
        check.base_complex_check(second_response, 400, schema={"error": {"type": "string"}})