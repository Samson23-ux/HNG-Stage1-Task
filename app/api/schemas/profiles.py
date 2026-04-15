from uuid import UUID
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"


class AgeGroupEnum(str, Enum):
    CHILD = "child"
    ADULT = "adult"
    SENIOR = "senior"
    TEENAGER = "teenager"


class ProfileCreate(BaseModel):
    name: str


class Profile(BaseModel):
    id: UUID
    name: str
    gender: GenderEnum
    gender_probability: float
    sample_size: int
    age: int
    age_group: AgeGroupEnum
    country_id: str
    country_probability: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProfileResponse(BaseModel):
    status: str = "success"
    data: Profile | list[Profile]


class ProfileExist(ProfileResponse):
    message: str = "Profile already exists"
