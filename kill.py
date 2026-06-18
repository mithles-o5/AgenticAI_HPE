import os
import subprocess

out = subprocess.check_output('powershell -Command "Get-CimInstance Win32_Process -Filter \\"CommandLine LIKE \'%uvicorn%\'\\" | Select-Object -ExpandProperty ProcessId"', shell=True)
for pid in out.decode().split():
    if pid.strip():
        os.system(f"taskkill /PID {pid.strip()} /F")
