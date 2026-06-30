with open(r'mock_server(iLO)/main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find all PUT routes on /redfish/v1/systems at collection level (no {system_id})
print("=== PUT routes on /systems (collection level) ===")
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if '@app' in stripped and 'PUT' in stripped and '/systems' in stripped and '{system_id}' not in stripped:
        print(f'{i}: {stripped}')

# Find devices endpoint
print("\n=== /devices routes ===")
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if '@app' in stripped and '/devices' in stripped:
        print(f'{i}: {stripped}')

# Find create handler - look for PUT /redfish/v1/systems/{system_id} (which is used to PUT a new server)
print("\n=== PUT /redfish/v1/systems/{system_id} ===")
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if '@app' in stripped and 'put' in stripped.lower() and '/systems/{system_id}' in stripped and 'actions' not in stripped.lower():
        print(f'{i}: {stripped}')
        for j in range(i, min(i+40, len(lines))):
            print(f'  {lines[j].rstrip()}')
        print()
        break
