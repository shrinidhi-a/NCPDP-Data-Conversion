
from fastapi import APIRouter, HTTPException
from typing import TypeVar, Type
from ..schemas.patient import CarePlan, Condition, Allergy, Device, Encounter, ImagingStudy, Immunization, Medication, Observation, PayerTransition, Procedure
from .patients import get_patient

router = APIRouter(prefix="/patients/{patient_id}", tags=["nested resources"])

T = TypeVar('T')

def create_resource_endpoint(resource_name: str, model: Type[T]):
    async def endpoint(patient_id: str, resource_id: str):
        patient = await get_patient(patient_id)
        collection = getattr(patient, resource_name)
        
        for item in collection:
            if item.Id == resource_id:
                return item
        
        raise HTTPException(
            status_code=404, 
            detail=f"{resource_name[:-1].capitalize()} not found"
        )
    return endpoint

resources = [
    ('careplans', CarePlan),
    ('allergies', Allergy),
    ('procedures', Procedure),
    ('observations', Observation),
    ('medications', Medication),
    ('conditions', Condition),
    ('encounters', Encounter),
    ('immunizations', Immunization),
    ('imaging_studies', ImagingStudy),
    ('payer_transitions', PayerTransition),
    ('devices', Device)  # Assuming Device is similar to Procedure
]

for path, model in resources:
    router.add_api_route(
        path=f"/{path}/{{resource_id}}",
        endpoint=create_resource_endpoint(path, model),
        methods=["GET"],
        response_model=model,
        name=f"Get {path[:-1]}"
    )