from sqlalchemy.orm import Mapped
from sqlalchemy import Index
from core.models.postgres.column_types import (
    unique_column,
    pk_key_identity_column,
    created_at_type,
    updated_at_type,
    one_to_many_relationship,
)
from core.models.postgres.base import Base


class RoleDB(Base):
    __tablename__ = "roles"

    id: Mapped[int] = pk_key_identity_column()
    name: Mapped[str] = unique_column(nullable=False)
    created_at: Mapped[created_at_type]
    updated_at: Mapped[updated_at_type]

    projects = one_to_many_relationship(
        "ProjectRoleAssociationDB", back_populates="role"
    )

    __table_args__ = (
        Index(
            "ix_roles_name_trgm",
            "name",
            postgresql_using="gin",
            postgresql_ops={"name": "gin_trgm_ops"},
        ),
    )
