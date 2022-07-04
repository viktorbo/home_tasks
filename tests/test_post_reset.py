import allure

from framework.helpers.checker import Checker as check


@allure.feature("POST")
@allure.story("RESET")
class TestPostReset:

    @allure.title("Check reset collection with POST new character")
    @allure.description("Test for 'POST /reset' method. Check response structure, data types and response time."
                        "Pipeline: get collection -> modified collection (post) -> reset -> check collection")
    def test_reset_collection_after_post(self, api, fake):
        # get collection
        old_collection_response = api.get_all_characters()
        check.status_code(old_collection_response.status_code, 200)

        # modified collection
        character_data = {"name": "TestName" + str(fake.random_number()),
                          "universe": "TestUniverse",
                          "education": "TestEducation",
                          "weight": 1,
                          "height": 2,
                          "identity": "TestIdentity"}
        character_response = api.post_character(character_data)
        check.status_code(character_response.status_code, 200)

        # reset
        reset_response = api.post_reset_collection()
        check.status_code(reset_response.status_code, 200)
        check.request_exec_time(reset_response.time, 1.5)

        # check
        check.matching_data(api.get_all_characters().content, old_collection_response.content)

    @allure.title("Check reset collection with PUT character")
    @allure.description("Test for 'POST /reset' method. Check response structure, data types and response time."
                        "Pipeline: get collection -> modified collection (put) -> reset -> check collection")
    def test_reset_collection_after_put(self, api, fake):
        # get collection
        old_collection_response = api.get_all_characters()
        check.status_code(old_collection_response.status_code, 200)

        # modified collection
        # возможно данный пайплайн надо будет доработать в заивисмости от частоты изменения данных в коллекции
        character_data = {"name": "Dracula",
                          "universe": "Romania",
                          "education": "High School of Transilvania",
                          "weight": 3,
                          "height": 1.2,
                          "identity": "Publicly known"}
        character_response = api.put_character(character_data)
        check.status_code(character_response.status_code, 200)

        # reset
        reset_response = api.post_reset_collection()
        check.status_code(reset_response.status_code, 200)
        check.request_exec_time(reset_response.time, 1.5)

        # check
        check.matching_data(api.get_all_characters().content, old_collection_response.content)

    @allure.title("Check reset collection with DELETE character")
    @allure.description("Test for 'POST /reset' method. Check response structure, data types and response time."
                        "Pipeline: get collection -> modified collection (delete) -> reset -> check collection")
    def test_reset_collection_after_delete(self, api, fake):
        # get collection
        old_collection_response = api.get_all_characters()
        check.status_code(old_collection_response.status_code, 200)

        # modified collection
        character_name = "Dracula"
        character_response = api.delete_character_by_name(character_name)
        check.status_code(character_response.status_code, 200)

        # reset
        reset_response = api.post_reset_collection()
        check.status_code(reset_response.status_code, 200)
        check.request_exec_time(reset_response.time, 1.5)

        # check
        check.matching_data(api.get_all_characters().content, old_collection_response.content)
