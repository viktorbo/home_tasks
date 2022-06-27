import os

import allure


class Credentials:
    """
    Класс для работы с данными авторизации (логин + пароль)
    """

    __login = None
    __password = None

    def __init__(self):
        self.__login, self.__password = self._get_credentials()

    @property
    def login(self):
        with allure.step("Return LOGIN"):
            return self.__login

    @property
    def password(self):
        with allure.step("Return PASSWORD"):
            return self.__password

    @staticmethod
    def _get_credentials():
        with allure.step("Getting LOGIN and PASSWORD for authorization"):
            return os.getenv('TEST_LOGIN'), os.getenv('TEST_PASSWORD')
