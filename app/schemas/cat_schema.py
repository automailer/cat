from pydantic import BaseModel


class CatBase(BaseModel):
    breed: str
    color: str
    description: str


class CatCreate(CatBase):
    year: str
    month: str
    day: str


class CatUpdate(CatBase):
    year: str
    month: str
    day: str


class Cat(CatBase):
    id: int
    age: str


class CatList(BaseModel):
    total: int
    cats: list[Cat] = []


class BreedList(BaseModel):
    total: int
    breeds: list[str] = []
