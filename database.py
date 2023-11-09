
import sqlite3
from contextlib import closing

from models import SlotInfo

DB_PATH = 'data_bomb.db'

def create_database():
    # Create the database or tables if they don't exist
    with closing(sqlite3.connect(DB_PATH)) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS slot_info (
                slot_number INTEGER PRIMARY KEY,
                tablet_count INTEGER,
                take_time TIME,
                before_food BOOLEAN
            )
        ''')
        connection.commit()





def get_slots_info():
    with closing(sqlite3.connect(DB_PATH)) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT slot_number, tablet_count, take_time, before_food FROM slot_info')
        slots_info = cursor.fetchall()
    return slots_info

def update_slot_info(slot_number: int, tablet_count: int, take_time: str, before_food: int):
    with closing(sqlite3.connect(DB_PATH)) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO slot_info (slot_number, tablet_count, take_time, before_food)
            VALUES (?, ?, ?, ?)
        ''', (slot_number, tablet_count, take_time, before_food))
        connection.commit()
        return True


def insert_data(slot_info: SlotInfo):
    with closing(sqlite3.connect('data_bomb.db')) as connection_obj:
        c = connection_obj.cursor()

        c.execute('SELECT slot_number FROM slot_info WHERE slot_number = ?', (slot_info.slot_number,))
        slot = c.fetchone()

        if slot:
            c.execute('UPDATE slot_info SET take_time = ?, tablet_count = ?, before_food = ? WHERE slot_number = ?',
                      (slot_info.take_time, slot_info.tablet_count, slot_info.before_food, slot_info.slot_number))
            connection_obj.commit()
            return True
        else:
            c.execute('INSERT INTO slot_info (slot_number, take_time, tablet_count, before_food) VALUES (?, ?, ?, ?)',
                      (slot_info.slot_number, slot_info.take_time, slot_info.tablet_count, slot_info.before_food))
            connection_obj.commit()
            return True
        



