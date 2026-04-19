from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from core.models.postgres.column_types import (
    unique_column,
    pk_key_identity_column,
    created_at_type,
    updated_at_type,
    one_to_many_relationship,
)
from core.models.postgres.base import Base


class UserDB(Base):
    __tablename__ = "users"

    id: Mapped[int] = pk_key_identity_column()
    role: Mapped[str] = mapped_column()
    first_name: Mapped[str] = mapped_column(String(50))
    patronymic: Mapped[str | None] = mapped_column(String(50), default=None)
    surname: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = unique_column(String(255))
    hash_password: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[created_at_type]
    updated_at: Mapped[updated_at_type]

    projects = one_to_many_relationship("ProjectDB", back_populates="organizer")
    competences = one_to_many_relationship(
        "UserCompetenceAssociationDB", back_populates="user"
    )
    forms = one_to_many_relationship(
        "UserProjectRoleAssociationDB", back_populates="user"
    )
    team_memberships = one_to_many_relationship("TeamMemberDB", back_populates="user")
