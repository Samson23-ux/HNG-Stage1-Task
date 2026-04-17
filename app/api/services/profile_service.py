from uuid import UUID
from uuid6 import uuid7
from typing import Optional
from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient, Response, ConnectTimeout, ConnectError


from app.utils import is_digit
from app.api.models.profiles import Profile
from app.api.schemas.profiles import ProfileCreate, Profile as ProfileSchema
from app.api.repo.profile_repo import profile_repo
from app.core.exceptions import (
    ServerError,
    ResponseError,
    InvalidNameError,
    CheckTimeoutError,
    ProfileNotFoundError,
    ProfilesNotFoundError,
)


class ProfileService:
    async def genderize_request(self, name: str):
        curr_retries: int = 0
        total_retries: int = 5
        status: str = "failure"

        if await is_digit(name):
            raise InvalidNameError()

        async with AsyncClient() as client:
            while curr_retries < total_retries and status != "success":
                try:
                    res: Response = await client.get(
                        f"https://api.genderize.io/?name={name}"
                    )
                    status: str = "success"
                except (ConnectTimeout, ConnectError):
                    curr_retries += 1

        if status == "failure":
            raise CheckTimeoutError()

        json_res: dict = res.json()
        gender: str | None = json_res.get("gender")
        sample_size: int = json_res.get("count")

        if not gender or sample_size == 0:
            raise ResponseError(external_api="Genderize")

        return json_res

    async def agify_request(self, name: str):
        curr_retries: int = 0
        total_retries: int = 5
        status: str = "failure"

        if await is_digit(name):
            raise InvalidNameError()

        async with AsyncClient() as client:
            while curr_retries < total_retries and status != "success":
                try:
                    res: Response = await client.get(
                        f"https://api.agify.io/?name={name}"
                    )
                    status: str = "success"
                except (ConnectTimeout, ConnectError):
                    curr_retries += 1

        if status == "failure":
            raise CheckTimeoutError()

        json_res: dict = res.json()
        age: str | None = json_res.get("age")

        if not age:
            raise ResponseError(external_api="Agify")

        return json_res

    async def nationalize_request(self, name: str):
        curr_retries: int = 0
        total_retries: int = 5
        status: str = "failure"

        if await is_digit(name):
            raise InvalidNameError()

        async with AsyncClient() as client:
            while curr_retries < total_retries and status != "success":
                try:
                    res: Response = await client.get(
                        f"https://api.nationalize.io/?name={name}"
                    )
                    status: str = "success"
                except (ConnectTimeout, ConnectError):
                    curr_retries += 1

        if status == "failure":
            raise CheckTimeoutError()

        json_res: dict = res.json()
        country: list = json_res.get("country")

        if len(country) < 1:
            raise ResponseError(external_api="Nationalize")

        return json_res

    async def get_profiles(
        self,
        session: AsyncSession,
        gender: Optional[str] = None,
        country_id: Optional[str] = None,
        age_group: Optional[str] = None,
    ) -> list[ProfileSchema]:
        try:
            profiles: Sequence[Profile] = await profile_repo.get_profiles(
                session, gender, country_id, age_group
            )

            if not profiles:
                raise ProfilesNotFoundError()

            profiles_out: list[ProfileSchema] = []
            for profile in profiles:
                profiles_out.append(ProfileSchema.model_validate(profile))
            return profiles_out
        except Exception as e:
            if isinstance(e, ProfilesNotFoundError):
                raise ProfilesNotFoundError()

            raise ServerError() from e

    async def get_profile(self, profile_id: UUID, session: AsyncSession) -> ProfileSchema:
        try:
            profile: Profile | None = await profile_repo.get_profile(
                profile_id, session
            )

            if not profile:
                raise ProfileNotFoundError(profile_id=profile_id)

            profile_out: ProfileSchema = ProfileSchema.model_validate(profile)
            return profile_out
        except Exception as e:
            if isinstance(e, ProfileNotFoundError):
                raise ProfileNotFoundError(profile_id=profile_id)

            raise ServerError() from e

    async def create_profile(
        self, profile_create: ProfileCreate, session: AsyncSession
    ) -> ProfileSchema:
        name: str = profile_create.name

        existing_profile: Profile | None = await profile_repo.get_profile_by_name(
            name, session
        )

        if existing_profile:
            existing_profile_out: ProfileSchema = ProfileSchema.model_validate(existing_profile)
            return {"data": existing_profile_out, "exists": True}

        agify_res: dict = await self.agify_request(name)
        genderize_res: dict = await self.genderize_request(name)
        nationalize_res: dict = await self.nationalize_request(name)

        age: int = agify_res.get("age")

        if age >= 0 and age <= 12:
            age_group: str = "child"
        elif age >= 13 and age <= 19:
            age_group: str = "teenager"
        elif age >= 20 and age <= 59:
            age_group: str = "adult"
        elif age >= 60:
            age_group: str = "senior"

        country: dict = {}
        max_probability = 0
        countries: list[dict] = nationalize_res.get("country")

        for c in countries:
            probability: float = c.get("probability")
            if probability > max_probability:
                country: dict = c
                max_probability: float = probability

        profile_db: Profile = Profile(
            id=uuid7(),
            name=name,
            gender=genderize_res.get("gender"),
            gender_probability=genderize_res.get("probability"),
            sample_size=genderize_res.get("count"),
            age=age,
            age_group=age_group,
            country_id=country.get("country_id"),
            country_probability=country.get("probability"),
        )

        try:
            await profile_repo.add_profile_to_db(profile_db, session)
            profile_id: UUID = profile_db.id

            profile: Profile = await profile_repo.get_profile(profile_id, session)
            profile_out: ProfileSchema = ProfileSchema.model_validate(profile)

            await session.commit()
            return {"data": profile_out, "exists": False}
        except Exception as e:
            await session.rollback()
            raise ServerError() from e

    async def delete_profile(self, profile_id: UUID, session: AsyncSession):
        profile: Profile | None = await profile_repo.get_profile(profile_id, session)

        if not profile:
            raise ProfileNotFoundError(profile_id=profile_id)

        try:
            await profile_repo.delete_profile(profile, session)
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise ServerError() from e


profile_service: ProfileService = ProfileService()
