from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field
from .base import PyObjectId, IdentifiableSchema

# Sub-models with preserved IDs
class CarePlan(IdentifiableSchema):
    Id: str  # Required ID
    START: str
    STOP: Optional[str] = None
    PATIENT: str
    ENCOUNTER: str
    CODE: str
    DESCRIPTION: str
    REASONCODE: Optional[str] = None
    REASONDESCRIPTION: Optional[str] = None

class Allergy(IdentifiableSchema):
    Id: Optional[str] = None  # Optional ID if present in data
    START: str
    STOP: Optional[str] = None
    PATIENT: str
    ENCOUNTER: str
    CODE: str
    DESCRIPTION: str

class Procedure(IdentifiableSchema):
    Id: Optional[str] = None  # Preserve if exists
    DATE: str
    PATIENT: str
    ENCOUNTER: str
    CODE: str
    DESCRIPTION: str
    BASE_COST: str
    REASONCODE: Optional[str] = None
    REASONDESCRIPTION: Optional[str] = None

class Observation(IdentifiableSchema):
    Id: Optional[str] = None
    DATE: str
    PATIENT: str
    ENCOUNTER: str
    CODE: str
    DESCRIPTION: str
    VALUE: str
    UNITS: str
    TYPE: str

class Medication(IdentifiableSchema):
    Id: Optional[str] = None
    START: str
    STOP: Optional[str] = None
    PATIENT: str
    PAYER: str
    ENCOUNTER: str
    CODE: str
    DESCRIPTION: str
    BASE_COST: str
    PAYER_COVERAGE: str
    DISPENSES: str
    TOTALCOST: str
    REASONCODE: Optional[str] = None
    REASONDESCRIPTION: Optional[str] = None

class Condition(IdentifiableSchema):
    Id: Optional[str] = None
    START: str
    STOP: Optional[str] = None
    PATIENT: str
    ENCOUNTER: str
    CODE: str
    DESCRIPTION: str

class Encounter(IdentifiableSchema):
    Id: str
    START: str
    STOP: str
    PATIENT: str
    ORGANIZATION: str
    PROVIDER: str
    PAYER: str
    ENCOUNTERCLASS: str
    CODE: str
    DESCRIPTION: str
    BASE_ENCOUNTER_COST: str
    TOTAL_CLAIM_COST: str
    PAYER_COVERAGE: str
    REASONCODE: Optional[str] = None
    REASONDESCRIPTION: Optional[str] = None

class Immunization(IdentifiableSchema):
    Id: Optional[str] = None
    DATE: str
    PATIENT: str
    ENCOUNTER: str
    CODE: str
    DESCRIPTION: str
    BASE_COST: str

class ImagingStudy(IdentifiableSchema):
    Id: str
    DATE: str
    PATIENT: str
    ENCOUNTER: str
    BODYSITE_CODE: str
    BODYSITE_DESCRIPTION: str
    MODALITY_CODE: str
    MODALITY_DESCRIPTION: str
    SOP_CODE: str
    SOP_DESCRIPTION: str

class PayerTransition(IdentifiableSchema):
    Id: Optional[str] = None
    PATIENT: str
    START_YEAR: str
    END_YEAR: str
    PAYER: str
    OWNERSHIP: str
    
class Device(IdentifiableSchema):
    START: str
    STOP: Optional[str] = None
    PATIENT: str
    ENCOUNTER: str
    CODE: str
    DESCRIPTION: str
    UDI: str

class PatientDetails(IdentifiableSchema):
    Id: Optional[str] = None
    BIRTHDATE: Optional[str] = None
    DEATHDATE: Optional[str] = None
    SSN: Optional[str] = None
    DRIVERS: Optional[str] = None
    PASSPORT: Optional[str] = None
    PREFIX: Optional[str] = None
    FIRST: Optional[str] = None
    LAST: Optional[str] = None
    SUFFIX: Optional[str] = None
    MAIDEN: Optional[str] = None
    MARITAL: Optional[str] = None
    RACE: Optional[str] = None
    ETHNICITY: Optional[str] = None
    GENDER: Optional[str] = None
    BIRTHPLACE: Optional[str] = None
    ADDRESS: Optional[str] = None
    CITY: Optional[str] = None
    STATE: Optional[str] = None
    COUNTY: Optional[str] = None
    ZIP: Optional[str] = None
    LAT: Optional[str] = None
    LON: Optional[str] = None
    HEALTHCARE_EXPENSES: Optional[str] = None
    HEALTHCARE_COVERAGE: Optional[str] = None

class PatientBase(BaseModel):
    id: Optional[PyObjectId] = Field(None, alias="_id")
    patient_details: PatientDetails
    careplans: List[CarePlan] = []
    allergies: List[Allergy] = []
    procedures: List[Procedure] = []
    observations: List[Observation] = []
    medications: List[Medication] = []
    conditions: List[Condition] = []
    encounters: List[Encounter] = []
    immunizations: List[Immunization] = []
    imaging_studies: List[ImagingStudy] = []
    devices: List[Device] = []

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        populate_by_name=True
    )