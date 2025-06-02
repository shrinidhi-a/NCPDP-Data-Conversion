from pydantic import BaseModel

class MTMRecord(BaseModel):
    RECORD_TYPE: str
    TRANSACTION_ID: str
    DATE: str
    PHARMACY_NCPDP_ID: str
    PHARMACIST_NPI: str
    PATIENT_ID: str
    PATIENT_NAME: str
    DOB: str
    GENDER: str
    PAYER_ID: str
    PLAN_NAME: str
    INTERVENTION_TYPE: str
    MTM_SERVICE_CODE: str
    START_DATE: str
    END_DATE: str
    OUTCOME: str
    RECOMMENDATIONS: str
    PRESCRIBER_CONTACTED: str
    PRESCRIBER_NPI: str
    PRESCRIBER_RESPONSE: str
    FOLLOW_UP_DATE: str
    NOTES: str
