from sqlalchemy.orm import Session
from database import models 
from schemas import ReadingCreate 
from typing import List, Dict, Any, Optional
from database.models import Reading 
from sqlalchemy import func, select 
import datetime
import statistics 

def create_reading(db: Session, device_id: str, reading: ReadingCreate):
    db_reading = models.Reading(
        device_id=device_id,
        x=reading.x,
        y=reading.y,
        z=reading.z
    )
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    return db_reading

def get_readings_for_device(db: Session, device_id: str, start_time: Optional[datetime.datetime] = None, end_time: Optional[datetime.datetime] = None) -> List[Reading]:
    query = db.query(models.Reading).filter(models.Reading.device_id == device_id)
    if start_time:
        query = query.filter(models.Reading.timestamp >= start_time)
    if end_time:
        query = query.filter(models.Reading.timestamp < end_time)
    return query.order_by(models.Reading.timestamp).all()

def calculate_stats(readings: List[Reading]) -> Dict[str, Any]:
    if not readings:
        return {
            "min_x": None, "max_x": None, "sum_x": 0, "count": 0, "median_x": None,
            "min_y": None, "max_y": None, "sum_y": 0, "median_y": None,
            "min_z": None, "max_z": None, "sum_z": 0, "median_z": None,
        }

    count = len(readings)
    x_values = [r.x for r in readings]
    y_values = [r.y for r in readings]
    z_values = [r.z for r in readings]

    stats = {
        "count": count,
        "min_x": min(x_values), "max_x": max(x_values), "sum_x": sum(x_values),
        "min_y": min(y_values), "max_y": max(y_values), "sum_y": sum(y_values),
        "min_z": min(z_values), "max_z": max(z_values), "sum_z": sum(z_values),
        "median_x": statistics.median(x_values) if x_values else None,
        "median_y": statistics.median(y_values) if y_values else None,
        "median_z": statistics.median(z_values) if z_values else None,
    }
    return stats
