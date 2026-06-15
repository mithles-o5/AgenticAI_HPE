"""Task Planner for decomposing compound user instructions."""

from __future__ import annotations
import uuid
from typing import List, Dict, Any

class TaskStatus:
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class Task:
    def __init__(self, action: str, category: str, identifier: str, params: Dict[str, Any] = None, dependencies: List[str] = None):
        self.task_id = str(uuid.uuid4())
        self.action = action.upper()
        self.category = category
        self.identifier = identifier
        self.params = params or {}
        self.dependencies = dependencies or []
        self.status = TaskStatus.PENDING

class TaskPlanner:
    @staticmethod
    def decompose_instruction(instruction: str) -> List[Task]:
        """Decompose compound natural language instructions into sequential Task objects."""
        if not instruction or not isinstance(instruction, str):
            return []

        # Split by typical command conjunctions in order of precedence
        import re
        import sys
        import os
        
        # Add resource_resolver to sys.path locally to import QueryAgent
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        resolver_dir = os.path.join(parent_dir, "resource_resolver")
        if resolver_dir not in sys.path:
            sys.path.insert(0, resolver_dir)
            
        from query_agent import QueryAgent

        conjunctions = [r"\band then\b", r"\bthen\b", r"\band\b"]
        
        clauses = [instruction]
        for conj in conjunctions:
            new_clauses = []
            for clause in clauses:
                split_parts = re.split(conj, clause, flags=re.IGNORECASE)
                new_clauses.extend([part.strip() for part in split_parts if part.strip()])
            clauses = new_clauses

        tasks = []
        previous_task_id = None
        for clause in clauses:
            parsed = QueryAgent.parse_query(clause)
            if not parsed.get("identifier"):
                continue
                
            dependencies = [previous_task_id] if previous_task_id else []
            task = Task(
                action=parsed.get("action", "STATUS"),
                category=parsed.get("category", "Operational"),
                identifier=parsed.get("identifier"),
                dependencies=dependencies
            )
            tasks.append(task)
            previous_task_id = task.task_id
            
        return tasks
