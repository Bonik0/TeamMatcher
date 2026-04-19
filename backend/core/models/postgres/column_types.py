from sqlalchemy import ForeignKey, Identity, func
from sqlalchemy.orm import mapped_column, MappedColumn, relationship
from sqlalchemy.orm.relationships import _RelationshipDeclared
from typing import Any, Annotated
from datetime import datetime


created_at_type = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at_type = Annotated[
    datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)
]


def cascade_foreign_key(column: str, *args, **kwargs) -> ForeignKey:
    return ForeignKey(column, *args, ondelete="CASCADE", **kwargs)


def pk_key_identity_column(*args, **kwargs) -> MappedColumn[Any]:
    return mapped_column(
        *args,
        Identity(start=1, increment=1),
        primary_key=True,
        autoincrement=True,
        **kwargs,
    )


def pk_key_column(*args, **kwargs) -> MappedColumn[Any]:
    return mapped_column(*args, primary_key=True, **kwargs)


def unique_column(*args, **kwargs) -> MappedColumn[Any]:
    return mapped_column(*args, unique=True, **kwargs)


def one_to_one_relationship(*args, **kwargs) -> _RelationshipDeclared[Any]:
    lazy: str = kwargs.pop("lazy", "raise_on_sql")
    cascade: str = kwargs.pop("cascade", "all")
    uselist: bool = kwargs.pop("uselist", False)
    return relationship(*args, lazy=lazy, cascade=cascade, uselist=uselist, **kwargs)


def many_to_one_relationship(*args, **kwargs) -> _RelationshipDeclared[Any]:
    lazy: str = kwargs.pop("lazy", "raise_on_sql")
    uselist: bool = kwargs.pop("uselist", False)
    return relationship(*args, lazy=lazy, uselist=uselist, **kwargs)


def one_to_many_relationship(*args, **kwargs) -> _RelationshipDeclared[Any]:
    lazy: str = kwargs.pop("lazy", "raise_on_sql")
    cascade: str = kwargs.pop("cascade", "all")
    passive_deletes: bool = kwargs.pop("passive_deletes", True)
    return relationship(
        *args, lazy=lazy, cascade=cascade, passive_deletes=passive_deletes, **kwargs
    )


def many_to_many_relationship(*args, **kwargs) -> _RelationshipDeclared[Any]:
    return one_to_many_relationship(*args, **kwargs)
