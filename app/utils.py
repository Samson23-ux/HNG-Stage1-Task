async def is_digit(val: str) -> bool:
    try:
        float(val)
        return True
    except ValueError:
        return False
