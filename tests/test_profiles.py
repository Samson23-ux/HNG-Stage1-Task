import pytest
from uuid import uuid7, UUID
from httpx import AsyncClient, Response


@pytest.mark.asyncio
async def test_create_profile(async_client: AsyncClient):
    payload: dict = {"name": "sergio"}

    res: Response = await async_client.post(
        "/api/profiles",
        json=payload
    )
    json_res = res.json()

    assert res.status_code == 201
    assert json_res["data"]["name"] == payload.get("name")


@pytest.mark.asyncio
async def test_wrong_name_type(async_client: AsyncClient):
    payload: dict = {"name": 2}

    res: Response = await async_client.post(
        "/api/profiles",
        json=payload
    )

    assert res.status_code == 422


@pytest.mark.asyncio
async def test_invalid_name(async_client: AsyncClient):
    payload: dict = {"name": "not342a6665name"}

    res: Response = await async_client.post(
        "/api/profiles",
        json=payload
    )

    assert res.status_code == 502


@pytest.mark.asyncio
async def test_get_profiles(async_client: AsyncClient):
    payload: dict = {"name": "sergio"}

    await async_client.post(
        "/api/profiles",
        json=payload
    )

    res = await async_client.get("/api/profiles")
    json_res = res.json()

    assert len(json_res["data"]) >= 1


@pytest.mark.asyncio
async def test_get_profiles_not_found(async_client: AsyncClient):
    res = await async_client.get("/api/profiles")
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_get_profile(async_client: AsyncClient):
    payload: dict = {"name": "sergio"}

    profile_res: Response = await async_client.post(
        "/api/profiles",
        json=payload
    )

    profile_id: str = profile_res.json()["data"]["id"]

    res = await async_client.get(f"/api/profiles/{profile_id}")
    json_res = res.json()

    assert json_res["data"]["name"] == payload.get("name")


@pytest.mark.asyncio
async def test_get_profile_not_found(async_client: AsyncClient):
    profile_id: UUID = uuid7()
    res = await async_client.get(f"/api/profiles/{profile_id}")

    assert res.status_code == 404


@pytest.mark.asyncio
async def test_delete_profile(async_client: AsyncClient):
    payload: dict = {"name": "sergio"}

    profile_res: Response = await async_client.post(
        "/api/profiles",
        json=payload
    )

    profile_id: str = profile_res.json()["data"]["id"]
    res = await async_client.delete(f"/api/profiles/{profile_id}")

    assert res.status_code == 204
