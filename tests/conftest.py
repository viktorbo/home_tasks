import allure
import pytest

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
