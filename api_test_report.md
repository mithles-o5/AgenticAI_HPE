# Mock Server Endpoint Verification Report

Executed on: 2026-06-23 19:46:22

## Execution Summary

- **Total Endpoints Tested**: 2062
- **Successful Responses (2xx)**: 1465
- **Resource Not Found (404)**: 301 *(Expected for unregistered resource IDs)*
- **Input Validation Failure (422)**: 14 *(Expected for empty/mock Pydantic validation)*
- **Other Client Errors (4xx)**: 0
- **Server Errors (5xx)**: 0 *(Potential route handler bugs)*
- **Python Crashes**: 282 *(Crashed during execution)*

## Endpoints with Server Errors (5xx) or Crashes

| Server | Method | Path | Status | Response / Error Preview |
| :--- | :--- | :--- | :--- | :--- |
| ilo | PATCH | `/redfish/v1/accountservice/Oem/Hpe/appaccounts/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/accountservice/accounts/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/accountservice/accounts/test_id_999/keys` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/accountservice/accounts/test_id_999/keys/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/accountservice/externalaccountproviders/ldap/certificates/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/accountservice/roles/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/accountservice/usercertificatemapping/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/certificateservice/certificateenrollments/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/certificateservice/enrollmentCAcertificates/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/chassis/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/PCIeDevices/test_id_999/assembly` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/assembly` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/basefrus` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/chassis/test_id_999/basefrus/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/basefrus/test_id_999/details` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/devices` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/chassis/test_id_999/devices/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/drives/test_id_999/assembly` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/drives/test_id_999/environmentmetrics` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/environmentmetrics` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/mezzfrus` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/chassis/test_id_999/mezzfrus/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/mezzfrus/test_id_999/details` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/networkadapters` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999/assembly` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999/networkdevicefunctions` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999/networkdevicefunctions/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999/networkdevicefunctions/test_id_999/settings` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999/ports` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999/ports/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999/ports/test_id_999/settings` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999/settings` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/pciedevices` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/chassis/test_id_999/pciedevices/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/pciedevices/test_id_999/pciefunctions` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/chassis/test_id_999/pciedevices/test_id_999/pciefunctions/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/pcieslots` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/power` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/power/fastpowermeter` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/power/powermeter` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/powersubsystem` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/powersubsystem/batteries` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/chassis/test_id_999/powersubsystem/batteries/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/powersubsystem/powersupplies` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/chassis/test_id_999/powersubsystem/powersupplies/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/powersubsystem/powersupplies/test_id_999/assembly` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/powersubsystem/powersupplies/test_id_999/metrics` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/chassis/test_id_999/sensors/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/thermal` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/thermalsubsystem` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/thermalsubsystem/fans` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/chassis/test_id_999/thermalsubsystem/fans/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/thermalsubsystem/fans/test_id_999/assembly` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/thermalsubsystem/pumps` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/thermalsubsystem/pumps/test_id_999/assembly` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/chassis/test_id_999/thermalsubsystem/thermalmetrics` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/componentintegrity/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/eventservice/cacertificates/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/eventservice/subscriptions/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/fabrics/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/fabrics/test_id_999/switches` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/fabrics/test_id_999/switches/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/fabrics/test_id_999/switches/test_id_999/ports` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/fabrics/test_id_999/switches/test_id_999/ports/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/jsonschemas/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/managers/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/managers/test_id_999/ManagerDiagnosticData` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/managers/test_id_999/activehealthsystem` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/managers/test_id_999/backuprestoreservice` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/managers/test_id_999/backuprestoreservice/backupfiles` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/managers/test_id_999/backuprestoreservice/backupfiles/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/managers/test_id_999/datetime` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/managers/test_id_999/dedicatednetworkports` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/managers/test_id_999/dedicatednetworkports/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/managers/test_id_999/ethernetinterfaces` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/managers/test_id_999/ethernetinterfaces/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/managers/test_id_999/hostinterfaces` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/managers/test_id_999/hostinterfaces/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/managers/test_id_999/licenseservice` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/managers/test_id_999/licenseservice/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/managers/test_id_999/logservices` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/managers/test_id_999/logservices/iel` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/managers/test_id_999/logservices/iel/entries` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/managers/test_id_999/logservices/iel/entries/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/managers/test_id_999/networkprotocol` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/managers/test_id_999/networkprotocol/HTTPS/certificates` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/managers/test_id_999/networkprotocol/HTTPS/certificates/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/managers/test_id_999/remotesupportservice` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/managers/test_id_999/remotesupportservice/serviceeventlogs` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/managers/test_id_999/remotesupportservice/serviceeventlogs/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/managers/test_id_999/securityservice` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/managers/test_id_999/securityservice/bmchpeldevid/certificates` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/managers/test_id_999/securityservice/bmchpeldevid/certificates/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/managers/test_id_999/securityservice/bmciak/certificates` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/managers/test_id_999/securityservice/bmciak/certificates/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/managers/test_id_999/securityservice/bmcidevidpca/certificates` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/managers/test_id_999/securityservice/bmcidevidpca/certificates/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/managers/test_id_999/securityservice/bmclak/certificates` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/managers/test_id_999/securityservice/bmclak/certificates/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/managers/test_id_999/securityservice/certificateauthentication` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/managers/test_id_999/securityservice/certificateauthentication/cacertificates` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/managers/test_id_999/securityservice/certificateauthentication/cacertificates/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/managers/test_id_999/securityservice/eskm` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/managers/test_id_999/securityservice/httpscert` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/managers/test_id_999/securityservice/platformcert/certificates` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/managers/test_id_999/securityservice/platformcert/certificates/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/managers/test_id_999/securityservice/securitydashboard` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/managers/test_id_999/securityservice/securitydashboard/securityparams` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/managers/test_id_999/securityservice/securitydashboard/securityparams/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/managers/test_id_999/securityservice/sso` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/managers/test_id_999/securityservice/systemiak/certificates` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/managers/test_id_999/securityservice/systemiak/certificates/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/managers/test_id_999/securityservice/systemidevid/certificates` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/managers/test_id_999/securityservice/systemidevid/certificates/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/managers/test_id_999/securityservice/systemlak/certificates` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/managers/test_id_999/securityservice/systemlak/certificates/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/managers/test_id_999/securityservice/systemldevid/certificates` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/managers/test_id_999/securityservice/systemldevid/certificates/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/managers/test_id_999/sharednetworkports` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/managers/test_id_999/sharednetworkports/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/managers/test_id_999/snmpservice` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/managers/test_id_999/snmpservice/snmpalertdestinations` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/managers/test_id_999/snmpservice/snmpalertdestinations/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/managers/test_id_999/snmpservice/snmpusers` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/managers/test_id_999/snmpservice/snmpusers/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/managers/test_id_999/virtualmedia` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/managers/test_id_999/virtualmedia/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/registries/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/sessionservice/sessions/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/bios` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/bios/baseconfigs` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/bios/boot` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/bios/boot/baseconfigs` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/bios/boot/settings` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/bios/iscsi` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/bios/iscsi/baseconfigs` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/bios/iscsi/settings` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/bios/kmsconfig` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/bios/kmsconfig/baseconfigs` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/bios/kmsconfig/settings` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/bios/mappings` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/bios/oem/hpe/tlsconfig` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/bios/oem/hpe/tlsconfig/baseconfigs` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/bios/oem/hpe/tlsconfig/settings` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/bios/serverconfiglock` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/bios/serverconfiglock/baseconfigs` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/bios/serverconfiglock/settings` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/bios/settings` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/bootoptions` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/bootoptions/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/ethernetinterfaces` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/ethernetinterfaces/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/keymanagement/KMIPcertificates` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/keymanagement/KMIPcertificates/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/keymanagement/KMIPclientcertificates` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/keymanagement/KMIPclientcertificates/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/logservices` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/logservices/dpu` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/logservices/dpu/entries` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/logservices/dpu/entries/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/logservices/event` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/logservices/event/entries` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/logservices/event/entries/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/logservices/iml` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/logservices/iml/entries` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/logservices/iml/entries/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/logservices/sl` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/logservices/sl/entries` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/logservices/sl/entries/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/memory` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/memory/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/memory/test_id_999/memorymetrics` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/memorydomains` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/memorydomains/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/memorydomains/test_id_999/memorychunks` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/memorydomains/test_id_999/memorychunks/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/networkinterfaces` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/networkinterfaces/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/networkinterfaces/test_id_999/networkdevicefunctions` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/networkinterfaces/test_id_999/networkdevicefunctions/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/networkinterfaces/test_id_999/networkdevicefunctions/test_id_999/settings` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/networkinterfaces/test_id_999/ports` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/networkinterfaces/test_id_999/ports/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/networkinterfaces/test_id_999/ports/test_id_999/settings` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/pcidevices` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/pcidevices/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/pcislots` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/pcislots/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/processors` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/processors/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/processors/test_id_999/environmentmetrics` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/processors/test_id_999/processormetrics` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/db` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/db/certificates` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/db/certificates/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/db/signatures` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/db/signatures/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbdefault` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbdefault/certificates` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbdefault/certificates/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbdefault/signatures` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbdefault/signatures/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbr` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbr/certificates` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbr/certificates/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbr/signatures` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbr/signatures/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbrdefault` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbrdefault/certificates` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbrdefault/certificates/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbrdefault/signatures` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbrdefault/signatures/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbt` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbt/certificates` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbt/certificates/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbt/signatures` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbt/signatures/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbtdefault` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbtdefault/certificates` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbtdefault/certificates/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbtdefault/signatures` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbtdefault/signatures/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbx` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbx/certificates` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbx/certificates/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbx/signatures` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbx/signatures/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbxdefault` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbxdefault/certificates` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbxdefault/certificates/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbxdefault/signatures` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbxdefault/signatures/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/kek` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/kek/certificates` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/kek/certificates/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/kekdefault` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/kekdefault/certificates` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/kekdefault/certificates/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/pk` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/pk/certificates` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/pk/certificates/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/pkdefault` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/pkdefault/certificates` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/pkdefault/certificates/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureerasereportservice` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/secureerasereportservice/secureerasereportentries` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/secureerasereportservice/secureerasereportentries/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/storage` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/storage/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/storage/test_id_999/controllers/` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/storage/test_id_999/controllers/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/storage/test_id_999/controllers/test_id_999/assembly` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | POST | `/redfish/v1/systems/test_id_999/storage/test_id_999/controllers/test_id_999/ports` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/storage/test_id_999/controllers/test_id_999/ports/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/storage/test_id_999/drives/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/storage/test_id_999/storagecontrollers/test_id_999/ports` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/storage/test_id_999/storagecontrollers/test_id_999/ports/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/storage/test_id_999/volumes` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/storage/test_id_999/volumes/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/usbdevices` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/usbdevices/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/usbports` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/usbports/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | POST | `/redfish/v1/systems/test_id_999/workloadperformanceadvisor` | CRASH | `Crash Exception: unrecognized token: "{" Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 175, in run_tests     resp = client.post(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 546, in post     return super().post(            ~~~~~~~~~~~~^ ` |
| ilo | PATCH | `/redfish/v1/systems/test_id_999/workloadperformanceadvisor/test_id_999` | CRASH | `Crash Exception: duplicate column name: name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/taskservice/tasks/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/telemetryservice/metricdefinitions/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/telemetryservice/metricreportdefinitions/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/telemetryservice/metricreports/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/telemetryservice/triggers/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/updateservice/componentrepository/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/updateservice/firmwareinventory/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/updateservice/installsets/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/updateservice/invalidimagerepository/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/updateservice/maintenancewindows/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/updateservice/runningsoftwareinventory/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/updateservice/softwareinventory/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |
| ilo | PATCH | `/redfish/v1/updateservice/updatetaskqueue/test_id_999` | CRASH | `Crash Exception: duplicate column name: Name Traceback (most recent call last):   File "D:\AgenticAI_HPE\test_all_948_endpoints.py", line 181, in run_tests     resp = client.patch(eval_path, json=payload)   File "D:\AgenticAI_HPE\env\Lib\site-packages\starlette\testclient.py", line 608, in patch     return super().patch(            ~~~~~~~~~~~` |

## Complete Results By Server

<details><summary><b>CLOUD Server - 660 Endpoints (Click to Expand)</b></summary>

| Method | Original Path | Replaced Path | Status Code | Result Category |
| :--- | :--- | :--- | :--- | :--- |
| GET | `/openapi.json` | `/openapi.json` | 200 | SUCCESS_2XX |
| GET | `/docs` | `/docs` | 200 | SUCCESS_2XX |
| GET | `/docs/oauth2-redirect` | `/docs/oauth2-redirect` | 200 | SUCCESS_2XX |
| GET | `/redoc` | `/redoc` | 200 | SUCCESS_2XX |
| GET | `/api/v1/access-controls` | `/api/v1/access-controls` | 200 | SUCCESS_2XX |
| GET | `/api/v1/audit-events` | `/api/v1/audit-events` | 200 | SUCCESS_2XX |
| GET | `/api/v1/host-initiator-groups` | `/api/v1/host-initiator-groups` | 200 | SUCCESS_2XX |
| POST | `/api/v1/host-initiator-groups` | `/api/v1/host-initiator-groups` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/host-initiator-groups/{hostGroupId}` | `/api/v1/host-initiator-groups/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/host-initiator-groups/{hostGroupId}` | `/api/v1/host-initiator-groups/test_id_999` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/host-initiator-groups/{hostGroupId}` | `/api/v1/host-initiator-groups/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/host-initiator-groups/{hostGroupId}/mappedDevices` | `/api/v1/host-initiator-groups/test_id_999/mappedDevices` | 200 | SUCCESS_2XX |
| GET | `/api/v1/host-initiator-groups/bulkmerge` | `/api/v1/host-initiator-groups/bulkmerge` | 200 | SUCCESS_2XX |
| POST | `/api/v1/host-initiator-groups/bulkmerge` | `/api/v1/host-initiator-groups/bulkmerge` | 200 | SUCCESS_2XX |
| POST | `/api/v1/host-initiator-groups/merge` | `/api/v1/host-initiator-groups/merge` | 200 | SUCCESS_2XX |
| GET | `/api/v1/host-initiators` | `/api/v1/host-initiators` | 200 | SUCCESS_2XX |
| POST | `/api/v1/host-initiators` | `/api/v1/host-initiators` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/host-initiators/{hostId}` | `/api/v1/host-initiators/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/host-initiators/{hostId}` | `/api/v1/host-initiators/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/host-initiators/{hostId}` | `/api/v1/host-initiators/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/host-initiators/{hostId}/chap` | `/api/v1/host-initiators/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/chap` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/host-initiators/{hostId}/chap` | `/api/v1/host-initiators/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/chap` | 200 | SUCCESS_2XX |
| POST | `/api/v1/host-initiators/{hostId}/chapkey` | `/api/v1/host-initiators/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/chapkey` | 200 | SUCCESS_2XX |
| GET | `/api/v1/host-initiators/{hostId}/mappedDevices` | `/api/v1/host-initiators/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/mappedDevices` | 200 | SUCCESS_2XX |
| GET | `/api/v1/host-initiators/{hostId}/storage-performance-history` | `/api/v1/host-initiators/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/storage-performance-history` | 200 | SUCCESS_2XX |
| GET | `/api/v1/host-initiators/{hostId}/volumes` | `/api/v1/host-initiators/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/volumes` | 200 | SUCCESS_2XX |
| GET | `/api/v1/host-initiators/{hostId}/volumes-snapshots` | `/api/v1/host-initiators/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/volumes-snapshots` | 200 | SUCCESS_2XX |
| GET | `/api/v1/host-initiators/bulkmerge` | `/api/v1/host-initiators/bulkmerge` | 200 | SUCCESS_2XX |
| POST | `/api/v1/host-initiators/bulkmerge` | `/api/v1/host-initiators/bulkmerge` | 200 | SUCCESS_2XX |
| POST | `/api/v1/host-initiators/merge` | `/api/v1/host-initiators/merge` | 200 | SUCCESS_2XX |
| GET | `/api/v1/initiators` | `/api/v1/initiators` | 200 | SUCCESS_2XX |
| POST | `/api/v1/initiators` | `/api/v1/initiators` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/initiators/{initiatorId}` | `/api/v1/initiators/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/initiators/{initiatorId}` | `/api/v1/initiators/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/issues` | `/api/v1/issues` | 200 | SUCCESS_2XX |
| GET | `/api/v1/issues/{id}` | `/api/v1/issues/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/resource-types` | `/api/v1/resource-types` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems` | `/api/v1/storage-systems` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/{id}` | `/api/v1/storage-systems/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/{systemId}/storage-pools` | `/api/v1/storage-systems/test_id_999/storage-pools` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/{systemId}/storage-pools/{id}` | `/api/v1/storage-systems/test_id_999/storage-pools/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/{systemId}/storage-pools/{id}/volumes` | `/api/v1/storage-systems/test_id_999/storage-pools/test_id_999/volumes` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/{systemId}/volume-sets` | `/api/v1/storage-systems/test_id_999/volume-sets` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/{systemId}/volume-sets/{id}` | `/api/v1/storage-systems/test_id_999/volume-sets/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/{systemId}/volumes` | `/api/v1/storage-systems/test_id_999/volumes` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1` | `/api/v1/storage-systems/device-type1` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{id}` | `/api/v1/storage-systems/device-type1/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{id}` | `/api/v1/storage-systems/device-type1/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/alert-contacts` | `/api/v1/storage-systems/device-type1/test_id_999/alert-contacts` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/alert-contacts` | `/api/v1/storage-systems/device-type1/test_id_999/alert-contacts` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type1/{systemId}/alert-contacts/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/alert-contacts/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/alert-contacts/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/alert-contacts/test_id_999` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type1/{systemId}/alert-contacts/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/alert-contacts/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/application-summary` | `/api/v1/storage-systems/device-type1/test_id_999/application-summary` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/applicationsets` | `/api/v1/storage-systems/device-type1/test_id_999/applicationsets` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/applicationsets` | `/api/v1/storage-systems/device-type1/test_id_999/applicationsets` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/export` | `/api/v1/storage-systems/device-type1/test_id_999/applicationsets/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/export` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/replication-partners` | `/api/v1/storage-systems/device-type1/test_id_999/applicationsets/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/replication-partners` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/replication-partners/{replicationPartnerId}/volumes` | `/api/v1/storage-systems/device-type1/test_id_999/applicationsets/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/replication-partners/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/volumes` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/snapsets/{snapsetId}` | `/api/v1/storage-systems/device-type1/test_id_999/applicationsets/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/snapsets/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/snapsets/{snapsetId}` | `/api/v1/storage-systems/device-type1/test_id_999/applicationsets/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/snapsets/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/un-export` | `/api/v1/storage-systems/device-type1/test_id_999/applicationsets/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/un-export` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/volumes` | `/api/v1/storage-systems/device-type1/test_id_999/applicationsets/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/volumes` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/applicationsets/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/applicationsets/test_id_999` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/applicationsets/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/capacity-statistics` | `/api/v1/storage-systems/device-type1/test_id_999/applicationsets/test_id_999/capacity-statistics` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/performance` | `/api/v1/storage-systems/device-type1/test_id_999/applicationsets/test_id_999/performance` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/protection-policies` | `/api/v1/storage-systems/device-type1/test_id_999/applicationsets/test_id_999/protection-policies` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/protection-policies` | `/api/v1/storage-systems/device-type1/test_id_999/applicationsets/test_id_999/protection-policies` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/protection-policies` | `/api/v1/storage-systems/device-type1/test_id_999/applicationsets/test_id_999/protection-policies` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/protection-policies/fix` | `/api/v1/storage-systems/device-type1/test_id_999/applicationsets/test_id_999/protection-policies/fix` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/protection-policies/remove` | `/api/v1/storage-systems/device-type1/test_id_999/applicationsets/test_id_999/protection-policies/remove` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/proximity-settings` | `/api/v1/storage-systems/device-type1/test_id_999/applicationsets/test_id_999/proximity-settings` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/proximity-settings` | `/api/v1/storage-systems/device-type1/test_id_999/applicationsets/test_id_999/proximity-settings` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/remote-protection/actions` | `/api/v1/storage-systems/device-type1/test_id_999/applicationsets/test_id_999/remote-protection/actions` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/snapsets` | `/api/v1/storage-systems/device-type1/test_id_999/applicationsets/test_id_999/snapsets` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/snapsets` | `/api/v1/storage-systems/device-type1/test_id_999/applicationsets/test_id_999/snapsets` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/supported-protection` | `/api/v1/storage-systems/device-type1/test_id_999/applicationsets/test_id_999/supported-protection` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/capacity-history` | `/api/v1/storage-systems/device-type1/test_id_999/capacity-history` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/capacity-summary` | `/api/v1/storage-systems/device-type1/test_id_999/capacity-summary` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/certificates` | `/api/v1/storage-systems/device-type1/test_id_999/certificates` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/certificates` | `/api/v1/storage-systems/device-type1/test_id_999/certificates` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/certificates/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/certificates/test_id_999` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type1/{systemId}/certificates/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/certificates/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/certificates/remove` | `/api/v1/storage-systems/device-type1/test_id_999/certificates/remove` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/collect-support-data` | `/api/v1/storage-systems/device-type1/test_id_999/collect-support-data` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/component-performance-statistics` | `/api/v1/storage-systems/device-type1/test_id_999/component-performance-statistics` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/enclosures` | `/api/v1/storage-systems/device-type1/test_id_999/enclosures` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/enclosures/{cageId}/disks` | `/api/v1/storage-systems/device-type1/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/disks` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/enclosures/{cageId}/disks/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/disks/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-card-ports` | `/api/v1/storage-systems/device-type1/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-card-ports` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-card-ports/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-card-ports/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-cards` | `/api/v1/storage-systems/device-type1/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-cards` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-cards/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-cards/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-cards/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-cards/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-disks` | `/api/v1/storage-systems/device-type1/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-disks` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-disks/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-disks/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-expanders` | `/api/v1/storage-systems/device-type1/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-expanders` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-expanders/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-expanders/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-fans` | `/api/v1/storage-systems/device-type1/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-fans` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-fans/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-fans/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-powers` | `/api/v1/storage-systems/device-type1/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-powers` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-powers/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-powers/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-powers/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-powers/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-sleds` | `/api/v1/storage-systems/device-type1/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-sleds` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-sleds/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-sleds/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-sleds/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-sleds/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/enclosures/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/enclosures/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/enclosures/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/enclosures/test_id_999` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type1/{systemId}/enclosures/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/enclosures/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/encryption/backup` | `/api/v1/storage-systems/device-type1/test_id_999/encryption/backup` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/encryption/checkekm` | `/api/v1/storage-systems/device-type1/test_id_999/encryption/checkekm` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/encryption/enable` | `/api/v1/storage-systems/device-type1/test_id_999/encryption/enable` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/encryption/rekey` | `/api/v1/storage-systems/device-type1/test_id_999/encryption/rekey` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/encryption/restore` | `/api/v1/storage-systems/device-type1/test_id_999/encryption/restore` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/encryption/setekm` | `/api/v1/storage-systems/device-type1/test_id_999/encryption/setekm` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/encryption/setekm/backup` | `/api/v1/storage-systems/device-type1/test_id_999/encryption/setekm/backup` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/headroom-utilization` | `/api/v1/storage-systems/device-type1/test_id_999/headroom-utilization` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/host-paths` | `/api/v1/storage-systems/device-type1/test_id_999/host-paths` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/host-paths/{hostPathId}` | `/api/v1/storage-systems/device-type1/test_id_999/host-paths/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/host-sets` | `/api/v1/storage-systems/device-type1/test_id_999/host-sets` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/host-sets/{hostSetId}` | `/api/v1/storage-systems/device-type1/test_id_999/host-sets/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/hosts` | `/api/v1/storage-systems/device-type1/test_id_999/hosts` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/hosts/{hostId}` | `/api/v1/storage-systems/device-type1/test_id_999/hosts/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/insights/latencyfactors` | `/api/v1/storage-systems/device-type1/test_id_999/insights/latencyfactors` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type1/{systemId}/mail-settings` | `/api/v1/storage-systems/device-type1/test_id_999/mail-settings` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/mail-settings` | `/api/v1/storage-systems/device-type1/test_id_999/mail-settings` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/mail-settings` | `/api/v1/storage-systems/device-type1/test_id_999/mail-settings` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type1/{systemId}/mail-settings` | `/api/v1/storage-systems/device-type1/test_id_999/mail-settings` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/network-services/cim` | `/api/v1/storage-systems/device-type1/test_id_999/network-services/cim` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type1/{systemId}/network-services/cim` | `/api/v1/storage-systems/device-type1/test_id_999/network-services/cim` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/network-services/snmp-mgr` | `/api/v1/storage-systems/device-type1/test_id_999/network-services/snmp-mgr` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/network-services/snmp-mgr` | `/api/v1/storage-systems/device-type1/test_id_999/network-services/snmp-mgr` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type1/{systemId}/network-services/snmp-mgr/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/network-services/snmp-mgr/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/network-services/snmp-mgr/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/network-services/snmp-mgr/test_id_999` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type1/{systemId}/network-services/snmp-mgr/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/network-services/snmp-mgr/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/network-services/vasa` | `/api/v1/storage-systems/device-type1/test_id_999/network-services/vasa` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/network-services/vasa/{vasaId}` | `/api/v1/storage-systems/device-type1/test_id_999/network-services/vasa/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/network-services/vasa/{vasaId}/services` | `/api/v1/storage-systems/device-type1/test_id_999/network-services/vasa/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/services` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/network-settings` | `/api/v1/storage-systems/device-type1/test_id_999/network-settings` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/network-settings` | `/api/v1/storage-systems/device-type1/test_id_999/network-settings` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/nodes` | `/api/v1/storage-systems/device-type1/test_id_999/nodes` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/nodes/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/nodes/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/nodes/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/nodes/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/component-performance-statistics` | `/api/v1/storage-systems/device-type1/test_id_999/nodes/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/component-performance-statistics` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-cards` | `/api/v1/storage-systems/device-type1/test_id_999/nodes/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/node-cards` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-cards/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/nodes/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/node-cards/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-cards/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/nodes/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/node-cards/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-cpus` | `/api/v1/storage-systems/device-type1/test_id_999/nodes/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/node-cpus` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-cpus/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/nodes/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/node-cpus/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-drives` | `/api/v1/storage-systems/device-type1/test_id_999/nodes/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/node-drives` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-drives/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/nodes/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/node-drives/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-mcus` | `/api/v1/storage-systems/device-type1/test_id_999/nodes/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/node-mcus` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-mcus/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/nodes/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/node-mcus/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-mems` | `/api/v1/storage-systems/device-type1/test_id_999/nodes/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/node-mems` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-mems/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/nodes/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/node-mems/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-powers` | `/api/v1/storage-systems/device-type1/test_id_999/nodes/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/node-powers` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-powers/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/nodes/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/node-powers/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-powers/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/nodes/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/node-powers/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/nodes-batteries` | `/api/v1/storage-systems/device-type1/test_id_999/nodes/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/nodes-batteries` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/nodes-batteries/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/nodes/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/nodes-batteries/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/service-ports` | `/api/v1/storage-systems/device-type1/test_id_999/nodes/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/service-ports` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/nodes/service-ports` | `/api/v1/storage-systems/device-type1/test_id_999/nodes/service-ports` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/performance-history` | `/api/v1/storage-systems/device-type1/test_id_999/performance-history` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/performance-statistics` | `/api/v1/storage-systems/device-type1/test_id_999/performance-statistics` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/physicaldrives-performance` | `/api/v1/storage-systems/device-type1/test_id_999/physicaldrives-performance` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/ports` | `/api/v1/storage-systems/device-type1/test_id_999/ports` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/ports-performance` | `/api/v1/storage-systems/device-type1/test_id_999/ports-performance` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/ports/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/ports/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/ports/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/ports/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/ports/{id}/clear` | `/api/v1/storage-systems/device-type1/test_id_999/ports/test_id_999/clear` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type1/{systemId}/ports/{id}/edit-iscsi` | `/api/v1/storage-systems/device-type1/test_id_999/ports/test_id_999/edit-iscsi` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type1/{systemId}/ports/{id}/edit-rcip` | `/api/v1/storage-systems/device-type1/test_id_999/ports/test_id_999/edit-rcip` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type1/{systemId}/ports/{id}/fc` | `/api/v1/storage-systems/device-type1/test_id_999/ports/test_id_999/fc` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/ports/{id}/initialize` | `/api/v1/storage-systems/device-type1/test_id_999/ports/test_id_999/initialize` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/ports/{id}/ping-iscsi` | `/api/v1/storage-systems/device-type1/test_id_999/ports/test_id_999/ping-iscsi` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/ports/{id}/ping-rcip` | `/api/v1/storage-systems/device-type1/test_id_999/ports/test_id_999/ping-rcip` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/qos-policy` | `/api/v1/storage-systems/device-type1/test_id_999/qos-policy` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/remotecopylinks-performance` | `/api/v1/storage-systems/device-type1/test_id_999/remotecopylinks-performance` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/snapshots/{snapshotId}/clone` | `/api/v1/storage-systems/device-type1/test_id_999/snapshots/test_id_999/clone` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/snapshots/{snapshotId}/export` | `/api/v1/storage-systems/device-type1/test_id_999/snapshots/test_id_999/export` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/snapshots/{snapshotId}/un-export` | `/api/v1/storage-systems/device-type1/test_id_999/snapshots/test_id_999/un-export` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/snapshots/{snapshotId}/vluns` | `/api/v1/storage-systems/device-type1/test_id_999/snapshots/test_id_999/vluns` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/snapshots/{snapshotId}/vluns/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/snapshots/test_id_999/vluns/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/storage-pools` | `/api/v1/storage-systems/device-type1/test_id_999/storage-pools` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/storage-pools/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/storage-pools/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/storage-pools/{id}/volumes` | `/api/v1/storage-systems/device-type1/test_id_999/storage-pools/test_id_999/volumes` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/support-settings` | `/api/v1/storage-systems/device-type1/test_id_999/support-settings` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/support-settings` | `/api/v1/storage-systems/device-type1/test_id_999/support-settings` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type1/{systemId}/support-settings` | `/api/v1/storage-systems/device-type1/test_id_999/support-settings` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/system-settings` | `/api/v1/storage-systems/device-type1/test_id_999/system-settings` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/system-settings` | `/api/v1/storage-systems/device-type1/test_id_999/system-settings` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type1/{systemId}/system-settings` | `/api/v1/storage-systems/device-type1/test_id_999/system-settings` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/system-settings/management-services/vvolscs` | `/api/v1/storage-systems/device-type1/test_id_999/system-settings/management-services/vvolscs` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/system-settings/management-services/vvolscs` | `/api/v1/storage-systems/device-type1/test_id_999/system-settings/management-services/vvolscs` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type1/{systemId}/system-settings/management-services/vvolscs/{vvolscId}` | `/api/v1/storage-systems/device-type1/test_id_999/system-settings/management-services/vvolscs/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type1/{systemId}/system-settings/management-services/vvolscs/{vvolscId}` | `/api/v1/storage-systems/device-type1/test_id_999/system-settings/management-services/vvolscs/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/system-settings/management-services/vvolscs/{vvolscId}/attach` | `/api/v1/storage-systems/device-type1/test_id_999/system-settings/management-services/vvolscs/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/attach` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/system-settings/quorum-witness` | `/api/v1/storage-systems/device-type1/test_id_999/system-settings/quorum-witness` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/system-settings/quorum-witness` | `/api/v1/storage-systems/device-type1/test_id_999/system-settings/quorum-witness` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type1/{systemId}/system-settings/quorum-witness/{replicationPartnerId}` | `/api/v1/storage-systems/device-type1/test_id_999/system-settings/quorum-witness/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/system-settings/quorum-witness/{replicationPartnerId}` | `/api/v1/storage-systems/device-type1/test_id_999/system-settings/quorum-witness/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type1/{systemId}/system-settings/quorum-witness/{replicationPartnerId}` | `/api/v1/storage-systems/device-type1/test_id_999/system-settings/quorum-witness/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/system-settings/replication-partners` | `/api/v1/storage-systems/device-type1/test_id_999/system-settings/replication-partners` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/system-settings/replication-partners` | `/api/v1/storage-systems/device-type1/test_id_999/system-settings/replication-partners` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/system-settings/replication-partners/{replicationPartnerId}` | `/api/v1/storage-systems/device-type1/test_id_999/system-settings/replication-partners/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type1/{systemId}/system-settings/replication-partners/{replicationPartnerId}` | `/api/v1/storage-systems/device-type1/test_id_999/system-settings/replication-partners/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/system-settings/replication-partners/remove` | `/api/v1/storage-systems/device-type1/test_id_999/system-settings/replication-partners/remove` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/targets/{targetName}/performance-history` | `/api/v1/storage-systems/device-type1/test_id_999/targets/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/performance-history` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/telemetry` | `/api/v1/storage-systems/device-type1/test_id_999/telemetry` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/trust-certificates` | `/api/v1/storage-systems/device-type1/test_id_999/trust-certificates` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/trust-certificates` | `/api/v1/storage-systems/device-type1/test_id_999/trust-certificates` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/trust-certificates/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/trust-certificates/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/trust-certificates/remove` | `/api/v1/storage-systems/device-type1/test_id_999/trust-certificates/remove` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/vm-manager-settings` | `/api/v1/storage-systems/device-type1/test_id_999/vm-manager-settings` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/vm-manager-settings` | `/api/v1/storage-systems/device-type1/test_id_999/vm-manager-settings` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type1/{systemId}/vm-manager-settings/{vcenterSettingId}` | `/api/v1/storage-systems/device-type1/test_id_999/vm-manager-settings/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/vm-manager-settings/{vcenterSettingId}` | `/api/v1/storage-systems/device-type1/test_id_999/vm-manager-settings/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type1/{systemId}/vm-manager-settings/{vcenterSettingId}` | `/api/v1/storage-systems/device-type1/test_id_999/vm-manager-settings/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/volumes` | `/api/v1/storage-systems/device-type1/test_id_999/volumes` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/volumes` | `/api/v1/storage-systems/device-type1/test_id_999/volumes` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/volumes-performance` | `/api/v1/storage-systems/device-type1/test_id_999/volumes-performance` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/volumes/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/volumes/test_id_999` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/volumes/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/capacity-history` | `/api/v1/storage-systems/device-type1/test_id_999/volumes/test_id_999/capacity-history` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/clone` | `/api/v1/storage-systems/device-type1/test_id_999/volumes/test_id_999/clone` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/export` | `/api/v1/storage-systems/device-type1/test_id_999/volumes/test_id_999/export` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/performance-history` | `/api/v1/storage-systems/device-type1/test_id_999/volumes/test_id_999/performance-history` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/performance-statistics` | `/api/v1/storage-systems/device-type1/test_id_999/volumes/test_id_999/performance-statistics` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/snapshots` | `/api/v1/storage-systems/device-type1/test_id_999/volumes/test_id_999/snapshots` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/snapshots` | `/api/v1/storage-systems/device-type1/test_id_999/volumes/test_id_999/snapshots` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/un-export` | `/api/v1/storage-systems/device-type1/test_id_999/volumes/test_id_999/un-export` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/vluns` | `/api/v1/storage-systems/device-type1/test_id_999/volumes/test_id_999/vluns` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/clones` | `/api/v1/storage-systems/device-type1/test_id_999/volumes/test_id_999/clones` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/clones/{cloneId}/promote` | `/api/v1/storage-systems/device-type1/test_id_999/volumes/test_id_999/clones/test_id_999/promote` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/clones/{cloneId}/resync` | `/api/v1/storage-systems/device-type1/test_id_999/volumes/test_id_999/clones/test_id_999/resync` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}` | `/api/v1/storage-systems/device-type1/test_id_999/volumes/test_id_999/snapshots/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}` | `/api/v1/storage-systems/device-type1/test_id_999/volumes/test_id_999/snapshots/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}` | `/api/v1/storage-systems/device-type1/test_id_999/volumes/test_id_999/snapshots/test_id_999` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/vluns/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/volumes/test_id_999/vluns/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/vluns/{id}` | `/api/v1/storage-systems/device-type1/test_id_999/volumes/test_id_999/vluns/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2` | `/api/v1/storage-systems/device-type2` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}` | `/api/v1/storage-systems/device-type2/test_id_999` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type2/{systemId}` | `/api/v1/storage-systems/device-type2/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/access-control-records` | `/api/v1/storage-systems/device-type2/test_id_999/access-control-records` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/access-control-records` | `/api/v1/storage-systems/device-type2/test_id_999/access-control-records` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type2/{systemId}/access-control-records/{accessControlRecordId}` | `/api/v1/storage-systems/device-type2/test_id_999/access-control-records/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/access-control-records/{accessControlRecordId}` | `/api/v1/storage-systems/device-type2/test_id_999/access-control-records/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type2/{systemId}/access-control-records/{accessControlRecordId}` | `/api/v1/storage-systems/device-type2/test_id_999/access-control-records/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/actions/merge` | `/api/v1/storage-systems/device-type2/test_id_999/actions/merge` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/alarms` | `/api/v1/storage-systems/device-type2/test_id_999/alarms` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/alarms/{alarmId}` | `/api/v1/storage-systems/device-type2/test_id_999/alarms/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/application-servers` | `/api/v1/storage-systems/device-type2/test_id_999/application-servers` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/application-servers` | `/api/v1/storage-systems/device-type2/test_id_999/application-servers` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type2/{systemId}/application-servers/{applicationServerId}` | `/api/v1/storage-systems/device-type2/test_id_999/application-servers/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/application-servers/{applicationServerId}` | `/api/v1/storage-systems/device-type2/test_id_999/application-servers/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type2/{systemId}/application-servers/{applicationServerId}` | `/api/v1/storage-systems/device-type2/test_id_999/application-servers/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/application-summary` | `/api/v1/storage-systems/device-type2/test_id_999/application-summary` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/applications/{id}/capacity-stats` | `/api/v1/storage-systems/device-type2/test_id_999/applications/test_id_999/capacity-stats` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/applications/capacity-stats` | `/api/v1/storage-systems/device-type2/test_id_999/applications/capacity-stats` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/arrays` | `/api/v1/storage-systems/device-type2/test_id_999/arrays` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/arrays` | `/api/v1/storage-systems/device-type2/test_id_999/arrays` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type2/{systemId}/arrays/{arrayId}` | `/api/v1/storage-systems/device-type2/test_id_999/arrays/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/arrays/{arrayId}` | `/api/v1/storage-systems/device-type2/test_id_999/arrays/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type2/{systemId}/arrays/{arrayId}` | `/api/v1/storage-systems/device-type2/test_id_999/arrays/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/arrays/{arrayId}/actions/failover` | `/api/v1/storage-systems/device-type2/test_id_999/arrays/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/actions/failover` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/autosupport/actions/send` | `/api/v1/storage-systems/device-type2/test_id_999/autosupport/actions/send` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/capacity-history` | `/api/v1/storage-systems/device-type2/test_id_999/capacity-history` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/controllers` | `/api/v1/storage-systems/device-type2/test_id_999/controllers` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/controllers/{controllerId}` | `/api/v1/storage-systems/device-type2/test_id_999/controllers/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/controllers/{controllerId}/actions/halt` | `/api/v1/storage-systems/device-type2/test_id_999/controllers/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/actions/halt` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/disks` | `/api/v1/storage-systems/device-type2/test_id_999/disks` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/disks/{diskId}` | `/api/v1/storage-systems/device-type2/test_id_999/disks/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type2/{systemId}/disks/{diskId}` | `/api/v1/storage-systems/device-type2/test_id_999/disks/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/events` | `/api/v1/storage-systems/device-type2/test_id_999/events` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/events/{eventId}` | `/api/v1/storage-systems/device-type2/test_id_999/events/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/external-key-manager` | `/api/v1/storage-systems/device-type2/test_id_999/external-key-manager` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/external-key-manager` | `/api/v1/storage-systems/device-type2/test_id_999/external-key-manager` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type2/{systemId}/external-key-manager/{externalKeyManagerId}` | `/api/v1/storage-systems/device-type2/test_id_999/external-key-manager/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/external-key-manager/{externalKeyManagerId}` | `/api/v1/storage-systems/device-type2/test_id_999/external-key-manager/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type2/{systemId}/external-key-manager/{externalKeyManagerId}` | `/api/v1/storage-systems/device-type2/test_id_999/external-key-manager/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/external-key-manager/{externalKeyManagerId}/actions/migrate` | `/api/v1/storage-systems/device-type2/test_id_999/external-key-manager/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/actions/migrate` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/external-key-manager/{externalKeyManagerId}/actions/remove` | `/api/v1/storage-systems/device-type2/test_id_999/external-key-manager/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/actions/remove` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/fibre-channel-configs` | `/api/v1/storage-systems/device-type2/test_id_999/fibre-channel-configs` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/fibre-channel-configs/{fcConfigId}` | `/api/v1/storage-systems/device-type2/test_id_999/fibre-channel-configs/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/fibre-channel-interfaces` | `/api/v1/storage-systems/device-type2/test_id_999/fibre-channel-interfaces` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/fibre-channel-sessions` | `/api/v1/storage-systems/device-type2/test_id_999/fibre-channel-sessions` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/fibre-channel-sessions/{fcSessionId}` | `/api/v1/storage-systems/device-type2/test_id_999/fibre-channel-sessions/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/folders` | `/api/v1/storage-systems/device-type2/test_id_999/folders` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/folders` | `/api/v1/storage-systems/device-type2/test_id_999/folders` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type2/{systemId}/folders/{folderId}` | `/api/v1/storage-systems/device-type2/test_id_999/folders/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/folders/{folderId}` | `/api/v1/storage-systems/device-type2/test_id_999/folders/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type2/{systemId}/folders/{folderId}` | `/api/v1/storage-systems/device-type2/test_id_999/folders/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/folders/{folderId}/attach` | `/api/v1/storage-systems/device-type2/test_id_999/folders/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/attach` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/health-status` | `/api/v1/storage-systems/device-type2/test_id_999/health-status` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/health-status/{healthStatusId}` | `/api/v1/storage-systems/device-type2/test_id_999/health-status/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/host-groups` | `/api/v1/storage-systems/device-type2/test_id_999/host-groups` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/host-groups` | `/api/v1/storage-systems/device-type2/test_id_999/host-groups` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type2/{systemId}/host-groups/{hostInitiatorGroupId}` | `/api/v1/storage-systems/device-type2/test_id_999/host-groups/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/host-groups/{hostInitiatorGroupId}` | `/api/v1/storage-systems/device-type2/test_id_999/host-groups/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type2/{systemId}/host-groups/{hostInitiatorGroupId}` | `/api/v1/storage-systems/device-type2/test_id_999/host-groups/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/host-initiators` | `/api/v1/storage-systems/device-type2/test_id_999/host-initiators` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/host-initiators` | `/api/v1/storage-systems/device-type2/test_id_999/host-initiators` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type2/{systemId}/host-initiators/{hostInitiatorId}` | `/api/v1/storage-systems/device-type2/test_id_999/host-initiators/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/host-initiators/{hostInitiatorId}` | `/api/v1/storage-systems/device-type2/test_id_999/host-initiators/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/local-key-manager` | `/api/v1/storage-systems/device-type2/test_id_999/local-key-manager` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/local-key-manager` | `/api/v1/storage-systems/device-type2/test_id_999/local-key-manager` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type2/{systemId}/local-key-manager/{localKeyManagerId}` | `/api/v1/storage-systems/device-type2/test_id_999/local-key-manager/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/local-key-manager/{localKeyManagerId}` | `/api/v1/storage-systems/device-type2/test_id_999/local-key-manager/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type2/{systemId}/local-key-manager/{localKeyManagerId}` | `/api/v1/storage-systems/device-type2/test_id_999/local-key-manager/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type2/{systemId}/mail-settings` | `/api/v1/storage-systems/device-type2/test_id_999/mail-settings` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/network-interfaces` | `/api/v1/storage-systems/device-type2/test_id_999/network-interfaces` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/network-interfaces/{networkInterfaceId}` | `/api/v1/storage-systems/device-type2/test_id_999/network-interfaces/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/network-settings` | `/api/v1/storage-systems/device-type2/test_id_999/network-settings` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/network-settings/{networkSettingId}` | `/api/v1/storage-systems/device-type2/test_id_999/network-settings/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type2/{systemId}/network-settings/{networkSettingId}` | `/api/v1/storage-systems/device-type2/test_id_999/network-settings/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/performance-history` | `/api/v1/storage-systems/device-type2/test_id_999/performance-history` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/performance-policies` | `/api/v1/storage-systems/device-type2/test_id_999/performance-policies` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/performance-policies` | `/api/v1/storage-systems/device-type2/test_id_999/performance-policies` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type2/{systemId}/performance-policies/{performancePolicyId}` | `/api/v1/storage-systems/device-type2/test_id_999/performance-policies/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/performance-policies/{performancePolicyId}` | `/api/v1/storage-systems/device-type2/test_id_999/performance-policies/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type2/{systemId}/performance-policies/{performancePolicyId}` | `/api/v1/storage-systems/device-type2/test_id_999/performance-policies/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/pools-performance` | `/api/v1/storage-systems/device-type2/test_id_999/pools-performance` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/ports` | `/api/v1/storage-systems/device-type2/test_id_999/ports` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/ports/{portId}` | `/api/v1/storage-systems/device-type2/test_id_999/ports/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type2/{systemId}/ports/{portId}` | `/api/v1/storage-systems/device-type2/test_id_999/ports/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/protection-templates` | `/api/v1/storage-systems/device-type2/test_id_999/protection-templates` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/protection-templates` | `/api/v1/storage-systems/device-type2/test_id_999/protection-templates` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/protection-templates/{protectionTemplateId}` | `/api/v1/storage-systems/device-type2/test_id_999/protection-templates/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type2/{systemId}/protection-templates/{protectionTemplateId}` | `/api/v1/storage-systems/device-type2/test_id_999/protection-templates/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/protection-templates/remove` | `/api/v1/storage-systems/device-type2/test_id_999/protection-templates/remove` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/provisioning` | `/api/v1/storage-systems/device-type2/test_id_999/provisioning` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/provisioning-review` | `/api/v1/storage-systems/device-type2/test_id_999/provisioning-review` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/shelves` | `/api/v1/storage-systems/device-type2/test_id_999/shelves` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/shelves/{shelfId}` | `/api/v1/storage-systems/device-type2/test_id_999/shelves/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/shelves/{shelfId}/actions/locate` | `/api/v1/storage-systems/device-type2/test_id_999/shelves/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/actions/locate` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type2/{systemId}/shelves/actions/activate` | `/api/v1/storage-systems/device-type2/test_id_999/shelves/actions/activate` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/snapshot-collections/{snapshotCollectionId}/actions/clone` | `/api/v1/storage-systems/device-type2/test_id_999/snapshot-collections/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/actions/clone` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/snapshots/actions/update` | `/api/v1/storage-systems/device-type2/test_id_999/snapshots/actions/update` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/storage-pools` | `/api/v1/storage-systems/device-type2/test_id_999/storage-pools` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/storage-pools` | `/api/v1/storage-systems/device-type2/test_id_999/storage-pools` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}` | `/api/v1/storage-systems/device-type2/test_id_999/storage-pools/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}` | `/api/v1/storage-systems/device-type2/test_id_999/storage-pools/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}` | `/api/v1/storage-systems/device-type2/test_id_999/storage-pools/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}/actions/merge` | `/api/v1/storage-systems/device-type2/test_id_999/storage-pools/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/actions/merge` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}/capacity-history` | `/api/v1/storage-systems/device-type2/test_id_999/storage-pools/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/capacity-history` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}/performance-history` | `/api/v1/storage-systems/device-type2/test_id_999/storage-pools/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/performance-history` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}/performance-statistics` | `/api/v1/storage-systems/device-type2/test_id_999/storage-pools/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/performance-statistics` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type2/{systemId}/system-settings` | `/api/v1/storage-systems/device-type2/test_id_999/system-settings` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners` | `/api/v1/storage-systems/device-type2/test_id_999/system-settings/replication-partners` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners` | `/api/v1/storage-systems/device-type2/test_id_999/system-settings/replication-partners` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners/{replicationpartnerId}` | `/api/v1/storage-systems/device-type2/test_id_999/system-settings/replication-partners/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners/{replicationpartnerId}` | `/api/v1/storage-systems/device-type2/test_id_999/system-settings/replication-partners/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners/actions/pause` | `/api/v1/storage-systems/device-type2/test_id_999/system-settings/replication-partners/actions/pause` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners/actions/resume` | `/api/v1/storage-systems/device-type2/test_id_999/system-settings/replication-partners/actions/resume` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners/actions/test` | `/api/v1/storage-systems/device-type2/test_id_999/system-settings/replication-partners/actions/test` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners/remove` | `/api/v1/storage-systems/device-type2/test_id_999/system-settings/replication-partners/remove` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/system-settings/witnesses` | `/api/v1/storage-systems/device-type2/test_id_999/system-settings/witnesses` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/system-settings/witnesses` | `/api/v1/storage-systems/device-type2/test_id_999/system-settings/witnesses` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type2/{systemId}/system-settings/witnesses/{witnessId}` | `/api/v1/storage-systems/device-type2/test_id_999/system-settings/witnesses/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/system-settings/witnesses/{witnessId}` | `/api/v1/storage-systems/device-type2/test_id_999/system-settings/witnesses/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/system-settings/witnesses/{witnessId}/actions/test` | `/api/v1/storage-systems/device-type2/test_id_999/system-settings/witnesses/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/actions/test` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/uninitialized-arrays` | `/api/v1/storage-systems/device-type2/test_id_999/uninitialized-arrays` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/uninitialized-arrays/{uninitializedArrayId}` | `/api/v1/storage-systems/device-type2/test_id_999/uninitialized-arrays/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/volume-collections` | `/api/v1/storage-systems/device-type2/test_id_999/volume-collections` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/volume-collections` | `/api/v1/storage-systems/device-type2/test_id_999/volume-collections` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}` | `/api/v1/storage-systems/device-type2/test_id_999/volume-collections/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}` | `/api/v1/storage-systems/device-type2/test_id_999/volume-collections/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}` | `/api/v1/storage-systems/device-type2/test_id_999/volume-collections/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/actions/abort-handover` | `/api/v1/storage-systems/device-type2/test_id_999/volume-collections/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/actions/abort-handover` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/actions/add-volumes` | `/api/v1/storage-systems/device-type2/test_id_999/volume-collections/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/actions/add-volumes` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/actions/demote` | `/api/v1/storage-systems/device-type2/test_id_999/volume-collections/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/actions/demote` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/actions/handover` | `/api/v1/storage-systems/device-type2/test_id_999/volume-collections/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/actions/handover` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/actions/promote` | `/api/v1/storage-systems/device-type2/test_id_999/volume-collections/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/actions/promote` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/actions/remove-volumes` | `/api/v1/storage-systems/device-type2/test_id_999/volume-collections/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/actions/remove-volumes` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/snapshot-collections` | `/api/v1/storage-systems/device-type2/test_id_999/volume-collections/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/snapshot-collections` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/snapshot-collections` | `/api/v1/storage-systems/device-type2/test_id_999/volume-collections/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/snapshot-collections` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/snapshot-collections/{snapshotCollectionId}` | `/api/v1/storage-systems/device-type2/test_id_999/volume-collections/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/snapshot-collections/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/snapshot-collections/remove` | `/api/v1/storage-systems/device-type2/test_id_999/volume-collections/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/snapshot-collections/remove` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/snapshot-collections/update` | `/api/v1/storage-systems/device-type2/test_id_999/volume-collections/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/snapshot-collections/update` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/volumes` | `/api/v1/storage-systems/device-type2/test_id_999/volumes` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/volumes` | `/api/v1/storage-systems/device-type2/test_id_999/volumes` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/volumes-performance` | `/api/v1/storage-systems/device-type2/test_id_999/volumes-performance` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}` | `/api/v1/storage-systems/device-type2/test_id_999/volumes/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}` | `/api/v1/storage-systems/device-type2/test_id_999/volumes/test_id_999` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}` | `/api/v1/storage-systems/device-type2/test_id_999/volumes/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/actions/move` | `/api/v1/storage-systems/device-type2/test_id_999/volumes/test_id_999/actions/move` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/actions/restore` | `/api/v1/storage-systems/device-type2/test_id_999/volumes/test_id_999/actions/restore` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/capacity-history` | `/api/v1/storage-systems/device-type2/test_id_999/volumes/test_id_999/capacity-history` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/clone` | `/api/v1/storage-systems/device-type2/test_id_999/volumes/test_id_999/clone` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/export` | `/api/v1/storage-systems/device-type2/test_id_999/volumes/test_id_999/export` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/performance-history` | `/api/v1/storage-systems/device-type2/test_id_999/volumes/test_id_999/performance-history` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/performance-statistics` | `/api/v1/storage-systems/device-type2/test_id_999/volumes/test_id_999/performance-statistics` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/snapshots` | `/api/v1/storage-systems/device-type2/test_id_999/volumes/test_id_999/snapshots` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/snapshots` | `/api/v1/storage-systems/device-type2/test_id_999/volumes/test_id_999/snapshots` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}` | `/api/v1/storage-systems/device-type2/test_id_999/volumes/test_id_999/snapshots/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}` | `/api/v1/storage-systems/device-type2/test_id_999/volumes/test_id_999/snapshots/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}/export` | `/api/v1/storage-systems/device-type2/test_id_999/volumes/test_id_999/snapshots/test_id_999/export` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}/un-export` | `/api/v1/storage-systems/device-type2/test_id_999/volumes/test_id_999/snapshots/test_id_999/un-export` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/un-export` | `/api/v1/storage-systems/device-type2/test_id_999/volumes/test_id_999/un-export` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4` | `/api/v1/storage-systems/device-type4` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{id}` | `/api/v1/storage-systems/device-type4/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{id}` | `/api/v1/storage-systems/device-type4/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/alert-contacts` | `/api/v1/storage-systems/device-type4/test_id_999/alert-contacts` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/alert-contacts` | `/api/v1/storage-systems/device-type4/test_id_999/alert-contacts` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type4/{systemId}/alert-contacts/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/alert-contacts/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/alert-contacts/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/alert-contacts/test_id_999` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type4/{systemId}/alert-contacts/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/alert-contacts/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/application-summary` | `/api/v1/storage-systems/device-type4/test_id_999/application-summary` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/applicationsets` | `/api/v1/storage-systems/device-type4/test_id_999/applicationsets` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/applicationsets` | `/api/v1/storage-systems/device-type4/test_id_999/applicationsets` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/export` | `/api/v1/storage-systems/device-type4/test_id_999/applicationsets/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/export` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/replication-partners` | `/api/v1/storage-systems/device-type4/test_id_999/applicationsets/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/replication-partners` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/replication-partners/{replicationPartnerId}/volumes` | `/api/v1/storage-systems/device-type4/test_id_999/applicationsets/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/replication-partners/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/volumes` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/snapsets/{snapsetId}` | `/api/v1/storage-systems/device-type4/test_id_999/applicationsets/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/snapsets/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/snapsets/{snapsetId}` | `/api/v1/storage-systems/device-type4/test_id_999/applicationsets/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/snapsets/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/un-export` | `/api/v1/storage-systems/device-type4/test_id_999/applicationsets/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/un-export` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/volumes` | `/api/v1/storage-systems/device-type4/test_id_999/applicationsets/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/volumes` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/applicationsets/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/applicationsets/test_id_999` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/applicationsets/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/capacity-statistics` | `/api/v1/storage-systems/device-type4/test_id_999/applicationsets/test_id_999/capacity-statistics` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/performance` | `/api/v1/storage-systems/device-type4/test_id_999/applicationsets/test_id_999/performance` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/protection-policies` | `/api/v1/storage-systems/device-type4/test_id_999/applicationsets/test_id_999/protection-policies` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/protection-policies` | `/api/v1/storage-systems/device-type4/test_id_999/applicationsets/test_id_999/protection-policies` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/protection-policies` | `/api/v1/storage-systems/device-type4/test_id_999/applicationsets/test_id_999/protection-policies` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/protection-policies/fix` | `/api/v1/storage-systems/device-type4/test_id_999/applicationsets/test_id_999/protection-policies/fix` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/protection-policies/remove` | `/api/v1/storage-systems/device-type4/test_id_999/applicationsets/test_id_999/protection-policies/remove` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/proximity-settings` | `/api/v1/storage-systems/device-type4/test_id_999/applicationsets/test_id_999/proximity-settings` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/proximity-settings` | `/api/v1/storage-systems/device-type4/test_id_999/applicationsets/test_id_999/proximity-settings` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/remote-protection/actions` | `/api/v1/storage-systems/device-type4/test_id_999/applicationsets/test_id_999/remote-protection/actions` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/snapsets` | `/api/v1/storage-systems/device-type4/test_id_999/applicationsets/test_id_999/snapsets` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/snapsets` | `/api/v1/storage-systems/device-type4/test_id_999/applicationsets/test_id_999/snapsets` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/supported-protection` | `/api/v1/storage-systems/device-type4/test_id_999/applicationsets/test_id_999/supported-protection` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/capacity-forecast` | `/api/v1/storage-systems/device-type4/test_id_999/capacity-forecast` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/capacity-history` | `/api/v1/storage-systems/device-type4/test_id_999/capacity-history` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/capacity-summary` | `/api/v1/storage-systems/device-type4/test_id_999/capacity-summary` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/capacity-timeuntilfull` | `/api/v1/storage-systems/device-type4/test_id_999/capacity-timeuntilfull` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/certificates` | `/api/v1/storage-systems/device-type4/test_id_999/certificates` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/certificates` | `/api/v1/storage-systems/device-type4/test_id_999/certificates` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/certificates/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/certificates/test_id_999` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type4/{systemId}/certificates/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/certificates/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/certificates/remove` | `/api/v1/storage-systems/device-type4/test_id_999/certificates/remove` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/collect-support-data` | `/api/v1/storage-systems/device-type4/test_id_999/collect-support-data` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/component-performance-statistics` | `/api/v1/storage-systems/device-type4/test_id_999/component-performance-statistics` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/enclosure-cards` | `/api/v1/storage-systems/device-type4/test_id_999/enclosure-cards` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/enclosure-connectors` | `/api/v1/storage-systems/device-type4/test_id_999/enclosure-connectors` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/enclosures` | `/api/v1/storage-systems/device-type4/test_id_999/enclosures` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/enclosures/{cageId}/disks` | `/api/v1/storage-systems/device-type4/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/disks` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/enclosures/{cageId}/disks/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/disks/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-card-ports` | `/api/v1/storage-systems/device-type4/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-card-ports` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-card-ports/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-card-ports/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-cards` | `/api/v1/storage-systems/device-type4/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-cards` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-cards/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-cards/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-cards/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-cards/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-connectors` | `/api/v1/storage-systems/device-type4/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-connectors` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-connectors/{enclosureConnectorId}` | `/api/v1/storage-systems/device-type4/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-connectors/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-disks` | `/api/v1/storage-systems/device-type4/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-disks` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-disks/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-disks/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-powers` | `/api/v1/storage-systems/device-type4/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-powers` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-powers/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-powers/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-sleds` | `/api/v1/storage-systems/device-type4/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-sleds` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-sleds/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-sleds/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-sleds/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/enclosures/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/enclosure-sleds/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/enclosures/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/enclosures/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/enclosures/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/enclosures/test_id_999` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type4/{systemId}/enclosures/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/enclosures/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/encryption/backup` | `/api/v1/storage-systems/device-type4/test_id_999/encryption/backup` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/encryption/checkekm` | `/api/v1/storage-systems/device-type4/test_id_999/encryption/checkekm` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/encryption/enable` | `/api/v1/storage-systems/device-type4/test_id_999/encryption/enable` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/encryption/rekey` | `/api/v1/storage-systems/device-type4/test_id_999/encryption/rekey` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/encryption/restore` | `/api/v1/storage-systems/device-type4/test_id_999/encryption/restore` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/encryption/setekm` | `/api/v1/storage-systems/device-type4/test_id_999/encryption/setekm` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/encryption/setekm/backup` | `/api/v1/storage-systems/device-type4/test_id_999/encryption/setekm/backup` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/file-shares` | `/api/v1/storage-systems/device-type4/test_id_999/file-shares` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/file-shares` | `/api/v1/storage-systems/device-type4/test_id_999/file-shares` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type4/{systemId}/file-shares/{fileShareId}` | `/api/v1/storage-systems/device-type4/test_id_999/file-shares/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/file-shares/{fileShareId}` | `/api/v1/storage-systems/device-type4/test_id_999/file-shares/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| PATCH | `/api/v1/storage-systems/device-type4/{systemId}/file-shares/{fileShareId}` | `/api/v1/storage-systems/device-type4/test_id_999/file-shares/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/filesystems` | `/api/v1/storage-systems/device-type4/test_id_999/filesystems` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type4/{systemId}/filesystems/{filesystemId}` | `/api/v1/storage-systems/device-type4/test_id_999/filesystems/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/filesystems/{filesystemId}` | `/api/v1/storage-systems/device-type4/test_id_999/filesystems/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/filesystems/{filesystemId}/capacity-history` | `/api/v1/storage-systems/device-type4/test_id_999/filesystems/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/capacity-history` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/filesystems/{filesystemId}/performance-history` | `/api/v1/storage-systems/device-type4/test_id_999/filesystems/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/performance-history` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/host-paths` | `/api/v1/storage-systems/device-type4/test_id_999/host-paths` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/host-paths/{hostPathId}` | `/api/v1/storage-systems/device-type4/test_id_999/host-paths/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/host-sets` | `/api/v1/storage-systems/device-type4/test_id_999/host-sets` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/host-sets/{hostSetId}` | `/api/v1/storage-systems/device-type4/test_id_999/host-sets/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/hosts` | `/api/v1/storage-systems/device-type4/test_id_999/hosts` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/hosts/{hostId}` | `/api/v1/storage-systems/device-type4/test_id_999/hosts/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/insights/headroom-contribution` | `/api/v1/storage-systems/device-type4/test_id_999/insights/headroom-contribution` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/insights/hotspots` | `/api/v1/storage-systems/device-type4/test_id_999/insights/hotspots` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/insights/latencyfactors` | `/api/v1/storage-systems/device-type4/test_id_999/insights/latencyfactors` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/insights/resource-contention` | `/api/v1/storage-systems/device-type4/test_id_999/insights/resource-contention` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/inventory-history` | `/api/v1/storage-systems/device-type4/test_id_999/inventory-history` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/inventory-history/{inventoryUpdateId}` | `/api/v1/storage-systems/device-type4/test_id_999/inventory-history/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/licenses` | `/api/v1/storage-systems/device-type4/test_id_999/licenses` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/licenses` | `/api/v1/storage-systems/device-type4/test_id_999/licenses` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type4/{systemId}/mail-settings` | `/api/v1/storage-systems/device-type4/test_id_999/mail-settings` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/mail-settings` | `/api/v1/storage-systems/device-type4/test_id_999/mail-settings` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/mail-settings` | `/api/v1/storage-systems/device-type4/test_id_999/mail-settings` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type4/{systemId}/mail-settings` | `/api/v1/storage-systems/device-type4/test_id_999/mail-settings` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/network-services/cim` | `/api/v1/storage-systems/device-type4/test_id_999/network-services/cim` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type4/{systemId}/network-services/cim` | `/api/v1/storage-systems/device-type4/test_id_999/network-services/cim` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-mgr` | `/api/v1/storage-systems/device-type4/test_id_999/network-services/snmp-mgr` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-mgr` | `/api/v1/storage-systems/device-type4/test_id_999/network-services/snmp-mgr` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-mgr/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/network-services/snmp-mgr/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-mgr/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/network-services/snmp-mgr/test_id_999` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-mgr/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/network-services/snmp-mgr/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-users` | `/api/v1/storage-systems/device-type4/test_id_999/network-services/snmp-users` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-users/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/network-services/snmp-users/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/network-services/vasa` | `/api/v1/storage-systems/device-type4/test_id_999/network-services/vasa` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/network-services/vasa/{vasaId}` | `/api/v1/storage-systems/device-type4/test_id_999/network-services/vasa/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/network-services/vasa/{vasaId}/services` | `/api/v1/storage-systems/device-type4/test_id_999/network-services/vasa/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/services` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/network-settings` | `/api/v1/storage-systems/device-type4/test_id_999/network-settings` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/network-settings` | `/api/v1/storage-systems/device-type4/test_id_999/network-settings` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/network-settings/vasaprovider` | `/api/v1/storage-systems/device-type4/test_id_999/network-settings/vasaprovider` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/network-settings/vasaprovider/clear` | `/api/v1/storage-systems/device-type4/test_id_999/network-settings/vasaprovider/clear` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/nodes` | `/api/v1/storage-systems/device-type4/test_id_999/nodes` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/nodes/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/nodes/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/nodes/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/nodes/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/nodes/{nodeId}/component-performance-statistics` | `/api/v1/storage-systems/device-type4/test_id_999/nodes/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/component-performance-statistics` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/nodes/{nodeId}/service-ports` | `/api/v1/storage-systems/device-type4/test_id_999/nodes/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/service-ports` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/nodes/service-ports` | `/api/v1/storage-systems/device-type4/test_id_999/nodes/service-ports` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/performance-history` | `/api/v1/storage-systems/device-type4/test_id_999/performance-history` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/performance-statistics` | `/api/v1/storage-systems/device-type4/test_id_999/performance-statistics` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/physicaldrives-performance` | `/api/v1/storage-systems/device-type4/test_id_999/physicaldrives-performance` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/ports` | `/api/v1/storage-systems/device-type4/test_id_999/ports` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/ports-performance` | `/api/v1/storage-systems/device-type4/test_id_999/ports-performance` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/ports/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/ports/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/ports/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/ports/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/clear` | `/api/v1/storage-systems/device-type4/test_id_999/ports/test_id_999/clear` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/edit-file` | `/api/v1/storage-systems/device-type4/test_id_999/ports/test_id_999/edit-file` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/edit-iscsi` | `/api/v1/storage-systems/device-type4/test_id_999/ports/test_id_999/edit-iscsi` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/edit-nvme` | `/api/v1/storage-systems/device-type4/test_id_999/ports/test_id_999/edit-nvme` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/edit-rcip` | `/api/v1/storage-systems/device-type4/test_id_999/ports/test_id_999/edit-rcip` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/fc` | `/api/v1/storage-systems/device-type4/test_id_999/ports/test_id_999/fc` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/initialize` | `/api/v1/storage-systems/device-type4/test_id_999/ports/test_id_999/initialize` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/ping-file` | `/api/v1/storage-systems/device-type4/test_id_999/ports/test_id_999/ping-file` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/ping-iscsi` | `/api/v1/storage-systems/device-type4/test_id_999/ports/test_id_999/ping-iscsi` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/ping-nvme` | `/api/v1/storage-systems/device-type4/test_id_999/ports/test_id_999/ping-nvme` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/ping-rcip` | `/api/v1/storage-systems/device-type4/test_id_999/ports/test_id_999/ping-rcip` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/remotecopylinks-performance` | `/api/v1/storage-systems/device-type4/test_id_999/remotecopylinks-performance` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/share-settings` | `/api/v1/storage-systems/device-type4/test_id_999/share-settings` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/share-settings/{sharesettingsId}` | `/api/v1/storage-systems/device-type4/test_id_999/share-settings/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/snapshots/{childSnapshotId}/restore-options` | `/api/v1/storage-systems/device-type4/test_id_999/snapshots/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/restore-options` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/snapshots/{parentSnapshotId}/snapshots/{childSnapshotId}/restore` | `/api/v1/storage-systems/device-type4/test_id_999/snapshots/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/snapshots/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/restore` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/snapshots/{snapshotId}/clone` | `/api/v1/storage-systems/device-type4/test_id_999/snapshots/test_id_999/clone` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/snapshots/{snapshotId}/export` | `/api/v1/storage-systems/device-type4/test_id_999/snapshots/test_id_999/export` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/snapshots/{snapshotId}/snapshots` | `/api/v1/storage-systems/device-type4/test_id_999/snapshots/test_id_999/snapshots` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/snapshots/{snapshotId}/un-export` | `/api/v1/storage-systems/device-type4/test_id_999/snapshots/test_id_999/un-export` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/snapshots/{snapshotId}/vluns` | `/api/v1/storage-systems/device-type4/test_id_999/snapshots/test_id_999/vluns` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/snapshots/{snapshotId}/vluns/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/snapshots/test_id_999/vluns/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/storage-pools` | `/api/v1/storage-systems/device-type4/test_id_999/storage-pools` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/storage-pools/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/storage-pools/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/storage-pools/{id}/volumes` | `/api/v1/storage-systems/device-type4/test_id_999/storage-pools/test_id_999/volumes` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/support-settings` | `/api/v1/storage-systems/device-type4/test_id_999/support-settings` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/support-settings` | `/api/v1/storage-systems/device-type4/test_id_999/support-settings` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type4/{systemId}/support-settings` | `/api/v1/storage-systems/device-type4/test_id_999/support-settings` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/sustainabilityMetrics` | `/api/v1/storage-systems/device-type4/test_id_999/sustainabilityMetrics` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/switch-ports` | `/api/v1/storage-systems/device-type4/test_id_999/switch-ports` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/switches` | `/api/v1/storage-systems/device-type4/test_id_999/switches` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/switches/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/switches/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/switches/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/switches/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-fans` | `/api/v1/storage-systems/device-type4/test_id_999/switches/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/switch-fans` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-fans/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/switches/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/switch-fans/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-ports` | `/api/v1/storage-systems/device-type4/test_id_999/switches/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/switch-ports` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-ports/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/switches/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/switch-ports/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-ps` | `/api/v1/storage-systems/device-type4/test_id_999/switches/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/switch-ps` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-ps/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/switches/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/switch-ps/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/system-settings` | `/api/v1/storage-systems/device-type4/test_id_999/system-settings` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/system-settings` | `/api/v1/storage-systems/device-type4/test_id_999/system-settings` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type4/{systemId}/system-settings` | `/api/v1/storage-systems/device-type4/test_id_999/system-settings` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvol` | `/api/v1/storage-systems/device-type4/test_id_999/system-settings/management-services/vvol` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvolscs` | `/api/v1/storage-systems/device-type4/test_id_999/system-settings/management-services/vvolscs` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvolscs` | `/api/v1/storage-systems/device-type4/test_id_999/system-settings/management-services/vvolscs` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvolscs/{vvolscId}` | `/api/v1/storage-systems/device-type4/test_id_999/system-settings/management-services/vvolscs/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvolscs/{vvolscId}` | `/api/v1/storage-systems/device-type4/test_id_999/system-settings/management-services/vvolscs/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvolscs/{vvolscId}/attach` | `/api/v1/storage-systems/device-type4/test_id_999/system-settings/management-services/vvolscs/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/attach` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvolscs/{vvolscId}/detach` | `/api/v1/storage-systems/device-type4/test_id_999/system-settings/management-services/vvolscs/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785/detach` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/system-settings/quorum-witness` | `/api/v1/storage-systems/device-type4/test_id_999/system-settings/quorum-witness` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/system-settings/quorum-witness` | `/api/v1/storage-systems/device-type4/test_id_999/system-settings/quorum-witness` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type4/{systemId}/system-settings/quorum-witness/{replicationPartnerId}` | `/api/v1/storage-systems/device-type4/test_id_999/system-settings/quorum-witness/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/system-settings/quorum-witness/{replicationPartnerId}` | `/api/v1/storage-systems/device-type4/test_id_999/system-settings/quorum-witness/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type4/{systemId}/system-settings/quorum-witness/{replicationPartnerId}` | `/api/v1/storage-systems/device-type4/test_id_999/system-settings/quorum-witness/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/system-settings/replication-partners` | `/api/v1/storage-systems/device-type4/test_id_999/system-settings/replication-partners` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/system-settings/replication-partners` | `/api/v1/storage-systems/device-type4/test_id_999/system-settings/replication-partners` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/system-settings/replication-partners/{replicationPartnerId}` | `/api/v1/storage-systems/device-type4/test_id_999/system-settings/replication-partners/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type4/{systemId}/system-settings/replication-partners/{replicationPartnerId}` | `/api/v1/storage-systems/device-type4/test_id_999/system-settings/replication-partners/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/system-settings/replication-partners/remove` | `/api/v1/storage-systems/device-type4/test_id_999/system-settings/replication-partners/remove` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/telemetry` | `/api/v1/storage-systems/device-type4/test_id_999/telemetry` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/trust-certificates` | `/api/v1/storage-systems/device-type4/test_id_999/trust-certificates` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/trust-certificates` | `/api/v1/storage-systems/device-type4/test_id_999/trust-certificates` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/trust-certificates/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/trust-certificates/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/trust-certificates/remove` | `/api/v1/storage-systems/device-type4/test_id_999/trust-certificates/remove` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/vm-manager-settings` | `/api/v1/storage-systems/device-type4/test_id_999/vm-manager-settings` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/vm-manager-settings` | `/api/v1/storage-systems/device-type4/test_id_999/vm-manager-settings` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type4/{systemId}/vm-manager-settings/{vcenterSettingId}` | `/api/v1/storage-systems/device-type4/test_id_999/vm-manager-settings/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/vm-manager-settings/{vcenterSettingId}` | `/api/v1/storage-systems/device-type4/test_id_999/vm-manager-settings/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type4/{systemId}/vm-manager-settings/{vcenterSettingId}` | `/api/v1/storage-systems/device-type4/test_id_999/vm-manager-settings/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/vme-manager-settings` | `/api/v1/storage-systems/device-type4/test_id_999/vme-manager-settings` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/vme-manager-settings` | `/api/v1/storage-systems/device-type4/test_id_999/vme-manager-settings` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type4/{systemId}/vme-manager-settings/{vmeSettingId}` | `/api/v1/storage-systems/device-type4/test_id_999/vme-manager-settings/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/vme-manager-settings/{vmeSettingId}` | `/api/v1/storage-systems/device-type4/test_id_999/vme-manager-settings/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type4/{systemId}/vme-manager-settings/{vmeSettingId}` | `/api/v1/storage-systems/device-type4/test_id_999/vme-manager-settings/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/volumes` | `/api/v1/storage-systems/device-type4/test_id_999/volumes` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/volumes` | `/api/v1/storage-systems/device-type4/test_id_999/volumes` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/volumes-performance` | `/api/v1/storage-systems/device-type4/test_id_999/volumes-performance` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/capacity-history` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999/capacity-history` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/clone` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999/clone` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/export` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999/export` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/performance-histogram` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999/performance-histogram` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/performance-history` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999/performance-history` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/performance-statistics` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999/performance-statistics` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/snapshots` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999/snapshots` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/snapshots` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999/snapshots` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/un-export` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999/un-export` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/vluns` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999/vluns` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/clones` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999/clones` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/clones/{cloneId}` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999/clones/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/clones/{cloneId}/promote` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999/clones/test_id_999/promote` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/clones/{cloneId}/resync` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999/clones/test_id_999/resync` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/insights/latency-annotations` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999/insights/latency-annotations` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/insights/performance-drifts` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999/insights/performance-drifts` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/schedules` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999/schedules` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/schedules` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999/schedules` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/schedules/{scheduleId}` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999/schedules/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/schedules/{scheduleId}` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999/schedules/test_id_999` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/schedules/{scheduleId}` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999/schedules/test_id_999` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999/snapshots/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999/snapshots/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999/snapshots/test_id_999` | 200 | SUCCESS_2XX |
| PUT | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999/snapshots/test_id_999` | 200 | SUCCESS_2XX |
| DELETE | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/vluns/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999/vluns/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/vluns/{id}` | `/api/v1/storage-systems/device-type4/test_id_999/volumes/test_id_999/vluns/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/device-type4/systemInsights/insights` | `/api/v1/storage-systems/device-type4/systemInsights/insights` | 200 | SUCCESS_2XX |
| POST | `/api/v1/storage-systems/provisioning-recommendations` | `/api/v1/storage-systems/provisioning-recommendations` | 200 | SUCCESS_2XX |
| GET | `/api/v1/storage-systems/storage-types` | `/api/v1/storage-systems/storage-types` | 200 | SUCCESS_2XX |
| GET | `/api/v1/tasks` | `/api/v1/tasks` | 200 | SUCCESS_2XX |
| GET | `/api/v1/tasks/{id}` | `/api/v1/tasks/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/volume-sets` | `/api/v1/volume-sets` | 200 | SUCCESS_2XX |
| GET | `/api/v1/volume-sets/{id}` | `/api/v1/volume-sets/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/volume-sets/{id}/volumes` | `/api/v1/volume-sets/test_id_999/volumes` | 200 | SUCCESS_2XX |
| GET | `/api/v1/volumes` | `/api/v1/volumes` | 200 | SUCCESS_2XX |
| GET | `/api/v1/volumes/{id}` | `/api/v1/volumes/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/api/v1/devices` | `/api/v1/devices` | 200 | SUCCESS_2XX |
| GET | `/api/v1/devices/{id}` | `/api/v1/devices/test_id_999` | 404 | NOT_FOUND_404 |
| POST | `/api/v1/devices` | `/api/v1/devices` | 200 | SUCCESS_2XX |
| POST | `/api/v1/devices/{id}` | `/api/v1/devices/test_id_999` | 404 | NOT_FOUND_404 |
| PUT | `/api/v1/devices/{id}` | `/api/v1/devices/test_id_999` | 404 | NOT_FOUND_404 |
| DELETE | `/api/v1/devices/{id}` | `/api/v1/devices/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/api/v1/devices/{id}` | `/api/v1/devices/test_id_999` | 404 | NOT_FOUND_404 |
| POST | `/api/v1/devices/{id}/power` | `/api/v1/devices/test_id_999/power` | 404 | NOT_FOUND_404 |
| POST | `/api/v1/devices/{id}/vms` | `/api/v1/devices/test_id_999/vms` | 422 | VALIDATION_422 |
| DELETE | `/api/v1/devices/{id}/vms/{vm_id}` | `/api/v1/devices/test_id_999/vms/6af62ce3-477f-4d7e-b3c7-c93a7bf3b785` | 404 | NOT_FOUND_404 |

