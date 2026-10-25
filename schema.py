from pydantic import BaseModel, ValidationError
# from errors import HttpError

class CreateAd(BaseModel):
    header: str
    ad_body: str
    owner: str

class UpdateAd(BaseModel):
    header: str | None = None
    ad_body: str | None = None

# def validate(json_data: dict, schema_cls: type[CreateAd]) -> dict:
#     try:
#         return schema_cls(**json_data).model_dump()
#     except ValidationError as err:
#         errors = err.errors()
#         for e in errors:
#             e.pop('ctx', None)
#         raise HttpError(errors, 400)
