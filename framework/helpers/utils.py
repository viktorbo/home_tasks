import allure


def get_first_duplicate_name(collection):
    with allure.step("Get first duplicate name in collection"):
        names_list = [record.get('name') for record in collection]
        names_set = set(names_list)
        for name in names_set:
            count = names_list.count(name)
            if count > 1:
                return name, count


def transform_to_float(obj):
    with allure.step(f"Transform object {obj} ({type(obj)}) to float"):
        return float(obj)


def update_dictionary_single_val(dictionary: dict, fields, new_val):
    with allure.step(f"Update dictionary"):
        dictionary.update(dict.fromkeys(fields, new_val))
