import sys
from datetime import datetime
from typing import Any
from typing import List

from sqlalchemy import String, Text, Date, Float, create_engine, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from sale_inventory.entity import Item
from sale_inventory.repository import BaseRepository


class Base(DeclarativeBase):
    pass


class DBItem(Base):
    __tablename__ = "item"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text(), nullable=False)
    owner: Mapped[str] = mapped_column(String(20), nullable=False)
    expiration_date: Mapped[datetime] = mapped_column(Date())
    shipping: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float())

    def to_item(self):
        return Item(
            id=self.id,
            name=self.name,
            description=self.description,
            owner=self.owner,
            expiration_date=self.expiration_date,
            shipping=self.shipping,
            price=self.price
        )

    @classmethod
    def from_item(cls, item: Item):
        return cls(
            id=item.id,
            name=item.name,
            description=item.description,
            owner=item.owner,
            expiration_date=item.expiration_date,
            shipping=item.shipping,
            price=item.price
        )

    @classmethod
    def from_item_no_id(cls, item: Item):
        return cls(
            name=item.name,
            description=item.description,
            owner=item.owner,
            expiration_date=item.expiration_date,
            shipping=item.shipping,
            price=item.price
        )


class DatabaseRepository(BaseRepository):
    _session: Any  # output of sessionmaker(engine)

    def __init__(self, session: Any):
        self._session = session

    def get_item(self, item_id: int) -> Item | None:
        with self._session() as session:
            stmt = select(DBItem).where(DBItem.id == item_id)
            try:
                item: DBItem = session.scalars(stmt).one()
            except NoResultFound:
                return None
            return item.to_item()

    def get_items(self) -> List[Item]:
        item_list = []
        with self._session() as session:
            stmt = select(DBItem)
            items = session.scalars(stmt).all()
            for i in items:
                item_list.append(i.to_item())
        return item_list

    def create_item(self, item: Item) -> Item:
        db_item = DBItem.from_item_no_id(item)
        with self._session() as session:
            session.add(db_item)
            session.commit()
            return db_item.to_item()

    def update_item(self, item: Item) -> Item | None:
        with self._session() as session:
            stmt = select(DBItem).where(DBItem.id == item.id)
            try:
                db_item: DBItem = session.scalars(stmt).one()
            except NoResultFound:
                return None
            db_item.name = item.name
            db_item.description = item.description
            db_item.owner = item.owner
            db_item.expiration_date = item.expiration_date
            db_item.shipping = item.shipping
            db_item.price = item.price

            session.commit()

            return db_item.to_item()

    def delete_item(self, item_id: int) -> bool:
        with self._session() as session:
            db_item = session.get(DBItem, item_id)
            if not db_item:
                return False
            session.flush()  # needed later for lazy loading
            session.delete(db_item)
            session.commit()

        return True


def migrate(url: str):
    engine = create_engine(url=url, echo=True)
    Base.metadata.create_all(engine)
    print("done")


def main():
    if len(sys.argv) == 2:
        migrate(url=sys.argv[1])
    else:
        print("missing parameter 'database url' (like sqlite:///my.db)")


if __name__ == "__main__":
    main()
