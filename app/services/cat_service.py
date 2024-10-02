from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import delete, distinct, func, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.models import cat_model
from app.schemas.cat_schema import BreedList, Cat, CatCreate, CatList, CatUpdate
from app.utils.helper import convert_date, validate_date


async def create_item(cat_schema: CatCreate, db: AsyncSession) -> Cat:
    date_string = await validate_date(cat_schema)

    stmt = (
        insert(cat_model.Cat)
        .values(
            breed=cat_schema.breed,
            age=datetime.strptime(date_string, '%Y-%m-%d'),
            description=cat_schema.description,
            color=cat_schema.color,
        )
        .returning(cat_model.Cat)
    )

    result = await db.execute(stmt)
    await db.commit()
    new_cat = result.scalar_one()
    return Cat(
        id=new_cat.id,
        breed=new_cat.breed,
        color=new_cat.color,
        description=new_cat.description,
        age=await convert_date(new_cat.age),
    )


async def get_item(id: int, db: AsyncSession) -> Cat:
    stmt = select(cat_model.Cat).where(cat_model.Cat.id == id)
    result = await db.execute(stmt)
    returned_cat = result.scalar_one_or_none()
    if not returned_cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cat with ID {id} does not exist",
        )
    return Cat(
        id=returned_cat.id,
        breed=returned_cat.breed,
        color=returned_cat.color,
        description=returned_cat.description,
        age=await convert_date(returned_cat.age),
    )


async def get_items(
    limit: int,
    page: int,
    db: AsyncSession,
    breed_only: bool = False,
    breed: str | None = '',
) -> CatList | BreedList:

    skip = (page - 1) * limit

    if breed_only:
        total_stmt = select(func.count(distinct(cat_model.Cat.breed)))

        breed_only_stmt = (
            select(cat_model.Cat.breed)
            .distinct()
            .order_by(cat_model.Cat.breed)
            .limit(limit)
            .offset(skip)
        )
        total = await db.execute(total_stmt)
        result = await db.execute(breed_only_stmt)
        return BreedList(total=total.scalar(), breeds=result.scalars().all())

    total_stmt = (
        select(func.count(cat_model.Cat.id))
        .where(cat_model.Cat.breed.ilike(f"%{breed}%"))
    )
    stmt = (
        select(cat_model.Cat)
        .where(cat_model.Cat.breed.ilike(f"%{breed}%"))
        .limit(limit)
        .offset(skip)
    )
    total = await db.execute(total_stmt)
    result = await db.execute(stmt)
    cats = result.scalars().all()

    cats_with_age = [
        Cat(
            id=cat.id,
            breed=cat.breed,
            color=cat.color,
            description=cat.description,
            age=await convert_date(cat.age),
        )
        for cat in cats
    ]

    return CatList(total=total.scalar(), cats=cats_with_age)


async def update_item(id: int, cat_schema: CatUpdate, db: AsyncSession) -> Cat:
    date_string = await validate_date(cat_schema)

    stmt = (
        update(cat_model.Cat)
        .where(cat_model.Cat.id == id)
        .values(
            breed=cat_schema.breed,
            age=datetime.strptime(date_string, '%Y-%m-%d').date(),
            description=cat_schema.description,
            color=cat_schema.color,
        )
        .execution_options(exclude_unset=True)
    ).returning(cat_model.Cat)

    stmt_check = select(cat_model.Cat).where(cat_model.Cat.id == id)
    result = await db.execute(stmt_check)
    existing_cat = result.scalar_one_or_none()

    if not existing_cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cat with ID {id} does not exist",
        )
    result = await db.execute(stmt)
    await db.commit()
    updated_cat = result.scalar_one()
    return Cat(
        id=updated_cat.id,
        breed=updated_cat.breed,
        color=updated_cat.color,
        description=updated_cat.description,
        age=await convert_date(updated_cat.age),
    )


async def delete_item(id: int, db: AsyncSession):
    stmt = delete(cat_model.Cat).where(cat_model.Cat.id == id)

    stmt_check = select(cat_model.Cat).where(cat_model.Cat.id == id)
    result = await db.execute(stmt_check)
    existing_cat = result.scalar_one_or_none()

    if not existing_cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cat with ID {id} does not exist",
        )
    await db.execute(stmt)
    await db.commit()
