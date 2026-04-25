from core.entities.base.team import Team
from core.entities.relationship.team_member import (
    TeamMemberWithRoleAndUser,
    TeamMemberWithUser,
)
from core.entities.base.project import Project


class TeamWithMembersAndProject(Team):
    members: list[TeamMemberWithRoleAndUser]
    project: Project


class TeamWithMembers(Team):
    members: list[TeamMemberWithUser]
