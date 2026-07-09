import re

with open(r'c:\AgenticAI_HPE\resource_resolver\query_agent.py', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'class QueryAgent:', content)
if match:
    new_code = '''class QueryAgent:
    """
    Lightweight, stateless, deterministic NLP preprocessing layer.
    """

    @staticmethod
    def _coerce_value(val_str: str) -> str | int | float | bool:
        v = val_str.lower()
        if v in {"true", "yes", "on", "enable", "enabled"}: return True
        if v in {"false", "no", "off", "disable", "disabled"}: return False
        try: return int(val_str)
        except ValueError: pass
        try: return float(val_str)
        except ValueError: pass
        return val_str

    @staticmethod
    def _parse(query: str) -> dict:
        """Pipeline extraction of action, identifier, and payload."""
        if not query or not isinstance(query, str):
            return _FAIL_CLOSED_PAYLOAD.copy()

        # 1. Normalization
        q = " ".join(query.lower().strip().split())
        import string
        punctuation_to_strip = ".,;:!?()[]\\\"'"
        q = q.strip(punctuation_to_strip)

        # 2. Action Detection
        action = "STATUS"
        category = "Operational"
        remaining_query = q
        
        for reg_item in ACTION_REGISTRY:
            m = reg_item.pattern.search(remaining_query)
            if m:
                action = reg_item.action
                category = reg_item.category
                # Remove ONLY the first matched action phrase
                remaining_query = remaining_query[:m.start()] + remaining_query[m.end():]
                remaining_query = " ".join(remaining_query.split())
                break

        # 3. Payload Extraction
        payload_dict = {}
        if action == "UPDATE":
            for pat in PAYLOAD_PATTERNS:
                m = pat.search(remaining_query)
                if m:
                    d = m.groupdict()
                    attr = d.get("attr").strip().replace(" ", "_") if d.get("attr") else ""
                    val = d.get("val").strip() if d.get("val") else ""
                    ident = d.get("ident").strip() if d.get("ident") else ""
                    
                    if attr in _FIELD_ALIASES:
                        attr = _FIELD_ALIASES[attr]
                        
                    payload_dict = {"attribute": attr, "value": val}
                    remaining_query = ident
                    break

        # 4. Identifier Extraction
        prev = None
        identifier = remaining_query
        while identifier != prev:
            prev = identifier
            identifier = PREFIX_PATTERN.sub('', identifier).strip()
            identifier = SUFFIX_PATTERN.sub('', identifier).strip()

        # Extract resource type for downstream schema consistency
        resource_type = ""
        words = identifier.lower().split()
        if any(k in words for k in ['firmware', 'firmwares']): resource_type = 'firmware'
        elif any(k in words for k in ['sensor', 'sensors', 'thermal', 'temperature']): resource_type = 'sensor'
        elif any(k in words for k in ['inventory', 'hardware', 'hw']): resource_type = 'inventory'
        elif any(k in words for k in ['media', 'iso', 'image']): resource_type = 'media'
        elif any(k in words for k in ['certificate', 'certificates', 'ca']): resource_type = 'certificate'
        elif any(k in words for k in ['metric', 'metrics', 'telemetry']): resource_type = 'metric'
        elif any(k in words for k in ['account', 'accounts', 'user', 'users']): resource_type = 'account'
        elif any(k in words for k in ['session', 'sessions', 'login']): resource_type = 'session'
        elif any(k in words for k in ['event', 'events', 'log', 'logs']): resource_type = 'event'
        elif any(k in words for k in ['license', 'licenses']): resource_type = 'license'
        elif any(k in words for k in ['profile', 'profiles']): resource_type = 'profile'
        elif any(k in words for k in ['power', 'powerstate']): resource_type = 'power'
        elif any(k in words for k in ['issue', 'issues', 'alert', 'alerts']): resource_type = 'issue'
        elif any(k in words for k in ['port', 'ports', 'interface', 'interfaces']): resource_type = 'port'
        
        # 5. Confidence Scoring
        # Start high, penalize for unparsed noise or empty identifiers
        confidence = 0.9 
        if not identifier:
            confidence = 0.5
        elif action == "STATUS" and remaining_query == q:
            # If nothing was parsed out and it just defaulted to STATUS
            confidence = 0.7
            
        if identifier in {"it", "this", "that", "the device", "the server", "the system"}:
            confidence = 0.2
            identifier = ""
            
        # Determine attributes payload
        attributes = []
        if payload_dict:
            attributes.append({"key": payload_dict["attribute"], "value": payload_dict["value"]})

        return {
            "identifier": identifier,
            "action": action,
            "category": category,
            "resource_type": resource_type,
            "attributes": attributes,
            "multi_intent": False,
            "ambiguous": confidence < 0.4,
            "confidence": confidence,
            "raw_query": query,
        }

    @staticmethod
    def parse_query_llm(query: str) -> dict:
        llm_res = _llm_extract(query)
        if llm_res and "identifier" in llm_res:
            return llm_res
        return _FAIL_CLOSED_PAYLOAD.copy()

    @staticmethod
    def parse_query_hybrid(query: str) -> dict:
        regex_res = QueryAgent._parse(query)
        if regex_res.get("confidence", 0.0) >= QUERY_AGENT_CONFIDENCE_THRESHOLD:
            return regex_res
        
        llm_res = QueryAgent.parse_query_llm(query)
        if llm_res.get("action") == "UNPARSEABLE":
            return regex_res
        return llm_res

    @staticmethod
    def parse_query(query: str) -> dict:
        return QueryAgent.parse_query_hybrid(query)

    @staticmethod
    def parse_update_payload(query: str) -> dict | None:
        res = QueryAgent._parse(query)
        if res.get("action") == "UPDATE" and res.get("attributes"):
            return {"attribute": res["attributes"][0]["key"], "value": res["attributes"][0]["value"]}
        return None
'''

    final_content = content[:match.start()] + new_code
    with open(r'c:\AgenticAI_HPE\resource_resolver\query_agent.py', 'w', encoding='utf-8') as f:
        f.write(final_content)
    print('Replaced QueryAgent class successfully!')
else:
    print('Failed to find QueryAgent class')
