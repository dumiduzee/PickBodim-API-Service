from fastapi import APIRouter

#Define router
router = APIRouter(tags=["User services"])

@router.get("/")
def root():
    return "Hello"