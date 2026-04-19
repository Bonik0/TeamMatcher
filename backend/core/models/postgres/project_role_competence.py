from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Index, Integer
from core.models.postgres.column_types import (
    created_at_type,
    updated_at_type,
    cascade_foreign_key,
    many_to_one_relationship,
)
from core.models.postgres.base import Base


class ProjectRoleCompetenceAssociationDB(Base):
    __tablename__ = "role_competences"

    project_role_id: Mapped[int] = mapped_column(
        Integer, cascade_foreign_key("project_roles.id"), primary_key=True
    )
    competence_id: Mapped[int] = mapped_column(
        Integer, cascade_foreign_key("competences.id"), primary_key=True
    )
    importance: Mapped[int] = mapped_column(Integer, nullable=False, default=1.0)
    created_at: Mapped[created_at_type]
    updated_at: Mapped[updated_at_type]

    project_role = many_to_one_relationship(
        "ProjectRoleAssociationDB", back_populates="competences"
    )
    competence = many_to_one_relationship(
        "CompetenceDB", back_populates="project_roles"
    )

    __table_args__ = (Index("ix_role_competences_competence_id", "competence_id"),)
