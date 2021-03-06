import allure
import pytest

from framework.helpers.checker import Checker as check
from framework.helpers.utils import get_first_duplicate_name


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
        expected_schema = {
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
        check.base_complex_check(response, 200, schema=expected_schema)

    @allure.description("Test for 'GET /character?name=...' method for duplicate records. "
                        "Check response structure and data types. "
                        "Expected only one record")
    def test_duplicate_name_single(self, api):
        collection = api.get_all_characters().content.get("result")
        duplicate_name, count = get_first_duplicate_name(collection)
        allure.dynamic.title(f"Request with duplicate name (expect one record): '{duplicate_name}' ({count} times)")
        response = api.get_character_by_name(duplicate_name)
        check.object_schema(response.content,
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
                            }})

    @allure.description("Test for 'GET /character?name=...' method for duplicate records. "
                        "Check response structure and data types. "
                        "Expected many records")
    def test_duplicate_name_many(self, api):
        """
        ???????????? ???????? ???????????? ????????????????, ?????? ?????? ?????? ???????????????????? ?? ?????? ?????????????? ???????????? ???????????????????????? ?????????????? ?? ?????????? ????????????.
        ?????????? ?????????????? ???? ???????????????????????? ???????????????????? ???? ???????????????????????? ????????????. ?????????????????? ???? ???????? ?????????????? ????????,
        ???????????? ?????? ?????? ?????????????????????????? ??????
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
        check.base_complex_check(response, expected_status_code)
        if check_msg:
            check.object_schema(response.content, {"error": {"type": "string", "regex": "name"}})
