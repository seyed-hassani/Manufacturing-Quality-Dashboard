import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Set DB path
DB_PATH = os.path.join('..', 'data', 'generated_sensor_data.db')

# Connect to SQLite
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensor_readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        machine_id TEXT,
        temperature REAL,
        pressure REAL,
        defect_rate REAL
    )
''')

# Simulate data
def simulate_data(start_date, days=30, machines=5):
    data = []
    for day in range(days):
        date = start_date + timedelta(days=day)
        for machine_id in range(1, machines + 1):
            for hour in range(0, 24, 2):  # every 2 hours
                timestamp = datetime(date.year, date.month, date.day, hour)
                temp = round(np.random.normal(75, 5), 2)
                pressure = round(np.random.normal(30, 3), 2)
                defect_rate = round(max(0, np.random.normal(2, 1)), 2)
                data.append((timestamp, f'Machine_{machine_id}', temp, pressure, defect_rate))
    return data

# Generate and insert
start_date = datetime.today() - timedelta(days=30)
sensor_data = simulate_data(start_date)

cursor.executemany('''
    INSERT INTO sensor_readings (timestamp, machine_id, temperature, pressure, defect_rate)
    VALUES (?, ?, ?, ?, ?)
''', sensor_data)

conn.commit()
conn.close()

print(f"Inserted {len(sensor_data)} rows into {DB_PATH}")
