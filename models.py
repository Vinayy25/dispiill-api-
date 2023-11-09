from pydantic import BaseModel

class SlotInfo(BaseModel):
    slot_number: int
    tablet_count: int
    take_time: str  # This corresponds to the 'time_taken' field
    before_food: bool
