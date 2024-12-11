import hashlib


async def get_plain_hash(plain: str | bytes) -> str:
    encoded = plain.encode("utf-8")
    result = hashlib.sha256(encoded)
    return result.hexdigest()
