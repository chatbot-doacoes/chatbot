from src.repositories.institution_repository import InstitutionRepository
from src.models.institution import InstitutionModel
from src.api.internal.payloads.institutions import RegisterInstitution, UpdateInstitution

class InstitutionService:
    def __init__(self, repository: InstitutionRepository):
        self.repository = repository

    def register_institution(self, payload: RegisterInstitution) -> bool:
        institution = InstitutionModel(
            institution_name=payload.institution_name,
            key_hash=payload.key_hash,
            is_active=True,
        )
        return self.repository.register(institution)

    def get_all_institutions(self) -> list[InstitutionModel]:
        return self.repository.get_all()

    def update_institution(self, institution_id: str, update_data: dict) -> InstitutionModel:
        return self.repository.update(institution_id, update_data)
        
    def is_institution_registered(self, key_hash: str) -> bool:
        return self.repository.is_registered(key_hash)
