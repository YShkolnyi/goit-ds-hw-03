from pymongo import MongoClient
from pymongo.server_api import ServerApi
from faker import Faker
from tabulate import tabulate

#Генерую фейкові дані українською
fake = Faker('uk_UA')

#допомагаю юзеру
help = [
    ('читай','прочитає усі записи в базі даних і виведе у термінал.'),
    ("читай *ім'я*","знайде у базі даних всю інформацію про хом'яків з цим ім'ям і виведе у термінал."),
    ("онови_вік *ім'я* *новий вік*","Замінить інформацію про вік у даного хом'яка і виведе у термінал вік до зміни і після зміни."),
    ("характеристика *ім'я* *текст*","Додасть ще одну текстову характеристику до конкретного хом'яка і покаже змінену версію у терміналі."),
    ("видали ім'я","Видалить всю інформацію про хом'яків з таким ім'ям. Покаже у терміналі що саме було видалено."),
    ("видали","Видалить усю інформацію з бази даних."),
    ("Стоп","Завершує роботу скрипту."),
    ("Вихід","Завершує роботу скрипту.")
]

#підключаюсь
client = MongoClient(
    "mongodb+srv://YShkolnyi:Stokrotka_13@cluster0.7wu4k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    server_api=ServerApi('1')
)

#вказую базу
db = client.GOIT_ds_hw03

#оброблюю вийнятки
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Невірні аргументи."
        except IndexError:
            return "Не достатньо аргументів."
        except UnboundLocalError:
            return "В колекції немає жодного елементу."
    return inner

@input_error    #використовую декоратор
def read(args=None):
    if args:
        name, *_ = args
        name = name.strip().capitalize()
        hamsters = db.hamsters.find({"name": name}) #структурую вхідні данні і шукаю в базі по запиту імені
    else:
        hamsters = db.hamsters.find() #інша функція реалізується, якщо імені не вказано
    result = list(hamsters)
    if len(result) == 0: #якщо такого імені немає, то список буде пустим
        return f"Не знайдено імені {name}."
    else:
        return tabulate(result, headers='keys', tablefmt='fancy_grid') #люблю таблички )

@input_error
def update_age(args=None):
        name, new_age, *_ = args
        new_age = int(new_age) #перевіряю чи це число
        name = name.strip().capitalize()
        hamsters_old = db.hamsters.find({"name": name}, {"features":0}) #не хочу бачити характеристики - вимикаю
        result_old = list(hamsters_old)
        db.hamsters.update_one({"name": name}, {"$set": {"age": new_age}}, upsert = False) #вписую False якщо не хочу додавати дані при заміні в разі їх відсутності
        hamsters_new = db.hamsters.find({"name": name}, {"age":1}) #після зміни витягую тільки вік (і айді бо так прийнято)
        result_new = list(hamsters_new)
        if len(result_old) == 0:
            return f"Не знайдено імені {name}."
        else:
            for old_record, new_record in zip(result_old, result_new): #склеюю результати для висвітлення у табличці
                old_record["new_age"] = new_record.get("age")
            return tabulate(result_old, headers='keys', tablefmt='fancy_grid')
        
@input_error
def update_features(args=None):
        name = args[0]
        name = name.strip().capitalize()
        new_features = ' '.join(args[1:])#список слів заміняю на рядок з пробілами
        if len(new_features) > 0: #виключаю можливість додавання рядку в якому 0 символів
            db.hamsters.update_one({"name": name}, {"$push": {"features": new_features}})
        hamsters = db.hamsters.find({"name": name}) #шукаю оновленний документ у колекції
        result = list(hamsters)
        if len(result) == 0:
            return f"Не знайдено імені {name}."
        else:
            return tabulate(result, headers='keys', tablefmt='fancy_grid') 
        
@input_error
def delete(args=None):
    if args:
        name, *_ = args
        name = name.strip().capitalize()
        hamsters = db.hamsters.find({"name": name})
        result = list(hamsters)
        db.hamsters.delete_many({"name": name}) #видаляю всіх з таким іменем
    else:
        db.hamsters.delete_many({}) # якщо аргументів немає, то видаляю всі дані. колекцію залишаю
        return "Всі елементи колекції видалено."
    if len(result) == 0:
        return f"Не знайдено імені {name}."
    else:
        return tabulate(result, headers='keys', tablefmt='fancy_grid')

def parse_input(user_input): #використовую раніше написаний код
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def main():
    print("На зв'язку база даних хом'яків.") #з невідомих причин вирішив українізувати скрипт. Більше не буду. дуже не зручно постійно перемикати мову. 15% коду довелось переписувати, бо мову не переключив :)
    while True:
        user_input = input("Чекаю команду:")
        command, *args = parse_input(user_input)
        if command in ["вихід", "стоп"]:
            print("Заходьте ще!")
            break
        elif command == "читай":
            print(read(args))
        elif command == "онови_вік":
            print(update_age(args))
        elif command == "характеристика":
            print(update_features(args))
        elif command == "видали":
            print(delete(args))
        elif command == "хелп": 
            print(tabulate(help, headers=['КОМАНДИ','ОПИС'], tablefmt='fancy_grid'))
        else:
            print('Невірна команда. Для списку команд напишіть "хелп".')
            
if __name__ == "__main__":
    main()
