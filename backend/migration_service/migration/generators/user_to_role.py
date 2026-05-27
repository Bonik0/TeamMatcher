import pandas as pd
import random







def generate_user_to_role(
    users_path: str,
    roles_path: str,
    path: str,
) -> None:
    users = pd.read_csv(users_path)
    roles = pd.read_csv(roles_path)
    
    user_to_role = []
    
    for user_id, role in users[["id", "role"]].values:
        if role != "user":
            continue
        k = random.randint(1, 4)
        random_roles = random.choices(roles["id"].values, k=k)
        for role_id in random_roles:
            user_to_role.append(
                (user_id, role_id)
            )
    pd.DataFrame(
        user_to_role,
        columns=["user_id", "role_id"],
    ).to_csv(
        path,
        index=False
    )


generate_user_to_role(
    "/home/bonik/giploma/backend/migration_service/migration/synthetic_data/users.csv",
    "/home/bonik/giploma/backend/migration_service/migration/synthetic_data/roles.csv",
    "/home/bonik/giploma/backend/migration_service/migration/synthetic_data/user_to_roles.csv"
)

    