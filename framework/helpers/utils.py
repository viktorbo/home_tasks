import allure

"""
Здесь описаны вспомогательные функции для работы с данными
"""


def get_duplicated_records(collection, duplicate_name):
    with allure.step("Get duplicated records from collection"):
        duplicated_records = [record if record["name"] == duplicate_name else None for record in collection]
        duplicated_records = clean_list(duplicated_records, None)
        return duplicated_records


def get_first_duplicate_name(collection):
    with allure.step("Get first duplicate name in collection"):
        names_list = [record.get('name') for record in collection]
        names_set = set(names_list)
        result_name = names_list[0]
        result_count = 1
        for name in names_set:
            count = names_list.count(name)
            if count > 1:
                result_name = name
                result_count = count
                break
        return result_name, result_count


def transform_to_float(obj):
    with allure.step(f"Transform object {obj} ({type(obj)}) to float"):
        return float(obj)


def update_dictionary_single_val(dictionary: dict, fields, new_val):
    with allure.step(f"Update dictionary"):
        dictionary.update(dict.fromkeys(fields, new_val))


def change_field_name(dictionary: dict, field, new_name):
    with allure.step(f"Rename field '{field}' to '{new_name}'"):
        data = pop_field(dictionary, field)
        with allure.step(f"Update data {dict({new_name: data})}"):
            dictionary.update({new_name: data})


def pop_field(dictionary: dict, field):
    with allure.step(f"Pop field '{field}'"):
        return dictionary.pop(field)


def clean_list(list_obj: list, target_val):
    with allure.step(f"Remove all '{target_val}' objects from list"):
        result = []
        for obj in list_obj:
            if obj != target_val:
                result.append(obj)
        return result
