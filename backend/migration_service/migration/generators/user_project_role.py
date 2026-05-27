import pandas as pd





def generate_user_project_role(
    user_to_role_path: str,
    project_role_path: str,
    path: str
) -> None:
    user_to_role = pd.read_csv(user_to_role_path)
    project_role = pd.read_csv(project_role_path)
    
    user_project_role = []
    user_to_project = {
        user_id: {
            project_id: 1
            for project_id in set(project_role["project_id"].values)
        }
        for user_id in user_to_role["user_id"].values
    }
    
    for user_id, role_id in user_to_role.values:
        
        for project_role_id, project_id in project_role[project_role["role_id"] == role_id][["id", "project_id"]].values:
            user_project_role.append(
                (user_id, project_role_id, user_to_project[user_id][project_id])
            )
            user_to_project[user_id][project_id] += 1
            
    pd.DataFrame(
        user_project_role,
        columns=["user_id", "project_role_id", "priority"]
    ).to_csv(
        path, index=False
    )
    
generate_user_project_role(
    "/home/bonik/giploma/backend/migration_service/migration/synthetic_data/user_to_roles.csv",
    "/home/bonik/giploma/backend/migration_service/migration/synthetic_data/project_role.csv",
    "/home/bonik/giploma/backend/migration_service/migration/synthetic_data/user_project_role.csv"
)