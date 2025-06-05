from bson.errors import InvalidId
from typing import List
from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from ..Database.connection import patients_collection
from ..schemas.patient import Patient, PatientCreate

router = APIRouter(prefix="/patients", tags=["patients"])


# Create patient
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Patient)
async def create_patient(patient: PatientCreate):
    if patient.patient_details.Id:
        # Check if a patient with this ID already exists
        existing = await patients_collection.find_one({"patient_details.Id": patient.patient_details.Id})
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Patient with ID {patient.patient_details.Id} already exists"
            )
    
    # Prepare data for insertion
    patient_dict = patient.model_dump()
    result = await patients_collection.insert_one(patient_dict)
    new_patient = await patients_collection.find_one({"_id": result.inserted_id})
    return Patient(**new_patient)


# Get patient by ID
@router.get("/{patient_id}", response_model=Patient)
async def get_patient(patient_id: str):
    try:
        # Try to find the patient by ObjectId
        obj_id = ObjectId(patient_id)
        patient = await patients_collection.find_one({"_id": obj_id})
    except InvalidId:
        # If not an ObjectId, try to find by patient_details.Id
        patient = await patients_collection.find_one({"patient_details.Id": patient_id})
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Return the patient in the correct Pydantic model format
    return Patient(**patient)


# Update patient by ID
@router.put("/{patient_id}", response_model=Patient)
async def update_patient(patient_id: str, patient_data: PatientCreate):
    try:
        # Try to find the patient by ObjectId
        obj_id = ObjectId(patient_id)
        existing = await patients_collection.find_one({"_id": obj_id})
        if existing:
            patient_dict = patient_data.model_dump()
            patient_dict["_id"] = existing["_id"]
            await patients_collection.replace_one({"_id": obj_id}, patient_dict)
            return Patient(**patient_dict)
    except InvalidId:
        pass
    
    # If ObjectId fails, try by patient_details.Id
    existing = await patients_collection.find_one({"patient_details.Id": patient_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient_dict = patient_data.model_dump()
    patient_dict["_id"] = existing["_id"]
    await patients_collection.replace_one(
        {"patient_details.Id": patient_id},
        patient_dict
    )
    return Patient(**patient_dict)


# Delete patient by ID
@router.delete("/{patient_id}")
async def delete_patient(patient_id: str):
    try:
        # Try to delete by ObjectId
        obj_id = ObjectId(patient_id)
        result = await patients_collection.delete_one({"_id": obj_id})
        if result.deleted_count > 0:
            return {"message": "Patient deleted successfully"}
    except InvalidId:
        pass
    
    # If ObjectId fails, try by patient_details.Id
    result = await patients_collection.delete_one({"patient_details.Id": patient_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deleted successfully"}


# Get all patients with pagination
@router.get("/", response_model=List[Patient])
async def get_all_patients(skip: int = 0, limit: int = 100):
    # Fetch patients with skip and limit (pagination)
    patients = await patients_collection.find().skip(skip).limit(limit).to_list(length=None)
    return [Patient(**patient) for patient in patients]
