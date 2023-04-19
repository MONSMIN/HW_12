import os
import pickle
from collections import UserDict
from datetime import datetime
from itertools import islice
import re


class Field:
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return str(self)
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value
    
 
class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return "Name: " + super().__str__()


class Phone(Field):
    def __init__(self, phone):
        super().__init__(phone)

    def __str__(self):
        return "Phone: " + super().__str__()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, phone):
        if phone.isnumeric() and len(phone) == 12:
            self._value = phone
        else:
            raise ValueError("Phone number must contain only 12 digits.")


class Birthday(Field):
    def __init__(self, value=None):
        super().__init__(value)

    def __str__(self):
        return "Birthday: " + (super().__str__() if self.value else '')

    def  value(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Incorrect date format, should be dd.mm.yyyy")
        self._value = value


class Record:
    def __init__(self, name, phone, birthday=None):
        self.name = name
        self.phone = phone
        self.birthday = birthday
        
    def add_phone(self, phone:Phone):
        self.phone.append(phone)
        
    def del_phone(self, phone):
        self.phone.remove(phone)
        
    def edit_phone(self, old_phone, new_phone):
        index = self.phone.index(old_phone)
        self.phone[index] = new_phone

    def add_birthday(self, birthday):
        if isinstance(birthday, Birthday):
            self.birthday = birthday
        else:
            raise ValueError("Invalid birthday")
        

    def days_to_birthday(self):
        if not self.birthday or not self.birthday.value:
            return None
        
        today = datetime.today()
        bday = datetime.strptime(self.birthday.value, "%d.%m.%Y").replace(year=today.year)
        
        if bday < today:
            bday = bday.replace(year=today.year + 1)
        
        delta = bday - today
        return delta.days


class AddressBook(UserDict):
    def __iter__(self):
        return self.data

    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self, page=None):
        start = 0
        while True:
            result = list(islice(self.data.items(), start, start + page))
            if not result:
                break
            yield result
            start += page

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self, file)
        return "AddressBook save successful"

    
    def load_from_file(self, filename):
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                self.data = pickle.load(file)
            return "AddressBook load successful"
    

    def __getstate__(self):
        return self.__dict__


    def __setstate__(self, state):
        self.__dict__ = state

    
    def search_by_name(self, name):
        result = []
        for record in self.data.values():
            if name.lower() in record.name.value.lower():
                result.append(record)
        return result
    

    def search_by_phone(self, phone):
        result = []
        pattern = re.compile(phone)
        for record in self.data.values():
            for ph in record.phones:
                if pattern.search(ph.value):
                    result.append(record)
                    break
        return result