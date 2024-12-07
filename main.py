from flask import Flask, request, jsonify, send_from_directory, render_template, session
import psycopg2
import pygeohash
app = Flask(__name__)
app.secret_key = 'acbb627042582aca619f60d9092b4a2c336d6aa2d44057a4'  

# файлы
music_folder = 'musics'

# подключение к базе данных
def get_db_connection():
    conn = psycopg2.connect(
        dbname='manita',
        user='postgres',
        password='1',  # Укажите свой пароль
        host='localhost',
        port='5432'
    )
    return conn

# загрузка точек из базы данных
def load_points():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT geohash, music_file_name FROM music_locations")
    points = cur.fetchall()
    cur.close()
    conn.close()
    
    # Преобразуем данные в удобный формат
    return [{'geohash': point[0], 'music_file': point[1]} for point in points]

# поиск ближайшей точки
def find_nearest_point(lat, lon):
    points = load_points()
    
    nearest_point_file_name = None
    min_dist = float('inf')
    current_point = pygeohash.encode(lat, lon)

    for point in points:
        geohash = point['geohash']
        music_file = point['music_file']
        
        dist = pygeohash.geohash_approximate_distance(current_point, geohash)
        if dist < min_dist:
            min_dist = dist
            nearest_point_file_name = music_file
    print(min_dist)
    return nearest_point_file_name

# обновление музыки по сессии
@app.route('/')
def index():
    session['previous_music_file'] = None  
    return render_template('web.html')  


@app.route('/coords', methods=['GET'])
def get_coords():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT latitude, longitude, music_file_name FROM music_locations")
        points = cur.fetchall()
        cur.close()
        conn.close()

        # Проверка динамически возвращаемых данных
        coords = []
        for point in points:
            if len(point) >= 3:  # Убедитесь, что кортеж содержит достаточное количество элементов
                coords.append({
                    'latitude': point[0],
                    'longitude': point[1],
                    'music_file': point[2]  # music_file_name должен быть на индекс 2
                })
            else:
                # Отладочная информация
                print("Недостаточно данных в точке:", point)

        return jsonify(coords)  # Возвращаем все координаты
    except Exception as e:
        print("Ошибка:", e)  # Сообщение об ошибке в консоль
        return jsonify({"error": str(e)}), 500


# обновление музыки
@app.route('/location', methods=['POST'])
def location():
    print("Ищу файл...")
    previous_music = session.get('previous_music_file')  
    current_music = session.get('current_music_file')    
    same_file_count = session.get('same_file_count', 0)        

    data = request.json
    lat = data['latitude']
    lon = data['longitude']
    new_music = find_nearest_point(lat, lon)

    print(f"Next: {new_music}, Prev: {previous_music}, Current: {current_music}, Count: {same_file_count}")
    
    if current_music is None:
        session['current_music_file'] = new_music  
        return jsonify({'music_file': new_music})  

    
    if new_music != current_music:
        same_file_count = 0
        session['current_music_file'] = new_music  
    else:
        same_file_count += 1
        session['same_file_count'] = same_file_count

    if new_music == previous_music:
        return jsonify({'music_file': None})  

    if same_file_count >= 2:
        session['previous_music_file'] = new_music  
        session['same_file_count'] = 0  
        return jsonify({'music_file': new_music})  

    return jsonify({'music_file': None})

# получение музыки по названию
@app.route('/music/<filename>')
def get_music(filename):
    return send_from_directory(music_folder, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
