from fastapi import APIRouter

router = APIRouter()          # ← this line is required

@router.get("/")
def read_items():
    return [{"name": "Item 1"}]