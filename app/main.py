
from fastapi import FastAPI, Depends 
from contextlib import asynccontextmanager
from schemas import ReadingCreate, ReadingResponse 
from database import database 
import database.crud as crud 
from sqlalchemy.orm import Session 
from sqlalchemy import text
from schemas import AnalysisResult 
import datetime 
from typing import Optional 

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    print("Application startup...")
    database.create_db_tables() 
    yield
    print("Application shutdown...")

app = FastAPI(title="Device Data Analysis Service", lifespan=lifespan)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Device Data Analysis Service"}

@app.get("/health")
async def health_check(db: Session = Depends(database.get_db)): 
    try:
        db.execute(text('SELECT 1'))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        print(f"Health check DB connection error: {e}")
        return {"status": "error", "database": "disconnected"}

@app.post("/devices/{device_id}/readings/", response_model=ReadingResponse, status_code=201)
def post_reading(
    device_id: str,
    reading: ReadingCreate,
    db: database.SessionLocal = Depends(database.get_db) 
):
   
    return crud.create_reading(db=db, device_id=device_id, reading=reading)

@app.get("/devices/{device_id}/analysis", response_model=AnalysisResult)
def get_analysis_all_time(
    device_id: str,
    db: database.SessionLocal = Depends(database.get_db)
):
    
    readings = crud.get_readings_for_device(db=db, device_id=device_id)
    if not readings:
         return AnalysisResult(count=0, sum_x=0, sum_y=0, sum_z=0)
    stats = crud.calculate_stats(readings) 
    return AnalysisResult(**stats)


@app.get("/devices/{device_id}/analysis/period", response_model=AnalysisResult)
def get_analysis_period(
    device_id: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    db: database.SessionLocal = Depends(database.get_db)
):
    
    readings = crud.get_readings_for_device(
        db=db, device_id=device_id, start_time=start_time, end_time=end_time
    )
    if not readings:
         return AnalysisResult(count=0, sum_x=0, sum_y=0, sum_z=0)
    stats = crud.calculate_stats(readings) 
    return AnalysisResult(**stats)