import allure


def get_first_duplicate_name(collection):
    with allure.step("Get first duplicate name in collection"):
        names_list = [record.get('name') for record in collection]
        names_set = set(names_list)
        for name in names_set:
            count = names_list.count(name)
            if count > 1:
                return name, count

