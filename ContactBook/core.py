from abc import abstractmethod, ABC
from collections import UserDict
from datetime import datetime
import pickle
import re


class AddressBook(UserDict):
    def __init__(self):
        try:
            with open("save_file.txt", "rb") as file:
                self.data = pickle.load(file)
        except:
            self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def del_record(self, record):
        self.data.pop(record.name.value)

    def save_contacts(self):
        if self.data:
            with open("save_file.txt", "wb") as file:
                pickle.dump(self.data, file)


class Record:
    def __init__(self, name, phone=None, birthday=None, note=None, address=None, email=None):
        self.name = Name(name)
        self.phones = [Phone(phone)] if phone else []
        self.birthday = Birthday(birthday) if birthday else ""
        self.note = Note(note) if note else ""
        self.email = Email(email) if email else ""
        self.address = Address(address) if address else ""
        self.tag = {}

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday).value.strftime('%d.%m.%Y')

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_note(self, note):
        self.note = Note(note).value

    def add_tag(self, tag):
        self.tag["name"] = self.name.value
        self.tag["tag"] = tag
        self.tag["note"] = self.note

    def add_address(self, address):
        self.address = Address(address)

    def add_email(self, email):
        self.email = Email(email)

    def update_dict(self, note):
        for tag in self.tag.keys():
            self.note = note
            self.tag["note"] = note

    def delete_phone(self, phone_for_delete):
        for phone in self.phones:
            if phone.value == phone_for_delete:
                self.phones.remove(phone)

    def change_phone(self, phone_for_change, new_phone):
        for index, phone in enumerate(self.phones):
            if phone.value == phone_for_change:
                self.phones[index] = Phone(new_phone)

    def days_to_birthday(self):
        if self.birthday:
            birthday = datetime.strptime(self.birthday, '%d.%m.%Y')
            if ((birthday).replace(year=(datetime.now()).year)) > datetime.now():
                print(
                    f"to birthday {(((birthday).replace(year=(datetime.now()).year)) - datetime.now()).days} days")
            else:
                print(
                    f"to birthday {(((birthday).replace(year=(datetime.now()).year + 1)) - datetime.now()).days} days")
        else:
            return TypeError

    def interval_birthday(self, interval):
        if self.birthday:
            birthday = datetime.strptime(self.birthday, '%d.%m.%Y')
            if ((birthday).replace(year=(datetime.now()).year)) > datetime.now():
                diference = (
                    ((birthday).replace(year=(datetime.now()).year)) - datetime.now()).days
            else:
                diference = (
                    ((birthday).replace(year=(datetime.now()).year + 1)) - datetime.now()).days
            if diference <= interval:
                print(f"{(self.name.value).capitalize()}, birthday: {self.birthday}")


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    pass


class Phone(Field):
    @Field.value.setter
    def value(self, value: str):
        if not all((value.startswith('+380'), value[1:].isdigit(), len(value) == 13)):
            raise ValueError(
                print("Your phone should be like this: +380888888888"))
        self._value = value


class Birthday(Field):
    @Field.value.setter
    def value(self, value):
        try:
            birthday = datetime.strptime(value, '%d.%m.%Y')
            self._value = birthday
        except:
            raise ValueError(
                print("Your birthday should be like this: 20.12.2000"))

    def __str__(self) -> str:
        return datetime.strftime(self._value, '%d.%m.%Y')


class Email(Field):
    @Field.value.setter
    def value(self, value: str):
        if not re.search("[a-zA-Z][a-zA-Z0-9_.]+@\w+\.\w\w+", value):
            raise ValueError(
                print("Your email should be like this: example@gmail.com"))
        self._value = value

    def __str__(self) -> str:
        return (self.value)


class Note(Field):
    pass


class Address(Field):
    pass


class IBot(ABC):
    @abstractmethod
    def show_contacts(self):
        pass

    @abstractmethod
    def show_notes(self):
        pass

    @abstractmethod
    def show_tags(self):
        pass

    @abstractmethod
    def show_address(self):
        pass

    @abstractmethod
    def show_emails(self):
        pass


class Bot(IBot):
    def __init__(self, data) -> None:
        self.data = data

    def show_contacts(self):
        for name in self.data:
            print("{:<10}{:^35}{:>10}".format((self.data[name].name.value).capitalize(),
            " ".join([phone.value for phone in self.data[name].phones]), self.data[name].birthday)) 

    def show_notes(self):
        show_list = []
        for name in self.data:
            if self.data[name].note:
                show_list.append(f"name: {(self.data[name].name.value).capitalize()}, note: {self.data[name].note}")
        if show_list:
            for item in show_list:
                print(item)
        else:
            raise TypeError

    def show_tags(self):
        show_list = []
        for name in self.data:
            if self.data[name].tag:
                show_list.append(self.data[name].tag)
        if show_list:
            show_list = sorted(show_list, key=lambda x: x['tag'])
            for item in show_list:
                print(item)
        else:
            raise TypeError
    
    def show_address(self):
        show_list = []
        for name in self.data:
            if self.data[name].address:
                show_list.append(f"name: {(self.data[name].name.value).capitalize()}, address: {self.data[name].address.value}")
        if show_list:
                for item in show_list:
                    print(item)
        else:
            raise TypeError

    def show_emails(self):
        show_list = []
        for name in self.data:
            if self.data[name].email:
                show_list.append(f"name: {(self.data[name].name.value).capitalize()}, email: {self.data[name].email}")
        if show_list:
                for item in show_list:
                    print(item)
        else:
            raise TypeError
