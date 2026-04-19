from core.repositories.team import TeamRepository



def get_team_repository() -> TeamRepository:
    return TeamRepository()