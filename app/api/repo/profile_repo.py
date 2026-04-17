from uuid import UUID
from sqlalchemy import select, Sequence, func
from sqlalchemy.ext.asyncio import AsyncSession


from app.api.models.profiles import Profile


class ProfileRepo:
    async def get_profiles(
        self,
        session: AsyncSession,
        gender: str,
        country_id: str,
        age_group: str,
    ) -> Sequence[Profile]:
        stmt = select(Profile)

        if gender:
            stmt = stmt.where(func.lower(Profile.gender) == gender.lower())

        if country_id:
            stmt = stmt.where(func.lower(Profile.country_id) == country_id.lower())

        if age_group:
            stmt = stmt.where(func.lower(Profile.age_group) == age_group.lower())

        res = await session.execute(stmt)
        profiles: Sequence[Profile] = res.scalars().all()
        return profiles

    async def get_profile(
        self, profile_id: UUID, session: AsyncSession
    ) -> Profile | None:
        stmt = select(Profile).where(Profile.id == profile_id)
        res = await session.execute(stmt)
        profile: Profile | None = res.scalar()
        return profile

    async def get_profile_by_name(
        self, name: str, session: AsyncSession
    ) -> Profile | None:
        stmt = select(Profile).where(Profile.name == name)
        res = await session.execute(stmt)
        profile: Profile | None = res.scalar()
        return profile

    async def add_profile_to_db(self, profile: Profile, session: AsyncSession):
        session.add(profile)
        await session.flush()
        await session.refresh(profile)

    async def delete_profile(self, profile: Profile, session: AsyncSession):
        await session.delete(profile)
        await session.flush()


profile_repo: ProfileRepo = ProfileRepo()
