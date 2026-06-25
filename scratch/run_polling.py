import sys
import os
import logging
logging.basicConfig(level=logging.INFO)
sys.path.append(r'd:\HPE CPP\MCP_Integrated')
sys.path.append(r'd:\HPE CPP\MCP_Integrated\resource_resolver')
from resource_resolver.polling_engine import PollingEngine
from resource_resolver.cache import ResourceCache
pe = PollingEngine(ResourceCache())
pe.run_poll_cycle()
