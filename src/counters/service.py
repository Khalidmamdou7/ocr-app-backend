# service.py
# Module specific business logic goes here

from typing import Annotated

from fastapi import Depends, HTTPException, status

from .models import *
from ..auth.schemas import UsersDB
from ..auth.models import User, RoleEnum
from datetime import datetime
from .schemas import CountersDB


def create_counter(counter: CounterCreate) -> Counter:
    counter = CountersDB().add_counter(CounterInDB(**counter.dict(), created_at=datetime.now(), updated_at=datetime.now()))
    return Counter(**counter.dict())

def get_counters() -> list[Counter]:
    counters = CountersDB().get_counters()
    return [Counter(**counter.dict()) for counter in counters]

def get_counters_by_machine_id(machine_id: str) -> list[Counter]:
    counters = CountersDB().get_counters_by_machine_id(machine_id)
    return [Counter(**counter.dict()) for counter in counters]


def get_counter(counter_id: str) -> Counter:
    counter = CountersDB().get_counter(counter_id)
    return Counter(**counter.dict())


def update_counter(counter_id: str, counter: CounterUpdate) -> Counter:
    counter = CountersDB().update_counter(counter_id, counter)
    return Counter(**counter.dict())

def delete_counter(counter_id: str):
    CountersDB().delete_counter(counter_id)