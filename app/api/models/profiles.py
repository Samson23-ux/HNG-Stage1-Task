from datetime import datetime, timezone
from sqlalchemy import (
    Enum,
    UUID,
    Index,
    Float,
    Column,
    String,
    Integer,
    PrimaryKeyConstraint,
)


from app.database.base import Base
from app.api.schemas.profiles import GenderEnum, AgeGroupEnum


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(UUID)
    name = Column(String, nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    gender_probability = Column(Float, nullable=False)
    sample_size = Column(Integer, nullable=False)
    age = Column(Integer, nullable=False)
    age_group = Column(Enum(AgeGroupEnum), nullable=False)
    country_id = Column(String, nullable=False)
    country_probability = Column(Float, nullable=False)
    created_at = Column(
        String, default=datetime.now(timezone.utc).isoformat(), nullable=False
    )

    __table_args__ = (
        PrimaryKeyConstraint("id", name="profiles_id_pk"),
        Index("idx_profiles_name", name),
        Index("idx_profiles_gender", gender),
        Index("idx_profiles_age_group", age_group),
        Index("idx_profiles_country_id", country_id),
    )
