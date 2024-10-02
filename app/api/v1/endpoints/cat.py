from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.schemas.cat_schema import BreedList, Cat, CatCreate, CatList, CatUpdate
from app.services.cat_service import (
    create_item,
    delete_item,
    get_item,
    get_items,
    update_item,
)

router = APIRouter()


@router.get('/cats/breeds', status_code=200, response_model=BreedList)
async def get_cat_breeds(
    limit: int = Query(10, ge=1),
    page: int = Query(1, ge=1),
    db: AsyncSession = Depends(get_db_session),
):
    return await get_items(limit=limit, page=page, breed_only=True, db=db)


@router.post('/cats', status_code=201, response_model=Cat)
async def create_cat(cat_schema: CatCreate, db: AsyncSession = Depends(get_db_session)):
    return await create_item(cat_schema=cat_schema, db=db)


@router.get('/cats', status_code=200, response_model=CatList)
async def get_cats(
    limit: int = Query(10, ge=1),
    page: int = Query(1, ge=1),
    breed: str = '',
    db: AsyncSession = Depends(get_db_session),
):
    return await get_items(limit=limit, page=page, breed=breed, db=db)


@router.get('/cats/{id}', status_code=200, response_model=Cat)
async def get_cat(id: int, db: AsyncSession = Depends(get_db_session)):
    return await get_item(id=id, db=db)


@router.patch('/cats/{id}', status_code=200, response_model=Cat)
async def update_cat(
    id: int, cat_schema: CatUpdate, db: AsyncSession = Depends(get_db_session)
):
    return await update_item(id=id, cat_schema=cat_schema, db=db)


@router.delete('/cats/{id}', status_code=204)
async def delete_cat(id: int, db: AsyncSession = Depends(get_db_session)):
    return await delete_item(id=id, db=db)
