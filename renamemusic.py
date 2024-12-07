import os

# Путь к папке с музыкой
folder_path = 'music_downloaded'
new_folder_path = 'musics'

# Получаем список всех файлов в папке
files = os.listdir(folder_path)

# Переименование файлов
for i, filename in enumerate(files, start=4):  # начинаем с 4
    # Создаем новое имя файла
    new_name = f'music{i}.mp3'
    print(filename)
    
    # Полные пути к старому и новому файлам
    old_file_path = os.path.join(folder_path, filename)
    new_file_path = os.path.join(new_folder_path, new_name)
    
    # Переименование файла
    os.rename(old_file_path, new_file_path)

print("Переименование завершено.")