</details>

<details><summary><b>COMOPS Server - 191 Endpoints (Click to Expand)</b></summary>

| Method | Original Path | Replaced Path | Status Code | Result Category |
| :--- | :--- | :--- | :--- | :--- |
| GET | `/openapi.json` | `/openapi.json` | 200 | SUCCESS_2XX |
| GET | `/docs` | `/docs` | 200 | SUCCESS_2XX |
| GET | `/docs/oauth2-redirect` | `/docs/oauth2-redirect` | 200 | SUCCESS_2XX |
| GET | `/redoc` | `/redoc` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta2/appliances/{device_id}` | `/compute-ops-mgmt/v1beta2/appliances/test_id_999` | 200 | SUCCESS_2XX |
| DELETE | `/compute-ops-mgmt/v1beta2/appliances/{device_id}` | `/compute-ops-mgmt/v1beta2/appliances/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta2/appliances/{device_id}/certificate` | `/compute-ops-mgmt/v1beta2/appliances/test_id_999/certificate` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1/appliance-firmware-bundles` | `/compute-ops-mgmt/v1/appliance-firmware-bundles` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1/appliance-firmware-bundles/{id}` | `/compute-ops-mgmt/v1/appliance-firmware-bundles/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/appliance-firmware-bundles` | `/compute-ops-mgmt/v1beta1/appliance-firmware-bundles` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/appliance-firmware-bundles/{id}` | `/compute-ops-mgmt/v1beta1/appliance-firmware-bundles/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1beta2/approval-policies` | `/compute-ops-mgmt/v1beta2/approval-policies` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta2/approval-policies` | `/compute-ops-mgmt/v1beta2/approval-policies` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta2/approval-policies/{policy_id}` | `/compute-ops-mgmt/v1beta2/approval-policies/test_id_999` | 200 | SUCCESS_2XX |
| PATCH | `/compute-ops-mgmt/v1beta2/approval-policies/{policy_id}` | `/compute-ops-mgmt/v1beta2/approval-policies/test_id_999` | 200 | SUCCESS_2XX |
| DELETE | `/compute-ops-mgmt/v1beta2/approval-policies/{policy_id}` | `/compute-ops-mgmt/v1beta2/approval-policies/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta2/approval-requests` | `/compute-ops-mgmt/v1beta2/approval-requests` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta2/approval-requests/{request_id}` | `/compute-ops-mgmt/v1beta2/approval-requests/test_id_999` | 200 | SUCCESS_2XX |
| PATCH | `/compute-ops-mgmt/v1beta2/approval-requests/{request_id}` | `/compute-ops-mgmt/v1beta2/approval-requests/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1beta2/approval-requests/{request_id}/approve` | `/compute-ops-mgmt/v1beta2/approval-requests/test_id_999/approve` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1/async-operations` | `/compute-ops-mgmt/v1/async-operations` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1/async-operations/{id}` | `/compute-ops-mgmt/v1/async-operations/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/async-operations` | `/compute-ops-mgmt/v1beta1/async-operations` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/async-operations/{id}` | `/compute-ops-mgmt/v1beta1/async-operations/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/accounts/{id}` | `/compute-ops-mgmt/v1beta1/accounts/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/accounts/{id}/tenants` | `/compute-ops-mgmt/v1beta1/accounts/test_id_999/tenants` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1beta1/activation-keys` | `/compute-ops-mgmt/v1beta1/activation-keys` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/activation-keys` | `/compute-ops-mgmt/v1beta1/activation-keys` | 200 | SUCCESS_2XX |
| DELETE | `/compute-ops-mgmt/v1beta1/activation-keys/{activation_key}` | `/compute-ops-mgmt/v1beta1/activation-keys/9e42edd9-6829-4a07-9d39-921a32bb9f95` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1beta1/activation-tokens` | `/compute-ops-mgmt/v1beta1/activation-tokens` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta2/activities` | `/compute-ops-mgmt/v1beta2/activities` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1beta1/ahs-files` | `/compute-ops-mgmt/v1beta1/ahs-files` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/ahs-files` | `/compute-ops-mgmt/v1beta1/ahs-files` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/ahs-files/{id}` | `/compute-ops-mgmt/v1beta1/ahs-files/test_id_999` | 200 | SUCCESS_2XX |
| PATCH | `/compute-ops-mgmt/v1beta1/ahs-files/{id}` | `/compute-ops-mgmt/v1beta1/ahs-files/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1beta1/ahs-files/{id}/parse` | `/compute-ops-mgmt/v1beta1/ahs-files/test_id_999/parse` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/ahs-files/{id}/download` | `/compute-ops-mgmt/v1beta1/ahs-files/test_id_999/download` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta2/appliances` | `/compute-ops-mgmt/v1beta2/appliances` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/energy-over-time` | `/compute-ops-mgmt/v1beta1/energy-over-time` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/energy-by-entity` | `/compute-ops-mgmt/v1beta1/energy-by-entity` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/external-services` | `/compute-ops-mgmt/v1beta1/external-services` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1beta1/external-services` | `/compute-ops-mgmt/v1beta1/external-services` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/external-services/{id}` | `/compute-ops-mgmt/v1beta1/external-services/test_id_999` | 200 | SUCCESS_2XX |
| DELETE | `/compute-ops-mgmt/v1beta1/external-services/{id}` | `/compute-ops-mgmt/v1beta1/external-services/test_id_999` | 200 | SUCCESS_2XX |
| PATCH | `/compute-ops-mgmt/v1beta1/external-services/{id}` | `/compute-ops-mgmt/v1beta1/external-services/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1beta1/external-services/{id}/test` | `/compute-ops-mgmt/v1beta1/external-services/test_id_999/test` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/filters` | `/compute-ops-mgmt/v1beta1/filters` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1beta1/filters` | `/compute-ops-mgmt/v1beta1/filters` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/filters/properties` | `/compute-ops-mgmt/v1beta1/filters/properties` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/filters/{id}` | `/compute-ops-mgmt/v1beta1/filters/test_id_999` | 200 | SUCCESS_2XX |
| DELETE | `/compute-ops-mgmt/v1beta1/filters/{id}` | `/compute-ops-mgmt/v1beta1/filters/test_id_999` | 200 | SUCCESS_2XX |
| PATCH | `/compute-ops-mgmt/v1beta1/filters/{id}` | `/compute-ops-mgmt/v1beta1/filters/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/filters/{id}/matches` | `/compute-ops-mgmt/v1beta1/filters/test_id_999/matches` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1/firmware-bundles` | `/compute-ops-mgmt/v1/firmware-bundles` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1/firmware-bundles/{id}` | `/compute-ops-mgmt/v1/firmware-bundles/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1/firmware-bundles/{id}/bundle-details` | `/compute-ops-mgmt/v1/firmware-bundles/test_id_999/bundle-details` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta2/firmware-bundles` | `/compute-ops-mgmt/v1beta2/firmware-bundles` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta2/firmware-bundles/{id}` | `/compute-ops-mgmt/v1beta2/firmware-bundles/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1/groups` | `/compute-ops-mgmt/v1/groups` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1/groups` | `/compute-ops-mgmt/v1/groups` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1/groups/{group-id}` | `/compute-ops-mgmt/v1/groups/test_id_999` | 404 | NOT_FOUND_404 |
| DELETE | `/compute-ops-mgmt/v1/groups/{group-id}` | `/compute-ops-mgmt/v1/groups/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/compute-ops-mgmt/v1/groups/{group-id}` | `/compute-ops-mgmt/v1/groups/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/compute-ops-mgmt/v1/groups/{group-id}/compliance` | `/compute-ops-mgmt/v1/groups/test_id_999/compliance` | 404 | NOT_FOUND_404 |
| GET | `/compute-ops-mgmt/v1/groups/{group-id}/compliance/{compliance-id}` | `/compute-ops-mgmt/v1/groups/test_id_999/compliance/9e42edd9-6829-4a07-9d39-921a32bb9f95` | 404 | NOT_FOUND_404 |
| GET | `/compute-ops-mgmt/v1/groups/{group-id}/devices` | `/compute-ops-mgmt/v1/groups/test_id_999/devices` | 404 | NOT_FOUND_404 |
| GET | `/compute-ops-mgmt/v1beta3/groups` | `/compute-ops-mgmt/v1beta3/groups` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1beta3/groups` | `/compute-ops-mgmt/v1beta3/groups` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta3/groups/{group-id}` | `/compute-ops-mgmt/v1beta3/groups/test_id_999` | 404 | NOT_FOUND_404 |
| DELETE | `/compute-ops-mgmt/v1beta3/groups/{group-id}` | `/compute-ops-mgmt/v1beta3/groups/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/compute-ops-mgmt/v1beta3/groups/{group-id}` | `/compute-ops-mgmt/v1beta3/groups/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/compute-ops-mgmt/v1beta3/groups/{group-id}/compliance` | `/compute-ops-mgmt/v1beta3/groups/test_id_999/compliance` | 404 | NOT_FOUND_404 |
| GET | `/compute-ops-mgmt/v1beta3/groups/{group-id}/compliance/{compliance-id}` | `/compute-ops-mgmt/v1beta3/groups/test_id_999/compliance/9e42edd9-6829-4a07-9d39-921a32bb9f95` | 404 | NOT_FOUND_404 |
| GET | `/compute-ops-mgmt/v1beta3/groups/{group-id}/devices` | `/compute-ops-mgmt/v1beta3/groups/test_id_999/devices` | 404 | NOT_FOUND_404 |
| GET | `/compute-ops/v1beta2/groups` | `/compute-ops/v1beta2/groups` | 200 | SUCCESS_2XX |
| POST | `/compute-ops/v1beta2/groups` | `/compute-ops/v1beta2/groups` | 200 | SUCCESS_2XX |
| GET | `/compute-ops/v1beta2/groups/{group-id}` | `/compute-ops/v1beta2/groups/test_id_999` | 404 | NOT_FOUND_404 |
| DELETE | `/compute-ops/v1beta2/groups/{group-id}` | `/compute-ops/v1beta2/groups/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/compute-ops/v1beta2/groups/{group-id}` | `/compute-ops/v1beta2/groups/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/compute-ops/v1beta2/groups/{group-id}/compliance` | `/compute-ops/v1beta2/groups/test_id_999/compliance` | 404 | NOT_FOUND_404 |
| GET | `/compute-ops/v1beta2/groups/{group-id}/compliance/{compliance-id}` | `/compute-ops/v1beta2/groups/test_id_999/compliance/9e42edd9-6829-4a07-9d39-921a32bb9f95` | 404 | NOT_FOUND_404 |
| GET | `/compute-ops/v1beta2/groups/{group-id}/devices` | `/compute-ops/v1beta2/groups/test_id_999/devices` | 404 | NOT_FOUND_404 |
| GET | `/compute-ops-mgmt/v1beta2/job-templates` | `/compute-ops-mgmt/v1beta2/job-templates` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta2/job-templates/{id}` | `/compute-ops-mgmt/v1beta2/job-templates/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1/jobs` | `/compute-ops-mgmt/v1/jobs` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1/jobs` | `/compute-ops-mgmt/v1/jobs` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1/jobs/{id}` | `/compute-ops-mgmt/v1/jobs/test_id_999` | 200 | SUCCESS_2XX |
| PATCH | `/compute-ops-mgmt/v1/jobs/{id}` | `/compute-ops-mgmt/v1/jobs/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta3/jobs` | `/compute-ops-mgmt/v1beta3/jobs` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1beta3/jobs` | `/compute-ops-mgmt/v1beta3/jobs` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta3/jobs/{id}` | `/compute-ops-mgmt/v1beta3/jobs/test_id_999` | 200 | SUCCESS_2XX |
| PATCH | `/compute-ops-mgmt/v1beta3/jobs/{id}` | `/compute-ops-mgmt/v1beta3/jobs/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta2/jobs` | `/compute-ops-mgmt/v1beta2/jobs` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1beta2/jobs` | `/compute-ops-mgmt/v1beta2/jobs` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta2/jobs/{id}` | `/compute-ops-mgmt/v1beta2/jobs/test_id_999` | 200 | SUCCESS_2XX |
| PATCH | `/compute-ops-mgmt/v1beta2/jobs/{id}` | `/compute-ops-mgmt/v1beta2/jobs/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1/metrics-configurations` | `/compute-ops-mgmt/v1/metrics-configurations` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1/metrics-configurations` | `/compute-ops-mgmt/v1/metrics-configurations` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1/metrics-configurations/{id}` | `/compute-ops-mgmt/v1/metrics-configurations/test_id_999` | 200 | SUCCESS_2XX |
| DELETE | `/compute-ops-mgmt/v1/metrics-configurations/{id}` | `/compute-ops-mgmt/v1/metrics-configurations/test_id_999` | 200 | SUCCESS_2XX |
| PATCH | `/compute-ops-mgmt/v1/metrics-configurations/{id}` | `/compute-ops-mgmt/v1/metrics-configurations/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/oneview-appliances` | `/compute-ops-mgmt/v1beta1/oneview-appliances` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1beta1/oneview-appliances` | `/compute-ops-mgmt/v1beta1/oneview-appliances` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/oneview-appliances/{device-id}` | `/compute-ops-mgmt/v1beta1/oneview-appliances/9e42edd9-6829-4a07-9d39-921a32bb9f95` | 404 | NOT_FOUND_404 |
| DELETE | `/compute-ops-mgmt/v1beta1/oneview-appliances/{device-id}` | `/compute-ops-mgmt/v1beta1/oneview-appliances/9e42edd9-6829-4a07-9d39-921a32bb9f95` | 404 | NOT_FOUND_404 |
| GET | `/compute-ops-mgmt/v1beta1/oneview-settings` | `/compute-ops-mgmt/v1beta1/oneview-settings` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/oneview-server-templates` | `/compute-ops-mgmt/v1beta1/oneview-server-templates` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/oneview-server-templates/{id}` | `/compute-ops-mgmt/v1beta1/oneview-server-templates/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta2/reports` | `/compute-ops-mgmt/v1beta2/reports` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1beta2/reports` | `/compute-ops-mgmt/v1beta2/reports` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta2/reports/{id}` | `/compute-ops-mgmt/v1beta2/reports/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta2/reports/{id}/data` | `/compute-ops-mgmt/v1beta2/reports/test_id_999/data` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta2/schedules` | `/compute-ops-mgmt/v1beta2/schedules` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1beta2/schedules` | `/compute-ops-mgmt/v1beta2/schedules` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta2/schedules/{id}` | `/compute-ops-mgmt/v1beta2/schedules/test_id_999` | 200 | SUCCESS_2XX |
| DELETE | `/compute-ops-mgmt/v1beta2/schedules/{id}` | `/compute-ops-mgmt/v1beta2/schedules/test_id_999` | 200 | SUCCESS_2XX |
| PATCH | `/compute-ops-mgmt/v1beta2/schedules/{id}` | `/compute-ops-mgmt/v1beta2/schedules/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta2/schedules/{id}/history` | `/compute-ops-mgmt/v1beta2/schedules/test_id_999/history` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta2/schedules/{id}/history/{history-id}` | `/compute-ops-mgmt/v1beta2/schedules/test_id_999/history/9e42edd9-6829-4a07-9d39-921a32bb9f95` | 404 | NOT_FOUND_404 |
| GET | `/compute-ops-mgmt/v1beta1/server-locations/{location_id}` | `/compute-ops-mgmt/v1beta1/server-locations/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1beta1/server-locations/{location_id}/servers` | `/compute-ops-mgmt/v1beta1/server-locations/test_id_999/servers` | 200 | SUCCESS_2XX |
| DELETE | `/compute-ops-mgmt/v1beta1/server-locations/{location_id}/servers` | `/compute-ops-mgmt/v1beta1/server-locations/test_id_999/servers` | 200 | SUCCESS_2XX |
| GET | `/compute-ops/v1beta1/server-settings` | `/compute-ops/v1beta1/server-settings` | 200 | SUCCESS_2XX |
| POST | `/compute-ops/v1beta1/server-settings` | `/compute-ops/v1beta1/server-settings` | 200 | SUCCESS_2XX |
| GET | `/compute-ops/v1beta1/server-settings/{id}` | `/compute-ops/v1beta1/server-settings/test_id_999` | 200 | SUCCESS_2XX |
| DELETE | `/compute-ops/v1beta1/server-settings/{id}` | `/compute-ops/v1beta1/server-settings/test_id_999` | 200 | SUCCESS_2XX |
| PATCH | `/compute-ops/v1beta1/server-settings/{id}` | `/compute-ops/v1beta1/server-settings/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1/settings` | `/compute-ops-mgmt/v1/settings` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1/settings` | `/compute-ops-mgmt/v1/settings` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1/settings/{id}` | `/compute-ops-mgmt/v1/settings/test_id_999` | 200 | SUCCESS_2XX |
| DELETE | `/compute-ops-mgmt/v1/settings/{id}` | `/compute-ops-mgmt/v1/settings/test_id_999` | 200 | SUCCESS_2XX |
| PATCH | `/compute-ops-mgmt/v1/settings/{id}` | `/compute-ops-mgmt/v1/settings/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/settings` | `/compute-ops-mgmt/v1beta1/settings` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1beta1/settings` | `/compute-ops-mgmt/v1beta1/settings` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/settings/{id}` | `/compute-ops-mgmt/v1beta1/settings/test_id_999` | 200 | SUCCESS_2XX |
| DELETE | `/compute-ops-mgmt/v1beta1/settings/{id}` | `/compute-ops-mgmt/v1beta1/settings/test_id_999` | 200 | SUCCESS_2XX |
| PATCH | `/compute-ops-mgmt/v1beta1/settings/{id}` | `/compute-ops-mgmt/v1beta1/settings/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1/servers` | `/compute-ops-mgmt/v1/servers` | 200 | SUCCESS_2XX |
| PATCH | `/compute-ops-mgmt/v1/servers` | `/compute-ops-mgmt/v1/servers` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1/servers` | `/compute-ops-mgmt/v1/servers` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1/servers/{id}` | `/compute-ops-mgmt/v1/servers/test_id_999` | 200 | SUCCESS_2XX |
| PATCH | `/compute-ops-mgmt/v1/servers/{id}` | `/compute-ops-mgmt/v1/servers/test_id_999` | 200 | SUCCESS_2XX |
| DELETE | `/compute-ops-mgmt/v1/servers/{id}` | `/compute-ops-mgmt/v1/servers/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1/servers/{id}/alerts` | `/compute-ops-mgmt/v1/servers/test_id_999/alerts` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1/servers/{id}/clear-alert` | `/compute-ops-mgmt/v1/servers/test_id_999/clear-alert` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta2/servers` | `/compute-ops-mgmt/v1beta2/servers` | 200 | SUCCESS_2XX |
| PATCH | `/compute-ops-mgmt/v1beta2/servers` | `/compute-ops-mgmt/v1beta2/servers` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1beta2/servers` | `/compute-ops-mgmt/v1beta2/servers` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta2/servers/{id}` | `/compute-ops-mgmt/v1beta2/servers/test_id_999` | 200 | SUCCESS_2XX |
| PATCH | `/compute-ops-mgmt/v1beta2/servers/{id}` | `/compute-ops-mgmt/v1beta2/servers/test_id_999` | 200 | SUCCESS_2XX |
| DELETE | `/compute-ops-mgmt/v1beta2/servers/{id}` | `/compute-ops-mgmt/v1beta2/servers/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta2/servers/{id}/alerts` | `/compute-ops-mgmt/v1beta2/servers/test_id_999/alerts` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1beta2/servers/{id}/clear-alert` | `/compute-ops-mgmt/v1beta2/servers/test_id_999/clear-alert` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta2/server-warranty` | `/compute-ops-mgmt/v1beta2/server-warranty` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta2/server-warranty/{id}` | `/compute-ops-mgmt/v1beta2/server-warranty/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1/user-preferences` | `/compute-ops-mgmt/v1/user-preferences` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1/user-preferences` | `/compute-ops-mgmt/v1/user-preferences` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1/user-preferences/{id}` | `/compute-ops-mgmt/v1/user-preferences/test_id_999` | 200 | SUCCESS_2XX |
| PUT | `/compute-ops-mgmt/v1/user-preferences/{id}` | `/compute-ops-mgmt/v1/user-preferences/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1/user-preferences/subscribe` | `/compute-ops-mgmt/v1/user-preferences/subscribe` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1/user-preferences/unsubscribe` | `/compute-ops-mgmt/v1/user-preferences/unsubscribe` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/user-preferences` | `/compute-ops-mgmt/v1beta1/user-preferences` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1beta1/user-preferences` | `/compute-ops-mgmt/v1beta1/user-preferences` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/user-preferences/{id}` | `/compute-ops-mgmt/v1beta1/user-preferences/test_id_999` | 200 | SUCCESS_2XX |
| PUT | `/compute-ops-mgmt/v1beta1/user-preferences/{id}` | `/compute-ops-mgmt/v1beta1/user-preferences/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/utilization-over-time` | `/compute-ops-mgmt/v1beta1/utilization-over-time` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/utilization-by-entity` | `/compute-ops-mgmt/v1beta1/utilization-by-entity` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/webhooks` | `/compute-ops-mgmt/v1beta1/webhooks` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1beta1/webhooks` | `/compute-ops-mgmt/v1beta1/webhooks` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/webhooks/{webhook_id}` | `/compute-ops-mgmt/v1beta1/webhooks/test_id_999` | 200 | SUCCESS_2XX |
| PATCH | `/compute-ops-mgmt/v1beta1/webhooks/{webhook_id}` | `/compute-ops-mgmt/v1beta1/webhooks/test_id_999` | 200 | SUCCESS_2XX |
| DELETE | `/compute-ops-mgmt/v1beta1/webhooks/{webhook_id}` | `/compute-ops-mgmt/v1beta1/webhooks/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/webhooks/{webhook_id}/deliveries` | `/compute-ops-mgmt/v1beta1/webhooks/test_id_999/deliveries` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1beta1/webhooks/{webhook_id}/deliveries/{delivery_id}` | `/compute-ops-mgmt/v1beta1/webhooks/test_id_999/deliveries/9e42edd9-6829-4a07-9d39-921a32bb9f95` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1/groups/{group-id}/devices` | `/compute-ops-mgmt/v1/groups/test_id_999/devices` | 404 | NOT_FOUND_404 |
| POST | `/compute-ops-mgmt/v1/groups/{group-id}/devices/unassign` | `/compute-ops-mgmt/v1/groups/test_id_999/devices/unassign` | 404 | NOT_FOUND_404 |
| GET | `/compute-ops-mgmt/v1/groups/{group-id}/external-storage-compliance` | `/compute-ops-mgmt/v1/groups/test_id_999/external-storage-compliance` | 404 | NOT_FOUND_404 |
| POST | `/compute-ops-mgmt/v1beta3/groups/{group-id}/devices` | `/compute-ops-mgmt/v1beta3/groups/test_id_999/devices` | 404 | NOT_FOUND_404 |
| POST | `/compute-ops-mgmt/v1beta3/groups/{group-id}/devices/unassign` | `/compute-ops-mgmt/v1beta3/groups/test_id_999/devices/unassign` | 404 | NOT_FOUND_404 |
| GET | `/compute-ops-mgmt/v1beta3/groups/{group-id}/external-storage-compliance` | `/compute-ops-mgmt/v1beta3/groups/test_id_999/external-storage-compliance` | 404 | NOT_FOUND_404 |
| GET | `/compute-ops-mgmt/v1beta3/groups/{group-id}/ilo-settings-compliance` | `/compute-ops-mgmt/v1beta3/groups/test_id_999/ilo-settings-compliance` | 404 | NOT_FOUND_404 |
| GET | `/compute-ops-mgmt/v1beta3/groups/{group-id}/ilo-settings-compliance/{ilo-settings-compliance-id}` | `/compute-ops-mgmt/v1beta3/groups/test_id_999/ilo-settings-compliance/9e42edd9-6829-4a07-9d39-921a32bb9f95` | 404 | NOT_FOUND_404 |
| GET | `/compute-ops-mgmt/v1/devices` | `/compute-ops-mgmt/v1/devices` | 200 | SUCCESS_2XX |
| GET | `/compute-ops-mgmt/v1/devices/{id}` | `/compute-ops-mgmt/v1/devices/test_id_999` | 404 | NOT_FOUND_404 |
| POST | `/compute-ops-mgmt/v1/devices` | `/compute-ops-mgmt/v1/devices` | 200 | SUCCESS_2XX |
| POST | `/compute-ops-mgmt/v1/devices/{id}` | `/compute-ops-mgmt/v1/devices/test_id_999` | 404 | NOT_FOUND_404 |
| PUT | `/compute-ops-mgmt/v1/devices/{id}` | `/compute-ops-mgmt/v1/devices/test_id_999` | 404 | NOT_FOUND_404 |
| DELETE | `/compute-ops-mgmt/v1/devices/{id}` | `/compute-ops-mgmt/v1/devices/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/compute-ops-mgmt/v1/devices/{id}` | `/compute-ops-mgmt/v1/devices/test_id_999` | 404 | NOT_FOUND_404 |
| POST | `/compute-ops-mgmt/v1/devices/{id}/power` | `/compute-ops-mgmt/v1/devices/test_id_999/power` | 404 | NOT_FOUND_404 |
| POST | `/compute-ops-mgmt/v1/devices/{id}/firmware` | `/compute-ops-mgmt/v1/devices/test_id_999/firmware` | 422 | VALIDATION_422 |

