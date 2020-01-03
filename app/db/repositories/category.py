from typing import Tuple, List

from fastapi.encoders import jsonable_encoder

from app.db.category import ProductCategory, ProductCategorySpec
from app.db.repositories.base import BaseRepository
from app.models.category import (
    CategoryCreate,
    CategoryUpdate,
    CategorySpecCreate,
    CategorySpecUpdate,
)


class CategoryRepository(BaseRepository):
    """
    商品分类Repo
    """

    async def get_categories(
        self, page: int, size: int, *, parent_id: int
    ) -> Tuple[List[ProductCategory], int]:
        """获取商品分类"""
        conditions = dict()

        if parent_id is not None:
            conditions['parent_id'] = parent_id

        total = await ProductCategory.filter(**conditions).count()

        queryset = await self._and_pagination(
            ProductCategory.filter(**conditions), page, size
        )

        return queryset, total

    @staticmethod
    async def get_category(cat_id: int) -> ProductCategory:
        """获取单个商品分类"""
        category = await ProductCategory.filter(id=cat_id).first()
        return category

    @staticmethod
    async def create_category(
        category_create: CategoryCreate, cat_level: int
    ) -> ProductCategory:
        """创建商品分类"""
        category_create_data = jsonable_encoder(category_create)
        category = ProductCategory(**category_create_data, cat_level=cat_level)
        await category.save()
        return category

    async def update_category(
        self, cat_id: int, category_update: CategoryUpdate
    ) -> ProductCategory:
        """修改商品分类"""
        category_update_data = jsonable_encoder(category_update)
        await ProductCategory.get(id=cat_id).update(**category_update_data)
        category = await self.get_category(cat_id)
        return category

    @staticmethod
    async def get_category_specs(cat_id: int) -> List[ProductCategorySpec]:
        """获取规格信息"""
        conditions = dict()

        conditions['cat_id'] = cat_id

        queryset = await ProductCategorySpec.filter(**conditions).all()
        return queryset

    @staticmethod
    async def get_category_spec(
        *, cat_id: int = None, spec_id: int = None
    ) -> ProductCategorySpec:
        """获取单个规格信息"""
        conditions = dict()

        if cat_id:
            conditions['cat_id'] = cat_id
        if spec_id:
            conditions['id'] = spec_id

        spec = await ProductCategorySpec.filter(**conditions).first()
        return spec

    @staticmethod
    async def bulk_create_category_specs(
        cat_id: int, spec_creates: List[CategorySpecCreate]
    ):
        """批量创建规格信息"""
        spec_creates_data = jsonable_encoder(spec_creates)

        await ProductCategorySpec.bulk_create(
            [
                ProductCategorySpec(**spec_create_data, cat_id=cat_id)
                for spec_create_data in spec_creates_data
            ]
        )
        return

    async def update_category_spec(
        self, spec_id: int, spec_update: CategorySpecUpdate
    ) -> ProductCategorySpec:
        """修改商品分类规格"""
        spec_update_data = jsonable_encoder(spec_update)
        await ProductCategorySpec.get(id=spec_id).update(**spec_update_data)
        spec = await self.get_category_spec(spec_id=spec_id)
        return spec
