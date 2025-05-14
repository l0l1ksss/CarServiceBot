import sqlite3



def initialization():
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    # Создаем таблицу Cars
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Cars (
    id TEXT,
    plate TEXT, 
    vin TEXT,
    brand TEXT, 
    model TEXT,
    year INTEGER,
    config TEXT,
    dealer TEXT,
    color TEXT
    )
    ''')

    connection.commit()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    id TEXT,
    phone TEXT,
    name TEXT
    )
    ''')


    cursor.execute('''
    CREATE TABLE IF NOT EXISTS History (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plate TEXT,
    place TEXT
    offical TEXT,
    type TEXT,
    comment TEXT,
    mileage INTEGER,
    date TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Dealers (
    name TEXT,
    idadmin INTEGER
    )
    ''')




    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()