</details>

<details><summary><b>NETWORK Server - 341 Endpoints (Click to Expand)</b></summary>

| Method | Original Path | Replaced Path | Status Code | Result Category |
| :--- | :--- | :--- | :--- | :--- |
| GET | `/openapi.json` | `/openapi.json` | 200 | SUCCESS_2XX |
| GET | `/docs` | `/docs` | 200 | SUCCESS_2XX |
| GET | `/docs/oauth2-redirect` | `/docs/oauth2-redirect` | 200 | SUCCESS_2XX |
| GET | `/redoc` | `/redoc` | 200 | SUCCESS_2XX |
| GET | `/network/v1/devices` | `/network/v1/devices` | 200 | SUCCESS_2XX |
| GET | `/network/v1/devices/{id}` | `/network/v1/devices/test_id_999` | 404 | NOT_FOUND_404 |
| POST | `/network/v1/devices` | `/network/v1/devices` | 422 | VALIDATION_422 |
| POST | `/network/v1/devices/{id}` | `/network/v1/devices/test_id_999` | 422 | VALIDATION_422 |
| PUT | `/network/v1/devices/{id}` | `/network/v1/devices/test_id_999` | 422 | VALIDATION_422 |
| DELETE | `/network/v1/devices/{id}` | `/network/v1/devices/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/network/v1/devices/{id}` | `/network/v1/devices/test_id_999` | 404 | NOT_FOUND_404 |
| POST | `/network/v1/devices/{id}/power` | `/network/v1/devices/test_id_999/power` | 404 | NOT_FOUND_404 |
| POST | `/network/v1/devices/{id}/vlans` | `/network/v1/devices/test_id_999/vlans` | 422 | VALIDATION_422 |
| POST | `/network/v1/devices/{id}/ports/{port_name}/status` | `/network/v1/devices/test_id_999/ports/eth9/status` | 422 | VALIDATION_422 |
| GET | `/monitoring/v1/switches` | `/monitoring/v1/switches` | 200 | SUCCESS_2XX |
| GET | `/monitoring/v1/switches/{serial}` | `/monitoring/v1/switches/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/monitoring/v1/switches/{serial}/ports` | `/monitoring/v1/switches/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/ports` | 200 | SUCCESS_2XX |
| GET | `/monitoring/v1/switches/{serial}/vlan` | `/monitoring/v1/switches/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/vlan` | 200 | SUCCESS_2XX |
| POST | `/monitoring/v1/switches/{serial}/vlan` | `/monitoring/v1/switches/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/vlan` | 422 | VALIDATION_422 |
| POST | `/monitoring/v1/switches/{serial}/ports/{port_name}/status` | `/monitoring/v1/switches/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/ports/eth9/status` | 422 | VALIDATION_422 |
| POST | `/as/token.oauth2` | `/as/token.oauth2` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/aps` | `/network-monitoring/v1/aps` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/radios` | `/network-monitoring/v1/radios` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/bssids` | `/network-monitoring/v1/bssids` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/wlans` | `/network-monitoring/v1/wlans` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/swarms` | `/network-monitoring/v1/swarms` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/top-aps-by-wireless-usage` | `/network-monitoring/v1/top-aps-by-wireless-usage` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/top-aps-by-wired-usage` | `/network-monitoring/v1/top-aps-by-wired-usage` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/top-aps-by-usage` | `/network-monitoring/v1/top-aps-by-usage` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/aps/{serial_number}` | `/network-monitoring/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/aps/{serial_number}/throughput-trends` | `/network-monitoring/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/throughput-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/aps/{serial_number}/cpu-utilization-trends` | `/network-monitoring/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/cpu-utilization-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/aps/{serial_number}/memory-utilization-trends` | `/network-monitoring/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/memory-utilization-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/aps/{serial_number}/power-consumption-trends` | `/network-monitoring/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/power-consumption-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/aps/{serial_number}/radios` | `/network-monitoring/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/radios` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/aps/{serial_number}/radios/{radio_number}/throughput-trends` | `/network-monitoring/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/radios/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/throughput-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/aps/{serial_number}/radios/{radio_number}/channel-utilization-trends` | `/network-monitoring/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/radios/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/channel-utilization-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/aps/{serial_number}/radios/{radio_number}/channel-quality-trends` | `/network-monitoring/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/radios/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/channel-quality-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/aps/{serial_number}/radios/{radio_number}/noise-floor-trends` | `/network-monitoring/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/radios/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/noise-floor-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/aps/{serial_number}/radios/{radio_number}/frames-trends` | `/network-monitoring/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/radios/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/frames-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/aps/{serial_number}/ports` | `/network-monitoring/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/ports` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/aps/{serial_number}/ports/{port_index}/throughput-trends` | `/network-monitoring/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/ports/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/throughput-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/aps/{serial_number}/ports/{port_index}/frames-trends` | `/network-monitoring/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/ports/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/frames-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/aps/{serial_number}/ports/{port_index}/crc-trends` | `/network-monitoring/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/ports/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/crc-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/aps/{serial_number}/ports/{port_index}/collisions-trends` | `/network-monitoring/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/ports/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/collisions-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/aps/{serial_number}/tunnels` | `/network-monitoring/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/tunnels` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/aps/{serial_number}/tunnels/{tunnel_id}` | `/network-monitoring/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/tunnels/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/aps/{serial_number}/tunnels/{tunnel_id}/throughput-trends` | `/network-monitoring/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/tunnels/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/throughput-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/aps/{serial_number}/tunnels/{tunnel_id}/packet-loss-trends` | `/network-monitoring/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/tunnels/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/packet-loss-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/aps/{serial_number}/tunnels/{tunnel_id}/mos-trends` | `/network-monitoring/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/tunnels/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/mos-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/aps/{serial_number}/tunnels/{tunnel_id}/jitter-trends` | `/network-monitoring/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/tunnels/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/jitter-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/aps/{serial_number}/tunnels/{tunnel_id}/latency-trends` | `/network-monitoring/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/tunnels/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/latency-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/aps/{serial_number}/wlans` | `/network-monitoring/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/wlans` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/aps/{serial_number}/wlans/{wlan_name}/throughput-trends` | `/network-monitoring/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/wlans/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/throughput-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/wlans/{wlan_name}` | `/network-monitoring/v1/wlans/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/wlans/{wlan_name}/throughput-trends` | `/network-monitoring/v1/wlans/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/throughput-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/swarms/{cluster_id}` | `/network-monitoring/v1/swarms/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/applications` | `/network-monitoring/v1/applications` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/client-onboarding-score` | `/network-monitoring/v1/client-onboarding-score` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/client-onboarding-stage/export` | `/network-monitoring/v1/client-onboarding-stage/export` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/client-onboarding-stage/reasons` | `/network-monitoring/v1/client-onboarding-stage/reasons` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/client-onboarding-stage/count` | `/network-monitoring/v1/client-onboarding-stage/count` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/clients` | `/network-monitoring/v1/clients` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/clients-trend` | `/network-monitoring/v1/clients-trend` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/clients-topn-usage` | `/network-monitoring/v1/clients-topn-usage` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/clients-usage` | `/network-monitoring/v1/clients-usage` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/clients/{mac_address}` | `/network-monitoring/v1/clients/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/clients/{mac_address}/mobility-trail` | `/network-monitoring/v1/clients/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/mobility-trail` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/devices` | `/network-monitoring/v1/devices` | 200 | SUCCESS_2XX |
| PATCH | `/network-monitoring/v1/devices/{serial_number}` | `/network-monitoring/v1/devices/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| DELETE | `/network-monitoring/v1/devices/{serial_number}` | `/network-monitoring/v1/devices/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/device-inventory` | `/network-monitoring/v1/device-inventory` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/site-firewall-sessions` | `/network-monitoring/v1/site-firewall-sessions` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/client-firewall-sessions` | `/network-monitoring/v1/client-firewall-sessions` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/firewall-clients` | `/network-monitoring/v1/firewall-clients` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/sitemaps-summary/{site_id}` | `/network-monitoring/v1/sitemaps-summary/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-monitoring/v1/sitemaps/{site_id}/network-devices-deployed` | `/network-monitoring/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/network-devices-deployed` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/sitemaps/{site_id}/network-devices-deployed` | `/network-monitoring/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/network-devices-deployed` | 200 | SUCCESS_2XX |
| POST | `/network-monitoring/v1/sitemaps/{site_id}/network-devices-undeploy` | `/network-monitoring/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/network-devices-undeploy` | 200 | SUCCESS_2XX |
| POST | `/network-monitoring/v1/sitemaps/{site_id}/network-devices-assigned` | `/network-monitoring/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/network-devices-assigned` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/sitemaps/{site_id}/network-devices-assigned` | `/network-monitoring/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/network-devices-assigned` | 200 | SUCCESS_2XX |
| POST | `/network-monitoring/v1/sitemaps/{site_id}/network-devices-planned` | `/network-monitoring/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/network-devices-planned` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/sitemaps/{site_id}/network-devices-planned` | `/network-monitoring/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/network-devices-planned` | 200 | SUCCESS_2XX |
| DELETE | `/network-monitoring/v1/sitemaps/{site_id}/network-devices-planned` | `/network-monitoring/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/network-devices-planned` | 422 | VALIDATION_422 |
| GET | `/network-monitoring/v1/catalogue-aps` | `/network-monitoring/v1/catalogue-aps` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/sitemaps/sites` | `/network-monitoring/v1/sitemaps/sites` | 200 | SUCCESS_2XX |
| POST | `/network-monitoring/v1/sitemaps/{site_id}/floors` | `/network-monitoring/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/floors` | 200 | SUCCESS_2XX |
| DELETE | `/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}` | `/network-monitoring/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/floors/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}` | `/network-monitoring/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/floors/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| PUT | `/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}` | `/network-monitoring/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/floors/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/scale` | `/network-monitoring/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/floors/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/scale` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/image` | `/network-monitoring/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/floors/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/image` | 200 | SUCCESS_2XX |
| PUT | `/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/image` | `/network-monitoring/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/floors/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/image` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/sitemaps/{site_id}/buildings` | `/network-monitoring/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/buildings` | 200 | SUCCESS_2XX |
| DELETE | `/network-monitoring/v1/sitemaps/{site_id}/buildings/{building_id}` | `/network-monitoring/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/buildings/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 404 | NOT_FOUND_404 |
| PUT | `/network-monitoring/v1/sitemaps/{site_id}/buildings/{building_id}` | `/network-monitoring/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/buildings/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-monitoring/v1/sitemaps/{site_id}/import` | `/network-monitoring/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/import` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/sitemaps/{site_id}/import/{id}` | `/network-monitoring/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/import/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/wall-types` | `/network-monitoring/v1/wall-types` | 200 | SUCCESS_2XX |
| POST | `/network-monitoring/v1/wall-types` | `/network-monitoring/v1/wall-types` | 200 | SUCCESS_2XX |
| PUT | `/network-monitoring/v1/wall-types` | `/network-monitoring/v1/wall-types` | 200 | SUCCESS_2XX |
| DELETE | `/network-monitoring/v1/wall-types` | `/network-monitoring/v1/wall-types` | 422 | VALIDATION_422 |
| GET | `/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/walls` | `/network-monitoring/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/floors/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/walls` | 200 | SUCCESS_2XX |
| POST | `/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/walls` | `/network-monitoring/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/floors/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/walls` | 200 | SUCCESS_2XX |
| PUT | `/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/walls` | `/network-monitoring/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/floors/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/walls` | 200 | SUCCESS_2XX |
| DELETE | `/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/walls` | `/network-monitoring/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/floors/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/walls` | 422 | VALIDATION_422 |
| GET | `/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/zones` | `/network-monitoring/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/floors/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/zones` | 200 | SUCCESS_2XX |
| POST | `/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/zones` | `/network-monitoring/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/floors/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/zones` | 200 | SUCCESS_2XX |
| PUT | `/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/zones` | `/network-monitoring/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/floors/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/zones` | 200 | SUCCESS_2XX |
| DELETE | `/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/zones` | `/network-monitoring/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/floors/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/zones` | 422 | VALIDATION_422 |
| GET | `/network-monitoring/v1/gateways` | `/network-monitoring/v1/gateways` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/clusters/{cluster_name}/vlan-mismatch` | `/network-monitoring/v1/clusters/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/vlan-mismatch` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/clusters/{cluster_name}/connectivity-graph` | `/network-monitoring/v1/clusters/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/connectivity-graph` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/vlans/{vlan_id}` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/vlans/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/clusters/{cluster_name}/members` | `/network-monitoring/v1/clusters/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/members` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/tunnels/{tunnel_name}` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/tunnels/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/ports` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/ports` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/ports/{port_number}` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/ports/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/clusters/{cluster_name}/tunnels` | `/network-monitoring/v1/clusters/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/tunnels` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/vlans` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/vlans` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/tunnels` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/tunnels` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/uplinks` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/uplinks` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/cpu-utilization-trends` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/cpu-utilization-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/memory-utilization-trends` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/memory-utilization-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/tunnels/{tunnel_name}/throughput-trends` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/tunnels/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/throughput-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/tunnels/{tunnel_name}/status-trends` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/tunnels/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/status-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/clusters/{cluster_name}/capacity-trends` | `/network-monitoring/v1/clusters/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/capacity-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/clusters/{cluster_name}/capacity-trends/{serial_number}` | `/network-monitoring/v1/clusters/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/capacity-trends/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/ports/{port_number}/throughput-trends` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/ports/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/throughput-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/clusters/{cluster_name}/tunnels-health-summary` | `/network-monitoring/v1/clusters/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/tunnels-health-summary` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/clusters/{cluster_name}/tunnels-status-summary` | `/network-monitoring/v1/clusters/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/tunnels-status-summary` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/lan-tunnels-health-summary` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/lan-tunnels-health-summary` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/wan-availability-trends` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/wan-availability-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/vpn-availability-trends` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/vpn-availability-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/ports/{port_number}/frames-trends` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/ports/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/frames-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/ports/{port_number}/frames-errors-trends` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/ports/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/frames-errors-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/ports/{port_number}/frames-packets-trends` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/ports/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/frames-packets-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/tunnels/{tunnel_name}/dropped-packet-trends` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/tunnels/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/dropped-packet-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/wan-tunnels-health-summary` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/wan-tunnels-health-summary` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/uplinks/{link_tag}` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/uplinks/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/uplinks/{link_tag}/throughput-trends` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/uplinks/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/throughput-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/uplinks/{link_tag}/wan-compression-trends` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/uplinks/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/wan-compression-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/uplinks/{link_tag}/probes` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/uplinks/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/probes` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/uplinks/{link_tag}/wan-availability-trends` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/uplinks/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/wan-availability-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/uplinks/{vlan_id}/vpn-availability-trends` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/uplinks/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/vpn-availability-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/hardware-temperature-trends` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/hardware-temperature-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/dhcp-pools` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/dhcp-pools` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/dhcp-clients` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/dhcp-clients` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/gateways/{serial_number}/uplinks/{link_tag}/probes/{probe}/performance-trends` | `/network-monitoring/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/uplinks/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/probes/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/performance-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/sites-health` | `/network-monitoring/v1/sites-health` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/site-health/{site_id}` | `/network-monitoring/v1/site-health/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/sites-device-health` | `/network-monitoring/v1/sites-device-health` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/tenant-device-health` | `/network-monitoring/v1/tenant-device-health` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/sites-client-health` | `/network-monitoring/v1/sites-client-health` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/tenant-client-health` | `/network-monitoring/v1/tenant-client-health` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/switches` | `/network-monitoring/v1/switches` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/switches/{serial_number}` | `/network-monitoring/v1/switches/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/stack/{serial_number}/members` | `/network-monitoring/v1/stack/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/members` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/switches/{serial_number}/hardware-categories` | `/network-monitoring/v1/switches/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/hardware-categories` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/switches/{serial_number}/lag` | `/network-monitoring/v1/switches/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/lag` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/switches/{serial_number}/interfaces` | `/network-monitoring/v1/switches/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/interfaces` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/switches/{serial_number}/vlans` | `/network-monitoring/v1/switches/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/vlans` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/switches/topn-interface-trends` | `/network-monitoring/v1/switches/topn-interface-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/switches/{serial_number}/interface-trends` | `/network-monitoring/v1/switches/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/interface-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/switches/{serial_number}/hardware-trends` | `/network-monitoring/v1/switches/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/hardware-trends` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/switches/{serial_number}/interface-poe` | `/network-monitoring/v1/switches/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/interface-poe` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/switches/{serial_number}/vsx` | `/network-monitoring/v1/switches/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/vsx` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/topology/{site_id}` | `/network-monitoring/v1/topology/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/unmanaged-device/{mac_address}` | `/network-monitoring/v1/unmanaged-device/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/isolated-devices/{site_id}` | `/network-monitoring/v1/isolated-devices/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-monitoring/v1/neighbours/{serial_number}` | `/network-monitoring/v1/neighbours/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-msp/v1/list-tenants` | `/network-msp/v1/list-tenants` | 200 | SUCCESS_2XX |
| GET | `/network-notifications/v1/alert-config` | `/network-notifications/v1/alert-config` | 200 | SUCCESS_2XX |
| GET | `/network-notifications/v1/alerts` | `/network-notifications/v1/alerts` | 200 | SUCCESS_2XX |
| POST | `/network-notifications/v1/alerts/clear` | `/network-notifications/v1/alerts/clear` | 200 | SUCCESS_2XX |
| POST | `/network-notifications/v1/alerts/defer` | `/network-notifications/v1/alerts/defer` | 200 | SUCCESS_2XX |
| POST | `/network-notifications/v1/alerts/active` | `/network-notifications/v1/alerts/active` | 200 | SUCCESS_2XX |
| POST | `/network-notifications/v1/alerts/priority` | `/network-notifications/v1/alerts/priority` | 200 | SUCCESS_2XX |
| GET | `/network-notifications/v1/alerts/classification` | `/network-notifications/v1/alerts/classification` | 200 | SUCCESS_2XX |
| GET | `/network-notifications/v1/alerts/async-operations/{task_id}` | `/network-notifications/v1/alerts/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-notifications/v1/insights` | `/network-notifications/v1/insights` | 200 | SUCCESS_2XX |
| GET | `/network-notifications/v1/insights-schema` | `/network-notifications/v1/insights-schema` | 200 | SUCCESS_2XX |
| GET | `/network-reporting/v1/reports` | `/network-reporting/v1/reports` | 200 | SUCCESS_2XX |
| PUT | `/network-reporting/v1/reports/{report_id}` | `/network-reporting/v1/reports/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| DELETE | `/network-reporting/v1/reports/{report_id}` | `/network-reporting/v1/reports/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-reporting/v1/reports/{report_id}/report-runs` | `/network-reporting/v1/reports/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/report-runs` | 200 | SUCCESS_2XX |
| DELETE | `/network-reporting/v1/reports/{report_id}/report-runs/{report_run_id}` | `/network-reporting/v1/reports/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/report-runs/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 404 | NOT_FOUND_404 |
| POST | `/network-reporting/v1/reports/{report_id}/report-runs/{report_run_id}/download-link` | `/network-reporting/v1/reports/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/report-runs/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/download-link` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/airmatch-radio/{radio_mac}` | `/network-services/v1/airmatch-radio/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/airmatch-radio` | `/network-services/v1/airmatch-radio` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/airmatch-ap/{serial_number}` | `/network-services/v1/airmatch-ap/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/airmatch-ap` | `/network-services/v1/airmatch-ap` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/airmatch-ap-radio-relations/{serial_number}` | `/network-services/v1/airmatch-ap-radio-relations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/airmatch-priority-rf-events/{radio_mac}` | `/network-services/v1/airmatch-priority-rf-events/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/airmatch-priority-rf-events` | `/network-services/v1/airmatch-priority-rf-events` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/airmatch-rf-events/{radio_mac}` | `/network-services/v1/airmatch-rf-events/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/airmatch-rf-events` | `/network-services/v1/airmatch-rf-events` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/airmatch-history/{radio_mac}` | `/network-services/v1/airmatch-history/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/airmatch-service-config` | `/network-services/v1/airmatch-service-config` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/airmatch-global-config-id` | `/network-services/v1/airmatch-global-config-id` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/airmatch-radio-feasibility/{radio_mac}` | `/network-services/v1/airmatch-radio-feasibility/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/airmatch-radio-feasibility` | `/network-services/v1/airmatch-radio-feasibility` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/airmatch-board-limit/{serial_number}/{radio_mac}` | `/network-services/v1/airmatch-board-limit/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/airmatch-device-config/{serial_number}` | `/network-services/v1/airmatch-device-config/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/airmatch-non-friend/{radio_mac}` | `/network-services/v1/airmatch-non-friend/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/airmatch-pathloss/{radio_mac}` | `/network-services/v1/airmatch-pathloss/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/airmatch-ap-neighbor-list/{serial_number}` | `/network-services/v1/airmatch-ap-neighbor-list/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/airmatch-partition` | `/network-services/v1/airmatch-partition` | 200 | SUCCESS_2XX |
| POST | `/network-services/v1/airmatch-partition` | `/network-services/v1/airmatch-partition` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/airmatch-radio-partition/{radio_mac}` | `/network-services/v1/airmatch-radio-partition/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-services/v1/airmatch-runnow` | `/network-services/v1/airmatch-runnow` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/airmatch-solution` | `/network-services/v1/airmatch-solution` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/airmatch-solution/{radio_mac}` | `/network-services/v1/airmatch-solution/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/airmatch-ap-coverage-plan/{serial_number}` | `/network-services/v1/airmatch-ap-coverage-plan/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/airmatch-ap-coverage-plan` | `/network-services/v1/airmatch-ap-coverage-plan` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/airmatch-state` | `/network-services/v1/airmatch-state` | 200 | SUCCESS_2XX |
| GET | `/audit/v1/logs/{id}` | `/audit/v1/logs/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/audit/v1/logs` | `/audit/v1/logs` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/fco-resp-info/{serial_number}` | `/network-services/v1/fco-resp-info/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/fco-resp-info-all` | `/network-services/v1/fco-resp-info-all` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/firmware-details` | `/network-services/v1/firmware-details` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/sites/{site_id}/device-locations` | `/network-services/v1/sites/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/device-locations` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/sites/{site_id}/device-locations/{location_id}` | `/network-services/v1/sites/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/device-locations/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/sites/{site_id}/devices/{serial_number}/location` | `/network-services/v1/sites/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/devices/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/location` | 200 | SUCCESS_2XX |
| POST | `/network-services/v1/sites/{site_id}/devices/{serial_number}/location` | `/network-services/v1/sites/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/devices/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/location` | 200 | SUCCESS_2XX |
| DELETE | `/network-services/v1/sites/{site_id}/devices/{serial_number}/location` | `/network-services/v1/sites/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/devices/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/location` | 200 | SUCCESS_2XX |
| POST | `/network-services/v1/ap-ranging-scans` | `/network-services/v1/ap-ranging-scans` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/sitemaps/{site_id}/floors/{floor_id}/ap-ranging-scans` | `/network-services/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/floors/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/ap-ranging-scans` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/sitemaps/{site_id}/floors/{floor_id}/ap-ranging-scans/{scan_id}` | `/network-services/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/floors/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/ap-ranging-scans/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| DELETE | `/network-services/v1/sitemaps/{site_id}/floors/{floor_id}/ap-ranging-scans/{scan_id}` | `/network-services/v1/sitemaps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/floors/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/ap-ranging-scans/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 404 | NOT_FOUND_404 |
| GET | `/network-services/v1/wifi-clients-locations` | `/network-services/v1/wifi-clients-locations` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/asset-tags` | `/network-services/v1/asset-tags` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/asset-tags/{asset_tag_id}` | `/network-services/v1/asset-tags/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| PUT | `/network-services/v1/asset-tags/{asset_tag_id}/metadata` | `/network-services/v1/asset-tags/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/metadata` | 200 | SUCCESS_2XX |
| POST | `/network-services/v1/asset-tags/{asset_tag_id}/metadata` | `/network-services/v1/asset-tags/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/metadata` | 200 | SUCCESS_2XX |
| DELETE | `/network-services/v1/asset-tags/{asset_tag_id}/metadata` | `/network-services/v1/asset-tags/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/metadata` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/location-analytics/trends` | `/network-services/v1/location-analytics/trends` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/location-analytics/sites/insights` | `/network-services/v1/location-analytics/sites/insights` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/webhooks` | `/network-services/v1/webhooks` | 200 | SUCCESS_2XX |
| POST | `/network-services/v1/webhooks` | `/network-services/v1/webhooks` | 200 | SUCCESS_2XX |
| GET | `/network-services/v1/webhooks/{id}` | `/network-services/v1/webhooks/test_id_999` | 200 | SUCCESS_2XX |
| PUT | `/network-services/v1/webhooks/{id}` | `/network-services/v1/webhooks/test_id_999` | 200 | SUCCESS_2XX |
| PATCH | `/network-services/v1/webhooks/{id}` | `/network-services/v1/webhooks/test_id_999` | 200 | SUCCESS_2XX |
| DELETE | `/network-services/v1/webhooks/{id}` | `/network-services/v1/webhooks/test_id_999` | 200 | SUCCESS_2XX |
| POST | `/network-services/v1/webhooks/{id}/rotate-hmac-key` | `/network-services/v1/webhooks/test_id_999/rotate-hmac-key` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/aos-s/{serial_number}/ping` | `/network-troubleshooting/v1/aos-s/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/ping` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/aos-s/{serial_number}/ping/async-operations/{task_id}` | `/network-troubleshooting/v1/aos-s/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/ping/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/aos-s/{serial_number}/traceroute` | `/network-troubleshooting/v1/aos-s/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/traceroute` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/aos-s/{serial_number}/traceroute/async-operations/{task_id}` | `/network-troubleshooting/v1/aos-s/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/traceroute/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/aos-s/{serial_number}/poeBounce` | `/network-troubleshooting/v1/aos-s/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/poeBounce` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/aos-s/{serial_number}/poeBounce/async-operations/{task_id}` | `/network-troubleshooting/v1/aos-s/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/poeBounce/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/aos-s/{serial_number}/portBounce` | `/network-troubleshooting/v1/aos-s/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/portBounce` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/aos-s/{serial_number}/portBounce/async-operations/{task_id}` | `/network-troubleshooting/v1/aos-s/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/portBounce/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/aos-s/{serial_number}/cableTest` | `/network-troubleshooting/v1/aos-s/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/cableTest` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/aos-s/{serial_number}/cableTest/async-operations/{task_id}` | `/network-troubleshooting/v1/aos-s/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/cableTest/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/aos-s/{serial_number}/getArpTable` | `/network-troubleshooting/v1/aos-s/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/getArpTable` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/aos-s/{serial_number}/getArpTable/async-operations/{task_id}` | `/network-troubleshooting/v1/aos-s/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/getArpTable/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/aos-s/{serial_number}/show-commands` | `/network-troubleshooting/v1/aos-s/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/show-commands` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/aos-s/{serial_number}/showCommands` | `/network-troubleshooting/v1/aos-s/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/showCommands` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/aos-s/{serial_number}/showCommands/async-operations/{task_id}` | `/network-troubleshooting/v1/aos-s/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/showCommands/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/aos-s/{serial_number}/reboot` | `/network-troubleshooting/v1/aos-s/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/reboot` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/aos-s/{serial_number}/locate` | `/network-troubleshooting/v1/aos-s/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/locate` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/aos-s/{serial_number}/list-tasks` | `/network-troubleshooting/v1/aos-s/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/list-tasks` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/aps/{serial_number}/ping` | `/network-troubleshooting/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/ping` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/aps/{serial_number}/ping/async-operations/{task_id}` | `/network-troubleshooting/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/ping/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/aps/{serial_number}/traceroute` | `/network-troubleshooting/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/traceroute` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/aps/{serial_number}/traceroute/async-operations/{task_id}` | `/network-troubleshooting/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/traceroute/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/aps/{serial_number}/speedtest` | `/network-troubleshooting/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/speedtest` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/aps/{serial_number}/speedtest/async-operations/{task_id}` | `/network-troubleshooting/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/speedtest/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/aps/{serial_number}/http` | `/network-troubleshooting/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/http` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/aps/{serial_number}/http/async-operations/{task_id}` | `/network-troubleshooting/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/http/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/aps/{serial_number}/https` | `/network-troubleshooting/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/https` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/aps/{serial_number}/https/async-operations/{task_id}` | `/network-troubleshooting/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/https/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/aps/{serial_number}/tcp` | `/network-troubleshooting/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/tcp` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/aps/{serial_number}/tcp/async-operations/{task_id}` | `/network-troubleshooting/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/tcp/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/aps/{serial_number}/getArpTable` | `/network-troubleshooting/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/getArpTable` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/aps/{serial_number}/getArpTable/async-operations/{task_id}` | `/network-troubleshooting/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/getArpTable/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/aps/{serial_number}/nslookup` | `/network-troubleshooting/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/nslookup` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/aps/{serial_number}/nslookup/async-operations/{task_id}` | `/network-troubleshooting/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/nslookup/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/aps/{serial_number}/aaa` | `/network-troubleshooting/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/aaa` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/aps/{serial_number}/aaa/async-operations/{task_id}` | `/network-troubleshooting/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/aaa/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/aps/{serial_number}/show-commands` | `/network-troubleshooting/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/show-commands` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/aps/{serial_number}/showCommands` | `/network-troubleshooting/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/showCommands` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/aps/{serial_number}/showCommands/async-operations/{task_id}` | `/network-troubleshooting/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/showCommands/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/aps/{serial_number}/reboot` | `/network-troubleshooting/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/reboot` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/aps/{serial_number}/rebootSwarm` | `/network-troubleshooting/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/rebootSwarm` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/aps/{serial_number}/locate` | `/network-troubleshooting/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/locate` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/aps/{serial_number}/disconnectUserAll` | `/network-troubleshooting/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/disconnectUserAll` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/aps/{serial_number}/disconnectUserByMacAddress` | `/network-troubleshooting/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/disconnectUserByMacAddress` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/aps/{serial_number}/disconnectUserByNetwork` | `/network-troubleshooting/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/disconnectUserByNetwork` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/aps/{serial_number}/list-tasks` | `/network-troubleshooting/v1/aps/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/list-tasks` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/cx/{serial_number}/ping` | `/network-troubleshooting/v1/cx/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/ping` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/cx/{serial_number}/ping/async-operations/{task_id}` | `/network-troubleshooting/v1/cx/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/ping/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/cx/{serial_number}/traceroute` | `/network-troubleshooting/v1/cx/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/traceroute` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/cx/{serial_number}/traceroute/async-operations/{task_id}` | `/network-troubleshooting/v1/cx/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/traceroute/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/cx/{serial_number}/poeBounce` | `/network-troubleshooting/v1/cx/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/poeBounce` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/cx/{serial_number}/poeBounce/async-operations/{task_id}` | `/network-troubleshooting/v1/cx/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/poeBounce/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/cx/{serial_number}/portBounce` | `/network-troubleshooting/v1/cx/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/portBounce` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/cx/{serial_number}/portBounce/async-operations/{task_id}` | `/network-troubleshooting/v1/cx/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/portBounce/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/cx/{serial_number}/cableTest` | `/network-troubleshooting/v1/cx/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/cableTest` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/cx/{serial_number}/cableTest/async-operations/{task_id}` | `/network-troubleshooting/v1/cx/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/cableTest/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/cx/{serial_number}/http` | `/network-troubleshooting/v1/cx/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/http` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/cx/{serial_number}/http/async-operations/{task_id}` | `/network-troubleshooting/v1/cx/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/http/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/cx/{serial_number}/aaa` | `/network-troubleshooting/v1/cx/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/aaa` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/cx/{serial_number}/aaa/async-operations/{task_id}` | `/network-troubleshooting/v1/cx/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/aaa/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/cx/{serial_number}/show-commands` | `/network-troubleshooting/v1/cx/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/show-commands` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/cx/{serial_number}/showCommands` | `/network-troubleshooting/v1/cx/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/showCommands` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/cx/{serial_number}/showCommands/async-operations/{task_id}` | `/network-troubleshooting/v1/cx/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/showCommands/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/cx/{serial_number}/locate` | `/network-troubleshooting/v1/cx/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/locate` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/cx/{serial_number}/reboot` | `/network-troubleshooting/v1/cx/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/reboot` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/cx/{serial_number}/list-tasks` | `/network-troubleshooting/v1/cx/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/list-tasks` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/events` | `/network-troubleshooting/v1/events` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/event-extra-attributes` | `/network-troubleshooting/v1/event-extra-attributes` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/event-filters` | `/network-troubleshooting/v1/event-filters` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/gateways/{serial_number}/ping` | `/network-troubleshooting/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/ping` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/gateways/{serial_number}/ping/async-operations/{task_id}` | `/network-troubleshooting/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/ping/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/gateways/{serial_number}/pingSweep` | `/network-troubleshooting/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/pingSweep` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/gateways/{serial_number}/pingSweep/async-operations/{task_id}` | `/network-troubleshooting/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/pingSweep/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/gateways/{serial_number}/traceroute` | `/network-troubleshooting/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/traceroute` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/gateways/{serial_number}/traceroute/async-operations/{task_id}` | `/network-troubleshooting/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/traceroute/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/gateways/{serial_number}/poeBounce` | `/network-troubleshooting/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/poeBounce` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/gateways/{serial_number}/poeBounce/async-operations/{task_id}` | `/network-troubleshooting/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/poeBounce/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/gateways/{serial_number}/portBounce` | `/network-troubleshooting/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/portBounce` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/gateways/{serial_number}/portBounce/async-operations/{task_id}` | `/network-troubleshooting/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/portBounce/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/gateways/{serial_number}/iperf` | `/network-troubleshooting/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/iperf` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/gateways/{serial_number}/iperf/async-operations/{task_id}` | `/network-troubleshooting/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/iperf/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/gateways/{serial_number}/http` | `/network-troubleshooting/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/http` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/gateways/{serial_number}/http/async-operations/{task_id}` | `/network-troubleshooting/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/http/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/gateways/{serial_number}/https` | `/network-troubleshooting/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/https` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/gateways/{serial_number}/https/async-operations/{task_id}` | `/network-troubleshooting/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/https/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/gateways/{serial_number}/getArpTable` | `/network-troubleshooting/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/getArpTable` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/gateways/{serial_number}/getArpTable/async-operations/{task_id}` | `/network-troubleshooting/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/getArpTable/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/gateways/{serial_number}/show-commands` | `/network-troubleshooting/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/show-commands` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/gateways/{serial_number}/showCommands` | `/network-troubleshooting/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/showCommands` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/gateways/{serial_number}/showCommands/async-operations/{task_id}` | `/network-troubleshooting/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/showCommands/async-operations/0035b61d-ffbf-51f8-b9cc-4de76a4273e3` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/gateways/{serial_number}/reboot` | `/network-troubleshooting/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/reboot` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/gateways/{serial_number}/disconnectClientAll` | `/network-troubleshooting/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/disconnectClientAll` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/gateways/{serial_number}/disconnectClientByMacAddress` | `/network-troubleshooting/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/disconnectClientByMacAddress` | 200 | SUCCESS_2XX |
| POST | `/network-troubleshooting/v1/gateways/{serial_number}/halt` | `/network-troubleshooting/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/halt` | 200 | SUCCESS_2XX |
| GET | `/network-troubleshooting/v1/gateways/{serial_number}/list-tasks` | `/network-troubleshooting/v1/gateways/0035b61d-ffbf-51f8-b9cc-4de76a4273e3/list-tasks` | 200 | SUCCESS_2XX |

</details>

<details><summary><b>ONEVIEW Server - 62 Endpoints (Click to Expand)</b></summary>

| Method | Original Path | Replaced Path | Status Code | Result Category |
| :--- | :--- | :--- | :--- | :--- |
| GET | `/openapi.json` | `/openapi.json` | 200 | SUCCESS_2XX |
| GET | `/docs` | `/docs` | 200 | SUCCESS_2XX |
| GET | `/docs/oauth2-redirect` | `/docs/oauth2-redirect` | 200 | SUCCESS_2XX |
| GET | `/redoc` | `/redoc` | 200 | SUCCESS_2XX |
| GET | `/rest/custom-servers` | `/rest/custom-servers` | 200 | SUCCESS_2XX |
| GET | `/rest/custom-servers/{id}` | `/rest/custom-servers/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/rest/custom-servers/{id}/{feature}` | `/rest/custom-servers/test_id_999/55fe56db-abb1-4da9-af99-20a59679552a` | 404 | NOT_FOUND_404 |
| POST | `/rest/custom-servers` | `/rest/custom-servers` | 200 | SUCCESS_2XX |
| PUT | `/rest/custom-servers/{id}` | `/rest/custom-servers/test_id_999` | 404 | NOT_FOUND_404 |
| DELETE | `/rest/custom-servers/{id}` | `/rest/custom-servers/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/rest/custom-switches` | `/rest/custom-switches` | 200 | SUCCESS_2XX |
| GET | `/rest/custom-switches/{id}` | `/rest/custom-switches/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/rest/custom-switches/{id}/{feature}` | `/rest/custom-switches/test_id_999/55fe56db-abb1-4da9-af99-20a59679552a` | 404 | NOT_FOUND_404 |
| POST | `/rest/custom-switches` | `/rest/custom-switches` | 200 | SUCCESS_2XX |
| PUT | `/rest/custom-switches/{id}` | `/rest/custom-switches/test_id_999` | 404 | NOT_FOUND_404 |
| DELETE | `/rest/custom-switches/{id}` | `/rest/custom-switches/test_id_999` | 404 | NOT_FOUND_404 |
| POST | `/rest/login-sessions` | `/rest/login-sessions` | 200 | SUCCESS_2XX |
| POST | `/rest/login-sessions/auth-token` | `/rest/login-sessions/auth-token` | 200 | SUCCESS_2XX |
| POST | `/rest/certificates/client/rabbitmq` | `/rest/certificates/client/rabbitmq` | 200 | SUCCESS_2XX |
| GET | `/rest/certificates/client/rabbitmq/keypair/default` | `/rest/certificates/client/rabbitmq/keypair/default` | 200 | SUCCESS_2XX |
| GET | `/rest/certificates/ca` | `/rest/certificates/ca` | 200 | SUCCESS_2XX |
| DELETE | `/rest/certificates/ca/rabbitmq_readonly` | `/rest/certificates/ca/rabbitmq_readonly` | 200 | SUCCESS_2XX |
| GET | `/rest/server-hardware/{id}/chassis` | `/rest/server-hardware/test_id_999/chassis` | 200 | SUCCESS_2XX |
| GET | `/rest/server-hardware/{id}/firmwareInventory` | `/rest/server-hardware/test_id_999/firmwareInventory` | 200 | SUCCESS_2XX |
| GET | `/rest/server-hardware/{id}/networkAdapters` | `/rest/server-hardware/test_id_999/networkAdapters` | 200 | SUCCESS_2XX |
| GET | `/rest/server-hardware/{id}/powerSupplies` | `/rest/server-hardware/test_id_999/powerSupplies` | 200 | SUCCESS_2XX |
| GET | `/rest/server-hardware/{id}/processors` | `/rest/server-hardware/test_id_999/processors` | 200 | SUCCESS_2XX |
| GET | `/rest/server-hardware/{id}/softwareInventory` | `/rest/server-hardware/test_id_999/softwareInventory` | 200 | SUCCESS_2XX |
| GET | `/rest/server-hardware/{id}/thermal` | `/rest/server-hardware/test_id_999/thermal` | 200 | SUCCESS_2XX |
| GET | `/rest/rack-managers/{id}/chassis/{uuid}` | `/rest/rack-managers/test_id_999/chassis/55fe56db-abb1-4da9-af99-20a59679552a` | 200 | SUCCESS_2XX |
| POST | `/rest/ethernet-networks/bulk` | `/rest/ethernet-networks/bulk` | 200 | SUCCESS_2XX |
| PUT | `/rest/storage-volumes/{id}` | `/rest/storage-volumes/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/rest/updates` | `/rest/updates` | 200 | SUCCESS_2XX |
| GET | `/rest/updates/{id}` | `/rest/updates/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/rest/rack-managers` | `/rest/rack-managers` | 200 | SUCCESS_2XX |
| POST | `/rest/rack-managers` | `/rest/rack-managers` | 200 | SUCCESS_2XX |
| GET | `/rest/rack-managers/chassis` | `/rest/rack-managers/chassis` | 200 | SUCCESS_2XX |
| GET | `/rest/rack-managers/managers` | `/rest/rack-managers/managers` | 200 | SUCCESS_2XX |
| GET | `/rest/rack-managers/partitions` | `/rest/rack-managers/partitions` | 200 | SUCCESS_2XX |
| GET | `/rest/rack-managers/{id}` | `/rest/rack-managers/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/rest/rack-managers/{id}` | `/rest/rack-managers/test_id_999` | 200 | SUCCESS_2XX |
| DELETE | `/rest/rack-managers/{id}` | `/rest/rack-managers/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/rest/rack-managers/{id}/chassis` | `/rest/rack-managers/test_id_999/chassis` | 200 | SUCCESS_2XX |
| GET | `/rest/rack-managers/{id}/chassis/utilization` | `/rest/rack-managers/test_id_999/chassis/utilization` | 200 | SUCCESS_2XX |
| GET | `/rest/rack-managers/{id}/environmentalConfiguration` | `/rest/rack-managers/test_id_999/environmentalConfiguration` | 200 | SUCCESS_2XX |
| GET | `/rest/rack-managers/{id}/managers` | `/rest/rack-managers/test_id_999/managers` | 200 | SUCCESS_2XX |
| GET | `/rest/rack-managers/{id}/managers/{managerid}` | `/rest/rack-managers/test_id_999/managers/55fe56db-abb1-4da9-af99-20a59679552a` | 200 | SUCCESS_2XX |
| GET | `/rest/rack-managers/{id}/partitions` | `/rest/rack-managers/test_id_999/partitions` | 200 | SUCCESS_2XX |
| GET | `/rest/rack-managers/{id}/partitions/{uuid}` | `/rest/rack-managers/test_id_999/partitions/55fe56db-abb1-4da9-af99-20a59679552a` | 200 | SUCCESS_2XX |
| GET | `/rest/rack-managers/{id}/remoteSupportSettings` | `/rest/rack-managers/test_id_999/remoteSupportSettings` | 200 | SUCCESS_2XX |
| GET | `/rest/server-hardware` | `/rest/server-hardware` | 200 | SUCCESS_2XX |
| POST | `/rest/server-hardware` | `/rest/server-hardware` | 200 | SUCCESS_2XX |
| GET | `/rest/server-hardware/*/firmware` | `/rest/server-hardware/*/firmware` | 200 | SUCCESS_2XX |
| POST | `/rest/server-hardware/discovery` | `/rest/server-hardware/discovery` | 200 | SUCCESS_2XX |
| POST | `/rest/server-hardware/firmware-compliance` | `/rest/server-hardware/firmware-compliance` | 200 | SUCCESS_2XX |
| GET | `/rest/server-hardware/schema` | `/rest/server-hardware/schema` | 200 | SUCCESS_2XX |
| GET | `/rest/server-hardware/{id}` | `/rest/server-hardware/test_id_999` | 404 | NOT_FOUND_404 |
| PUT | `/rest/server-hardware/{id}` | `/rest/server-hardware/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/rest/server-hardware/{id}` | `/rest/server-hardware/test_id_999` | 404 | NOT_FOUND_404 |
| DELETE | `/rest/server-hardware/{id}` | `/rest/server-hardware/test_id_999` | 404 | NOT_FOUND_404 |
| POST | `/rest/server-hardware/{id}/power` | `/rest/server-hardware/test_id_999/power` | 404 | NOT_FOUND_404 |
| PUT | `/rest/server-hardware/{id}/powerState` | `/rest/server-hardware/test_id_999/powerState` | 404 | NOT_FOUND_404 |

</details>

<details><summary><b>STORAGE Server - 41 Endpoints (Click to Expand)</b></summary>

| Method | Original Path | Replaced Path | Status Code | Result Category |
| :--- | :--- | :--- | :--- | :--- |
| GET | `/openapi.json` | `/openapi.json` | 200 | SUCCESS_2XX |
| GET | `/docs` | `/docs` | 200 | SUCCESS_2XX |
| GET | `/docs/oauth2-redirect` | `/docs/oauth2-redirect` | 200 | SUCCESS_2XX |
| GET | `/redoc` | `/redoc` | 200 | SUCCESS_2XX |
| GET | `/data-services/v1beta1/async-operations` | `/data-services/v1beta1/async-operations` | 200 | SUCCESS_2XX |
| GET | `/data-services/v1beta1/async-operations/{id}` | `/data-services/v1beta1/async-operations/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/data-services/v1beta1/dual-auth-operations` | `/data-services/v1beta1/dual-auth-operations` | 200 | SUCCESS_2XX |
| GET | `/data-services/v1beta1/dual-auth-operations/{id}` | `/data-services/v1beta1/dual-auth-operations/test_id_999` | 200 | SUCCESS_2XX |
| PATCH | `/data-services/v1beta1/dual-auth-operations/{id}` | `/data-services/v1beta1/dual-auth-operations/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/data-services/v1beta1/issues` | `/data-services/v1beta1/issues` | 200 | SUCCESS_2XX |
| GET | `/data-services/v1beta1/issues/{id}` | `/data-services/v1beta1/issues/test_id_999` | 200 | SUCCESS_2XX |
| PATCH | `/data-services/v1beta1/issues/{id}` | `/data-services/v1beta1/issues/test_id_999` | 200 | SUCCESS_2XX |
| DELETE | `/data-services/v1beta1/issues/{id}` | `/data-services/v1beta1/issues/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/data-services/v1beta1/issues-metadata` | `/data-services/v1beta1/issues-metadata` | 200 | SUCCESS_2XX |
| GET | `/data-services/v1beta1/secrets/{id}` | `/data-services/v1beta1/secrets/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/data-services/v1beta1/secrets` | `/data-services/v1beta1/secrets` | 200 | SUCCESS_2XX |
| POST | `/data-services/v1beta1/secrets` | `/data-services/v1beta1/secrets` | 200 | SUCCESS_2XX |
| PATCH | `/data-services/v1beta1/secrets/{id}` | `/data-services/v1beta1/secrets/test_id_999` | 200 | SUCCESS_2XX |
| DELETE | `/data-services/v1beta1/secrets/{id}` | `/data-services/v1beta1/secrets/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/data-services/v1beta1/secret-assignments/{id}` | `/data-services/v1beta1/secret-assignments/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/data-services/v1beta1/secret-assignments` | `/data-services/v1beta1/secret-assignments` | 200 | SUCCESS_2XX |
| GET | `/data-services/v1beta1/settings` | `/data-services/v1beta1/settings` | 200 | SUCCESS_2XX |
| GET | `/data-services/v1beta1/settings/{id}` | `/data-services/v1beta1/settings/test_id_999` | 200 | SUCCESS_2XX |
| PATCH | `/data-services/v1beta1/settings/{id}` | `/data-services/v1beta1/settings/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/data-services/v1beta1/software-components/{id}/install-release` | `/data-services/v1beta1/software-components/test_id_999/install-release` | 200 | SUCCESS_2XX |
| GET | `/data-services/v1beta1/software-releases/{id}` | `/data-services/v1beta1/software-releases/test_id_999` | 200 | SUCCESS_2XX |
| GET | `/data-services/v1beta1/software-releases` | `/data-services/v1beta1/software-releases` | 200 | SUCCESS_2XX |
| POST | `/data-services/v1beta1/software-releases/{id}/download` | `/data-services/v1beta1/software-releases/test_id_999/download` | 200 | SUCCESS_2XX |
| GET | `/data-services/v1beta1/software-upgrades` | `/data-services/v1beta1/software-upgrades` | 200 | SUCCESS_2XX |
| GET | `/data-services/v1beta1/storage-locations` | `/data-services/v1beta1/storage-locations` | 200 | SUCCESS_2XX |
| GET | `/data-services/v1beta1/tags` | `/data-services/v1beta1/tags` | 200 | SUCCESS_2XX |
| GET | `/data-services/v1beta1/devices` | `/data-services/v1beta1/devices` | 200 | SUCCESS_2XX |
| GET | `/data-services/v1beta1/devices/{id}` | `/data-services/v1beta1/devices/test_id_999` | 404 | NOT_FOUND_404 |
| POST | `/data-services/v1beta1/devices` | `/data-services/v1beta1/devices` | 200 | SUCCESS_2XX |
| POST | `/data-services/v1beta1/devices/{id}` | `/data-services/v1beta1/devices/test_id_999` | 404 | NOT_FOUND_404 |
| PUT | `/data-services/v1beta1/devices/{id}` | `/data-services/v1beta1/devices/test_id_999` | 404 | NOT_FOUND_404 |
| DELETE | `/data-services/v1beta1/devices/{id}` | `/data-services/v1beta1/devices/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/data-services/v1beta1/devices/{id}` | `/data-services/v1beta1/devices/test_id_999` | 404 | NOT_FOUND_404 |
| POST | `/data-services/v1beta1/devices/{id}/power` | `/data-services/v1beta1/devices/test_id_999/power` | 404 | NOT_FOUND_404 |
| POST | `/data-services/v1beta1/devices/{id}/volumes` | `/data-services/v1beta1/devices/test_id_999/volumes` | 422 | VALIDATION_422 |
| DELETE | `/data-services/v1beta1/devices/{id}/volumes/{volume_id}` | `/data-services/v1beta1/devices/test_id_999/volumes/test_id_999` | 404 | NOT_FOUND_404 |

</details>

<details><summary><b>ILO Server - 767 Endpoints (Click to Expand)</b></summary>

| Method | Original Path | Replaced Path | Status Code | Result Category |
| :--- | :--- | :--- | :--- | :--- |
| GET | `/openapi.json` | `/openapi.json` | 200 | SUCCESS_2XX |
| GET | `/docs` | `/docs` | 200 | SUCCESS_2XX |
| GET | `/docs/oauth2-redirect` | `/docs/oauth2-redirect` | 200 | SUCCESS_2XX |
| GET | `/redoc` | `/redoc` | 200 | SUCCESS_2XX |
| GET | `/` | `/` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/` | `/redfish/v1/` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/accountservice` | `/redfish/v1/accountservice` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/accountservice` | `/redfish/v1/accountservice` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/accountservice/Oem/Hpe/appaccounts` | `/redfish/v1/accountservice/Oem/Hpe/appaccounts` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/accountservice/Oem/Hpe/appaccounts` | `/redfish/v1/accountservice/Oem/Hpe/appaccounts` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/accountservice/Oem/Hpe/appaccounts/{appaccount_id}` | `/redfish/v1/accountservice/Oem/Hpe/appaccounts/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/accountservice/Oem/Hpe/appaccounts/{appaccount_id}` | `/redfish/v1/accountservice/Oem/Hpe/appaccounts/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/accountservice/Oem/Hpe/appaccounts/{appaccount_id}` | `/redfish/v1/accountservice/Oem/Hpe/appaccounts/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/accountservice/Oem/Hpe/passwordrecovery` | `/redfish/v1/accountservice/Oem/Hpe/passwordrecovery` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/accountservice/Oem/Hpe/passwordrecovery` | `/redfish/v1/accountservice/Oem/Hpe/passwordrecovery` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/accountservice/accounts` | `/redfish/v1/accountservice/accounts` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/accountservice/accounts` | `/redfish/v1/accountservice/accounts` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/accountservice/accounts/{account_id}` | `/redfish/v1/accountservice/accounts/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/accountservice/accounts/{account_id}` | `/redfish/v1/accountservice/accounts/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/accountservice/accounts/{account_id}` | `/redfish/v1/accountservice/accounts/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/accountservice/accounts/{account_id}/keys` | `/redfish/v1/accountservice/accounts/test_id_999/keys` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/accountservice/accounts/{account_id}/keys` | `/redfish/v1/accountservice/accounts/test_id_999/keys` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/accountservice/accounts/{account_id}/keys/{key_id}` | `/redfish/v1/accountservice/accounts/test_id_999/keys/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/accountservice/accounts/{account_id}/keys/{key_id}` | `/redfish/v1/accountservice/accounts/test_id_999/keys/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/accountservice/accounts/{account_id}/keys/{key_id}` | `/redfish/v1/accountservice/accounts/test_id_999/keys/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/accountservice/directorytest` | `/redfish/v1/accountservice/directorytest` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/accountservice/directorytest` | `/redfish/v1/accountservice/directorytest` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/accountservice/externalaccountproviders/ldap/certificates` | `/redfish/v1/accountservice/externalaccountproviders/ldap/certificates` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/accountservice/externalaccountproviders/ldap/certificates` | `/redfish/v1/accountservice/externalaccountproviders/ldap/certificates` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/accountservice/externalaccountproviders/ldap/certificates/{certificat_id}` | `/redfish/v1/accountservice/externalaccountproviders/ldap/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/accountservice/externalaccountproviders/ldap/certificates/{certificat_id}` | `/redfish/v1/accountservice/externalaccountproviders/ldap/certificates/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/accountservice/externalaccountproviders/ldap/certificates/{certificat_id}` | `/redfish/v1/accountservice/externalaccountproviders/ldap/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/accountservice/roles` | `/redfish/v1/accountservice/roles` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/accountservice/roles` | `/redfish/v1/accountservice/roles` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/accountservice/roles/{rol_id}` | `/redfish/v1/accountservice/roles/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/accountservice/roles/{rol_id}` | `/redfish/v1/accountservice/roles/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/accountservice/roles/{rol_id}` | `/redfish/v1/accountservice/roles/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/accountservice/usercertificatemapping` | `/redfish/v1/accountservice/usercertificatemapping` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/accountservice/usercertificatemapping` | `/redfish/v1/accountservice/usercertificatemapping` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/accountservice/usercertificatemapping/{usercertificatemapping_id}` | `/redfish/v1/accountservice/usercertificatemapping/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/accountservice/usercertificatemapping/{usercertificatemapping_id}` | `/redfish/v1/accountservice/usercertificatemapping/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/accountservice/usercertificatemapping/{usercertificatemapping_id}` | `/redfish/v1/accountservice/usercertificatemapping/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/certificateservice` | `/redfish/v1/certificateservice` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/certificateservice` | `/redfish/v1/certificateservice` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/certificateservice/certificateenrollments` | `/redfish/v1/certificateservice/certificateenrollments` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/certificateservice/certificateenrollments` | `/redfish/v1/certificateservice/certificateenrollments` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/certificateservice/certificateenrollments/{certificateenrollment_id}` | `/redfish/v1/certificateservice/certificateenrollments/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/certificateservice/certificateenrollments/{certificateenrollment_id}` | `/redfish/v1/certificateservice/certificateenrollments/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/certificateservice/certificateenrollments/{certificateenrollment_id}` | `/redfish/v1/certificateservice/certificateenrollments/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/certificateservice/certificatelocations` | `/redfish/v1/certificateservice/certificatelocations` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/certificateservice/certificatelocations` | `/redfish/v1/certificateservice/certificatelocations` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/certificateservice/enrollmentCAcertificates` | `/redfish/v1/certificateservice/enrollmentCAcertificates` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/certificateservice/enrollmentCAcertificates` | `/redfish/v1/certificateservice/enrollmentCAcertificates` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/certificateservice/enrollmentCAcertificates/{enrollmentcacertificat_id}` | `/redfish/v1/certificateservice/enrollmentCAcertificates/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/certificateservice/enrollmentCAcertificates/{enrollmentcacertificat_id}` | `/redfish/v1/certificateservice/enrollmentCAcertificates/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/certificateservice/enrollmentCAcertificates/{enrollmentcacertificat_id}` | `/redfish/v1/certificateservice/enrollmentCAcertificates/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/chassis` | `/redfish/v1/chassis` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis` | `/redfish/v1/chassis` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/chassis/{chassi_id}` | `/redfish/v1/chassis/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/chassis/{chassi_id}` | `/redfish/v1/chassis/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/chassis/{chassi_id}` | `/redfish/v1/chassis/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/chassis/{chassi_id}/PCIeDevices/{pciedevic_id}/assembly` | `/redfish/v1/chassis/test_id_999/PCIeDevices/test_id_999/assembly` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/PCIeDevices/{pciedevic_id}/assembly` | `/redfish/v1/chassis/test_id_999/PCIeDevices/test_id_999/assembly` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/assembly` | `/redfish/v1/chassis/test_id_999/assembly` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/assembly` | `/redfish/v1/chassis/test_id_999/assembly` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/basefrus` | `/redfish/v1/chassis/test_id_999/basefrus` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/basefrus` | `/redfish/v1/chassis/test_id_999/basefrus` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/basefrus/{basefru_id}` | `/redfish/v1/chassis/test_id_999/basefrus/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/chassis/{chassi_id}/basefrus/{basefru_id}` | `/redfish/v1/chassis/test_id_999/basefrus/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/chassis/{chassi_id}/basefrus/{basefru_id}` | `/redfish/v1/chassis/test_id_999/basefrus/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/chassis/{chassi_id}/basefrus/{basefru_id}/details` | `/redfish/v1/chassis/test_id_999/basefrus/test_id_999/details` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/basefrus/{basefru_id}/details` | `/redfish/v1/chassis/test_id_999/basefrus/test_id_999/details` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/devices` | `/redfish/v1/chassis/test_id_999/devices` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/devices` | `/redfish/v1/chassis/test_id_999/devices` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/devices/{devic_id}` | `/redfish/v1/chassis/test_id_999/devices/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/chassis/{chassi_id}/devices/{devic_id}` | `/redfish/v1/chassis/test_id_999/devices/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/chassis/{chassi_id}/devices/{devic_id}` | `/redfish/v1/chassis/test_id_999/devices/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/chassis/{chassi_id}/drives/{driv_id}/assembly` | `/redfish/v1/chassis/test_id_999/drives/test_id_999/assembly` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/drives/{driv_id}/assembly` | `/redfish/v1/chassis/test_id_999/drives/test_id_999/assembly` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/drives/{driv_id}/environmentmetrics` | `/redfish/v1/chassis/test_id_999/drives/test_id_999/environmentmetrics` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/drives/{driv_id}/environmentmetrics` | `/redfish/v1/chassis/test_id_999/drives/test_id_999/environmentmetrics` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/environmentmetrics` | `/redfish/v1/chassis/test_id_999/environmentmetrics` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/environmentmetrics` | `/redfish/v1/chassis/test_id_999/environmentmetrics` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/mezzfrus` | `/redfish/v1/chassis/test_id_999/mezzfrus` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/mezzfrus` | `/redfish/v1/chassis/test_id_999/mezzfrus` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/mezzfrus/{mezzfru_id}` | `/redfish/v1/chassis/test_id_999/mezzfrus/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/chassis/{chassi_id}/mezzfrus/{mezzfru_id}` | `/redfish/v1/chassis/test_id_999/mezzfrus/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/chassis/{chassi_id}/mezzfrus/{mezzfru_id}` | `/redfish/v1/chassis/test_id_999/mezzfrus/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/chassis/{chassi_id}/mezzfrus/{mezzfru_id}/details` | `/redfish/v1/chassis/test_id_999/mezzfrus/test_id_999/details` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/mezzfrus/{mezzfru_id}/details` | `/redfish/v1/chassis/test_id_999/mezzfrus/test_id_999/details` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/networkadapters` | `/redfish/v1/chassis/test_id_999/networkadapters` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/networkadapters` | `/redfish/v1/chassis/test_id_999/networkadapters` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}` | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}` | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}` | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/assembly` | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999/assembly` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/assembly` | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999/assembly` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions` | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999/networkdevicefunctions` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions` | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999/networkdevicefunctions` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions/{networkdevicefunction_id}` | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999/networkdevicefunctions/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions/{networkdevicefunction_id}` | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999/networkdevicefunctions/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions/{networkdevicefunction_id}` | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999/networkdevicefunctions/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions/{networkdevicefunction_id}/settings` | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999/networkdevicefunctions/test_id_999/settings` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions/{networkdevicefunction_id}/settings` | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999/networkdevicefunctions/test_id_999/settings` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports` | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999/ports` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports` | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999/ports` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports/{port_id}` | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999/ports/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports/{port_id}` | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999/ports/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports/{port_id}` | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999/ports/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports/{port_id}/settings` | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999/ports/test_id_999/settings` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports/{port_id}/settings` | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999/ports/test_id_999/settings` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/settings` | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999/settings` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/settings` | `/redfish/v1/chassis/test_id_999/networkadapters/test_id_999/settings` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/pciedevices` | `/redfish/v1/chassis/test_id_999/pciedevices` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/pciedevices` | `/redfish/v1/chassis/test_id_999/pciedevices` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}` | `/redfish/v1/chassis/test_id_999/pciedevices/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}` | `/redfish/v1/chassis/test_id_999/pciedevices/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}` | `/redfish/v1/chassis/test_id_999/pciedevices/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}/pciefunctions` | `/redfish/v1/chassis/test_id_999/pciedevices/test_id_999/pciefunctions` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}/pciefunctions` | `/redfish/v1/chassis/test_id_999/pciedevices/test_id_999/pciefunctions` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}/pciefunctions/{pciefunction_id}` | `/redfish/v1/chassis/test_id_999/pciedevices/test_id_999/pciefunctions/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}/pciefunctions/{pciefunction_id}` | `/redfish/v1/chassis/test_id_999/pciedevices/test_id_999/pciefunctions/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}/pciefunctions/{pciefunction_id}` | `/redfish/v1/chassis/test_id_999/pciedevices/test_id_999/pciefunctions/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/chassis/{chassi_id}/pcieslots` | `/redfish/v1/chassis/test_id_999/pcieslots` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/pcieslots` | `/redfish/v1/chassis/test_id_999/pcieslots` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/power` | `/redfish/v1/chassis/test_id_999/power` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/power` | `/redfish/v1/chassis/test_id_999/power` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/power/fastpowermeter` | `/redfish/v1/chassis/test_id_999/power/fastpowermeter` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/power/fastpowermeter` | `/redfish/v1/chassis/test_id_999/power/fastpowermeter` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/power/powermeter` | `/redfish/v1/chassis/test_id_999/power/powermeter` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/power/powermeter` | `/redfish/v1/chassis/test_id_999/power/powermeter` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/powersubsystem` | `/redfish/v1/chassis/test_id_999/powersubsystem` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/powersubsystem` | `/redfish/v1/chassis/test_id_999/powersubsystem` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/powersubsystem/batteries` | `/redfish/v1/chassis/test_id_999/powersubsystem/batteries` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/powersubsystem/batteries` | `/redfish/v1/chassis/test_id_999/powersubsystem/batteries` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/powersubsystem/batteries/{battery_id}` | `/redfish/v1/chassis/test_id_999/powersubsystem/batteries/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/chassis/{chassi_id}/powersubsystem/batteries/{battery_id}` | `/redfish/v1/chassis/test_id_999/powersubsystem/batteries/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/chassis/{chassi_id}/powersubsystem/batteries/{battery_id}` | `/redfish/v1/chassis/test_id_999/powersubsystem/batteries/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies` | `/redfish/v1/chassis/test_id_999/powersubsystem/powersupplies` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies` | `/redfish/v1/chassis/test_id_999/powersubsystem/powersupplies` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}` | `/redfish/v1/chassis/test_id_999/powersubsystem/powersupplies/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}` | `/redfish/v1/chassis/test_id_999/powersubsystem/powersupplies/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}` | `/redfish/v1/chassis/test_id_999/powersubsystem/powersupplies/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}/assembly` | `/redfish/v1/chassis/test_id_999/powersubsystem/powersupplies/test_id_999/assembly` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}/assembly` | `/redfish/v1/chassis/test_id_999/powersubsystem/powersupplies/test_id_999/assembly` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}/metrics` | `/redfish/v1/chassis/test_id_999/powersubsystem/powersupplies/test_id_999/metrics` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}/metrics` | `/redfish/v1/chassis/test_id_999/powersubsystem/powersupplies/test_id_999/metrics` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/sensors/{sensor_id}` | `/redfish/v1/chassis/test_id_999/sensors/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/chassis/{chassi_id}/sensors/{sensor_id}` | `/redfish/v1/chassis/test_id_999/sensors/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/chassis/{chassi_id}/sensors/{sensor_id}` | `/redfish/v1/chassis/test_id_999/sensors/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/chassis/{chassi_id}/thermal` | `/redfish/v1/chassis/test_id_999/thermal` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/thermal` | `/redfish/v1/chassis/test_id_999/thermal` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/thermalsubsystem` | `/redfish/v1/chassis/test_id_999/thermalsubsystem` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/thermalsubsystem` | `/redfish/v1/chassis/test_id_999/thermalsubsystem` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans` | `/redfish/v1/chassis/test_id_999/thermalsubsystem/fans` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans` | `/redfish/v1/chassis/test_id_999/thermalsubsystem/fans` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans/{fan_id}` | `/redfish/v1/chassis/test_id_999/thermalsubsystem/fans/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans/{fan_id}` | `/redfish/v1/chassis/test_id_999/thermalsubsystem/fans/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans/{fan_id}` | `/redfish/v1/chassis/test_id_999/thermalsubsystem/fans/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans/{fan_id}/assembly` | `/redfish/v1/chassis/test_id_999/thermalsubsystem/fans/test_id_999/assembly` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans/{fan_id}/assembly` | `/redfish/v1/chassis/test_id_999/thermalsubsystem/fans/test_id_999/assembly` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/thermalsubsystem/pumps` | `/redfish/v1/chassis/test_id_999/thermalsubsystem/pumps` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/thermalsubsystem/pumps` | `/redfish/v1/chassis/test_id_999/thermalsubsystem/pumps` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/thermalsubsystem/pumps/{pump_id}/assembly` | `/redfish/v1/chassis/test_id_999/thermalsubsystem/pumps/test_id_999/assembly` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/thermalsubsystem/pumps/{pump_id}/assembly` | `/redfish/v1/chassis/test_id_999/thermalsubsystem/pumps/test_id_999/assembly` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/chassis/{chassi_id}/thermalsubsystem/thermalmetrics` | `/redfish/v1/chassis/test_id_999/thermalsubsystem/thermalmetrics` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/chassis/{chassi_id}/thermalsubsystem/thermalmetrics` | `/redfish/v1/chassis/test_id_999/thermalsubsystem/thermalmetrics` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/componentintegrity` | `/redfish/v1/componentintegrity` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/componentintegrity` | `/redfish/v1/componentintegrity` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/componentintegrity/{componentintegrity_id}` | `/redfish/v1/componentintegrity/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/componentintegrity/{componentintegrity_id}` | `/redfish/v1/componentintegrity/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/componentintegrity/{componentintegrity_id}` | `/redfish/v1/componentintegrity/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/eventservice` | `/redfish/v1/eventservice` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/eventservice` | `/redfish/v1/eventservice` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/eventservice/cacertificates` | `/redfish/v1/eventservice/cacertificates` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/eventservice/cacertificates` | `/redfish/v1/eventservice/cacertificates` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/eventservice/cacertificates/{cacertificat_id}` | `/redfish/v1/eventservice/cacertificates/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/eventservice/cacertificates/{cacertificat_id}` | `/redfish/v1/eventservice/cacertificates/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/eventservice/cacertificates/{cacertificat_id}` | `/redfish/v1/eventservice/cacertificates/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/eventservice/subscriptions` | `/redfish/v1/eventservice/subscriptions` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/eventservice/subscriptions` | `/redfish/v1/eventservice/subscriptions` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/eventservice/subscriptions/{subscription_id}` | `/redfish/v1/eventservice/subscriptions/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/eventservice/subscriptions/{subscription_id}` | `/redfish/v1/eventservice/subscriptions/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/eventservice/subscriptions/{subscription_id}` | `/redfish/v1/eventservice/subscriptions/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/fabrics` | `/redfish/v1/fabrics` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/fabrics` | `/redfish/v1/fabrics` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/fabrics/{fabric_id}` | `/redfish/v1/fabrics/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/fabrics/{fabric_id}` | `/redfish/v1/fabrics/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/fabrics/{fabric_id}` | `/redfish/v1/fabrics/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/fabrics/{fabric_id}/switches` | `/redfish/v1/fabrics/test_id_999/switches` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/fabrics/{fabric_id}/switches` | `/redfish/v1/fabrics/test_id_999/switches` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/fabrics/{fabric_id}/switches/{switch_id}` | `/redfish/v1/fabrics/test_id_999/switches/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/fabrics/{fabric_id}/switches/{switch_id}` | `/redfish/v1/fabrics/test_id_999/switches/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/fabrics/{fabric_id}/switches/{switch_id}` | `/redfish/v1/fabrics/test_id_999/switches/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/fabrics/{fabric_id}/switches/{switch_id}/ports` | `/redfish/v1/fabrics/test_id_999/switches/test_id_999/ports` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/fabrics/{fabric_id}/switches/{switch_id}/ports` | `/redfish/v1/fabrics/test_id_999/switches/test_id_999/ports` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/fabrics/{fabric_id}/switches/{switch_id}/ports/{port_id}` | `/redfish/v1/fabrics/test_id_999/switches/test_id_999/ports/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/fabrics/{fabric_id}/switches/{switch_id}/ports/{port_id}` | `/redfish/v1/fabrics/test_id_999/switches/test_id_999/ports/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/fabrics/{fabric_id}/switches/{switch_id}/ports/{port_id}` | `/redfish/v1/fabrics/test_id_999/switches/test_id_999/ports/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/jsonschemas` | `/redfish/v1/jsonschemas` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/jsonschemas` | `/redfish/v1/jsonschemas` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/jsonschemas/{jsonschema_id}` | `/redfish/v1/jsonschemas/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/jsonschemas/{jsonschema_id}` | `/redfish/v1/jsonschemas/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/jsonschemas/{jsonschema_id}` | `/redfish/v1/jsonschemas/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/managers` | `/redfish/v1/managers` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers` | `/redfish/v1/managers` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/managers/{manager_id}` | `/redfish/v1/managers/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/managers/{manager_id}` | `/redfish/v1/managers/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/managers/{manager_id}` | `/redfish/v1/managers/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/managers/{manager_id}/ManagerDiagnosticData` | `/redfish/v1/managers/test_id_999/ManagerDiagnosticData` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/ManagerDiagnosticData` | `/redfish/v1/managers/test_id_999/ManagerDiagnosticData` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/activehealthsystem` | `/redfish/v1/managers/test_id_999/activehealthsystem` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/activehealthsystem` | `/redfish/v1/managers/test_id_999/activehealthsystem` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/backuprestoreservice` | `/redfish/v1/managers/test_id_999/backuprestoreservice` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/backuprestoreservice` | `/redfish/v1/managers/test_id_999/backuprestoreservice` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/backuprestoreservice/backupfiles` | `/redfish/v1/managers/test_id_999/backuprestoreservice/backupfiles` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/backuprestoreservice/backupfiles` | `/redfish/v1/managers/test_id_999/backuprestoreservice/backupfiles` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/backuprestoreservice/backupfiles/{backupfil_id}` | `/redfish/v1/managers/test_id_999/backuprestoreservice/backupfiles/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/managers/{manager_id}/backuprestoreservice/backupfiles/{backupfil_id}` | `/redfish/v1/managers/test_id_999/backuprestoreservice/backupfiles/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/managers/{manager_id}/backuprestoreservice/backupfiles/{backupfil_id}` | `/redfish/v1/managers/test_id_999/backuprestoreservice/backupfiles/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/managers/{manager_id}/datetime` | `/redfish/v1/managers/test_id_999/datetime` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/datetime` | `/redfish/v1/managers/test_id_999/datetime` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/dedicatednetworkports` | `/redfish/v1/managers/test_id_999/dedicatednetworkports` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/dedicatednetworkports` | `/redfish/v1/managers/test_id_999/dedicatednetworkports` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/dedicatednetworkports/{dedicatednetworkport_id}` | `/redfish/v1/managers/test_id_999/dedicatednetworkports/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/managers/{manager_id}/dedicatednetworkports/{dedicatednetworkport_id}` | `/redfish/v1/managers/test_id_999/dedicatednetworkports/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/managers/{manager_id}/dedicatednetworkports/{dedicatednetworkport_id}` | `/redfish/v1/managers/test_id_999/dedicatednetworkports/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/managers/{manager_id}/ethernetinterfaces` | `/redfish/v1/managers/test_id_999/ethernetinterfaces` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/ethernetinterfaces` | `/redfish/v1/managers/test_id_999/ethernetinterfaces` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/ethernetinterfaces/{ethernetinterfac_id}` | `/redfish/v1/managers/test_id_999/ethernetinterfaces/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/managers/{manager_id}/ethernetinterfaces/{ethernetinterfac_id}` | `/redfish/v1/managers/test_id_999/ethernetinterfaces/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/managers/{manager_id}/ethernetinterfaces/{ethernetinterfac_id}` | `/redfish/v1/managers/test_id_999/ethernetinterfaces/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/managers/{manager_id}/hostinterfaces` | `/redfish/v1/managers/test_id_999/hostinterfaces` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/hostinterfaces` | `/redfish/v1/managers/test_id_999/hostinterfaces` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/hostinterfaces/{hostinterfac_id}` | `/redfish/v1/managers/test_id_999/hostinterfaces/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/managers/{manager_id}/hostinterfaces/{hostinterfac_id}` | `/redfish/v1/managers/test_id_999/hostinterfaces/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/managers/{manager_id}/hostinterfaces/{hostinterfac_id}` | `/redfish/v1/managers/test_id_999/hostinterfaces/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/managers/{manager_id}/licenseservice` | `/redfish/v1/managers/test_id_999/licenseservice` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/licenseservice` | `/redfish/v1/managers/test_id_999/licenseservice` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/licenseservice/{licenseservice_id}` | `/redfish/v1/managers/test_id_999/licenseservice/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/managers/{manager_id}/licenseservice/{licenseservice_id}` | `/redfish/v1/managers/test_id_999/licenseservice/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/managers/{manager_id}/licenseservice/{licenseservice_id}` | `/redfish/v1/managers/test_id_999/licenseservice/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/managers/{manager_id}/logservices` | `/redfish/v1/managers/test_id_999/logservices` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/logservices` | `/redfish/v1/managers/test_id_999/logservices` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/logservices/iel` | `/redfish/v1/managers/test_id_999/logservices/iel` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/logservices/iel` | `/redfish/v1/managers/test_id_999/logservices/iel` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/logservices/iel/entries` | `/redfish/v1/managers/test_id_999/logservices/iel/entries` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/logservices/iel/entries` | `/redfish/v1/managers/test_id_999/logservices/iel/entries` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/logservices/iel/entries/{entry_id}` | `/redfish/v1/managers/test_id_999/logservices/iel/entries/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/managers/{manager_id}/logservices/iel/entries/{entry_id}` | `/redfish/v1/managers/test_id_999/logservices/iel/entries/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/managers/{manager_id}/logservices/iel/entries/{entry_id}` | `/redfish/v1/managers/test_id_999/logservices/iel/entries/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/managers/{manager_id}/networkprotocol` | `/redfish/v1/managers/test_id_999/networkprotocol` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/networkprotocol` | `/redfish/v1/managers/test_id_999/networkprotocol` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/networkprotocol/HTTPS/certificates` | `/redfish/v1/managers/test_id_999/networkprotocol/HTTPS/certificates` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/networkprotocol/HTTPS/certificates` | `/redfish/v1/managers/test_id_999/networkprotocol/HTTPS/certificates` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/networkprotocol/HTTPS/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/networkprotocol/HTTPS/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/managers/{manager_id}/networkprotocol/HTTPS/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/networkprotocol/HTTPS/certificates/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/managers/{manager_id}/networkprotocol/HTTPS/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/networkprotocol/HTTPS/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/managers/{manager_id}/remotesupportservice` | `/redfish/v1/managers/test_id_999/remotesupportservice` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/remotesupportservice` | `/redfish/v1/managers/test_id_999/remotesupportservice` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/remotesupportservice/serviceeventlogs` | `/redfish/v1/managers/test_id_999/remotesupportservice/serviceeventlogs` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/remotesupportservice/serviceeventlogs` | `/redfish/v1/managers/test_id_999/remotesupportservice/serviceeventlogs` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/remotesupportservice/serviceeventlogs/{serviceeventlog_id}` | `/redfish/v1/managers/test_id_999/remotesupportservice/serviceeventlogs/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/managers/{manager_id}/remotesupportservice/serviceeventlogs/{serviceeventlog_id}` | `/redfish/v1/managers/test_id_999/remotesupportservice/serviceeventlogs/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/managers/{manager_id}/remotesupportservice/serviceeventlogs/{serviceeventlog_id}` | `/redfish/v1/managers/test_id_999/remotesupportservice/serviceeventlogs/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/managers/{manager_id}/securityservice` | `/redfish/v1/managers/test_id_999/securityservice` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/securityservice` | `/redfish/v1/managers/test_id_999/securityservice` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/securityservice/bmchpeldevid/certificates` | `/redfish/v1/managers/test_id_999/securityservice/bmchpeldevid/certificates` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/securityservice/bmchpeldevid/certificates` | `/redfish/v1/managers/test_id_999/securityservice/bmchpeldevid/certificates` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/securityservice/bmchpeldevid/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/bmchpeldevid/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/managers/{manager_id}/securityservice/bmchpeldevid/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/bmchpeldevid/certificates/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/managers/{manager_id}/securityservice/bmchpeldevid/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/bmchpeldevid/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/managers/{manager_id}/securityservice/bmciak/certificates` | `/redfish/v1/managers/test_id_999/securityservice/bmciak/certificates` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/securityservice/bmciak/certificates` | `/redfish/v1/managers/test_id_999/securityservice/bmciak/certificates` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/securityservice/bmciak/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/bmciak/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/managers/{manager_id}/securityservice/bmciak/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/bmciak/certificates/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/managers/{manager_id}/securityservice/bmciak/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/bmciak/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/managers/{manager_id}/securityservice/bmcidevidpca/certificates` | `/redfish/v1/managers/test_id_999/securityservice/bmcidevidpca/certificates` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/securityservice/bmcidevidpca/certificates` | `/redfish/v1/managers/test_id_999/securityservice/bmcidevidpca/certificates` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/securityservice/bmcidevidpca/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/bmcidevidpca/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/managers/{manager_id}/securityservice/bmcidevidpca/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/bmcidevidpca/certificates/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/managers/{manager_id}/securityservice/bmcidevidpca/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/bmcidevidpca/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/managers/{manager_id}/securityservice/bmclak/certificates` | `/redfish/v1/managers/test_id_999/securityservice/bmclak/certificates` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/securityservice/bmclak/certificates` | `/redfish/v1/managers/test_id_999/securityservice/bmclak/certificates` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/securityservice/bmclak/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/bmclak/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/managers/{manager_id}/securityservice/bmclak/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/bmclak/certificates/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/managers/{manager_id}/securityservice/bmclak/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/bmclak/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/managers/{manager_id}/securityservice/certificateauthentication` | `/redfish/v1/managers/test_id_999/securityservice/certificateauthentication` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/securityservice/certificateauthentication` | `/redfish/v1/managers/test_id_999/securityservice/certificateauthentication` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/securityservice/certificateauthentication/cacertificates` | `/redfish/v1/managers/test_id_999/securityservice/certificateauthentication/cacertificates` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/securityservice/certificateauthentication/cacertificates` | `/redfish/v1/managers/test_id_999/securityservice/certificateauthentication/cacertificates` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/securityservice/certificateauthentication/cacertificates/{cacertificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/certificateauthentication/cacertificates/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/managers/{manager_id}/securityservice/certificateauthentication/cacertificates/{cacertificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/certificateauthentication/cacertificates/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/managers/{manager_id}/securityservice/certificateauthentication/cacertificates/{cacertificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/certificateauthentication/cacertificates/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/managers/{manager_id}/securityservice/eskm` | `/redfish/v1/managers/test_id_999/securityservice/eskm` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/securityservice/eskm` | `/redfish/v1/managers/test_id_999/securityservice/eskm` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/securityservice/httpscert` | `/redfish/v1/managers/test_id_999/securityservice/httpscert` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/securityservice/httpscert` | `/redfish/v1/managers/test_id_999/securityservice/httpscert` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/securityservice/platformcert/certificates` | `/redfish/v1/managers/test_id_999/securityservice/platformcert/certificates` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/securityservice/platformcert/certificates` | `/redfish/v1/managers/test_id_999/securityservice/platformcert/certificates` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/securityservice/platformcert/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/platformcert/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/managers/{manager_id}/securityservice/platformcert/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/platformcert/certificates/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/managers/{manager_id}/securityservice/platformcert/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/platformcert/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/managers/{manager_id}/securityservice/securitydashboard` | `/redfish/v1/managers/test_id_999/securityservice/securitydashboard` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/securityservice/securitydashboard` | `/redfish/v1/managers/test_id_999/securityservice/securitydashboard` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/securityservice/securitydashboard/securityparams` | `/redfish/v1/managers/test_id_999/securityservice/securitydashboard/securityparams` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/securityservice/securitydashboard/securityparams` | `/redfish/v1/managers/test_id_999/securityservice/securitydashboard/securityparams` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/securityservice/securitydashboard/securityparams/{securityparam_id}` | `/redfish/v1/managers/test_id_999/securityservice/securitydashboard/securityparams/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/managers/{manager_id}/securityservice/securitydashboard/securityparams/{securityparam_id}` | `/redfish/v1/managers/test_id_999/securityservice/securitydashboard/securityparams/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/managers/{manager_id}/securityservice/securitydashboard/securityparams/{securityparam_id}` | `/redfish/v1/managers/test_id_999/securityservice/securitydashboard/securityparams/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/managers/{manager_id}/securityservice/sso` | `/redfish/v1/managers/test_id_999/securityservice/sso` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/securityservice/sso` | `/redfish/v1/managers/test_id_999/securityservice/sso` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/securityservice/systemiak/certificates` | `/redfish/v1/managers/test_id_999/securityservice/systemiak/certificates` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/securityservice/systemiak/certificates` | `/redfish/v1/managers/test_id_999/securityservice/systemiak/certificates` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/securityservice/systemiak/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/systemiak/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/managers/{manager_id}/securityservice/systemiak/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/systemiak/certificates/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/managers/{manager_id}/securityservice/systemiak/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/systemiak/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/managers/{manager_id}/securityservice/systemidevid/certificates` | `/redfish/v1/managers/test_id_999/securityservice/systemidevid/certificates` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/securityservice/systemidevid/certificates` | `/redfish/v1/managers/test_id_999/securityservice/systemidevid/certificates` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/securityservice/systemidevid/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/systemidevid/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/managers/{manager_id}/securityservice/systemidevid/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/systemidevid/certificates/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/managers/{manager_id}/securityservice/systemidevid/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/systemidevid/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/managers/{manager_id}/securityservice/systemlak/certificates` | `/redfish/v1/managers/test_id_999/securityservice/systemlak/certificates` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/securityservice/systemlak/certificates` | `/redfish/v1/managers/test_id_999/securityservice/systemlak/certificates` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/securityservice/systemlak/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/systemlak/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/managers/{manager_id}/securityservice/systemlak/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/systemlak/certificates/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/managers/{manager_id}/securityservice/systemlak/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/systemlak/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/managers/{manager_id}/securityservice/systemldevid/certificates` | `/redfish/v1/managers/test_id_999/securityservice/systemldevid/certificates` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/securityservice/systemldevid/certificates` | `/redfish/v1/managers/test_id_999/securityservice/systemldevid/certificates` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/securityservice/systemldevid/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/systemldevid/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/managers/{manager_id}/securityservice/systemldevid/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/systemldevid/certificates/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/managers/{manager_id}/securityservice/systemldevid/certificates/{certificat_id}` | `/redfish/v1/managers/test_id_999/securityservice/systemldevid/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/managers/{manager_id}/sharednetworkports` | `/redfish/v1/managers/test_id_999/sharednetworkports` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/sharednetworkports` | `/redfish/v1/managers/test_id_999/sharednetworkports` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/sharednetworkports/{sharednetworkport_id}` | `/redfish/v1/managers/test_id_999/sharednetworkports/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/managers/{manager_id}/sharednetworkports/{sharednetworkport_id}` | `/redfish/v1/managers/test_id_999/sharednetworkports/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/managers/{manager_id}/sharednetworkports/{sharednetworkport_id}` | `/redfish/v1/managers/test_id_999/sharednetworkports/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/managers/{manager_id}/snmpservice` | `/redfish/v1/managers/test_id_999/snmpservice` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/snmpservice` | `/redfish/v1/managers/test_id_999/snmpservice` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/snmpservice/snmpalertdestinations` | `/redfish/v1/managers/test_id_999/snmpservice/snmpalertdestinations` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/snmpservice/snmpalertdestinations` | `/redfish/v1/managers/test_id_999/snmpservice/snmpalertdestinations` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/snmpservice/snmpalertdestinations/{snmpalertdestination_id}` | `/redfish/v1/managers/test_id_999/snmpservice/snmpalertdestinations/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/managers/{manager_id}/snmpservice/snmpalertdestinations/{snmpalertdestination_id}` | `/redfish/v1/managers/test_id_999/snmpservice/snmpalertdestinations/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/managers/{manager_id}/snmpservice/snmpalertdestinations/{snmpalertdestination_id}` | `/redfish/v1/managers/test_id_999/snmpservice/snmpalertdestinations/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/managers/{manager_id}/snmpservice/snmpusers` | `/redfish/v1/managers/test_id_999/snmpservice/snmpusers` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/snmpservice/snmpusers` | `/redfish/v1/managers/test_id_999/snmpservice/snmpusers` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/snmpservice/snmpusers/{snmpuser_id}` | `/redfish/v1/managers/test_id_999/snmpservice/snmpusers/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/managers/{manager_id}/snmpservice/snmpusers/{snmpuser_id}` | `/redfish/v1/managers/test_id_999/snmpservice/snmpusers/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/managers/{manager_id}/snmpservice/snmpusers/{snmpuser_id}` | `/redfish/v1/managers/test_id_999/snmpservice/snmpusers/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/managers/{manager_id}/virtualmedia` | `/redfish/v1/managers/test_id_999/virtualmedia` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/managers/{manager_id}/virtualmedia` | `/redfish/v1/managers/test_id_999/virtualmedia` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/managers/{manager_id}/virtualmedia/{virtualmedia_id}` | `/redfish/v1/managers/test_id_999/virtualmedia/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/managers/{manager_id}/virtualmedia/{virtualmedia_id}` | `/redfish/v1/managers/test_id_999/virtualmedia/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/managers/{manager_id}/virtualmedia/{virtualmedia_id}` | `/redfish/v1/managers/test_id_999/virtualmedia/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/registries` | `/redfish/v1/registries` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/registries` | `/redfish/v1/registries` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/registries/{registry_id}` | `/redfish/v1/registries/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/registries/{registry_id}` | `/redfish/v1/registries/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/registries/{registry_id}` | `/redfish/v1/registries/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/resourcedirectory` | `/redfish/v1/resourcedirectory` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/resourcedirectory` | `/redfish/v1/resourcedirectory` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/sessionservice` | `/redfish/v1/sessionservice` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/sessionservice` | `/redfish/v1/sessionservice` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/sessionservice/sessions` | `/redfish/v1/sessionservice/sessions` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/sessionservice/sessions` | `/redfish/v1/sessionservice/sessions` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/sessionservice/sessions/{session_id}` | `/redfish/v1/sessionservice/sessions/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/sessionservice/sessions/{session_id}` | `/redfish/v1/sessionservice/sessions/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/sessionservice/sessions/{session_id}` | `/redfish/v1/sessionservice/sessions/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems` | `/redfish/v1/systems` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems` | `/redfish/v1/systems` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/systems/{system_id}` | `/redfish/v1/systems/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}` | `/redfish/v1/systems/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}` | `/redfish/v1/systems/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/bios` | `/redfish/v1/systems/test_id_999/bios` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/bios` | `/redfish/v1/systems/test_id_999/bios` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/bios/baseconfigs` | `/redfish/v1/systems/test_id_999/bios/baseconfigs` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/bios/baseconfigs` | `/redfish/v1/systems/test_id_999/bios/baseconfigs` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/bios/boot` | `/redfish/v1/systems/test_id_999/bios/boot` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/bios/boot` | `/redfish/v1/systems/test_id_999/bios/boot` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/bios/boot/baseconfigs` | `/redfish/v1/systems/test_id_999/bios/boot/baseconfigs` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/bios/boot/baseconfigs` | `/redfish/v1/systems/test_id_999/bios/boot/baseconfigs` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/bios/boot/settings` | `/redfish/v1/systems/test_id_999/bios/boot/settings` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/bios/boot/settings` | `/redfish/v1/systems/test_id_999/bios/boot/settings` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/bios/iscsi` | `/redfish/v1/systems/test_id_999/bios/iscsi` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/bios/iscsi` | `/redfish/v1/systems/test_id_999/bios/iscsi` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/bios/iscsi/baseconfigs` | `/redfish/v1/systems/test_id_999/bios/iscsi/baseconfigs` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/bios/iscsi/baseconfigs` | `/redfish/v1/systems/test_id_999/bios/iscsi/baseconfigs` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/bios/iscsi/settings` | `/redfish/v1/systems/test_id_999/bios/iscsi/settings` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/bios/iscsi/settings` | `/redfish/v1/systems/test_id_999/bios/iscsi/settings` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/bios/kmsconfig` | `/redfish/v1/systems/test_id_999/bios/kmsconfig` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/bios/kmsconfig` | `/redfish/v1/systems/test_id_999/bios/kmsconfig` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/bios/kmsconfig/baseconfigs` | `/redfish/v1/systems/test_id_999/bios/kmsconfig/baseconfigs` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/bios/kmsconfig/baseconfigs` | `/redfish/v1/systems/test_id_999/bios/kmsconfig/baseconfigs` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/bios/kmsconfig/settings` | `/redfish/v1/systems/test_id_999/bios/kmsconfig/settings` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/bios/kmsconfig/settings` | `/redfish/v1/systems/test_id_999/bios/kmsconfig/settings` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/bios/mappings` | `/redfish/v1/systems/test_id_999/bios/mappings` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/bios/mappings` | `/redfish/v1/systems/test_id_999/bios/mappings` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig` | `/redfish/v1/systems/test_id_999/bios/oem/hpe/tlsconfig` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig` | `/redfish/v1/systems/test_id_999/bios/oem/hpe/tlsconfig` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig/baseconfigs` | `/redfish/v1/systems/test_id_999/bios/oem/hpe/tlsconfig/baseconfigs` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig/baseconfigs` | `/redfish/v1/systems/test_id_999/bios/oem/hpe/tlsconfig/baseconfigs` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig/settings` | `/redfish/v1/systems/test_id_999/bios/oem/hpe/tlsconfig/settings` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig/settings` | `/redfish/v1/systems/test_id_999/bios/oem/hpe/tlsconfig/settings` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/bios/serverconfiglock` | `/redfish/v1/systems/test_id_999/bios/serverconfiglock` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/bios/serverconfiglock` | `/redfish/v1/systems/test_id_999/bios/serverconfiglock` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/bios/serverconfiglock/baseconfigs` | `/redfish/v1/systems/test_id_999/bios/serverconfiglock/baseconfigs` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/bios/serverconfiglock/baseconfigs` | `/redfish/v1/systems/test_id_999/bios/serverconfiglock/baseconfigs` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/bios/serverconfiglock/settings` | `/redfish/v1/systems/test_id_999/bios/serverconfiglock/settings` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/bios/serverconfiglock/settings` | `/redfish/v1/systems/test_id_999/bios/serverconfiglock/settings` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/bios/settings` | `/redfish/v1/systems/test_id_999/bios/settings` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/bios/settings` | `/redfish/v1/systems/test_id_999/bios/settings` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/bootoptions` | `/redfish/v1/systems/test_id_999/bootoptions` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/bootoptions` | `/redfish/v1/systems/test_id_999/bootoptions` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/bootoptions/{bootoption_id}` | `/redfish/v1/systems/test_id_999/bootoptions/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/bootoptions/{bootoption_id}` | `/redfish/v1/systems/test_id_999/bootoptions/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/bootoptions/{bootoption_id}` | `/redfish/v1/systems/test_id_999/bootoptions/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/ethernetinterfaces` | `/redfish/v1/systems/test_id_999/ethernetinterfaces` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/ethernetinterfaces` | `/redfish/v1/systems/test_id_999/ethernetinterfaces` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/ethernetinterfaces/{ethernetinterfac_id}` | `/redfish/v1/systems/test_id_999/ethernetinterfaces/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/ethernetinterfaces/{ethernetinterfac_id}` | `/redfish/v1/systems/test_id_999/ethernetinterfaces/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/ethernetinterfaces/{ethernetinterfac_id}` | `/redfish/v1/systems/test_id_999/ethernetinterfaces/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/keymanagement/KMIPcertificates` | `/redfish/v1/systems/test_id_999/keymanagement/KMIPcertificates` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/keymanagement/KMIPcertificates` | `/redfish/v1/systems/test_id_999/keymanagement/KMIPcertificates` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/keymanagement/KMIPcertificates/{kmipcertificat_id}` | `/redfish/v1/systems/test_id_999/keymanagement/KMIPcertificates/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/keymanagement/KMIPcertificates/{kmipcertificat_id}` | `/redfish/v1/systems/test_id_999/keymanagement/KMIPcertificates/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/keymanagement/KMIPcertificates/{kmipcertificat_id}` | `/redfish/v1/systems/test_id_999/keymanagement/KMIPcertificates/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/keymanagement/KMIPclientcertificates` | `/redfish/v1/systems/test_id_999/keymanagement/KMIPclientcertificates` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/keymanagement/KMIPclientcertificates` | `/redfish/v1/systems/test_id_999/keymanagement/KMIPclientcertificates` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/keymanagement/KMIPclientcertificates/{kmipclientcertificat_id}` | `/redfish/v1/systems/test_id_999/keymanagement/KMIPclientcertificates/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/keymanagement/KMIPclientcertificates/{kmipclientcertificat_id}` | `/redfish/v1/systems/test_id_999/keymanagement/KMIPclientcertificates/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/keymanagement/KMIPclientcertificates/{kmipclientcertificat_id}` | `/redfish/v1/systems/test_id_999/keymanagement/KMIPclientcertificates/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/logservices` | `/redfish/v1/systems/test_id_999/logservices` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/logservices` | `/redfish/v1/systems/test_id_999/logservices` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/logservices/dpu` | `/redfish/v1/systems/test_id_999/logservices/dpu` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/logservices/dpu` | `/redfish/v1/systems/test_id_999/logservices/dpu` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/logservices/dpu/entries` | `/redfish/v1/systems/test_id_999/logservices/dpu/entries` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/logservices/dpu/entries` | `/redfish/v1/systems/test_id_999/logservices/dpu/entries` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/logservices/dpu/entries/{entry_id}` | `/redfish/v1/systems/test_id_999/logservices/dpu/entries/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/logservices/dpu/entries/{entry_id}` | `/redfish/v1/systems/test_id_999/logservices/dpu/entries/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/logservices/dpu/entries/{entry_id}` | `/redfish/v1/systems/test_id_999/logservices/dpu/entries/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/logservices/event` | `/redfish/v1/systems/test_id_999/logservices/event` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/logservices/event` | `/redfish/v1/systems/test_id_999/logservices/event` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/logservices/event/entries` | `/redfish/v1/systems/test_id_999/logservices/event/entries` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/logservices/event/entries` | `/redfish/v1/systems/test_id_999/logservices/event/entries` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/logservices/event/entries/{entry_id}` | `/redfish/v1/systems/test_id_999/logservices/event/entries/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/logservices/event/entries/{entry_id}` | `/redfish/v1/systems/test_id_999/logservices/event/entries/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/logservices/event/entries/{entry_id}` | `/redfish/v1/systems/test_id_999/logservices/event/entries/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/logservices/iml` | `/redfish/v1/systems/test_id_999/logservices/iml` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/logservices/iml` | `/redfish/v1/systems/test_id_999/logservices/iml` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/logservices/iml/entries` | `/redfish/v1/systems/test_id_999/logservices/iml/entries` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/logservices/iml/entries` | `/redfish/v1/systems/test_id_999/logservices/iml/entries` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/logservices/iml/entries/{entry_id}` | `/redfish/v1/systems/test_id_999/logservices/iml/entries/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/logservices/iml/entries/{entry_id}` | `/redfish/v1/systems/test_id_999/logservices/iml/entries/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/logservices/iml/entries/{entry_id}` | `/redfish/v1/systems/test_id_999/logservices/iml/entries/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/logservices/sl` | `/redfish/v1/systems/test_id_999/logservices/sl` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/logservices/sl` | `/redfish/v1/systems/test_id_999/logservices/sl` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/logservices/sl/entries` | `/redfish/v1/systems/test_id_999/logservices/sl/entries` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/logservices/sl/entries` | `/redfish/v1/systems/test_id_999/logservices/sl/entries` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/logservices/sl/entries/{entry_id}` | `/redfish/v1/systems/test_id_999/logservices/sl/entries/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/logservices/sl/entries/{entry_id}` | `/redfish/v1/systems/test_id_999/logservices/sl/entries/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/logservices/sl/entries/{entry_id}` | `/redfish/v1/systems/test_id_999/logservices/sl/entries/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/memory` | `/redfish/v1/systems/test_id_999/memory` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/memory` | `/redfish/v1/systems/test_id_999/memory` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/memory/{memory_id}` | `/redfish/v1/systems/test_id_999/memory/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/memory/{memory_id}` | `/redfish/v1/systems/test_id_999/memory/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/memory/{memory_id}` | `/redfish/v1/systems/test_id_999/memory/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/memory/{memory_id}/memorymetrics` | `/redfish/v1/systems/test_id_999/memory/test_id_999/memorymetrics` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/memory/{memory_id}/memorymetrics` | `/redfish/v1/systems/test_id_999/memory/test_id_999/memorymetrics` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/memorydomains` | `/redfish/v1/systems/test_id_999/memorydomains` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/memorydomains` | `/redfish/v1/systems/test_id_999/memorydomains` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}` | `/redfish/v1/systems/test_id_999/memorydomains/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}` | `/redfish/v1/systems/test_id_999/memorydomains/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}` | `/redfish/v1/systems/test_id_999/memorydomains/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}/memorychunks` | `/redfish/v1/systems/test_id_999/memorydomains/test_id_999/memorychunks` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}/memorychunks` | `/redfish/v1/systems/test_id_999/memorydomains/test_id_999/memorychunks` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}/memorychunks/{memorychunk_id}` | `/redfish/v1/systems/test_id_999/memorydomains/test_id_999/memorychunks/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}/memorychunks/{memorychunk_id}` | `/redfish/v1/systems/test_id_999/memorydomains/test_id_999/memorychunks/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}/memorychunks/{memorychunk_id}` | `/redfish/v1/systems/test_id_999/memorydomains/test_id_999/memorychunks/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/networkinterfaces` | `/redfish/v1/systems/test_id_999/networkinterfaces` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/networkinterfaces` | `/redfish/v1/systems/test_id_999/networkinterfaces` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}` | `/redfish/v1/systems/test_id_999/networkinterfaces/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}` | `/redfish/v1/systems/test_id_999/networkinterfaces/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}` | `/redfish/v1/systems/test_id_999/networkinterfaces/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions` | `/redfish/v1/systems/test_id_999/networkinterfaces/test_id_999/networkdevicefunctions` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions` | `/redfish/v1/systems/test_id_999/networkinterfaces/test_id_999/networkdevicefunctions` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions/{networkdevicefunction_id}` | `/redfish/v1/systems/test_id_999/networkinterfaces/test_id_999/networkdevicefunctions/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions/{networkdevicefunction_id}` | `/redfish/v1/systems/test_id_999/networkinterfaces/test_id_999/networkdevicefunctions/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions/{networkdevicefunction_id}` | `/redfish/v1/systems/test_id_999/networkinterfaces/test_id_999/networkdevicefunctions/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions/{networkdevicefunction_id}/settings` | `/redfish/v1/systems/test_id_999/networkinterfaces/test_id_999/networkdevicefunctions/test_id_999/settings` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions/{networkdevicefunction_id}/settings` | `/redfish/v1/systems/test_id_999/networkinterfaces/test_id_999/networkdevicefunctions/test_id_999/settings` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports` | `/redfish/v1/systems/test_id_999/networkinterfaces/test_id_999/ports` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports` | `/redfish/v1/systems/test_id_999/networkinterfaces/test_id_999/ports` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports/{port_id}` | `/redfish/v1/systems/test_id_999/networkinterfaces/test_id_999/ports/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports/{port_id}` | `/redfish/v1/systems/test_id_999/networkinterfaces/test_id_999/ports/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports/{port_id}` | `/redfish/v1/systems/test_id_999/networkinterfaces/test_id_999/ports/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports/{port_id}/settings` | `/redfish/v1/systems/test_id_999/networkinterfaces/test_id_999/ports/test_id_999/settings` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports/{port_id}/settings` | `/redfish/v1/systems/test_id_999/networkinterfaces/test_id_999/ports/test_id_999/settings` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/pcidevices` | `/redfish/v1/systems/test_id_999/pcidevices` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/pcidevices` | `/redfish/v1/systems/test_id_999/pcidevices` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/pcidevices/{pcidevic_id}` | `/redfish/v1/systems/test_id_999/pcidevices/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/pcidevices/{pcidevic_id}` | `/redfish/v1/systems/test_id_999/pcidevices/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/pcidevices/{pcidevic_id}` | `/redfish/v1/systems/test_id_999/pcidevices/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/pcislots` | `/redfish/v1/systems/test_id_999/pcislots` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/pcislots` | `/redfish/v1/systems/test_id_999/pcislots` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/pcislots/{pcislot_id}` | `/redfish/v1/systems/test_id_999/pcislots/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/pcislots/{pcislot_id}` | `/redfish/v1/systems/test_id_999/pcislots/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/pcislots/{pcislot_id}` | `/redfish/v1/systems/test_id_999/pcislots/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/processors` | `/redfish/v1/systems/test_id_999/processors` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/processors` | `/redfish/v1/systems/test_id_999/processors` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/processors/{processor_id}` | `/redfish/v1/systems/test_id_999/processors/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/processors/{processor_id}` | `/redfish/v1/systems/test_id_999/processors/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/processors/{processor_id}` | `/redfish/v1/systems/test_id_999/processors/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/processors/{processor_id}/environmentmetrics` | `/redfish/v1/systems/test_id_999/processors/test_id_999/environmentmetrics` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/processors/{processor_id}/environmentmetrics` | `/redfish/v1/systems/test_id_999/processors/test_id_999/environmentmetrics` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/processors/{processor_id}/processormetrics` | `/redfish/v1/systems/test_id_999/processors/test_id_999/processormetrics` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/processors/{processor_id}/processormetrics` | `/redfish/v1/systems/test_id_999/processors/test_id_999/processormetrics` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot` | `/redfish/v1/systems/test_id_999/secureboot` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot` | `/redfish/v1/systems/test_id_999/secureboot` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/db` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/db` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/certificates` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/db/certificates` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/certificates` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/db/certificates` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/db/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/db/certificates/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/db/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/signatures` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/db/signatures` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/signatures` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/db/signatures` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/signatures/{signatur_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/db/signatures/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/signatures/{signatur_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/db/signatures/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/signatures/{signatur_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/db/signatures/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbdefault` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbdefault` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/certificates` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbdefault/certificates` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/certificates` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbdefault/certificates` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbdefault/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbdefault/certificates/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbdefault/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/signatures` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbdefault/signatures` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/signatures` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbdefault/signatures` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/signatures/{signatur_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbdefault/signatures/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/signatures/{signatur_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbdefault/signatures/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/signatures/{signatur_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbdefault/signatures/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbr` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbr` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/certificates` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbr/certificates` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/certificates` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbr/certificates` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbr/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbr/certificates/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbr/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/signatures` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbr/signatures` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/signatures` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbr/signatures` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/signatures/{signatur_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbr/signatures/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/signatures/{signatur_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbr/signatures/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/signatures/{signatur_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbr/signatures/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbrdefault` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbrdefault` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/certificates` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbrdefault/certificates` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/certificates` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbrdefault/certificates` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbrdefault/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbrdefault/certificates/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbrdefault/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/signatures` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbrdefault/signatures` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/signatures` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbrdefault/signatures` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/signatures/{signatur_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbrdefault/signatures/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/signatures/{signatur_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbrdefault/signatures/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/signatures/{signatur_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbrdefault/signatures/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbt` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbt` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/certificates` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbt/certificates` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/certificates` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbt/certificates` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbt/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbt/certificates/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbt/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/signatures` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbt/signatures` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/signatures` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbt/signatures` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/signatures/{signatur_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbt/signatures/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/signatures/{signatur_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbt/signatures/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/signatures/{signatur_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbt/signatures/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbtdefault` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbtdefault` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/certificates` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbtdefault/certificates` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/certificates` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbtdefault/certificates` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbtdefault/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbtdefault/certificates/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbtdefault/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/signatures` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbtdefault/signatures` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/signatures` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbtdefault/signatures` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/signatures/{signatur_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbtdefault/signatures/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/signatures/{signatur_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbtdefault/signatures/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/signatures/{signatur_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbtdefault/signatures/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbx` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbx` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/certificates` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbx/certificates` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/certificates` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbx/certificates` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbx/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbx/certificates/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbx/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/signatures` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbx/signatures` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/signatures` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbx/signatures` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/signatures/{signatur_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbx/signatures/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/signatures/{signatur_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbx/signatures/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/signatures/{signatur_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbx/signatures/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbxdefault` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbxdefault` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/certificates` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbxdefault/certificates` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/certificates` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbxdefault/certificates` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbxdefault/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbxdefault/certificates/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbxdefault/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/signatures` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbxdefault/signatures` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/signatures` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbxdefault/signatures` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/signatures/{signatur_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbxdefault/signatures/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/signatures/{signatur_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbxdefault/signatures/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/signatures/{signatur_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/dbxdefault/signatures/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/kek` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/kek` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek/certificates` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/kek/certificates` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek/certificates` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/kek/certificates` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/kek/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/kek/certificates/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/kek/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/kekdefault` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/kekdefault` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault/certificates` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/kekdefault/certificates` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault/certificates` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/kekdefault/certificates` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/kekdefault/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/kekdefault/certificates/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/kekdefault/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/pk` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/pk` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk/certificates` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/pk/certificates` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk/certificates` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/pk/certificates` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/pk/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/pk/certificates/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/pk/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/pkdefault` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/pkdefault` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault/certificates` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/pkdefault/certificates` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault/certificates` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/pkdefault/certificates` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/pkdefault/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/pkdefault/certificates/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault/certificates/{certificat_id}` | `/redfish/v1/systems/test_id_999/secureboot/securebootdatabases/pkdefault/certificates/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/secureerasereportservice` | `/redfish/v1/systems/test_id_999/secureerasereportservice` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureerasereportservice` | `/redfish/v1/systems/test_id_999/secureerasereportservice` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureerasereportservice/secureerasereportentries` | `/redfish/v1/systems/test_id_999/secureerasereportservice/secureerasereportentries` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/secureerasereportservice/secureerasereportentries` | `/redfish/v1/systems/test_id_999/secureerasereportservice/secureerasereportentries` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/secureerasereportservice/secureerasereportentries/{secureerasereportentry_id}` | `/redfish/v1/systems/test_id_999/secureerasereportservice/secureerasereportentries/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/secureerasereportservice/secureerasereportentries/{secureerasereportentry_id}` | `/redfish/v1/systems/test_id_999/secureerasereportservice/secureerasereportentries/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/secureerasereportservice/secureerasereportentries/{secureerasereportentry_id}` | `/redfish/v1/systems/test_id_999/secureerasereportservice/secureerasereportentries/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/storage` | `/redfish/v1/systems/test_id_999/storage` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/storage` | `/redfish/v1/systems/test_id_999/storage` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/storage/{storage_id}` | `/redfish/v1/systems/test_id_999/storage/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/storage/{storage_id}` | `/redfish/v1/systems/test_id_999/storage/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/storage/{storage_id}` | `/redfish/v1/systems/test_id_999/storage/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/` | `/redfish/v1/systems/test_id_999/storage/test_id_999/controllers/` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/` | `/redfish/v1/systems/test_id_999/storage/test_id_999/controllers/` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}` | `/redfish/v1/systems/test_id_999/storage/test_id_999/controllers/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}` | `/redfish/v1/systems/test_id_999/storage/test_id_999/controllers/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}` | `/redfish/v1/systems/test_id_999/storage/test_id_999/controllers/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/assembly` | `/redfish/v1/systems/test_id_999/storage/test_id_999/controllers/test_id_999/assembly` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/assembly` | `/redfish/v1/systems/test_id_999/storage/test_id_999/controllers/test_id_999/assembly` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/ports` | `/redfish/v1/systems/test_id_999/storage/test_id_999/controllers/test_id_999/ports` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/ports` | `/redfish/v1/systems/test_id_999/storage/test_id_999/controllers/test_id_999/ports` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/ports/{port_id}` | `/redfish/v1/systems/test_id_999/storage/test_id_999/controllers/test_id_999/ports/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/ports/{port_id}` | `/redfish/v1/systems/test_id_999/storage/test_id_999/controllers/test_id_999/ports/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/ports/{port_id}` | `/redfish/v1/systems/test_id_999/storage/test_id_999/controllers/test_id_999/ports/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/storage/{storage_id}/drives/{driv_id}` | `/redfish/v1/systems/test_id_999/storage/test_id_999/drives/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/storage/{storage_id}/drives/{driv_id}` | `/redfish/v1/systems/test_id_999/storage/test_id_999/drives/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/storage/{storage_id}/drives/{driv_id}` | `/redfish/v1/systems/test_id_999/storage/test_id_999/drives/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/storage/{storage_id}/storagecontrollers/{storagecontroller_id}/ports` | `/redfish/v1/systems/test_id_999/storage/test_id_999/storagecontrollers/test_id_999/ports` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/storage/{storage_id}/storagecontrollers/{storagecontroller_id}/ports` | `/redfish/v1/systems/test_id_999/storage/test_id_999/storagecontrollers/test_id_999/ports` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/storage/{storage_id}/storagecontrollers/{storagecontroller_id}/ports/{port_id}` | `/redfish/v1/systems/test_id_999/storage/test_id_999/storagecontrollers/test_id_999/ports/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/storage/{storage_id}/storagecontrollers/{storagecontroller_id}/ports/{port_id}` | `/redfish/v1/systems/test_id_999/storage/test_id_999/storagecontrollers/test_id_999/ports/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/storage/{storage_id}/storagecontrollers/{storagecontroller_id}/ports/{port_id}` | `/redfish/v1/systems/test_id_999/storage/test_id_999/storagecontrollers/test_id_999/ports/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/storage/{storage_id}/volumes` | `/redfish/v1/systems/test_id_999/storage/test_id_999/volumes` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/storage/{storage_id}/volumes` | `/redfish/v1/systems/test_id_999/storage/test_id_999/volumes` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/storage/{storage_id}/volumes/{volum_id}` | `/redfish/v1/systems/test_id_999/storage/test_id_999/volumes/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/storage/{storage_id}/volumes/{volum_id}` | `/redfish/v1/systems/test_id_999/storage/test_id_999/volumes/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/storage/{storage_id}/volumes/{volum_id}` | `/redfish/v1/systems/test_id_999/storage/test_id_999/volumes/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/usbdevices` | `/redfish/v1/systems/test_id_999/usbdevices` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/usbdevices` | `/redfish/v1/systems/test_id_999/usbdevices` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/usbdevices/{usbdevic_id}` | `/redfish/v1/systems/test_id_999/usbdevices/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/usbdevices/{usbdevic_id}` | `/redfish/v1/systems/test_id_999/usbdevices/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/usbdevices/{usbdevic_id}` | `/redfish/v1/systems/test_id_999/usbdevices/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/usbports` | `/redfish/v1/systems/test_id_999/usbports` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/usbports` | `/redfish/v1/systems/test_id_999/usbports` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/usbports/{usbport_id}` | `/redfish/v1/systems/test_id_999/usbports/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/usbports/{usbport_id}` | `/redfish/v1/systems/test_id_999/usbports/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/usbports/{usbport_id}` | `/redfish/v1/systems/test_id_999/usbports/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/systems/{system_id}/workloadperformanceadvisor` | `/redfish/v1/systems/test_id_999/workloadperformanceadvisor` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/systems/{system_id}/workloadperformanceadvisor` | `/redfish/v1/systems/test_id_999/workloadperformanceadvisor` | CRASH | CRASH_EXCEPTION |
| GET | `/redfish/v1/systems/{system_id}/workloadperformanceadvisor/{workloadperformanceadvisor_id}` | `/redfish/v1/systems/test_id_999/workloadperformanceadvisor/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/systems/{system_id}/workloadperformanceadvisor/{workloadperformanceadvisor_id}` | `/redfish/v1/systems/test_id_999/workloadperformanceadvisor/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/systems/{system_id}/workloadperformanceadvisor/{workloadperformanceadvisor_id}` | `/redfish/v1/systems/test_id_999/workloadperformanceadvisor/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/taskservice` | `/redfish/v1/taskservice` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/taskservice` | `/redfish/v1/taskservice` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/taskservice/tasks` | `/redfish/v1/taskservice/tasks` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/taskservice/tasks` | `/redfish/v1/taskservice/tasks` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/taskservice/tasks/{task_id}` | `/redfish/v1/taskservice/tasks/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/taskservice/tasks/{task_id}` | `/redfish/v1/taskservice/tasks/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/taskservice/tasks/{task_id}` | `/redfish/v1/taskservice/tasks/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/telemetryservice` | `/redfish/v1/telemetryservice` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/telemetryservice` | `/redfish/v1/telemetryservice` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/telemetryservice/metricdefinitions` | `/redfish/v1/telemetryservice/metricdefinitions` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/telemetryservice/metricdefinitions` | `/redfish/v1/telemetryservice/metricdefinitions` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/telemetryservice/metricdefinitions/{metricdefinition_id}` | `/redfish/v1/telemetryservice/metricdefinitions/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/telemetryservice/metricdefinitions/{metricdefinition_id}` | `/redfish/v1/telemetryservice/metricdefinitions/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/telemetryservice/metricdefinitions/{metricdefinition_id}` | `/redfish/v1/telemetryservice/metricdefinitions/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/telemetryservice/metricreportdefinitions` | `/redfish/v1/telemetryservice/metricreportdefinitions` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/telemetryservice/metricreportdefinitions` | `/redfish/v1/telemetryservice/metricreportdefinitions` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/telemetryservice/metricreportdefinitions/{metricreportdefinition_id}` | `/redfish/v1/telemetryservice/metricreportdefinitions/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/telemetryservice/metricreportdefinitions/{metricreportdefinition_id}` | `/redfish/v1/telemetryservice/metricreportdefinitions/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/telemetryservice/metricreportdefinitions/{metricreportdefinition_id}` | `/redfish/v1/telemetryservice/metricreportdefinitions/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/telemetryservice/metricreports` | `/redfish/v1/telemetryservice/metricreports` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/telemetryservice/metricreports` | `/redfish/v1/telemetryservice/metricreports` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/telemetryservice/metricreports/{metricreport_id}` | `/redfish/v1/telemetryservice/metricreports/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/telemetryservice/metricreports/{metricreport_id}` | `/redfish/v1/telemetryservice/metricreports/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/telemetryservice/metricreports/{metricreport_id}` | `/redfish/v1/telemetryservice/metricreports/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/telemetryservice/triggers` | `/redfish/v1/telemetryservice/triggers` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/telemetryservice/triggers` | `/redfish/v1/telemetryservice/triggers` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/telemetryservice/triggers/{trigger_id}` | `/redfish/v1/telemetryservice/triggers/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/telemetryservice/triggers/{trigger_id}` | `/redfish/v1/telemetryservice/triggers/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/telemetryservice/triggers/{trigger_id}` | `/redfish/v1/telemetryservice/triggers/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/updateservice` | `/redfish/v1/updateservice` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/updateservice` | `/redfish/v1/updateservice` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/updateservice/componentrepository` | `/redfish/v1/updateservice/componentrepository` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/updateservice/componentrepository` | `/redfish/v1/updateservice/componentrepository` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/updateservice/componentrepository/{componentrepository_id}` | `/redfish/v1/updateservice/componentrepository/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/updateservice/componentrepository/{componentrepository_id}` | `/redfish/v1/updateservice/componentrepository/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/updateservice/componentrepository/{componentrepository_id}` | `/redfish/v1/updateservice/componentrepository/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/updateservice/firmwareinventory` | `/redfish/v1/updateservice/firmwareinventory` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/updateservice/firmwareinventory` | `/redfish/v1/updateservice/firmwareinventory` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/updateservice/firmwareinventory/{firmwareinventory_id}` | `/redfish/v1/updateservice/firmwareinventory/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/updateservice/firmwareinventory/{firmwareinventory_id}` | `/redfish/v1/updateservice/firmwareinventory/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/updateservice/firmwareinventory/{firmwareinventory_id}` | `/redfish/v1/updateservice/firmwareinventory/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/updateservice/installsets` | `/redfish/v1/updateservice/installsets` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/updateservice/installsets` | `/redfish/v1/updateservice/installsets` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/updateservice/installsets/{installset_id}` | `/redfish/v1/updateservice/installsets/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/updateservice/installsets/{installset_id}` | `/redfish/v1/updateservice/installsets/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/updateservice/installsets/{installset_id}` | `/redfish/v1/updateservice/installsets/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/updateservice/invalidimagerepository` | `/redfish/v1/updateservice/invalidimagerepository` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/updateservice/invalidimagerepository` | `/redfish/v1/updateservice/invalidimagerepository` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/updateservice/invalidimagerepository/{invalidimagerepository_id}` | `/redfish/v1/updateservice/invalidimagerepository/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/updateservice/invalidimagerepository/{invalidimagerepository_id}` | `/redfish/v1/updateservice/invalidimagerepository/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/updateservice/invalidimagerepository/{invalidimagerepository_id}` | `/redfish/v1/updateservice/invalidimagerepository/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/updateservice/maintenancewindows` | `/redfish/v1/updateservice/maintenancewindows` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/updateservice/maintenancewindows` | `/redfish/v1/updateservice/maintenancewindows` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/updateservice/maintenancewindows/{maintenancewindow_id}` | `/redfish/v1/updateservice/maintenancewindows/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/updateservice/maintenancewindows/{maintenancewindow_id}` | `/redfish/v1/updateservice/maintenancewindows/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/updateservice/maintenancewindows/{maintenancewindow_id}` | `/redfish/v1/updateservice/maintenancewindows/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/updateservice/runningsoftwareinventory` | `/redfish/v1/updateservice/runningsoftwareinventory` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/updateservice/runningsoftwareinventory` | `/redfish/v1/updateservice/runningsoftwareinventory` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/updateservice/runningsoftwareinventory/{runningsoftwareinventory_id}` | `/redfish/v1/updateservice/runningsoftwareinventory/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/updateservice/runningsoftwareinventory/{runningsoftwareinventory_id}` | `/redfish/v1/updateservice/runningsoftwareinventory/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/updateservice/runningsoftwareinventory/{runningsoftwareinventory_id}` | `/redfish/v1/updateservice/runningsoftwareinventory/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/updateservice/softwareinventory` | `/redfish/v1/updateservice/softwareinventory` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/updateservice/softwareinventory` | `/redfish/v1/updateservice/softwareinventory` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/updateservice/softwareinventory/{softwareinventory_id}` | `/redfish/v1/updateservice/softwareinventory/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/updateservice/softwareinventory/{softwareinventory_id}` | `/redfish/v1/updateservice/softwareinventory/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/updateservice/softwareinventory/{softwareinventory_id}` | `/redfish/v1/updateservice/softwareinventory/test_id_999` | 404 | NOT_FOUND_404 |
| GET | `/redfish/v1/updateservice/updatetaskqueue` | `/redfish/v1/updateservice/updatetaskqueue` | 200 | SUCCESS_2XX |
| POST | `/redfish/v1/updateservice/updatetaskqueue` | `/redfish/v1/updateservice/updatetaskqueue` | 200 | SUCCESS_2XX |
| GET | `/redfish/v1/updateservice/updatetaskqueue/{updatetaskqueue_id}` | `/redfish/v1/updateservice/updatetaskqueue/test_id_999` | 404 | NOT_FOUND_404 |
| PATCH | `/redfish/v1/updateservice/updatetaskqueue/{updatetaskqueue_id}` | `/redfish/v1/updateservice/updatetaskqueue/test_id_999` | CRASH | CRASH_EXCEPTION |
| DELETE | `/redfish/v1/updateservice/updatetaskqueue/{updatetaskqueue_id}` | `/redfish/v1/updateservice/updatetaskqueue/test_id_999` | 404 | NOT_FOUND_404 |

</details>

