from csv import DictReader, DictWriter
from os.path import exists

class NameError(Exception):
    def __init__(self, txt):
        self.txt = txt

def get_info():
    flag = False
    while not flag:
        try:
            first_name = input('Имя: ')
            if len(first_name) < 2:
                raise NameError('Слишком короткое имя')
            second_name = input('Введите фамилию: ')
            if len(second_name) < 4:
                raise NameError('Слишком короткая фамилия')
            phone_number = input('Введите номер телефона: ')
            if len(phone_number) < 11:
                raise NameError('Слишком короткий номер телефона')
        except NameError as err:
            print(err)
        else:
            flag = True
    return [first_name, second_name, phone_number]

def create_file(file_name):
    with open(file_name, 'w', encoding='utf-8', newline='') as data:
        f_w = DictWriter(data, fieldnames=['first_name', 'second_name', 'phone_number'])
        f_w.writeheader()

def write_file(file_name):
    user_data = get_info()
    res = read_file(file_name)
    new_obj = {'first_name': user_data[0], 'second_name': user_data[1], 'phone_number': user_data[2]}
    res.append(new_obj)
    standart_write(file_name, res)

def read_file(file_name):
    with open(file_name, encoding='utf-8') as data:
        f_r = DictReader(data)
        return list(f_r)

def remove_row(file_name):
    search = input('Введите имя или фамилию для удаления: ')
    res = read_file(file_name)
    new_res = [entry for entry in res if entry['first_name'].lower() != search.lower() and entry['second_name'].lower() != search.lower()]
    
    if len(new_res) != len(res):
        standart_write(file_name, new_res)
        print(f'Запись с именем или фамилией "{search}" удалена.')
    else:
        print(f'Запись с именем или фамилией "{search}" не найдена.')

def update_entry(file_name):
    search = input('Введите имя или фамилию для изменения: ')
    res = read_file(file_name)
    
    entry_found = False
    for entry in res:
        if entry['first_name'].lower() == search.lower() or entry['second_name'].lower() == search.lower():
            print(f'Найдена запись: {entry}')
            new_first_name = input('Введите новое имя (оставьте пустым для пропуска): ') or entry['first_name']
            new_second_name = input('Введите новую фамилию (оставьте пустым для пропуска): ') or entry['second_name']
            new_phone_number = input('Введите новый номер телефона (оставьте пустым для пропуска): ') or entry['phone_number']
            
            entry.update({'first_name': new_first_name, 'second_name': new_second_name, 'phone_number': new_phone_number})
            entry_found = True
            
    if entry_found:
        standart_write(file_name, res)
        print(f'Запись с именем или фамилией "{search}" обновлена.')
    else:
        print(f'Запись с именем или фамилией "{search}" не найдена.')

def standart_write(file_name, res):
    with open(file_name, 'w', encoding='utf-8', newline='') as data:
        f_w = DictWriter(data, fieldnames=['first_name', 'second_name', 'phone_number'])
        f_w.writeheader()
        f_w.writerows(res)

def copy_data(source_file, destination_file):
    if not exists(source_file):
        print(f'Файл {source_file} отсутствует.')
        return
    data = read_file(source_file)
    standart_write(destination_file, data)
    print(f'Данные скопированы из {source_file} в {destination_file}.')

file_name = 'phone.csv'
destination_file = 'phone2.csv'

def main():
    while True:
        command = input('Введите команду: ')
        if command == 'q':
            break
        elif command == 'w':
            if not exists(file_name):
                create_file(file_name)
            write_file(file_name)
        elif command == 'r':
            if not exists(file_name):
                print('Файл отсутствует, пожалуйста создайте файл')
                continue
            print(*read_file(file_name))
        elif command == 'd':
            if not exists(file_name):
                print('Файл отсутствует, пожалуйста создайте файл')
                continue
            remove_row(file_name)
        elif command == 'u':
            if not exists(file_name):
                print('Файл отсутствует, пожалуйста создайте файл')
                continue
            update_entry(file_name)
        elif command == 'c':
            copy_data(file_name, destination_file)

main()
