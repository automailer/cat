from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Cat(Base):  # type: ignore
    __tablename__ = 'cat'

    id = Column(Integer, primary_key=True, index=True)
    breed = Column(String(50), index=True)
    age = Column(Date, index=True)
    color = Column(String(20), index=True)
    description = Column(String(200), index=True)

    def __repr__(self):
        return f"<Cat(id={self.id}, breed={self.breed}, age={self.age}, color={self.color}, description={self.description}>"
