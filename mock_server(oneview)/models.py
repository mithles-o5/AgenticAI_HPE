from pydantic import BaseModel
from typing import Any

class PostRestCertificatesClientRabbitmqRequest(BaseModel):
    type: str = None
    commonName: str = None

class GetRestCertificatesClientRabbitmqKeypairDefaultRequest(BaseModel):
    type: str = None
    commonName: str = None

class GetRestCertificatesCaRequest(BaseModel):
    type: str = None
    commonName: str = None

