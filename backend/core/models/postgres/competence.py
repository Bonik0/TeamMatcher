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


class CompetenceDB(Base):
    __tablename__ = "competences"

    id: Mapped[int] = pk_key_identity_column()
    name: Mapped[str] = unique_column(nullable=False)
    created_at: Mapped[created_at_type]
    updated_at: Mapped[updated_at_type]

    project_roles = one_to_many_relationship(
        "ProjectRoleCompetenceAssociationDB", back_populates="competence"
    )
    user_competences = one_to_many_relationship(
        "UserCompetenceAssociationDB", back_populates="competence"
    )

    __table_args__ = (
        Index(
            "ix_competences_name_trgm",
            "name",
            postgresql_using="gin",
            postgresql_ops={"name": "gin_trgm_ops"},
        ),
    )
