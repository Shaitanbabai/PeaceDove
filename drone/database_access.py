import asyncio
import sqlite3


class DatabaseAccess:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)

    async def get_drones(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM drones")
        return cursor.fetchall()

    async def save_mission_parameters(self, parameters):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO missions (params) VALUES (?)", (parameters,))
        self.connection.commit()

    async def get_feedback(self, drone_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT feedback FROM feedback WHERE drone_id=?", (drone_id,))
        return cursor.fetchone()