from fastapi import HTTPException


async def _get_or_404(result, detail: str = "Not found"):
    """Вспомогательная функция: проверяет результат и выбрасывает 404 при отсутствии."""
    if not result:
        raise HTTPException(status_code=404, detail=detail)
    return result
