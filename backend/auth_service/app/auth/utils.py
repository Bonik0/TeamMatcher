from fastapi import Request


async def login_key_executor(request: Request) -> list[str]:
    try:
        body = await request.json()
    except Exception:
        return []
    email = body.get("email")
    return [request.url.path, "email", email] if email is not None else []
