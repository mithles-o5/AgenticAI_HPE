"""Vendor Synthesizer for batching and optimizing resolved tasks."""

from __future__ import annotations
from typing import List, Dict, Any

class SynthesizedBatch:
    def __init__(self, management_source: str, source_host: str):
        self.management_source = management_source
        self.source_host = source_host
        self.tasks: List[Any] = []
        self.device_ids: List[str] = []

    def can_bulk_execute(self) -> bool:
        return len(self.device_ids) > 1

class VendorSynthesizer:
    @staticmethod
    def synthesize_batches(resolved_tasks: List[tuple[Any, Any]]) -> Dict[str, SynthesizedBatch]:
        """Group and optimize tasks by management source and host IP."""
        batches: Dict[str, SynthesizedBatch] = {}
        for task, route in resolved_tasks:
            if not route or not route.management_source or not route.device:
                continue
            
            key = f"{route.management_source}@{route.device.source_host}"
            if key not in batches:
                batches[key] = SynthesizedBatch(
                    management_source=route.management_source,
                    source_host=route.device.source_host
                )
            
            # Check for duplicate action + identifier in this batch
            is_duplicate = False
            for t in batches[key].tasks:
                if t.identifier == task.identifier and t.action == task.action:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                batches[key].tasks.append(task)
                device_id = route.device.id
                if device_id not in batches[key].device_ids:
                    batches[key].device_ids.append(device_id)
                    
        return batches
