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


def show_all(*args, contacts=contacts):
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


def save(contacts, filename="contacts.txt"):
    with open(filename, "wb") as f:
        pickle.dump(contacts, f)
    print(f"Contacts saved to {filename}")

def load(filename="contacts.txt"):
    with open(filename, 'rb') as f:
        contacts = pickle.load(f)
    print(f"Contacts loaded from {filename}")
    return contacts


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
            exit: 'exit',
            save: 'save',
            load: 'load'}


def command_handler(text):
    for command, kword in COMMANDS.items():
        if text.startswith(kword):
            return command, text.replace(kword, '').strip()
    return no_command, None




def main():
    print('Hello user!')
    load(contacts)
    while True:
        
        user_input = input('>>>')
        command, data = command_handler(user_input)

        print(command(data))

        

        if user_input == 'exit':
            save(contacts) 
            break 
            

if __name__ == '__main__':

    # record = Record(Name("Marina"), [Phone("380993456789")], Birthday("15.05.1995"))
    # record1 = Record(Name("Petro"), [Phone("380977654321")], Birthday("10.10.1988"))
    # record2 = Record(Name("Olena"), [Phone("380994567890")], Birthday("20.06.1987"))
    # record3 = Record(Name("Serg"), [Phone("380956789012")], Birthday("07.12.1990"))
    # record4 = Record(Name("Lydmila"), [Phone("380983456789")], Birthday("23.08.1992"))
    # record5 = Record(Name("Sanya"), [Phone("380963210987")], Birthday("02.03.1983"))
    # record6 = Record(Name("Vasya"), [Phone("380977890123")], Birthday("18.09.1998"))
    # record7 = Record(Name("Oleg"), [Phone("380954321098")], Birthday("25.11.1985"))
    # record8 = Record(Name("Tanya"), [Phone("380979012345")], Birthday("12.07.1991"))
    
    
    # contacts.add_record(record)
    # contacts.add_record(record1)
    # contacts.add_record(record2)
    # contacts.add_record(record3)
    # contacts.add_record(record4)
    # contacts.add_record(record5)
    # contacts.add_record(record6)
    # contacts.add_record(record7)
    # contacts.add_record(record8)


    main()
    