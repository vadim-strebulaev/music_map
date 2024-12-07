import json
import random
import os
import re

def generate_random_coordinates(center_lat, center_lon, delta_lat, delta_lon):
    lat = random.uniform(-delta_lat, delta_lat)
    lon = random.uniform(-delta_lon, delta_lon)
    random_lat = center_lat + lat
    random_lon = center_lon + lon
    return random_lat, random_lon

def extract_music_number(music_file):
    # Используем регулярное выражение для извлечения числа из названия файла
    match = re.search(r'\d+', music_file)
    return int(match.group()) if match else float('inf')  # Возвращаем бесконечность, если нет числа

def generate_music_coordinates(music_folder):
    center_lat = 55.752282 
    center_lon = 37.621661
    delta_lat = 0.4
    delta_lon = 0.5

    # Получаем список музыкальных файлов
    music_files = [f for f in os.listdir(music_folder) if os.path.isfile(os.path.join(music_folder, f))]
    print("\n".join(music_files))
    data = []
    for music_file in music_files:
        lat, lon = generate_random_coordinates(center_lat, center_lon, delta_lat, delta_lon)
        data.append({
            'latitude': lat,
            'longitude': lon,
            'music_file': music_file
        })

    # Сортируем данные по числовой части названия музыкальных файлов
    sorted_data = sorted(data, key=lambda x: extract_music_number(x['music_file']))
    return sorted_data

# Укажите путь к папке с музыкой
music_folder = 'musics'

# Генерация данных с координатами
updated_data = generate_music_coordinates(music_folder)

# Запись данных в JSON файл
with open('updated_check_cords.json', 'w') as f:
    json.dump(updated_data, f, separators=(', ', ': '), indent=4)  

print("Координаты успешно обновлены и записаны в updated_check_cords.json.")
