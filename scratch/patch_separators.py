import sys
import re

with open(r'c:\AgenticAI_HPE\resource_resolver\query_agent.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the resource_type extraction logic:
old_r_type = '''        # 2. Extract resource type ONLY (no device type inference)
        # We do this from the original query string (q) before we start destroying it.
        resource_type = ""
        words = q.lower().split()
        for r_type, aliases in RESOURCE_TYPE_ALIASES.items():
            if any(alias in words for alias in aliases):
                resource_type = r_type
                break'''

new_r_type = '''        # 2. Extract resource type ONLY (no device type inference)
        # We do this from the original query string (q) before we start destroying it.
        # Normalize separators for resource type detection (so 'firmware-version' -> 'firmware', 'version')
        r_type_q = re.sub(r'[-_/\\]', ' ', q.lower())
        resource_type = ""
        words = r_type_q.split()
        for r_type, aliases in RESOURCE_TYPE_ALIASES.items():
            if any(alias in words for alias in aliases):
                resource_type = r_type
                break'''

content = content.replace(old_r_type, new_r_type)

old_ident = '''        # Strip resource_type from identifier if present
        if resource_type:
            identifier = " ".join([w for w in identifier.split() if w.lower() not in NOISE_RESOURCE_TYPES]).strip()'''

new_ident = '''        # Strip resource_type from identifier if present
        if resource_type:
            clean_words = []
            for w in identifier.split():
                parts = re.split(r'[-_/\\]', w.lower())
                # If the hyphenated word consists entirely of resource types and attributes, strip it.
                if all(p in NOISE_RESOURCE_TYPES or p in NOISE_ATTRIBUTES for p in parts):
                    continue
                clean_words.append(w)
            identifier = " ".join(clean_words).strip()'''

content = content.replace(old_ident, new_ident)

with open(r'c:\AgenticAI_HPE\resource_resolver\query_agent.py', 'w', encoding='utf-8') as f:
    f.write(content)
