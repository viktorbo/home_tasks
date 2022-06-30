import allure
import pytest
from faker import Faker

from framework.api import API


@pytest.fixture(scope="session")
def api():
    """
    Create API object

    :return: API object
    """
    with allure.step("Create API object"):
        api = API()
    yield api
    with allure.step("Delete API object"):
        del api


@pytest.fixture(scope="session")
def fake():
    """
    Create Faker object

    :return: Faker object
    """
    with allure.step("Create Faker object"):
        fake = Faker()
    yield fake
    with allure.step("Delete Faker object"):
        del fake
