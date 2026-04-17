from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession


from app.dependencies import get_session
from app.api.schemas.profiles import Profile
from app.api.services.profile_service import profile_service
from app.api.schemas.profiles import ProfileResponse, ProfileCreate, ProfileExist


profile_router = APIRouter()


@profile_router.get(
    "/profiles",
    status_code=200,
    response_model=ProfileResponse,
    description="Get all profile",
)
async def get_all_profiles(
    session: Annotated[AsyncSession, Depends(get_session)],
    gender: Annotated[str, Query(description="Filter profiles by gender")] = None,
    country_id: Annotated[str, Query(description="Filter profiles by country")] = None,
    age_group: Annotated[str, Query(description="Filter profiles by age_group")] = None,
):
    profiles: list[Profile] = await profile_service.get_profiles(
        session, gender, country_id, age_group
    )
    return ProfileResponse(data=profiles)


@profile_router.get(
    "/profiles/{profile_id}",
    status_code=200,
    response_model=ProfileResponse,
    description="Get a profile",
)
async def get_profile_by_id(
    profile_id: UUID, session: Annotated[AsyncSession, Depends(get_session)]
):
    profile: Profile = await profile_service.get_profile(profile_id, session)
    return ProfileResponse(data=profile)


@profile_router.post(
    "/profiles",
    status_code=201,
    response_model=ProfileExist | ProfileResponse,
    description="Create a profile",
)
async def create_profile(
    profile_create: ProfileCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    profile_data: dict = await profile_service.create_profile(profile_create, session)
    exists: bool = profile_data.get("exists")
    user_profile: Profile = profile_data.get("data")

    return (
        ProfileExist(data=user_profile)
        if exists
        else ProfileResponse(data=user_profile)
    )


@profile_router.delete(
    "/profiles/{profile_id}", status_code=204, description="Delete a profile"
)
async def delete_profile(
    profile_id: UUID, session: Annotated[AsyncSession, Depends(get_session)]
):
    await profile_service.delete_profile(profile_id, session)
