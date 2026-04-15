from enum import Enum


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"


class AgeGroupEnum(str, Enum):
    CHILD = "child"
    ADULT = "adult"
    SENIOR = "senior"
    TEENAGER = "teenager"
