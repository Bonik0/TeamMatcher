from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Index, Integer, UniqueConstraint
from core.models.postgres.column_types import (
    created_at_type,
    updated_at_type,
    cascade_foreign_key,
    many_to_one_relationship,
)
from core.models.postgres.base import Base


class UserCompetenceAssociationDB(Base):
    __tablename__ = "user_competences"

    user_id: Mapped[int] = mapped_column(
        Integer, cascade_foreign_key("users.id"), primary_key=True
    )
    competence_id: Mapped[int] = mapped_column(
        Integer, cascade_foreign_key("competences.id"), primary_key=True
    )
    level: Mapped[int]
    created_at: Mapped[created_at_type]
    updated_at: Mapped[updated_at_type]

    user = many_to_one_relationship("UserDB", back_populates="competences")
    competence = many_to_one_relationship(
        "CompetenceDB", back_populates="user_competences"
    )

    __table_args__ = (
        Index("ix_user_competences_competence_id", "competence_id"),
        UniqueConstraint("user_id", "competence_id", name="uq_user_competences"),
    )
