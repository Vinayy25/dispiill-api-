#app for fastapi endpoint 
from fastapi import FastAPI, HTTPException
from typing import List

from database import create_database, get_slots_info, insert_data
from models import SlotInfo

app = FastAPI()

create_database()
# Retrieve slot information
@app.get("/slot_info", response_model=List[SlotInfo])
def display_slot_info():
    slots_info = get_slots_info()
    return [SlotInfo(slot_number=slot[0], tablet_count=slot[1], take_time=slot[2], before_food=bool(slot[3])) for slot in slots_info]

# Update or insert slot information
@app.put("/insert_data")
def update_slot_time(slot_info: SlotInfo):
    success = insert_data(slot_info)
    if success:
        return {"message": f"Slot {slot_info.slot_number} updated with new details"}
    else:
        raise HTTPException(status_code=404, detail=f"Failed to update slot {slot_info.slot_number}")
# Get slot information by slot number
@app.get("/slot_info/{slot_number}", response_model=SlotInfo)
def get_slot_info(slot_number: int):
    slots_info = get_slots_info()
    for slot in slots_info:
        if slot[0] == slot_number:
            return SlotInfo(slot_number=slot[0], tablet_count=slot[1], take_time=slot[2], before_food=bool(slot[3]))
    raise HTTPException(status_code=404, detail="Slot number not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)