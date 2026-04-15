"""
com_mock/agents/__init__.py
All five specialized agents exported from one place.
"""

from com_mock.agents.doc_fetcher import run_doc_fetcher
from com_mock.agents.schema_extractor import run_schema_extractor_batch
from com_mock.agents.relationship_mapper import run_relationship_mapper
from com_mock.agents.data_synthesizer import run_data_synthesizer
from com_mock.agents.validator import run_validator

__all__ = [
    "run_doc_fetcher",
    "run_schema_extractor_batch",
    "run_relationship_mapper",
    "run_data_synthesizer",
    "run_validator",
]
