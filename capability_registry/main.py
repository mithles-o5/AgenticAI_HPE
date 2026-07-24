import logging
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger("capability-registry")

app = FastAPI(
    title="OASF Capability Registry",
    description="Maintains OASF agent profiles and maps requests to agents dynamically.",
    version="1.0.0",
)

# Store registered agents in memory
# Key: agent name, Value: agent oasf_record dict
_REGISTRY: Dict[str, dict] = {}

class AgentRecord(BaseModel):
    name: str
    version: str
    schema_version: str
    description: Optional[str] = ""
    skills: List[dict] = []
    domains: List[str] = []
    locators: List[dict] = []
    modules: dict = {}

@app.post("/agents", status_code=201)
async def register_agent(record: AgentRecord):
    """Register or update an agent capability profile."""
    _REGISTRY[record.name] = record.model_dump()
    logger.info(f"Registered agent: {record.name} with {len(record.skills)} skills.")
    return {"status": "registered", "agent": record.name}

@app.get("/agents")
async def list_agents():
    """List all registered agent profiles."""
    return list(_REGISTRY.values())

@app.get("/agents/lookup")
async def lookup_agent(
    resource_type: Optional[str] = None,
    provider: Optional[str] = None,
    skill: Optional[str] = None,
):
    """
    Find the most suitable agent for the given request criteria.
    Looks up matching resource_types, providers/protocols, or explicit skills.
    """
    # Normalize inputs
    rt = resource_type.lower() if resource_type else None
    prov = provider.lower() if provider else None
    
    # 1. Try to match by explicit skill name
    if skill:
        for name, agent in _REGISTRY.items():
            skill_names = [s.get("name").lower() for s in agent.get("skills", [])]
            if skill.lower() in skill_names:
                return agent

    # Helper function to check if resource type matches
    def match_resource(agent_rt_list, target_rt):
        if not target_rt:
            return False
        agent_rt_list_lower = [r.lower() for r in agent_rt_list]
        if target_rt in agent_rt_list_lower:
            return True
        # Handle generic 'server' matching 'server_hardware' or 'server_profile'
        if target_rt == "server" and any("server" in r for r in agent_rt_list_lower):
            return True
        return False

    # Helper function to check if provider matches
    def match_provider(agent_modules, target_prov):
        if not target_prov:
            return False
        providers = [p.lower() for p in agent_modules.get("providers", [])]
        protocols = [p.lower() for p in agent_modules.get("protocols", [])]
        return target_prov in providers or target_prov in protocols

    # 2. Perfect match (both resource_type and provider match)
    for name, agent in _REGISTRY.items():
        modules = agent.get("modules", {})
        if rt and prov:
            if match_resource(modules.get("resource_types", []), rt) and match_provider(modules, prov):
                return agent

    # 3. Provider match (provider is usually highly specific, e.g. "oneview" -> onprem)
    if prov:
        for name, agent in _REGISTRY.items():
            if match_provider(agent.get("modules", {}), prov):
                return agent

    # 4. Resource type match
    if rt:
        for name, agent in _REGISTRY.items():
            if match_resource(agent.get("modules", {}).get("resource_types", []), rt):
                return agent

    # Fallback/default logic
    if _REGISTRY:
        # Match by name substring
        if rt:
            for name, agent in _REGISTRY.items():
                if rt in name.lower():
                    return agent
        # Return first registered agent
        return list(_REGISTRY.values())[0]

    raise HTTPException(status_code=404, detail="No matching OASF agent found in registry.")

    raise HTTPException(status_code=404, detail="No matching OASF agent found in registry.")

@app.get("/agents/lookup-all")
async def lookup_all_agents(
    resource_type: Optional[str] = None,
):
    """
    Return EVERY (agent, provider) dispatch descriptor that can handle the given resource_type.

    Each entry in the returned list contains:
      - agent_name      : canonical name from the OASF record
      - agent_type      : execution-engine key (cloud / network / storage / server / onprem)
      - provider        : provider/protocol string for the adapter (e.g. mock_cloud, coms)
      - label           : human-readable display label
      - api_base        : base API path to call on the provider's mock server
      - resource_types  : all resource_types this (agent, provider) pair supports

    Matching is done against modules.provider_resource_map in the OASF record.
    Falls back to modules.resource_types (flat list) if no provider_resource_map is present.
    """
    rt = resource_type.lower().strip() if resource_type else None
    results = []

    for name, agent in _REGISTRY.items():
        modules = agent.get("modules", {})
        provider_resource_map = modules.get("provider_resource_map", {})
        # Derive a short agent_type key from the agent name (e.g. "cloud-agent" -> "cloud")
        agent_type = name.replace("-agent", "").lower().strip()

        if provider_resource_map:
            # Structured lookup: each provider declares its own resource_types
            for provider, info in provider_resource_map.items():
                supported = [r.lower() for r in info.get("resource_types", [])]
                if rt is None or rt in supported or any(rt in r or r in rt for r in supported):
                    results.append({
                        "agent_name":     name,
                        "agent_type":     agent_type,
                        "provider":       provider,
                        "label":          info.get("label", f"mock_server({provider})"),
                        "api_base":       info.get("api_base", ""),
                        "resource_types": info.get("resource_types", []),
                    })
        else:
            # Fallback: flat resource_types list — treat agent-level protocols as providers
            flat_rts = [r.lower() for r in modules.get("resource_types", [])]
            if rt is None or rt in flat_rts or any(rt in r or r in rt for r in flat_rts):
                protocols = modules.get("protocols", modules.get("providers", []))
                for prov in protocols:
                    results.append({
                        "agent_name":     name,
                        "agent_type":     agent_type,
                        "provider":       prov,
                        "label":          f"mock_server({prov})",
                        "api_base":       "",
                        "resource_types": modules.get("resource_types", []),
                    })

    return results


@app.get("/health")
def health():
    return {"status": "healthy", "service": "capability-registry"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8020, reload=True)
