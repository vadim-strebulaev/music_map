import psycopg2
import json
import pygeohash

def insert_music_file(cur, geohashC, lat, lon, file_path):
    # Вставка данных в таблицу
    cur.execute("""
        INSERT INTO music_locations (latitude, longitude, geohash, music_file_name)
        VALUES (%s, %s, %s, %s)
    """, (lat, lon, geohashC, file_path))
    
    print(f"Inserted: {file_path} with Geohash: {geohashC}")

def clear_music_locations(cur):
    # Удаление всех строк из таблицы
    cur.execute("DELETE FROM music_locations")
    print("Cleared all records from music_locations table.")

def load_music_data(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)

if __name__ == "__main__":
    jsonpath = "1.json"  # Укажите путь к вашему JSON-файлу

    # Подключение к базе данных
    conn = psycopg2.connect(
        dbname='manita',
        user='postgres',
        password='1',  # Укажите свой пароль
        host='localhost',
        port='5432'
    )
    
    cur = conn.cursor()
    
    # Очистка таблицы перед вставкой новых данных
    clear_music_locations(cur)

    # Загрузка данных из JSON-файла
    music_data = load_music_data(jsonpath)

    for item in music_data:
        latitude = item['latitude']
        longitude = item['longitude']
        music_file_name = item['music_file']
        print(latitude, longitude, music_file_name)
        
        # Генерируем Geohash
        geohashC = pygeohash.encode(latitude, longitude)
        print(geohashC)
        
        # Вызов функции для вставки данных в базу
        insert_music_file(cur, geohashC, latitude, longitude, music_file_name)

    # Сохранение изменений и закрытие соединения
    conn.commit()
    cur.close()
    conn.close()
