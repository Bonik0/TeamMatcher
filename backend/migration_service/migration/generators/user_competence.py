import pandas as pd
import random



def generate_user_to_competence(
    user_to_role_path: str,
    role_to_competence_path: str,
    path: str
) -> None:
    user_to_role = pd.read_csv(user_to_role_path)
    role_to_competence = pd.read_csv(role_to_competence_path)
    
    user_competence = []
    
    for user_id, role_id in user_to_role.values:
        
        for _, competence_id, importance in role_to_competence[role_to_competence["role_id"] == role_id].values:
            level = random.randint(1, 3)
            user_competence.append(
                (user_id, competence_id, level)
            )
    
    pd.DataFrame(
        user_competence,
        columns=["user_id", "competence_id", "level"]
    ).drop_duplicates(["user_id", "competence_id"]).to_csv(path, index=False)
    

generate_user_to_competence(
    "/home/bonik/giploma/backend/migration_service/migration/synthetic_data/user_to_roles.csv",
    "/home/bonik/giploma/backend/migration_service/migration/synthetic_data/role_to_competence.csv",
    "/home/bonik/giploma/backend/migration_service/migration/synthetic_data/user_competence.csv"
)