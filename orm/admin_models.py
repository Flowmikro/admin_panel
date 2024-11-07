from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    item_children: Mapped[list["ItemModel"]] = relationship(cascade='save-update, merge, delete', back_populates="user_parent")


class ItemModel(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    item_name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_parent: Mapped["UserModel"] = relationship(back_populates="employee_children")

