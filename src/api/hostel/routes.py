from fastapi import APIRouter

#Define router
router = APIRouter(tags=["Hostel services"])

@router.get("/")
def root():
    return "Hello"