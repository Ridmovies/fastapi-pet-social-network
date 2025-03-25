import os
from datetime import timedelta, datetime

import gpxpy
from fastapi import HTTPException
import folium

from src.workout.models import WorkoutType

def create_map_filename():
    # Количество секунд с 1 января 1970 года
    now = datetime.now()
    file_name = now.timestamp()
    file_name = f"{file_name}_map.html"
    return file_name


async def calculate_track_info(file, workout_type: WorkoutType, map_filename: str):
    # Проверка типа файла
    if file.content_type != "application/gpx+xml":
        raise HTTPException(status_code=400, detail="Файл должен быть GPX")


    # Текущее время
    now = datetime.now()


    gpx_file_name = f"{now.timestamp()}_{workout_type}.gpx"

    # Чтение файла
    contents = await file.read()

    # Сохранение файла на сервере
    upload_dir = "src/static/tracks"
    os.makedirs(upload_dir, exist_ok=True)  # Создание директории, если её нет
    file_path = os.path.join(upload_dir, gpx_file_name)
    with open(file_path, "wb") as f:
        f.write(contents)

    # Парсинг GPX-файла
    try:
        gpx = gpxpy.parse(contents)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при парсинге GPX-файла: {str(e)}")

    # Инициализация переменных
    total_distance = 0  # Общее расстояние
    total_time = timedelta()  # Общее время
    total_elevation_gain = 0  # Общий набор высоты
    points = []  # Список всех точек трека

    # Обработка треков и сегментов
    for track in gpx.tracks:
        for segment in track.segments:
            points.extend(segment.points)
            for i in range(1, len(segment.points)):
                prev_point = segment.points[i - 1]
                curr_point = segment.points[i]

                # Расчет расстояния между точками
                distance = prev_point.distance_2d(curr_point)
                total_distance += distance

                # Расчет времени между точками
                if prev_point.time and curr_point.time:
                    time_diff = curr_point.time - prev_point.time
                    total_time += time_diff

                # Расчет набора высоты
                if prev_point.elevation and curr_point.elevation:
                    elevation_diff = curr_point.elevation - prev_point.elevation
                    if elevation_diff > 0:
                        total_elevation_gain += elevation_diff

    # Расчет средней скорости (в км/ч)
    if total_time.total_seconds() > 0:
        avg_speed = (total_distance / 1000) / (total_time.total_seconds() / 3600)
    else:
        avg_speed = 0

    # Создание карты
    map_center = [points[0].latitude, points[0].longitude]
    m = folium.Map(location=map_center, zoom_start=13)

    # Добавление маршрута
    folium.PolyLine(
        locations=[[point.latitude, point.longitude] for point in points],
        color='blue'
    ).add_to(m)


    # Сохранение карты в HTML
    m.save(f'src/static/maps/{map_filename}')


    # print(f"{total_time.total_seconds()=}", type(total_time.total_seconds()))
    distance_km = f"{total_distance / 1000:.2f}"
    duration_sec = int(total_time.total_seconds() )
    avg_speed_kmh = f"{avg_speed:.2f}"


    # Возврат результата
    return {
        "distance_km": float(distance_km),
        "duration_sec": duration_sec,
        "avg_speed_kmh": float(avg_speed_kmh),
    }

