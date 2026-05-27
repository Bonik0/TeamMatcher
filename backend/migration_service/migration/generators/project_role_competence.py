import pandas as pd








def generate_project_role_competence(
    role_to_competence_path: str, 
    project_role_path: str,
    path: str
) -> None:
    role_to_competence = pd.read_csv(role_to_competence_path)
    project_roles = pd.read_csv(project_role_path)
    
    project_role_competence = []
    
    for project_role in project_roles.values:
        
        id, _, role_id, _, _ = project_role
        for competence in role_to_competence[role_to_competence["role_id"] == role_id].values:
            _,competence_id, importance = competence
            
            project_role_competence.append(
                (id, competence_id, importance)
            )
    pd.DataFrame(
        project_role_competence,
        columns=["project_role_id", "competence_id", "importance"]
    ).to_csv(
        path, index=False
    )
            
            
generate_project_role_competence(
    "/home/bonik/giploma/backend/migration_service/migration/synthetic_data/role_to_competence.csv",
    "/home/bonik/giploma/backend/migration_service/migration/synthetic_data/project_role.csv",
    "/home/bonik/giploma/backend/migration_service/migration/synthetic_data/project_role_competence.csv"
)
            
