import httpx
from fastapi import APIRouter, HTTPException
from sqlalchemy import text

import gpxpy
import gpxpy.gpx
import folium
from datetime import timedelta, datetime

from src.database import engine, Base, SessionDep

router = APIRouter(prefix="/dev", tags=["dev"])


@router.get("")
async def root():
    return {"message": "Hello World"}


@router.delete("/drop_db")
async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        # Удаляем таблицу alembic_version
        await conn.execute(text("DROP TABLE IF EXISTS alembic_version"))
        # await conn.run_sync(Base.metadata.create_all)
    return {"message": "Database dropped"}


@router.get("/check-db-connection")
async def check_db_connection(session: SessionDep):
    """Check if the database connection is successful"""
    await session.execute(text("SELECT 1"))
    return {"message": "Connection to the database successful"}


async def get_github_commits(owner: str, repo: str, limit: int = 5):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    headers = {
        "Accept": "application/vnd.github.v3+json",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to fetch commits from GitHub",
            )
        commits = response.json()
        return commits[:limit]  # Возвращаем только последние `limit` коммитов



@router.get("/track")
async def get_track_stat():

    # Загрузка GPX-файла
    with open('src/static/tracks/track.gpx', 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

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
                time_diff = curr_point.time - prev_point.time
                total_time += time_diff

                # Расчет набора высоты
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

    # Текущее время
    now = datetime.now()

    # Количество секунд с 1 января 1970 года
    file_name = now.timestamp()

    # Сохранение карты в HTML
    m.save(f'src/static/maps/{file_name}_map.html')

    return {
        "Общее расстояние": f"{total_distance / 1000:.2f} км",
        "Общее время": str(total_time),
        "Общий набор высоты": f"{total_elevation_gain:.2f} м",
        "Средняя скорость": f"{avg_speed:.2f} км/ч",
    }
