import sqlite3
from db_initialization import initialization



# Устанавливаем соединение с базой данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Добавляем нового пользователя

def registrationcar_plate_db(id, plate):
    cursor.execute('INSERT INTO Cars (id, plate) VALUES (?, ?)', (id, plate))
    connection.commit()

def registrationcar_vin_db(id, vin):
    cursor.execute('UPDATE Cars SET vin = ? WHERE id = ? AND vin is NULL', (vin, id))
    connection.commit()

def registrationcar_brand_db(id, brand):
    cursor.execute('UPDATE Cars SET brand = ? WHERE id = ? AND brand is NULL', (brand, id))
    connection.commit()

def registrationcar_model_db(id, model):
    cursor.execute('UPDATE Cars SET model = ? WHERE id = ? AND model is NULL', (model, id))
    connection.commit()

def registrationcar_year_db(id, year):
    cursor.execute('UPDATE Cars SET year = ? WHERE id = ? AND year is NULL', (year, id))
    connection.commit()

def registrationcar_config_db(id, config):
    cursor.execute('UPDATE Cars SET config = ? WHERE id = ? AND config is NULL', (config, id))
    connection.commit()

def registrationcar_dealer_db(id, dealer):
    cursor.execute('UPDATE Cars SET dealer = ? WHERE id = ? AND dealer is NULL', (dealer, id))
    connection.commit()

def registrationcar_color_db(id, color):
    cursor.execute('UPDATE Cars SET color = ? WHERE id = ? AND color is NULL', (color, id))
    connection.commit()

def registration_phone(id, phone):
    cursor.execute('INSERT INTO Users (id, phone) VALUES (?, ?)', (f'{id}', f'{phone}'))
    connection.commit()

def registration_name(id, name):
    cursor.execute('UPDATE Users SET name = ? WHERE id = ?', (name, id))
    connection.commit()

def check_registration(id):
    cursor.execute(f'SELECT COUNT(*) FROM Users WHERE id = {id}')
    users = cursor.fetchall()
    return users[0][0]

def get_cars(id):
    cursor.execute(f'SELECT * FROM Cars WHERE id = ?', (id, ))
    cars = cursor.fetchall()
    return cars

def get_car_information(plate):
    cursor.execute(f'SELECT * FROM Cars WHERE plate = ?', (plate, ))
    cars = cursor.fetchone()
    return cars

def check_all():
    cursor.execute('SELECT * FROM Cars')
    users = cursor.fetchall()
    print(users)
    connection.commit()

def get_all_dealers():
    cursor.execute('SELECT name FROM Dealers')
    dealers = cursor.fetchall()
    connection.commit()
    return dealers

def put_new_dealer(name, idadmin):
    cursor.execute('INSERT INTO Dealers (name, idadmin) VALUES (?, ?)', (name, idadmin))
    connection.commit()

def delete_every_unfinished(id):
    cursor.execute('DELETE FROM Cars WHERE id = ? AND color is NULL', (id,))
    connection.commit()

def puthistory_place_db(plate, place):
    cursor.execute('INSERT INTO History (plate, place) VALUES (?, ?)', (plate, place))
    connection.commit()

def puthistory_type_db(type, plate):
    cursor.execute('UPDATE History SET type = ? WHERE plate = ? AND type is NULL', (type, plate))
    connection.commit()

def puthistory_comment_db(comment, plate):
    cursor.execute('UPDATE History SET comment = ? WHERE plate = ? AND comment is NULL', (comment, plate))
    connection.commit()

def puthistory_mileage_db(mileage, date, plate):
    cursor.execute('UPDATE History SET mileage = ?,date = ? WHERE plate = ? AND mileage is NULL', (mileage, date, plate))
    connection.commit()

def clear_history(plate):
    cursor.execute('DELETE FROM History WHERE plate = ? AND mileage is NULL', (plate,))
    connection.commit()

def get_history(plate):
    cursor.execute(f'SELECT id, type, date FROM History WHERE plate = ?', (plate,))
    history = cursor.fetchall()
    connection.commit()
    return history

def get_order(id):
    cursor.execute(f'SELECT place, type, comment, mileage, date, plate FROM History WHERE id = ?', (id,))
    history = cursor.fetchall()
    connection.commit()
    return history

# Сохраняем изменения и закрываем соединение
def over():
    check_all()
    connection.close()

initialization()
