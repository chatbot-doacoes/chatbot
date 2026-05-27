from src.api.base_response import BaseResponse
from src.models.institution import InstitutionModel


class GetAllInstitutionsResponse(BaseResponse):
    institutions: list[InstitutionModel]

class UpdateInstitutionResponse(BaseResponse):
    institution: InstitutionModel

class RegisterInstitutionResponse(BaseResponse):
    institution: InstitutionModel
    api_key: str