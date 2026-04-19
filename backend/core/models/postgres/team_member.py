from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Float, ForeignKey, UniqueConstraint, Index
from core.models.postgres.column_types import (
    pk_key_identity_column,
    created_at_type,
    updated_at_type,
    many_to_one_relationship,
    cascade_foreign_key
)
from core.models.postgres.base import Base

class TeamMemberDB(Base):
    __tablename__ = "team_members"

    id: Mapped[int] = pk_key_identity_column()
    team_id: Mapped[int] = mapped_column(Integer, cascade_foreign_key("teams.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, cascade_foreign_key("users.id"), nullable=False)
    project_role_id: Mapped[int] = mapped_column(Integer, cascade_foreign_key("project_roles.id"), nullable=False)
    competence_match: Mapped[float]
    role_score: Mapped[float]
    created_at: Mapped[created_at_type]
    updated_at: Mapped[updated_at_type]

    team = many_to_one_relationship("TeamDB", back_populates="members")
    user = many_to_one_relationship("UserDB", back_populates="team_memberships")
    project_role = many_to_one_relationship("ProjectRoleAssociationDB", back_populates="team_members")

    __table_args__ = (
        UniqueConstraint("team_id", "user_id", "project_role_id", name="uq_team_member_role"),
        Index("ix_team_members_user_id", "user_id")
    )