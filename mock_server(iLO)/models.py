from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class GenericPayload(BaseModel):
    Id: Optional[str] = None
    Name: Optional[str] = None
    Description: Optional[str] = None
    Status: Optional[Dict[str, Any]] = None
    Properties: Optional[Dict[str, Any]] = None
