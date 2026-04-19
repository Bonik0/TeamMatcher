from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    Text,
    Index,
    Integer,
    UniqueConstraint,
)
from core.models.postgres.column_types import (
    pk_key_identity_column,
    created_at_type,
    updated_at_type,
    one_to_many_relationship,
    cascade_foreign_key,
    many_to_one_relationship,
)
from core.models.postgres.base import Base


class ProjectRoleAssociationDB(Base):
    __tablename__ = "project_roles"

    id: Mapped[int] = pk_key_identity_column()

    project_id: Mapped[int] = mapped_column(Integer, cascade_foreign_key("projects.id"))
    role_id: Mapped[int] = mapped_column(Integer, cascade_foreign_key("roles.id"))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    quantity_per_team: Mapped[int] = mapped_column(nullable=False, default=1)
    created_at: Mapped[created_at_type]
    updated_at: Mapped[updated_at_type]

    project = many_to_one_relationship("ProjectDB", back_populates="roles")
    role = many_to_one_relationship("RoleDB", back_populates="projects")

    competences = one_to_many_relationship(
        "ProjectRoleCompetenceAssociationDB", back_populates="project_role"
    )
    forms = one_to_many_relationship(
        "UserProjectRoleAssociationDB", back_populates="project_role"
    )
    team_members = one_to_many_relationship("TeamMemberDB", back_populates="project_role")

    __table_args__ = (
        UniqueConstraint("project_id", "role_id", name="uq_project_role"),
        Index("ix_projects_roles_role_id", "role_id"),
    )
