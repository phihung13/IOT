import auth
from fastapi import APIRouter, Depends

router = APIRouter(dependencies=[Depends(auth.validate_api_key)])


@router.get("/my_endpoint")
async def my_endpoint():
    return {"message": "success"}