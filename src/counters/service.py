# service.py
# Module specific business logic goes here

from typing import Annotated

from fastapi import Depends, HTTPException, status

from .models import *
from ..auth.schemas import UsersDB
from ..auth.models import User, RoleEnum

counters = []

def create_counter(counter: CounterCreate) -> Counter:
    # TODO: Call the DB to create a counter
    counter = CounterInDB(
        id="1",
        name=counter.name,
        machine_id=counter.machine_id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    counters.append(counter)
    return Counter(**counter.dict())

def get_counters() -> list[Counter]:
    counters_in_db = []
    for counter in counters:
        counters_in_db.append(Counter(**counter.dict()))
    return counters_in_db

def get_counters_by_machine_id(machine_id: str) -> list[Counter]:
    counters_in_db = []
    for counter in counters:
        if counter.machine_id == machine_id:
            counters_in_db.append(Counter(**counter.dict()))
    return counters_in_db

def get_counter(counter_id: int) -> Counter:
    if counter_id > len(counters):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="counter not found")
    return Counter(**counters[counter_id - 1].dict())

def update_counter(counter_id: int, counter: CounterUpdate) -> Counter:
    if counter_id > len(counters):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="counter not found")
    counter = counters[counter_id - 1]
    counter.name = counter.name
    counter.machine_id = counter.machine_id
    counter.updated_at = datetime.now()
    return Counter(**counter.dict())

def delete_counter(counter_id: int):
    counters.pop(counter_id - 1)