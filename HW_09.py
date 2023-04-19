from classes import AddressBook, Record, Name, Phone, Birthday
from datetime import date
import pickle


contacts = AddressBook()


def input_error(func):
    
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Not enough params. Print help"
        except KeyError:
            return 'Contact not found, try again or use help'
        except AttributeError:
            return 'Not enough params. Print help'
    return inner


@input_error
def add(*args):
    list_of_param = args[0].split()
    name = list_of_param[0]
    birthday = None
    phone_numbers = []
    for param in list_of_param[1:]:
        if len(param) == 12 and param.isnumeric():
            phone_numbers.append(Phone(param))
        else:
            birthday = Birthday(param)

    record = Record(Name(name), phone_numbers, birthday)
    contacts.add_record(record)

    if not birthday:
        return f'{name}, {phone_numbers[0]}'
    return f'{name},{phone_numbers[0]},{birthday}'


def show_all(*args):
    if not contacts.data:
        return 'No contacts'

    contact_list = []
    for name, record in contacts.data.items():
        phones = ', '.join(str(phone) for phone in record.phone)
        if record.birthday:
            contact_list.append(f"{name} {phones} days to birthday: {record.days_to_birthday()}")
        else:
            contact_list.append(f"{name} {phones}, Date of birth is not specified")
    page = args[0]
    if not page:
        return "\n".join(contact_list)
    
    for records in contacts.iterator(int(page)):
        for name, record in records:
            phones = ', '.join(str(phone) for phone in record.phone)
            days_to_birthday = f"days to birthday: {record.days_to_birthday()}" if record.birthday else ""
            print(f"{name} {phones} {days_to_birthday}")
        print('*' * 100)
    

@input_error
def phone(*args):
    list_of_param = args[0].split()
    name = Name(list_of_param[0])
    phone_number = [Phone(phone) for phone in list_of_param[1:-1]]
    record = contacts.get(name.value)
    phone_number = record.phone[0]
    return f'{phone_number}'


@input_error
def change(*args):
    list_of_param = args[0].split()
    name = Name(list_of_param[0])
    phone_number = [Phone(phone) for phone in list_of_param[1:]]
    record = contacts.get(name.value)
    if not record:
        raise KeyError
    if not phone_number:
        raise AttributeError
    record.phone = phone_number
    return f'Contact {name.value} updated {str(phone_number[0])}'


def save(contacts, filename):
    with open(filename, mode="a") as f:
        pickle.dump(contacts, f)
    print(f"Contacts saved to {filename}")

def load(filename):
    with open(filename, 'rb') as f:
        pickle.load(f)
    print(f"Contacts loaded from {filename}")


def search_contacts(name):
    name = Name(name)
    f_contacts = contacts.search_by_name(name.value)
    result = []
    if f_contacts:
        for contact in f_contacts:
            result.append(f"{contact.name.value} Phone: {contact.phone[0].value} days to birthday: {contact.days_to_birthday()}")
    return "\n".join(result)


def exit(*args):
    return "Good bye!"


def no_command(*args):
    return 'Unknown command, try again or help'


def help(*args):
    return "If there are problems, read the file, readme!"


def hello(*args):
    return "How can I help you?"


COMMANDS = {help: 'help',
            hello: 'hello',
            add: 'add',
            show_all: 'show all',
            phone: 'phone',
            change: 'change',
            save: 'save',
            load: 'load',
            exit: 'exit',
            search_contacts: 'search'
            }



def command_handler(text):
    for command, kword in COMMANDS.items():
        if text.startswith(kword):
            return command, text.replace(kword, '').strip()
    return no_command, None




def main():
    print('Hello user!')
    print(contacts.load_from_file('contacts.bin'))
    while True:
        
        user_input = input('>>>')
        command, data = command_handler(user_input)

        print(command(data))

        

        if user_input == 'exit':
            print(contacts.save_to_file('contacts.bin')) 
            break 
            

if __name__ == '__main__':

    main()
    