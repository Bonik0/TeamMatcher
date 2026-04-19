from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey
from core.models.postgres.column_types import (
    pk_key_identity_column,
    created_at_type,
    updated_at_type,
    many_to_one_relationship,
    one_to_many_relationship,
    cascade_foreign_key
)
from core.models.postgres.base import Base

class TeamDB(Base):
    __tablename__ = "teams"

    id: Mapped[int] = pk_key_identity_column()
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    project_id: Mapped[int] = mapped_column(Integer, cascade_foreign_key("projects.id"), nullable=False)
    created_at: Mapped[created_at_type]
    updated_at: Mapped[updated_at_type]

    project = many_to_one_relationship("ProjectDB", back_populates="teams")
    members = one_to_many_relationship("TeamMemberDB", back_populates="team")