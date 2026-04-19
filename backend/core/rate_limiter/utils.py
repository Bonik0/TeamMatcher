from fastapi import Request


async def extract_ip(request: Request) -> list[str]:
    forwarded = request.headers.get("X-Forwarded-For")
    ip = forwarded.split(",")[0].strip() if forwarded else request.client.host
    return ["ip", ip]
