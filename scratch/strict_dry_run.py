import sys, os, glob, importlib.util

VENDOR_MAP = {
    'ilo': 'mock_server', 'comops': 'coms', 'oneview': 'oneview',
    'network': 'mock_network', 'storage': 'mock_storage', 'cloud': 'mock_cloud'
}

DEVICE_TYPE_MAP = {
    'systems': 'server', 'server-hardware': 'server', 'servers': 'server',
    'storage-volumes': 'volume', 'volumes': 'volume', 'storage-systems': 'storage_system',
    'storage': 'storage', 'arrays': 'storage_system', 'ethernet-networks': 'network',
    'networks': 'network', 'switches': 'switch', 'interconnects': 'switch',
    'snapshots': 'snapshot', 'snapshot-collections': 'snapshot', 'routers': 'router',
    'access-points': 'access_point', 'aps': 'access_point', 'vlans': 'vlan',
    'database-services': 'database_service', 'databases': 'database_service',
    'virtual-machines': 'virtual_machine', 'kubernetes-clusters': 'kubernetes_cluster',
    'firewalls': 'firewall', 'subnets': 'subnet'
}

def get_fallback_device(vendor):
    if vendor == 'mock_server' or vendor == 'oneview': return 'server'
    if vendor == 'mock_network': return 'switch'
    if vendor == 'mock_storage': return 'storage'
    if vendor == 'mock_cloud': return 'virtual_machine'
    return 'generic'

def run():
    mock_dirs = glob.glob('mock_server(*)') + glob.glob('mock_*') + ['oneview', 'comops']
    mock_dirs = list(set(d for d in mock_dirs if os.path.isdir(d)))
    all_endpoints = []
    
    for d in mock_dirs:
        vendor_name = os.path.basename(d)
        if vendor_name.startswith('mock_server('): vendor_name = vendor_name.replace('mock_server(', '').replace(')', '')
        elif vendor_name.startswith('mock_'): vendor_name = vendor_name.replace('mock_', '')
        canonical_vendor = VENDOR_MAP.get(vendor_name.lower(), vendor_name.lower())
            
        main_py = os.path.join(d, 'main.py')
        if not os.path.exists(main_py): continue
        
        to_delete = [m for m, mod in sys.modules.items() if getattr(mod, '__file__', None) and ('mock_' in mod.__file__ or 'mock_server' in mod.__file__)]
        for m in to_delete: del sys.modules[m]
            
        sys.path.insert(0, d)
        spec = importlib.util.spec_from_file_location('main', main_py)
        main_mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(main_mod)
            if hasattr(main_mod, 'app') and hasattr(main_mod.app, 'routes'):
                for r in main_mod.app.routes:
                    if hasattr(r, 'methods') and hasattr(r, 'path'):
                        for method in r.methods:
                            if method == 'HEAD': continue
                            http_method = method.upper()
                            api_path = r.path
                            path_lower = api_path.lower()
                            
                            path_parts = [p for p in api_path.split('/') if p]
                            collection_segment = ''
                            for i, part in enumerate(path_parts):
                                if part.startswith('{') and part.endswith('}'):
                                    if i > 0: collection_segment = path_parts[i-1]
                                    break
                            else:
                                if path_parts: collection_segment = path_parts[-1]
                                    
                            device_type = DEVICE_TYPE_MAP.get(collection_segment.lower())
                            if not device_type:
                                device_type = get_fallback_device(canonical_vendor)
                            
                            action_keys = []
                            if 'powerstate' in path_lower:
                                if http_method in ('PUT', 'POST', 'PATCH'): action_keys = ['ON', 'OFF', 'RESET', 'COLD_BOOT']
                                elif http_method == 'GET': action_keys = ['STATUS']
                            elif path_lower.endswith('/power-on') and http_method in ('PUT', 'POST', 'PATCH'): action_keys = ['ON']
                            elif path_lower.endswith('/power-off') and http_method in ('PUT', 'POST', 'PATCH'): action_keys = ['OFF']
                            elif (path_lower.endswith('/reboot') or path_lower.endswith('/reset')) and http_method in ('PUT', 'POST', 'PATCH'): action_keys = ['RESET']
                            elif 'cold-boot' in path_lower and http_method in ('PUT', 'POST', 'PATCH'): action_keys = ['COLD_BOOT']
                            
                            if not action_keys:
                                is_single_resource = api_path.endswith('}')
                                is_collection = not is_single_resource
                                if is_single_resource:
                                    if http_method == 'GET': action_keys = ['STATUS']
                                    elif http_method == 'DELETE': action_keys = ['DELETE']
                                    elif http_method in ('PUT', 'PATCH', 'POST'): action_keys = ['UPDATE']
                                elif is_collection:
                                    if http_method == 'GET': action_keys = ['LIST']
                                    elif http_method == 'POST': action_keys = ['CREATE']
                            
                            if not action_keys:
                                if http_method == 'GET': action_keys = ['STATUS']
                                elif http_method in ('PUT', 'PATCH'): action_keys = ['UPDATE']
                                elif http_method == 'POST': action_keys = ['CREATE']
                                elif http_method == 'DELETE': action_keys = ['DELETE']
                                
                            for ak in action_keys:
                                all_endpoints.append({'vendor': canonical_vendor, 'device_type': device_type, 'action_key': ak, 'http_method': http_method, 'api_path': api_path})
        except Exception as e: pass
        finally:
            if sys.path[0] == d: sys.path.pop(0)
    return all_endpoints

eps = run()
vendors = sorted(set(e['vendor'] for e in eps))
dtypes = sorted(set(e['device_type'] for e in eps))
akeys = sorted(set(e['action_key'] for e in eps))

print('Vendors:', vendors)
print('Device Types:', dtypes)
print('Action Keys:', akeys)
print('\\n20 Sample Rows:')
for ep in eps[:20]:
    # Using python string formatting safely without powershell pipeline characters failing
    print(f"{ep['vendor']:<15} | {ep['device_type']:<20} | {ep['action_key']:<12} | {ep['http_method']:<6} | {ep['api_path']}")
