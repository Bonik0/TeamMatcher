from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Index, Integer, UniqueConstraint
from core.models.postgres.column_types import (
    created_at_type,
    updated_at_type,
    cascade_foreign_key,
    many_to_one_relationship,
)
from core.models.postgres.base import Base


class UserProjectRoleAssociationDB(Base):
    __tablename__ = "project_users"

    user_id: Mapped[int] = mapped_column(
        Integer, cascade_foreign_key("users.id"), primary_key=True
    )
    project_role_id: Mapped[int] = mapped_column(
        Integer, cascade_foreign_key("project_roles.id"), primary_key=True
    )
    priority: Mapped[int]
    created_at: Mapped[created_at_type]
    updated_at: Mapped[updated_at_type]

    user = many_to_one_relationship("UserDB", back_populates="forms")
    project_role = many_to_one_relationship(
        "ProjectRoleAssociationDB", back_populates="forms"
    )

    __table_args__ = (
        Index("ix_project_users_project_role_id", "project_role_id"),
        UniqueConstraint("user_id", "project_role_id", name="uq_project_users"),
    )
