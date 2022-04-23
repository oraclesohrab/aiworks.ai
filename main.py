import json
from distutils.util import strtobool
import time

file_choices = {
    'users': 'users.json',
    'tickets': 'tickets.json',
    'organizations': 'organizations.json',
    'quit': 'quit'
}


class Search:
    def __init__(self, inputs: dict) -> None:
        self.search_parameters = inputs
        self.__search_result = self.__search
        if not self.__search_result:
            print("No results found!")
        else:
            for record in self.__search_result:
                record = self.__extend_record(record)
                self.__show_record(record)
                print("-" * 90)
            print(f"Hit count: {len(self.__search_result)}")
        time.sleep(5)

    def __extend_record(self, record: dict) -> dict:
        if record.get('organization_id'):
            organization_id = record.pop('organization_id')
            org = {
                "key": "_id",
                "value": organization_id,
                "file": open_file('organizations.json')
            }
            self.search_parameters = org
            organization = self.__search
            if organization:
                record['organization'] = organization[0]
            else:
                record['organization_id'] = organization_id
                record['organization'] = "Organization data is not available in our archive!!!"
        if record.get("submitter_id"):
            user_id = record.pop('submitter_id')
            user = {
                "key": "_id",
                "value": user_id,
                "file": open_file('users.json')
            }
            print(user['value'])
            self.search_parameters = user
            submitter = self.__search
            if submitter:
                record['submitter'] = submitter[0]
            else:
                record['submitter_id'] = user_id
                record['submitter'] = "User data is not available in our archive!!!"
        if record.get("assignee_id"):
            user_id = record.pop('assignee_id')
            user = {
                "key": "_id",
                "value": user_id,
                "file": open_file('users.json')
            }
            self.search_parameters = user
            assignee = self.__search
            if assignee:
                record['assignee'] = assignee[0]
            else:
                record['assignee_id'] = user_id
                record['assignee'] = "User data is not available in our archive!!!"
        return record

    @staticmethod
    def __show_record(obj: dict, prefix_space="") -> None:
        for key, value in obj.items():
            space = 30 - len(key)
            space = " " * space
            if isinstance(value, dict):
                print(f'{prefix_space}{key}:{space}(')
                Search.__show_record(value, " " * 31)
                print(" " * 30 + ')')
            else:
                print(f'{prefix_space}{key}:{space}{value}')

    def __is_exists(self, field_value) -> bool:
        if isinstance(field_value, list):
            return self.search_parameters['value'] in field_value
        if isinstance(field_value, bool):
            return bool(strtobool(self.search_parameters['value'])) == field_value
        if isinstance(field_value, int):
            return int(self.search_parameters['value']) == field_value
        return self.search_parameters['value'].lower() == field_value.lower()

    @property
    def __search(self) -> list:
        if self.search_parameters['value'] == "is_empty":
            return list(filter(lambda record: (
                    self.search_parameters['key'] not in record.keys()
                    or record[self.search_parameters['key']] is None
                    or record[self.search_parameters['key']] == ''),
                               self.search_parameters['file']))
        else:
            return list(
                filter(lambda record: self.__is_exists(record.get(self.search_parameters['key'], '')),
                       self.search_parameters['file'])
            )


def open_file(name: str) -> list:
    with open(f"files/{name}", 'r') as file:
        return json.load(file)


def show_options(dictionary: dict) -> None:
    for key in dictionary.keys():
        if key == 'quit':
            continue
        print(f"->{key}<-")


def main() -> None:
    while True:
        print("Welcome to Sohrab Search App.")
        print("Enter 'quit' whenever you want to quit the app.")
        search_parameters = {
            "file": None,
            "key": None,
            "value": None
        }
        while not search_parameters.get('file'):
            print('\n\n')
            print("-----CHOOSING THE FILE-----")
            print("Please press one of the options.\n")
            print("Options are:")
            show_options(file_choices)
            search_parameters['file'] = file_choices.get(input("Please select a file: "), None)
        if search_parameters['file'] == "quit":
            break
        search_parameters['file'] = open_file(search_parameters['file'])
        while not search_parameters.get('key'):
            print('\n\n')
            print("-----SELECTING A KEY TO SEARCH ON-----")
            print("Please press one of the options.")
            print("Options are:")
            show_options(max(search_parameters['file'], key=len))
            search_parameters['key'] = input("Please enter a key:\n")
        if search_parameters['key'] == "quit":
            break
        while not search_parameters.get('value'):
            print('\n\n')
            print("-----ENTERING A VALUE TO SEARCH-----")
            print("Please enter a Value to search:")
            search_parameters['value'] = input("(Enter 'is_empty' to search for empty values)\n")
        if search_parameters['value'] == "quit":
            break
        Search(search_parameters)


if __name__ == '__main__':
    main()
    print("Thank you for using my app!!!\n\n")
