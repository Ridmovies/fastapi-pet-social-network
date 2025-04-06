import os
import re
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


import json
from pathlib import Path


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
    Path(upload_dir).mkdir(parents=True, exist_ok=True)
    file_path = Path(upload_dir) / gpx_file_name
    with open(file_path, "wb") as f:
        f.write(contents)

    # Парсинг GPX-файла
    try:
        gpx = gpxpy.parse(contents)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при парсинге GPX-файла: {str(e)}")

    # Инициализация переменных
    total_distance = 0
    total_time = timedelta()
    total_elevation_gain = 0
    points = []

    # Обработка треков и сегментов
    for track in gpx.tracks:
        for segment in track.segments:
            points.extend(segment.points)
            for i in range(1, len(segment.points)):
                prev_point = segment.points[i - 1]
                curr_point = segment.points[i]

                distance = prev_point.distance_2d(curr_point)
                total_distance += distance

                if prev_point.time and curr_point.time:
                    time_diff = curr_point.time - prev_point.time
                    total_time += time_diff

                if prev_point.elevation and curr_point.elevation:
                    elevation_diff = curr_point.elevation - prev_point.elevation
                    if elevation_diff > 0:
                        total_elevation_gain += elevation_diff

    # Расчет средней скорости
    if total_time.total_seconds() > 0:
        avg_speed = (total_distance / 1000) / (total_time.total_seconds() / 3600)
    else:
        avg_speed = 0

    # Создание индивидуальной карты
    map_center = [points[0].latitude, points[0].longitude]
    m = folium.Map(location=map_center, zoom_start=13)

    folium.PolyLine(
        locations=[[point.latitude, point.longitude] for point in points],
        color='blue'
    ).add_to(m)

    # Сохранение индивидуальной карты
    m.save(f'src/static/maps/{map_filename}')

    # Работа с общей картой
    common_tracks_path = Path('src/static/maps/common_tracks.json')

    # Загружаем существующие треки или создаем новый файл
    try:
        if common_tracks_path.exists():
            with open(common_tracks_path, 'r') as f:
                all_tracks = json.load(f)
        else:
            all_tracks = []
    except Exception as e:
        print(f"Ошибка при загрузке common_tracks.json: {e}")
        all_tracks = []

    # Добавляем новый трек
    new_track = {
        "id": str(now.timestamp()),
        "type": workout_type.value,
        "date": now.strftime('%Y-%m-%d'),
        "points": [[point.latitude, point.longitude] for point in points],
        "color": {
            WorkoutType.RUN: 'blue',
            WorkoutType.BICYCLE: 'green',
            WorkoutType.WALK: 'orange',
        }.get(workout_type, 'red')
    }
    all_tracks.append(new_track)

    # Сохраняем обновленные треки
    with open(common_tracks_path, 'w') as f:
        json.dump(all_tracks, f, indent=2)

    # Генерируем общую карту из всех треков
    generate_common_map(all_tracks)

    # Форматирование результатов
    distance_km = f"{total_distance / 1000:.2f}"
    duration_sec = int(total_time.total_seconds())
    avg_speed_kmh = f"{avg_speed:.2f}"

    return {
        "distance_km": float(distance_km),
        "duration_sec": duration_sec,
        "avg_speed_kmh": float(avg_speed_kmh),
    }


def generate_common_map(tracks):
    """Генерирует общую карту из всех сохраненных треков"""
    if not tracks:
        return

    # Определяем центр карты по первому треку
    map_center = tracks[0]['points'][0]
    common_map = folium.Map(location=map_center, zoom_start=13)

    # Добавляем все треки на карту
    for track in tracks:
        folium.PolyLine(
            locations=track['points'],
            color=track['color'],
            weight=2,
            opacity=0.7,
            popup=f"{track['type']} - {track['date']}"
        ).add_to(common_map)

    # Сохраняем общую карту
    common_map.save('src/static/maps/common_map.html')

