from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, DateTime, Index, Integer
from core.models.postgres.column_types import (
    pk_key_identity_column,
    created_at_type,
    updated_at_type,
    one_to_many_relationship,
    cascade_foreign_key,
    many_to_one_relationship,
)
from core.models.postgres.base import Base
from datetime import datetime


class ProjectDB(Base):
    __tablename__ = "projects"

    id: Mapped[int] = pk_key_identity_column()
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    organizer_id: Mapped[int] = mapped_column(Integer, cascade_foreign_key("users.id"))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[created_at_type]
    updated_at: Mapped[updated_at_type]

    organizer = many_to_one_relationship("UserDB", back_populates="projects")
    roles = one_to_many_relationship(
        "ProjectRoleAssociationDB", back_populates="project"
    )
    teams = one_to_many_relationship("TeamDB", back_populates="project")

    __table_args__ = (
        Index("ix_projects_status", "status"),
        Index("ix_projects_start_time", "start_time"),
        Index("ix_projects_organizer_id", "organizer_id"),
        Index(
            "ix_projects_name_trgm",
            "name",
            postgresql_using="gin",
            postgresql_ops={"name": "gin_trgm_ops"},
        ),
        Index(
            "ix_projects_description_trgm",
            "description",
            postgresql_using="gin",
            postgresql_ops={"description": "gin_trgm_ops"},
        ),
    )
