from fastapi import APIRouter


router = APIRouter()


@router.get('/ping', summary='测试联通性')
async def ping():
    return dict(
        name='market-admin',
        using='fastapi',
        description='market-admin is a Market background management system with fastapi',
    )
