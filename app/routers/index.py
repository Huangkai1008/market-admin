from fastapi import APIRouter

router = APIRouter()


@router.get('/ping')
async def ping():
    return dict(name='market-admin', using='fastapi',
                description='market-admin is a Market background management system with fastapi')
