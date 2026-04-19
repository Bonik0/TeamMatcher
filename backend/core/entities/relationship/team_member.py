from core.entities.base.team_member import TeamMember
from core.entities.relationship.project_role import ProjectRoleWithRole
from core.entities.base.user import User



class TeamMemberWithUser(TeamMember):
    user: User


class TeamMemberWithRoleAndUser(TeamMemberWithUser):
    project_role: ProjectRoleWithRole
    
    
