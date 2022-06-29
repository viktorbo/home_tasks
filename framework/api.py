import json

import allure
from requests import request
from requests.auth import HTTPBasicAuth

from framework.helpers.credentials import Credentials
from framework.helpers.simple_response import SimpleResponse


class API:
    """
    Класс для работы с API, логирование работы методов через Allure
    """

    _service_address = "http://rest.test.ivi.ru/v2/"
    _credentials = None

    def __init__(self):
        self._credentials = Credentials()

    def auth_request(self, request_type, api_method, **kwargs):
        with allure.step(f"Execute {request_type.upper()} {api_method.upper()} with {kwargs}"):
            with allure.step("Create full URL address"):
                url = self._service_address + api_method
            with allure.step(f"Execute '{request_type.upper()}' request to '{url}' "
                             f"with HTTPBasicAuth and args: {kwargs}"):
                response = request(method=request_type, url=url,
                                   auth=HTTPBasicAuth(self._credentials.login, self._credentials.password),
                                   **kwargs)
            with allure.step(f"Transform response to SimpleResponse (custom type)"):
                # Сатус коды для преобразования контента могут быть дополненены
                return SimpleResponse(status_code=response.status_code,
                                      time=response.elapsed.total_seconds(),
                                      headers=dict(response.headers),
                                      content=json.loads(response.text) if (response.text
                                                                            and response.status_code not in [414, ])
                                      else response.text)

    # GET
    def get_all_characters(self) -> SimpleResponse:
        return self.auth_request("GET", "characters")

    def get_character_by_name(self, name) -> SimpleResponse:
        return self.auth_request("GET", "character", params={"name": name})

    # POST
    def post_character(self, character_data: dict) -> SimpleResponse:
        return self.auth_request("POST", "character", json=character_data)

    def post_reset_collection(self) -> SimpleResponse:
        return self.auth_request("POST", "reset")

    # PUT
    def put_character(self, character_data: dict) -> SimpleResponse:
        return self.auth_request("PUT", "character", json=character_data)

    # DELETE
    def delete_character_by_name(self, name) -> SimpleResponse:
        return self.auth_request("DELETE", "character", params={"name": name})
