from fastapi import Path, HTTPException, Depends
from starlette.status import HTTP_404_NOT_FOUND

from app.db.repositories.category import CategoryRepository


async def get_category_by_id(
    cat_id: int = Path(..., ge=1, description='商品分类id'),
    category_repo: CategoryRepository = Depends(),
):
    category = await category_repo.get_category(cat_id)
    if not category:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    return category


async def get_category_spec_by_union_id(
    cat_id: int = Path(..., ge=1, description='商品分类id'),
    spec_id=Path(..., ge=1, description='规格id'),
    category_repo: CategoryRepository = Depends(),
):
    category_spec = await category_repo.get_category_spec(
        cat_id=cat_id, spec_id=spec_id
    )
    if not category_spec:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    return category_spec
