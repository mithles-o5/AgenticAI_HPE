"""
api_mocker/models.py
Pydantic data models for discovered API specifications.
"""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


class APIParameter(BaseModel):
    """A single parameter for an API endpoint."""

    name: str
    location: str = Field(
        default="query",
        description="Where the parameter goes: path, query, header, body",
    )
    param_type: str = Field(default="string", description="Data type")
    required: bool = False
    description: str = ""


class APIEndpoint(BaseModel):
    """A single REST API endpoint."""

    method: str = Field(description="HTTP method: GET, POST, PUT, DELETE, PATCH")
    path: str = Field(description="URL path, e.g. /rest/server-hardware")
    summary: str = ""
    description: str = ""
    category: str = ""
    subcategory: str = ""
    parameters: list[APIParameter] = Field(default_factory=list)
    request_body: Optional[dict[str, Any]] = None
    response_example: Optional[Any] = None


class APISection(BaseModel):
    """A section of the API documentation (e.g., Server Hardware)."""

    name: str
    url: str = ""
    category_group: str = ""
    endpoints: list[APIEndpoint] = Field(default_factory=list)


class DiscoveredAPI(BaseModel):
    """Complete discovered API specification."""

    title: str = "HPE OneView API"
    version: str = "4600"
    base_url: str = "/rest"
    source_url: str = ""
    sections: list[APISection] = Field(default_factory=list)

    @property
    def all_endpoints(self) -> list[APIEndpoint]:
        return [ep for s in self.sections for ep in s.endpoints]

    @property
    def endpoint_count(self) -> int:
        return sum(len(s.endpoints) for s in self.sections)
