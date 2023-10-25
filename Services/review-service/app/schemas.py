from pydantic import BaseModel, Field, Base64Bytes
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue
from typing import Optional, List, Any, Annotated

from ..database.models import ProductStatusEnum

from uuid import UUID

from bson import ObjectId


class ObjectIdPydanticAnnotation:
    @classmethod
    def validate_object_id(cls, v: Any, handler) -> str:
        if isinstance(v, ObjectId):
            return v

        s = handler(v)
        if ObjectId.is_valid(s):
            return str(s)
        else:
            raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, _handler) -> core_schema.CoreSchema:
        assert source_type is str
        return core_schema.no_info_wrap_validator_function(
            cls.validate_object_id,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema, handler) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


class ProductBase(BaseModel):
    product_name: str = Field(title="Product name")
    description: Optional[str] = Field(title="Product description", default="Description")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    status: ProductStatusEnum = Field(title="Product status")


class Product(ProductBase):
    id: Annotated[str, ObjectIdPydanticAnnotation]
    status: ProductStatusEnum = Field(title="Product status")
    images: List[UUID] = Field(title="Product images", default=[])



# Pydantic-модель для отзыва
class ReviewBase(BaseModel):
    title: str
    description: str

# Pydantic-модель для создания отзыва
class ReviewCreate(ReviewBase):
    pass

# Pydantic-модель для обновления отзыва
class ReviewUpdate(ReviewBase):
    pass

# Pydantic-модель для ответа с отзывом
class ReviewResponse(ReviewBase):
    id: str
