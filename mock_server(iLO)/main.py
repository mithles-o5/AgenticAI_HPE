from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database import db

app = FastAPI(title='iLO 7 version 1.21 Mock Server', description='Generated automatically from Redfish resource map.')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint redirect to ServiceRoot
@app.get("/")
def get_root():
    return get_redfish_v1()

# --- AUTO-GENERATED ROUTES ---

@app.api_route("/redfish/v1/", methods=["GET"])
def get_redfish_v1():
    """
    iLO Redfish Endpoint: GET /redfish/v1/
    Type: ServiceRoot
    """
    collection_path = "/redfish/v1/"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1//{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/accountservice", methods=["GET"])
def get_redfish_v1_accountservice():
    """
    iLO Redfish Endpoint: GET /redfish/v1/accountservice
    Type: AccountService
    """
    collection_path = "/redfish/v1/accountservice"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_accountservice", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/accountservice/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/accountservice", methods=["POST"])
def post_redfish_v1_accountservice(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/accountservice
    Type: AccountService
    """
    collection_path = "/redfish/v1/accountservice"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/accountservice/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/accountservice/Oem/Hpe/appaccounts", methods=["GET"])
def get_redfish_v1_accountservice_oem_hpe_appaccounts():
    """
    iLO Redfish Endpoint: GET /redfish/v1/accountservice/Oem/Hpe/appaccounts
    Type: Collection ofHpeiLOAppAccount
    """
    collection_path = "/redfish/v1/accountservice/Oem/Hpe/appaccounts"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_accountservice_oem_hpe_appaccounts", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/accountservice/Oem/Hpe/appaccounts/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/accountservice/Oem/Hpe/appaccounts", methods=["POST"])
def post_redfish_v1_accountservice_oem_hpe_appaccounts(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/accountservice/Oem/Hpe/appaccounts
    Type: Collection ofHpeiLOAppAccount
    """
    collection_path = "/redfish/v1/accountservice/Oem/Hpe/appaccounts"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/accountservice/Oem/Hpe/appaccounts/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/accountservice/Oem/Hpe/appaccounts/{appaccount_id}", methods=["GET"])
def get_redfish_v1_accountservice_oem_hpe_appaccounts_appaccount_id(appaccount_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/accountservice/Oem/Hpe/appaccounts/{appaccount_id}
    Type: HpeiLOAppAccount
    """
    collection_path = f"/redfish/v1/accountservice/Oem/Hpe/appaccounts"
    item = db.get_item(collection_path, appaccount_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_accountservice_oem_hpe_appaccounts_appaccount_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/accountservice/Oem/Hpe/appaccounts/{appaccount_id}"
            static_val["Id"] = appaccount_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/accountservice/Oem/Hpe/appaccounts/{appaccount_id}", methods=["PATCH"])
def patch_redfish_v1_accountservice_oem_hpe_appaccounts_appaccount_id(appaccount_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/accountservice/Oem/Hpe/appaccounts/{appaccount_id}
    Type: HpeiLOAppAccount
    """
    collection_path = f"/redfish/v1/accountservice/Oem/Hpe/appaccounts"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, appaccount_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_accountservice_oem_hpe_appaccounts_appaccount_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = appaccount_id
            existing["@odata.id"] = f"/redfish/v1/accountservice/Oem/Hpe/appaccounts/{appaccount_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, appaccount_id, existing)
    return existing

@app.api_route("/redfish/v1/accountservice/Oem/Hpe/appaccounts/{appaccount_id}", methods=["DELETE"])
def delete_redfish_v1_accountservice_oem_hpe_appaccounts_appaccount_id(appaccount_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/accountservice/Oem/Hpe/appaccounts/{appaccount_id}
    Type: HpeiLOAppAccount
    """
    collection_path = f"/redfish/v1/accountservice/Oem/Hpe/appaccounts"
    deleted = db.delete_item(collection_path, appaccount_id)
    if deleted:
        return {"message": "Deleted successfully", "id": appaccount_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_accountservice_oem_hpe_appaccounts_appaccoget_redfish_v1_accountservice_oem_hpe_appaccounts_appaccount_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": appaccount_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/accountservice/Oem/Hpe/passwordrecovery", methods=["GET"])
def get_redfish_v1_accountservice_oem_hpe_passwordrecovery():
    """
    iLO Redfish Endpoint: GET /redfish/v1/accountservice/Oem/Hpe/passwordrecovery
    Type: HpeiLONonce
    """
    collection_path = "/redfish/v1/accountservice/Oem/Hpe/passwordrecovery"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_accountservice_oem_hpe_passwordrecovery", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/accountservice/Oem/Hpe/passwordrecovery/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/accountservice/Oem/Hpe/passwordrecovery", methods=["POST"])
def post_redfish_v1_accountservice_oem_hpe_passwordrecovery(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/accountservice/Oem/Hpe/passwordrecovery
    Type: HpeiLONonce
    """
    collection_path = "/redfish/v1/accountservice/Oem/Hpe/passwordrecovery"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/accountservice/Oem/Hpe/passwordrecovery/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/accountservice/accounts", methods=["GET"])
def get_redfish_v1_accountservice_accounts():
    """
    iLO Redfish Endpoint: GET /redfish/v1/accountservice/accounts
    Type: Collection ofManagerAccount
    """
    collection_path = "/redfish/v1/accountservice/accounts"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_accountservice_accounts", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/accountservice/accounts/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/accountservice/accounts", methods=["POST"])
def post_redfish_v1_accountservice_accounts(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/accountservice/accounts
    Type: Collection ofManagerAccount
    """
    collection_path = "/redfish/v1/accountservice/accounts"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/accountservice/accounts/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/accountservice/accounts/{account_id}", methods=["GET"])
def get_redfish_v1_accountservice_accounts_account_id(account_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/accountservice/accounts/{account_id}
    Type: ManagerAccount
    """
    collection_path = f"/redfish/v1/accountservice/accounts"
    item = db.get_item(collection_path, account_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_accountservice_accounts_account_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/accountservice/accounts/{account_id}"
            static_val["Id"] = account_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/accountservice/accounts/{account_id}", methods=["PATCH"])
def patch_redfish_v1_accountservice_accounts_account_id(account_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/accountservice/accounts/{account_id}
    Type: ManagerAccount
    """
    collection_path = f"/redfish/v1/accountservice/accounts"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, account_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_accountservice_accounts_account_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = account_id
            existing["@odata.id"] = f"/redfish/v1/accountservice/accounts/{account_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, account_id, existing)
    return existing

@app.api_route("/redfish/v1/accountservice/accounts/{account_id}", methods=["DELETE"])
def delete_redfish_v1_accountservice_accounts_account_id(account_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/accountservice/accounts/{account_id}
    Type: ManagerAccount
    """
    collection_path = f"/redfish/v1/accountservice/accounts"
    deleted = db.delete_item(collection_path, account_id)
    if deleted:
        return {"message": "Deleted successfully", "id": account_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_accountservice_accounts_accoget_redfish_v1_accountservice_accounts_account_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": account_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/accountservice/accounts/{account_id}/keys", methods=["GET"])
def get_redfish_v1_accountservice_accounts_account_id_keys(account_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/accountservice/accounts/{account_id}/keys
    Type: Collection ofKeySchema
    """
    collection_path = f"/redfish/v1/accountservice/accounts/{account_id}/keys"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_accountservice_accounts_account_id_keys", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/accountservice/accounts/{account_id}/keys/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/accountservice/accounts/{account_id}/keys", methods=["POST"])
def post_redfish_v1_accountservice_accounts_account_id_keys(account_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/accountservice/accounts/{account_id}/keys
    Type: Collection ofKeySchema
    """
    collection_path = f"/redfish/v1/accountservice/accounts/{account_id}/keys"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/accountservice/accounts/{account_id}/keys/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/accountservice/accounts/{account_id}/keys/{key_id}", methods=["GET"])
def get_redfish_v1_accountservice_accounts_account_id_keys_key_id(account_id: str, key_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/accountservice/accounts/{account_id}/keys/{key_id}
    Type: KeySchema
    """
    collection_path = f"/redfish/v1/accountservice/accounts/{account_id}/keys"
    item = db.get_item(collection_path, key_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_accountservice_accounts_account_id_keys_key_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/accountservice/accounts/{account_id}/keys/{key_id}"
            static_val["Id"] = key_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/accountservice/accounts/{account_id}/keys/{key_id}", methods=["PATCH"])
def patch_redfish_v1_accountservice_accounts_account_id_keys_key_id(account_id: str, key_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/accountservice/accounts/{account_id}/keys/{key_id}
    Type: KeySchema
    """
    collection_path = f"/redfish/v1/accountservice/accounts/{account_id}/keys"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, key_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_accountservice_accounts_account_id_keys_key_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = key_id
            existing["@odata.id"] = f"/redfish/v1/accountservice/accounts/{account_id}/keys/{key_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, key_id, existing)
    return existing

@app.api_route("/redfish/v1/accountservice/accounts/{account_id}/keys/{key_id}", methods=["DELETE"])
def delete_redfish_v1_accountservice_accounts_account_id_keys_key_id(account_id: str, key_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/accountservice/accounts/{account_id}/keys/{key_id}
    Type: KeySchema
    """
    collection_path = f"/redfish/v1/accountservice/accounts/{account_id}/keys"
    deleted = db.delete_item(collection_path, key_id)
    if deleted:
        return {"message": "Deleted successfully", "id": key_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_accountservice_accounts_account_id_keys_get_redfish_v1_accountservice_accounts_account_id_keys_key_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": key_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/accountservice/directorytest", methods=["GET"])
def get_redfish_v1_accountservice_directorytest():
    """
    iLO Redfish Endpoint: GET /redfish/v1/accountservice/directorytest
    Type: HpeDirectoryTest
    """
    collection_path = "/redfish/v1/accountservice/directorytest"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_accountservice_directorytest", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/accountservice/directorytest/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/accountservice/directorytest", methods=["POST"])
def post_redfish_v1_accountservice_directorytest(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/accountservice/directorytest
    Type: HpeDirectoryTest
    """
    collection_path = "/redfish/v1/accountservice/directorytest"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/accountservice/directorytest/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/accountservice/externalaccountproviders/ldap/certificates", methods=["GET"])
def get_redfish_v1_accountservice_externalaccountproviders_ldap_certificates():
    """
    iLO Redfish Endpoint: GET /redfish/v1/accountservice/externalaccountproviders/ldap/certificates
    Type: Collection ofCertificate
    """
    collection_path = "/redfish/v1/accountservice/externalaccountproviders/ldap/certificates"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_accountservice_externalaccountproviders_ldap_certificates", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/accountservice/externalaccountproviders/ldap/certificates/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/accountservice/externalaccountproviders/ldap/certificates", methods=["POST"])
def post_redfish_v1_accountservice_externalaccountproviders_ldap_certificates(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/accountservice/externalaccountproviders/ldap/certificates
    Type: Collection ofCertificate
    """
    collection_path = "/redfish/v1/accountservice/externalaccountproviders/ldap/certificates"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/accountservice/externalaccountproviders/ldap/certificates/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/accountservice/externalaccountproviders/ldap/certificates/{certificat_id}", methods=["GET"])
def get_redfish_v1_accountservice_externalaccountproviders_ldap_certificates_certificat_id(certificat_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/accountservice/externalaccountproviders/ldap/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/accountservice/externalaccountproviders/ldap/certificates"
    item = db.get_item(collection_path, certificat_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_accountservice_externalaccountproviders_ldap_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/accountservice/externalaccountproviders/ldap/certificates/{certificat_id}"
            static_val["Id"] = certificat_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/accountservice/externalaccountproviders/ldap/certificates/{certificat_id}", methods=["PATCH"])
def patch_redfish_v1_accountservice_externalaccountproviders_ldap_certificates_certificat_id(certificat_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/accountservice/externalaccountproviders/ldap/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/accountservice/externalaccountproviders/ldap/certificates"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, certificat_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_accountservice_externalaccountproviders_ldap_certificates_certificat_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = certificat_id
            existing["@odata.id"] = f"/redfish/v1/accountservice/externalaccountproviders/ldap/certificates/{certificat_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, certificat_id, existing)
    return existing

@app.api_route("/redfish/v1/accountservice/externalaccountproviders/ldap/certificates/{certificat_id}", methods=["DELETE"])
def delete_redfish_v1_accountservice_externalaccountproviders_ldap_certificates_certificat_id(certificat_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/accountservice/externalaccountproviders/ldap/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/accountservice/externalaccountproviders/ldap/certificates"
    deleted = db.delete_item(collection_path, certificat_id)
    if deleted:
        return {"message": "Deleted successfully", "id": certificat_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_accountservice_externalaccountproviders_ldap_certificates_certifiget_redfish_v1_accountservice_externalaccountproviders_ldap_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": certificat_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/accountservice/roles", methods=["GET"])
def get_redfish_v1_accountservice_roles():
    """
    iLO Redfish Endpoint: GET /redfish/v1/accountservice/roles
    Type: Collection ofRole
    """
    collection_path = "/redfish/v1/accountservice/roles"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_accountservice_roles", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/accountservice/roles/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/accountservice/roles", methods=["POST"])
def post_redfish_v1_accountservice_roles(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/accountservice/roles
    Type: Collection ofRole
    """
    collection_path = "/redfish/v1/accountservice/roles"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/accountservice/roles/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/accountservice/roles/{rol_id}", methods=["GET"])
def get_redfish_v1_accountservice_roles_rol_id(rol_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/accountservice/roles/{rol_id}
    Type: Role
    """
    collection_path = f"/redfish/v1/accountservice/roles"
    item = db.get_item(collection_path, rol_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_accountservice_roles_rol_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/accountservice/roles/{rol_id}"
            static_val["Id"] = rol_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/accountservice/roles/{rol_id}", methods=["PATCH"])
def patch_redfish_v1_accountservice_roles_rol_id(rol_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/accountservice/roles/{rol_id}
    Type: Role
    """
    collection_path = f"/redfish/v1/accountservice/roles"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, rol_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_accountservice_roles_rol_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = rol_id
            existing["@odata.id"] = f"/redfish/v1/accountservice/roles/{rol_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, rol_id, existing)
    return existing

@app.api_route("/redfish/v1/accountservice/roles/{rol_id}", methods=["DELETE"])
def delete_redfish_v1_accountservice_roles_rol_id(rol_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/accountservice/roles/{rol_id}
    Type: Role
    """
    collection_path = f"/redfish/v1/accountservice/roles"
    deleted = db.delete_item(collection_path, rol_id)
    if deleted:
        return {"message": "Deleted successfully", "id": rol_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_accountservice_roles_get_redfish_v1_accountservice_roles_rol_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": rol_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/accountservice/usercertificatemapping", methods=["GET"])
def get_redfish_v1_accountservice_usercertificatemapping():
    """
    iLO Redfish Endpoint: GET /redfish/v1/accountservice/usercertificatemapping
    Type: Collection ofHpeiLOAccountCertificateMap
    """
    collection_path = "/redfish/v1/accountservice/usercertificatemapping"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_accountservice_usercertificatemapping", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/accountservice/usercertificatemapping/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/accountservice/usercertificatemapping", methods=["POST"])
def post_redfish_v1_accountservice_usercertificatemapping(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/accountservice/usercertificatemapping
    Type: Collection ofHpeiLOAccountCertificateMap
    """
    collection_path = "/redfish/v1/accountservice/usercertificatemapping"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/accountservice/usercertificatemapping/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/accountservice/usercertificatemapping/{usercertificatemapping_id}", methods=["GET"])
def get_redfish_v1_accountservice_usercertificatemapping_usercertificatemapping_id(usercertificatemapping_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/accountservice/usercertificatemapping/{usercertificatemapping_id}
    Type: HpeiLOAccountCertificateMap
    """
    collection_path = f"/redfish/v1/accountservice/usercertificatemapping"
    item = db.get_item(collection_path, usercertificatemapping_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_accountservice_usercertificatemapping_usercertificatemapping_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/accountservice/usercertificatemapping/{usercertificatemapping_id}"
            static_val["Id"] = usercertificatemapping_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/accountservice/usercertificatemapping/{usercertificatemapping_id}", methods=["PATCH"])
def patch_redfish_v1_accountservice_usercertificatemapping_usercertificatemapping_id(usercertificatemapping_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/accountservice/usercertificatemapping/{usercertificatemapping_id}
    Type: HpeiLOAccountCertificateMap
    """
    collection_path = f"/redfish/v1/accountservice/usercertificatemapping"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, usercertificatemapping_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_accountservice_usercertificatemapping_usercertificatemapping_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = usercertificatemapping_id
            existing["@odata.id"] = f"/redfish/v1/accountservice/usercertificatemapping/{usercertificatemapping_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, usercertificatemapping_id, existing)
    return existing

@app.api_route("/redfish/v1/accountservice/usercertificatemapping/{usercertificatemapping_id}", methods=["DELETE"])
def delete_redfish_v1_accountservice_usercertificatemapping_usercertificatemapping_id(usercertificatemapping_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/accountservice/usercertificatemapping/{usercertificatemapping_id}
    Type: HpeiLOAccountCertificateMap
    """
    collection_path = f"/redfish/v1/accountservice/usercertificatemapping"
    deleted = db.delete_item(collection_path, usercertificatemapping_id)
    if deleted:
        return {"message": "Deleted successfully", "id": usercertificatemapping_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_accountservice_usercertificatemapping_usercertificatemappget_redfish_v1_accountservice_usercertificatemapping_usercertificatemapping_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": usercertificatemapping_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/certificateservice", methods=["GET"])
def get_redfish_v1_certificateservice():
    """
    iLO Redfish Endpoint: GET /redfish/v1/certificateservice
    Type: CertificateService
    """
    collection_path = "/redfish/v1/certificateservice"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_certificateservice", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/certificateservice/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/certificateservice", methods=["POST"])
def post_redfish_v1_certificateservice(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/certificateservice
    Type: CertificateService
    """
    collection_path = "/redfish/v1/certificateservice"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/certificateservice/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/certificateservice/certificateenrollments", methods=["GET"])
def get_redfish_v1_certificateservice_certificateenrollments():
    """
    iLO Redfish Endpoint: GET /redfish/v1/certificateservice/certificateenrollments
    Type: Collection ofCertificateEnrollment
    """
    collection_path = "/redfish/v1/certificateservice/certificateenrollments"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_certificateservice_certificateenrollments", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/certificateservice/certificateenrollments/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/certificateservice/certificateenrollments", methods=["POST"])
def post_redfish_v1_certificateservice_certificateenrollments(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/certificateservice/certificateenrollments
    Type: Collection ofCertificateEnrollment
    """
    collection_path = "/redfish/v1/certificateservice/certificateenrollments"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/certificateservice/certificateenrollments/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/certificateservice/certificateenrollments/{certificateenrollment_id}", methods=["GET"])
def get_redfish_v1_certificateservice_certificateenrollments_certificateenrollment_id(certificateenrollment_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/certificateservice/certificateenrollments/{certificateenrollment_id}
    Type: CertificateEnrollment
    """
    collection_path = f"/redfish/v1/certificateservice/certificateenrollments"
    item = db.get_item(collection_path, certificateenrollment_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_certificateservice_certificateenrollments_certificateenrollment_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/certificateservice/certificateenrollments/{certificateenrollment_id}"
            static_val["Id"] = certificateenrollment_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/certificateservice/certificateenrollments/{certificateenrollment_id}", methods=["PATCH"])
def patch_redfish_v1_certificateservice_certificateenrollments_certificateenrollment_id(certificateenrollment_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/certificateservice/certificateenrollments/{certificateenrollment_id}
    Type: CertificateEnrollment
    """
    collection_path = f"/redfish/v1/certificateservice/certificateenrollments"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, certificateenrollment_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_certificateservice_certificateenrollments_certificateenrollment_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = certificateenrollment_id
            existing["@odata.id"] = f"/redfish/v1/certificateservice/certificateenrollments/{certificateenrollment_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, certificateenrollment_id, existing)
    return existing

@app.api_route("/redfish/v1/certificateservice/certificateenrollments/{certificateenrollment_id}", methods=["DELETE"])
def delete_redfish_v1_certificateservice_certificateenrollments_certificateenrollment_id(certificateenrollment_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/certificateservice/certificateenrollments/{certificateenrollment_id}
    Type: CertificateEnrollment
    """
    collection_path = f"/redfish/v1/certificateservice/certificateenrollments"
    deleted = db.delete_item(collection_path, certificateenrollment_id)
    if deleted:
        return {"message": "Deleted successfully", "id": certificateenrollment_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_certificateservice_certificateenrollments_certificateenrollmget_redfish_v1_certificateservice_certificateenrollments_certificateenrollment_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": certificateenrollment_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/certificateservice/certificatelocations", methods=["GET"])
def get_redfish_v1_certificateservice_certificatelocations():
    """
    iLO Redfish Endpoint: GET /redfish/v1/certificateservice/certificatelocations
    Type: CertificateLocations
    """
    collection_path = "/redfish/v1/certificateservice/certificatelocations"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_certificateservice_certificatelocations", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/certificateservice/certificatelocations/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/certificateservice/certificatelocations", methods=["POST"])
def post_redfish_v1_certificateservice_certificatelocations(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/certificateservice/certificatelocations
    Type: CertificateLocations
    """
    collection_path = "/redfish/v1/certificateservice/certificatelocations"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/certificateservice/certificatelocations/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/certificateservice/enrollmentCAcertificates", methods=["GET"])
def get_redfish_v1_certificateservice_enrollmentcacertificates():
    """
    iLO Redfish Endpoint: GET /redfish/v1/certificateservice/enrollmentCAcertificates
    Type: CertificateCollection
    """
    collection_path = "/redfish/v1/certificateservice/enrollmentCAcertificates"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_certificateservice_enrollmentcacertificates", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/certificateservice/enrollmentCAcertificates/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/certificateservice/enrollmentCAcertificates", methods=["POST"])
def post_redfish_v1_certificateservice_enrollmentcacertificates(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/certificateservice/enrollmentCAcertificates
    Type: CertificateCollection
    """
    collection_path = "/redfish/v1/certificateservice/enrollmentCAcertificates"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/certificateservice/enrollmentCAcertificates/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/certificateservice/enrollmentCAcertificates/{enrollmentcacertificat_id}", methods=["GET"])
def get_redfish_v1_certificateservice_enrollmentcacertificates_enrollmentcacertificat_id(enrollmentcacertificat_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/certificateservice/enrollmentCAcertificates/{enrollmentcacertificat_id}
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/certificateservice/enrollmentCAcertificates"
    item = db.get_item(collection_path, enrollmentcacertificat_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_certificateservice_enrollmentcacertificates_enrollmentcacertificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/certificateservice/enrollmentCAcertificates/{enrollmentcacertificat_id}"
            static_val["Id"] = enrollmentcacertificat_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/certificateservice/enrollmentCAcertificates/{enrollmentcacertificat_id}", methods=["PATCH"])
def patch_redfish_v1_certificateservice_enrollmentcacertificates_enrollmentcacertificat_id(enrollmentcacertificat_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/certificateservice/enrollmentCAcertificates/{enrollmentcacertificat_id}
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/certificateservice/enrollmentCAcertificates"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, enrollmentcacertificat_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_certificateservice_enrollmentcacertificates_enrollmentcacertificat_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = enrollmentcacertificat_id
            existing["@odata.id"] = f"/redfish/v1/certificateservice/enrollmentCAcertificates/{enrollmentcacertificat_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, enrollmentcacertificat_id, existing)
    return existing

@app.api_route("/redfish/v1/certificateservice/enrollmentCAcertificates/{enrollmentcacertificat_id}", methods=["DELETE"])
def delete_redfish_v1_certificateservice_enrollmentcacertificates_enrollmentcacertificat_id(enrollmentcacertificat_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/certificateservice/enrollmentCAcertificates/{enrollmentcacertificat_id}
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/certificateservice/enrollmentCAcertificates"
    deleted = db.delete_item(collection_path, enrollmentcacertificat_id)
    if deleted:
        return {"message": "Deleted successfully", "id": enrollmentcacertificat_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_certificateservice_enrollmentcacertificates_enrollmentcacertifiget_redfish_v1_certificateservice_enrollmentcacertificates_enrollmentcacertificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": enrollmentcacertificat_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/chassis", methods=["GET"])
def get_redfish_v1_chassis():
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis
    Type: Collection ofChassis
    """
    collection_path = "/redfish/v1/chassis"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis", methods=["POST"])
def post_redfish_v1_chassis(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis
    Type: Collection ofChassis
    """
    collection_path = "/redfish/v1/chassis"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}", methods=["GET"])
def get_redfish_v1_chassis_chassi_id(chassi_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}
    Type: Chassis
    """
    collection_path = f"/redfish/v1/chassis"
    item = db.get_item(collection_path, chassi_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}"
            static_val["Id"] = chassi_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/chassis/{chassi_id}", methods=["PATCH"])
def patch_redfish_v1_chassis_chassi_id(chassi_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/chassis/{chassi_id}
    Type: Chassis
    """
    collection_path = f"/redfish/v1/chassis"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, chassi_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_chassis_chassi_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = chassi_id
            existing["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, chassi_id, existing)
    return existing

@app.api_route("/redfish/v1/chassis/{chassi_id}", methods=["DELETE"])
def delete_redfish_v1_chassis_chassi_id(chassi_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/chassis/{chassi_id}
    Type: Chassis
    """
    collection_path = f"/redfish/v1/chassis"
    deleted = db.delete_item(collection_path, chassi_id)
    if deleted:
        return {"message": "Deleted successfully", "id": chassi_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_chassis_chaget_redfish_v1_chassis_chassi_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": chassi_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/chassis/{chassi_id}/PCIeDevices/{pciedevic_id}/assembly", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_pciedevices_pciedevic_id_assembly(chassi_id: str, pciedevic_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/PCIeDevices/{pciedevic_id}/assembly
    Type: Assembly
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/PCIeDevices/{pciedevic_id}/assembly"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_pciedevices_pciedevic_id_assembly", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/PCIeDevices/{pciedevic_id}/assembly/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/PCIeDevices/{pciedevic_id}/assembly", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_pciedevices_pciedevic_id_assembly(chassi_id: str, pciedevic_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/PCIeDevices/{pciedevic_id}/assembly
    Type: Assembly
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/PCIeDevices/{pciedevic_id}/assembly"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/PCIeDevices/{pciedevic_id}/assembly/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/assembly", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_assembly(chassi_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/assembly
    Type: Assembly
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/assembly"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_assembly", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/assembly/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/assembly", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_assembly(chassi_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/assembly
    Type: Assembly
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/assembly"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/assembly/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/basefrus", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_basefrus(chassi_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/basefrus
    Type: Collection ofHpeiLOFrus
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/basefrus"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_basefrus", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/basefrus/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/basefrus", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_basefrus(chassi_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/basefrus
    Type: Collection ofHpeiLOFrus
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/basefrus"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/basefrus/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/basefrus/{basefru_id}", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_basefrus_basefru_id(chassi_id: str, basefru_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/basefrus/{basefru_id}
    Type: HpeiLOFrus
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/basefrus"
    item = db.get_item(collection_path, basefru_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_basefrus_basefru_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/basefrus/{basefru_id}"
            static_val["Id"] = basefru_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/chassis/{chassi_id}/basefrus/{basefru_id}", methods=["PATCH"])
def patch_redfish_v1_chassis_chassi_id_basefrus_basefru_id(chassi_id: str, basefru_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/chassis/{chassi_id}/basefrus/{basefru_id}
    Type: HpeiLOFrus
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/basefrus"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, basefru_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_chassis_chassi_id_basefrus_basefru_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = basefru_id
            existing["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/basefrus/{basefru_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, basefru_id, existing)
    return existing

@app.api_route("/redfish/v1/chassis/{chassi_id}/basefrus/{basefru_id}", methods=["DELETE"])
def delete_redfish_v1_chassis_chassi_id_basefrus_basefru_id(chassi_id: str, basefru_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/chassis/{chassi_id}/basefrus/{basefru_id}
    Type: HpeiLOFrus
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/basefrus"
    deleted = db.delete_item(collection_path, basefru_id)
    if deleted:
        return {"message": "Deleted successfully", "id": basefru_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_chassis_chassi_id_basefrus_baseget_redfish_v1_chassis_chassi_id_basefrus_basefru_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": basefru_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/chassis/{chassi_id}/basefrus/{basefru_id}/details", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_basefrus_basefru_id_details(chassi_id: str, basefru_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/basefrus/{basefru_id}/details
    Type: HpeiLOFrus
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/basefrus/{basefru_id}/details"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_basefrus_basefru_id_details", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/basefrus/{basefru_id}/details/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/basefrus/{basefru_id}/details", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_basefrus_basefru_id_details(chassi_id: str, basefru_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/basefrus/{basefru_id}/details
    Type: HpeiLOFrus
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/basefrus/{basefru_id}/details"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/basefrus/{basefru_id}/details/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/devices", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_devices(chassi_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/devices
    Type: Collection ofHpeServerDevice
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/devices"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_devices", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/devices/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/devices", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_devices(chassi_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/devices
    Type: Collection ofHpeServerDevice
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/devices"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/devices/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/devices/{devic_id}", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_devices_devic_id(chassi_id: str, devic_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/devices/{devic_id}
    Type: HpeServerDevice
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/devices"
    item = db.get_item(collection_path, devic_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_devices_devic_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/devices/{devic_id}"
            static_val["Id"] = devic_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/chassis/{chassi_id}/devices/{devic_id}", methods=["PATCH"])
def patch_redfish_v1_chassis_chassi_id_devices_devic_id(chassi_id: str, devic_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/chassis/{chassi_id}/devices/{devic_id}
    Type: HpeServerDevice
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/devices"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, devic_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_chassis_chassi_id_devices_devic_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = devic_id
            existing["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/devices/{devic_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, devic_id, existing)
    return existing

@app.api_route("/redfish/v1/chassis/{chassi_id}/devices/{devic_id}", methods=["DELETE"])
def delete_redfish_v1_chassis_chassi_id_devices_devic_id(chassi_id: str, devic_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/chassis/{chassi_id}/devices/{devic_id}
    Type: HpeServerDevice
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/devices"
    deleted = db.delete_item(collection_path, devic_id)
    if deleted:
        return {"message": "Deleted successfully", "id": devic_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_chassis_chassi_id_devices_deget_redfish_v1_chassis_chassi_id_devices_devic_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": devic_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/chassis/{chassi_id}/drives/{driv_id}/assembly", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_drives_driv_id_assembly(chassi_id: str, driv_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/drives/{driv_id}/assembly
    Type: Assembly
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/drives/{driv_id}/assembly"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_drives_driv_id_assembly", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/drives/{driv_id}/assembly/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/drives/{driv_id}/assembly", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_drives_driv_id_assembly(chassi_id: str, driv_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/drives/{driv_id}/assembly
    Type: Assembly
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/drives/{driv_id}/assembly"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/drives/{driv_id}/assembly/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/drives/{driv_id}/environmentmetrics", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_drives_driv_id_environmentmetrics(chassi_id: str, driv_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/drives/{driv_id}/environmentmetrics
    Type: EnvironmentMetrics
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/drives/{driv_id}/environmentmetrics"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_drives_driv_id_environmentmetrics", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/drives/{driv_id}/environmentmetrics/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/drives/{driv_id}/environmentmetrics", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_drives_driv_id_environmentmetrics(chassi_id: str, driv_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/drives/{driv_id}/environmentmetrics
    Type: EnvironmentMetrics
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/drives/{driv_id}/environmentmetrics"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/drives/{driv_id}/environmentmetrics/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/environmentmetrics", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_environmentmetrics(chassi_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/environmentmetrics
    Type: EnvironmentMetrics
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/environmentmetrics"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_environmentmetrics", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/environmentmetrics/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/environmentmetrics", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_environmentmetrics(chassi_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/environmentmetrics
    Type: EnvironmentMetrics
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/environmentmetrics"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/environmentmetrics/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/mezzfrus", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_mezzfrus(chassi_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/mezzfrus
    Type: Collection ofHpeiLOFrus
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/mezzfrus"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_mezzfrus", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/mezzfrus/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/mezzfrus", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_mezzfrus(chassi_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/mezzfrus
    Type: Collection ofHpeiLOFrus
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/mezzfrus"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/mezzfrus/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/mezzfrus/{mezzfru_id}", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_mezzfrus_mezzfru_id(chassi_id: str, mezzfru_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/mezzfrus/{mezzfru_id}
    Type: HpeiLOFrus
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/mezzfrus"
    item = db.get_item(collection_path, mezzfru_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_mezzfrus_mezzfru_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/mezzfrus/{mezzfru_id}"
            static_val["Id"] = mezzfru_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/chassis/{chassi_id}/mezzfrus/{mezzfru_id}", methods=["PATCH"])
def patch_redfish_v1_chassis_chassi_id_mezzfrus_mezzfru_id(chassi_id: str, mezzfru_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/chassis/{chassi_id}/mezzfrus/{mezzfru_id}
    Type: HpeiLOFrus
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/mezzfrus"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, mezzfru_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_chassis_chassi_id_mezzfrus_mezzfru_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = mezzfru_id
            existing["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/mezzfrus/{mezzfru_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, mezzfru_id, existing)
    return existing

@app.api_route("/redfish/v1/chassis/{chassi_id}/mezzfrus/{mezzfru_id}", methods=["DELETE"])
def delete_redfish_v1_chassis_chassi_id_mezzfrus_mezzfru_id(chassi_id: str, mezzfru_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/chassis/{chassi_id}/mezzfrus/{mezzfru_id}
    Type: HpeiLOFrus
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/mezzfrus"
    deleted = db.delete_item(collection_path, mezzfru_id)
    if deleted:
        return {"message": "Deleted successfully", "id": mezzfru_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_chassis_chassi_id_mezzfrus_mezzget_redfish_v1_chassis_chassi_id_mezzfrus_mezzfru_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": mezzfru_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/chassis/{chassi_id}/mezzfrus/{mezzfru_id}/details", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_mezzfrus_mezzfru_id_details(chassi_id: str, mezzfru_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/mezzfrus/{mezzfru_id}/details
    Type: HpeiLOFrus
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/mezzfrus/{mezzfru_id}/details"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_mezzfrus_mezzfru_id_details", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/mezzfrus/{mezzfru_id}/details/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/mezzfrus/{mezzfru_id}/details", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_mezzfrus_mezzfru_id_details(chassi_id: str, mezzfru_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/mezzfrus/{mezzfru_id}/details
    Type: HpeiLOFrus
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/mezzfrus/{mezzfru_id}/details"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/mezzfrus/{mezzfru_id}/details/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/networkadapters", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_networkadapters(chassi_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/networkadapters
    Type: Collection ofNetworkAdapter
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/networkadapters"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_networkadapters", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/networkadapters/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/networkadapters", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_networkadapters(chassi_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/networkadapters
    Type: Collection ofNetworkAdapter
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/networkadapters"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id(chassi_id: str, networkadapter_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}
    Type: NetworkAdapter
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/networkadapters"
    item = db.get_item(collection_path, networkadapter_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}"
            static_val["Id"] = networkadapter_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}", methods=["PATCH"])
def patch_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id(chassi_id: str, networkadapter_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}
    Type: NetworkAdapter
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/networkadapters"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, networkadapter_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = networkadapter_id
            existing["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, networkadapter_id, existing)
    return existing

@app.api_route("/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}", methods=["DELETE"])
def delete_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id(chassi_id: str, networkadapter_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}
    Type: NetworkAdapter
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/networkadapters"
    deleted = db.delete_item(collection_path, networkadapter_id)
    if deleted:
        return {"message": "Deleted successfully", "id": networkadapter_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_chassis_chassi_id_networkadapters_networkadapget_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": networkadapter_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/assembly", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_assembly(chassi_id: str, networkadapter_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/assembly
    Type: Assembly
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/assembly"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_assembly", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/assembly/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/assembly", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_assembly(chassi_id: str, networkadapter_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/assembly
    Type: Assembly
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/assembly"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/assembly/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_networkdevicefunctions(chassi_id: str, networkadapter_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions
    Type: Collection ofNetworkDeviceFunction
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_networkdevicefunctions", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_networkdevicefunctions(chassi_id: str, networkadapter_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions
    Type: Collection ofNetworkDeviceFunction
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions/{networkdevicefunction_id}", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_networkdevicefunctions_networkdevicefunction_id(chassi_id: str, networkadapter_id: str, networkdevicefunction_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions/{networkdevicefunction_id}
    Type: NetworkDeviceFunction
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions"
    item = db.get_item(collection_path, networkdevicefunction_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_networkdevicefunctions_networkdevicefunction_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions/{networkdevicefunction_id}"
            static_val["Id"] = networkdevicefunction_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions/{networkdevicefunction_id}", methods=["PATCH"])
def patch_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_networkdevicefunctions_networkdevicefunction_id(chassi_id: str, networkadapter_id: str, networkdevicefunction_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions/{networkdevicefunction_id}
    Type: NetworkDeviceFunction
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, networkdevicefunction_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_networkdevicefunctions_networkdevicefunction_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = networkdevicefunction_id
            existing["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions/{networkdevicefunction_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, networkdevicefunction_id, existing)
    return existing

@app.api_route("/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions/{networkdevicefunction_id}", methods=["DELETE"])
def delete_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_networkdevicefunctions_networkdevicefunction_id(chassi_id: str, networkadapter_id: str, networkdevicefunction_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions/{networkdevicefunction_id}
    Type: NetworkDeviceFunction
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions"
    deleted = db.delete_item(collection_path, networkdevicefunction_id)
    if deleted:
        return {"message": "Deleted successfully", "id": networkdevicefunction_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_networkdevicefunctions_networkdevicefunctget_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_networkdevicefunctions_networkdevicefunction_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": networkdevicefunction_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions/{networkdevicefunction_id}/settings", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_networkdevicefunctions_networkdevicefunction_id_settings(chassi_id: str, networkadapter_id: str, networkdevicefunction_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions/{networkdevicefunction_id}/settings
    Type: NetworkDeviceFunction
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions/{networkdevicefunction_id}/settings"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_networkdevicefunctions_networkdevicefunction_id_settings", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions/{networkdevicefunction_id}/settings/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions/{networkdevicefunction_id}/settings", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_networkdevicefunctions_networkdevicefunction_id_settings(chassi_id: str, networkadapter_id: str, networkdevicefunction_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions/{networkdevicefunction_id}/settings
    Type: NetworkDeviceFunction
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions/{networkdevicefunction_id}/settings"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/networkdevicefunctions/{networkdevicefunction_id}/settings/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_ports(chassi_id: str, networkadapter_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports
    Type: Collection ofPort
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_ports", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_ports(chassi_id: str, networkadapter_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports
    Type: Collection ofPort
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports/{port_id}", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_ports_port_id(chassi_id: str, networkadapter_id: str, port_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports/{port_id}
    Type: Port
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports"
    item = db.get_item(collection_path, port_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_ports_port_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports/{port_id}"
            static_val["Id"] = port_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports/{port_id}", methods=["PATCH"])
def patch_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_ports_port_id(chassi_id: str, networkadapter_id: str, port_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports/{port_id}
    Type: Port
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, port_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_ports_port_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = port_id
            existing["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports/{port_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, port_id, existing)
    return existing

@app.api_route("/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports/{port_id}", methods=["DELETE"])
def delete_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_ports_port_id(chassi_id: str, networkadapter_id: str, port_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports/{port_id}
    Type: Port
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports"
    deleted = db.delete_item(collection_path, port_id)
    if deleted:
        return {"message": "Deleted successfully", "id": port_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_ports_pget_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_ports_port_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": port_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports/{port_id}/settings", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_ports_port_id_settings(chassi_id: str, networkadapter_id: str, port_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports/{port_id}/settings
    Type: Port
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports/{port_id}/settings"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_ports_port_id_settings", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports/{port_id}/settings/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports/{port_id}/settings", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_ports_port_id_settings(chassi_id: str, networkadapter_id: str, port_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports/{port_id}/settings
    Type: Port
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports/{port_id}/settings"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/ports/{port_id}/settings/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/settings", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_settings(chassi_id: str, networkadapter_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/settings
    Type: NetworkAdapter
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/settings"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_settings", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/settings/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/settings", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_networkadapters_networkadapter_id_settings(chassi_id: str, networkadapter_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/settings
    Type: NetworkAdapter
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/settings"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/networkadapters/{networkadapter_id}/settings/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/pciedevices", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_pciedevices(chassi_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/pciedevices
    Type: Collection ofPCIeDevice
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/pciedevices"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_pciedevices", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/pciedevices/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/pciedevices", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_pciedevices(chassi_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/pciedevices
    Type: Collection ofPCIeDevice
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/pciedevices"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/pciedevices/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_pciedevices_pciedevic_id(chassi_id: str, pciedevic_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}
    Type: PCIeDevice
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/pciedevices"
    item = db.get_item(collection_path, pciedevic_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_pciedevices_pciedevic_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}"
            static_val["Id"] = pciedevic_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}", methods=["PATCH"])
def patch_redfish_v1_chassis_chassi_id_pciedevices_pciedevic_id(chassi_id: str, pciedevic_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}
    Type: PCIeDevice
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/pciedevices"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, pciedevic_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_chassis_chassi_id_pciedevices_pciedevic_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = pciedevic_id
            existing["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, pciedevic_id, existing)
    return existing

@app.api_route("/redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}", methods=["DELETE"])
def delete_redfish_v1_chassis_chassi_id_pciedevices_pciedevic_id(chassi_id: str, pciedevic_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}
    Type: PCIeDevice
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/pciedevices"
    deleted = db.delete_item(collection_path, pciedevic_id)
    if deleted:
        return {"message": "Deleted successfully", "id": pciedevic_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_chassis_chassi_id_pciedevices_pciedeget_redfish_v1_chassis_chassi_id_pciedevices_pciedevic_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": pciedevic_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}/pciefunctions", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_pciedevices_pciedevic_id_pciefunctions(chassi_id: str, pciedevic_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}/pciefunctions
    Type: Collection ofPCIeFunction
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}/pciefunctions"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_pciedevices_pciedevic_id_pciefunctions", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}/pciefunctions/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}/pciefunctions", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_pciedevices_pciedevic_id_pciefunctions(chassi_id: str, pciedevic_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}/pciefunctions
    Type: Collection ofPCIeFunction
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}/pciefunctions"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}/pciefunctions/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}/pciefunctions/{pciefunction_id}", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_pciedevices_pciedevic_id_pciefunctions_pciefunction_id(chassi_id: str, pciedevic_id: str, pciefunction_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}/pciefunctions/{pciefunction_id}
    Type: PCIeFunction
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}/pciefunctions"
    item = db.get_item(collection_path, pciefunction_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_pciedevices_pciedevic_id_pciefunctions_pciefunction_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}/pciefunctions/{pciefunction_id}"
            static_val["Id"] = pciefunction_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}/pciefunctions/{pciefunction_id}", methods=["PATCH"])
def patch_redfish_v1_chassis_chassi_id_pciedevices_pciedevic_id_pciefunctions_pciefunction_id(chassi_id: str, pciedevic_id: str, pciefunction_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}/pciefunctions/{pciefunction_id}
    Type: PCIeFunction
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}/pciefunctions"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, pciefunction_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_chassis_chassi_id_pciedevices_pciedevic_id_pciefunctions_pciefunction_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = pciefunction_id
            existing["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}/pciefunctions/{pciefunction_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, pciefunction_id, existing)
    return existing

@app.api_route("/redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}/pciefunctions/{pciefunction_id}", methods=["DELETE"])
def delete_redfish_v1_chassis_chassi_id_pciedevices_pciedevic_id_pciefunctions_pciefunction_id(chassi_id: str, pciedevic_id: str, pciefunction_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}/pciefunctions/{pciefunction_id}
    Type: PCIeFunction
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/pciedevices/{pciedevic_id}/pciefunctions"
    deleted = db.delete_item(collection_path, pciefunction_id)
    if deleted:
        return {"message": "Deleted successfully", "id": pciefunction_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_chassis_chassi_id_pciedevices_pciedevic_id_pciefunctions_pciefunctget_redfish_v1_chassis_chassi_id_pciedevices_pciedevic_id_pciefunctions_pciefunction_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": pciefunction_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/chassis/{chassi_id}/pcieslots", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_pcieslots(chassi_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/pcieslots
    Type: PCIeSlots
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/pcieslots"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_pcieslots", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/pcieslots/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/pcieslots", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_pcieslots(chassi_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/pcieslots
    Type: PCIeSlots
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/pcieslots"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/pcieslots/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/power", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_power(chassi_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/power
    Type: Power
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/power"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_power", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/power/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/power", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_power(chassi_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/power
    Type: Power
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/power"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/power/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/power/fastpowermeter", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_power_fastpowermeter(chassi_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/power/fastpowermeter
    Type: HpePowerMeter
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/power/fastpowermeter"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_power_fastpowermeter", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/power/fastpowermeter/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/power/fastpowermeter", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_power_fastpowermeter(chassi_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/power/fastpowermeter
    Type: HpePowerMeter
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/power/fastpowermeter"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/power/fastpowermeter/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/power/powermeter", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_power_powermeter(chassi_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/power/powermeter
    Type: HpePowerMeter
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/power/powermeter"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_power_powermeter", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/power/powermeter/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/power/powermeter", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_power_powermeter(chassi_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/power/powermeter
    Type: HpePowerMeter
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/power/powermeter"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/power/powermeter/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/powersubsystem", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_powersubsystem(chassi_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/powersubsystem
    Type: PowerSubsystem
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/powersubsystem"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_powersubsystem", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/powersubsystem/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/powersubsystem", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_powersubsystem(chassi_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/powersubsystem
    Type: PowerSubsystem
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/powersubsystem"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/powersubsystem/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/powersubsystem/batteries", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_powersubsystem_batteries(chassi_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/powersubsystem/batteries
    Type: Collection ofBattery
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/powersubsystem/batteries"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_powersubsystem_batteries", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/powersubsystem/batteries/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/powersubsystem/batteries", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_powersubsystem_batteries(chassi_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/powersubsystem/batteries
    Type: Collection ofBattery
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/powersubsystem/batteries"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/powersubsystem/batteries/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/powersubsystem/batteries/{battery_id}", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_powersubsystem_batteries_battery_id(chassi_id: str, battery_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/powersubsystem/batteries/{battery_id}
    Type: Battery
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/powersubsystem/batteries"
    item = db.get_item(collection_path, battery_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_powersubsystem_batteries_battery_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/powersubsystem/batteries/{battery_id}"
            static_val["Id"] = battery_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/chassis/{chassi_id}/powersubsystem/batteries/{battery_id}", methods=["PATCH"])
def patch_redfish_v1_chassis_chassi_id_powersubsystem_batteries_battery_id(chassi_id: str, battery_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/chassis/{chassi_id}/powersubsystem/batteries/{battery_id}
    Type: Battery
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/powersubsystem/batteries"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, battery_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_chassis_chassi_id_powersubsystem_batteries_battery_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = battery_id
            existing["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/powersubsystem/batteries/{battery_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, battery_id, existing)
    return existing

@app.api_route("/redfish/v1/chassis/{chassi_id}/powersubsystem/batteries/{battery_id}", methods=["DELETE"])
def delete_redfish_v1_chassis_chassi_id_powersubsystem_batteries_battery_id(chassi_id: str, battery_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/chassis/{chassi_id}/powersubsystem/batteries/{battery_id}
    Type: Battery
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/powersubsystem/batteries"
    deleted = db.delete_item(collection_path, battery_id)
    if deleted:
        return {"message": "Deleted successfully", "id": battery_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_chassis_chassi_id_powersubsystem_batteries_battget_redfish_v1_chassis_chassi_id_powersubsystem_batteries_battery_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": battery_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_powersubsystem_powersupplies(chassi_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies
    Type: Collection ofPowerSupply
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_powersubsystem_powersupplies", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_powersubsystem_powersupplies(chassi_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies
    Type: Collection ofPowerSupply
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_powersubsystem_powersupplies_powersupply_id(chassi_id: str, powersupply_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}
    Type: PowerSupply
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies"
    item = db.get_item(collection_path, powersupply_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_powersubsystem_powersupplies_powersupply_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}"
            static_val["Id"] = powersupply_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}", methods=["PATCH"])
def patch_redfish_v1_chassis_chassi_id_powersubsystem_powersupplies_powersupply_id(chassi_id: str, powersupply_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}
    Type: PowerSupply
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, powersupply_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_chassis_chassi_id_powersubsystem_powersupplies_powersupply_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = powersupply_id
            existing["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, powersupply_id, existing)
    return existing

@app.api_route("/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}", methods=["DELETE"])
def delete_redfish_v1_chassis_chassi_id_powersubsystem_powersupplies_powersupply_id(chassi_id: str, powersupply_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}
    Type: PowerSupply
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies"
    deleted = db.delete_item(collection_path, powersupply_id)
    if deleted:
        return {"message": "Deleted successfully", "id": powersupply_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_chassis_chassi_id_powersubsystem_powersupplies_powersupget_redfish_v1_chassis_chassi_id_powersubsystem_powersupplies_powersupply_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": powersupply_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}/assembly", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_powersubsystem_powersupplies_powersupply_id_assembly(chassi_id: str, powersupply_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}/assembly
    Type: Assembly
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}/assembly"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_powersubsystem_powersupplies_powersupply_id_assembly", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}/assembly/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}/assembly", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_powersubsystem_powersupplies_powersupply_id_assembly(chassi_id: str, powersupply_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}/assembly
    Type: Assembly
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}/assembly"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}/assembly/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}/metrics", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_powersubsystem_powersupplies_powersupply_id_metrics(chassi_id: str, powersupply_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}/metrics
    Type: PowerSupplyMetrics
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}/metrics"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_powersubsystem_powersupplies_powersupply_id_metrics", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}/metrics/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}/metrics", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_powersubsystem_powersupplies_powersupply_id_metrics(chassi_id: str, powersupply_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}/metrics
    Type: PowerSupplyMetrics
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}/metrics"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/powersubsystem/powersupplies/{powersupply_id}/metrics/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/sensors/{sensor_id}", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_sensors_sensor_id(chassi_id: str, sensor_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/sensors/{sensor_id}
    Type: Sensor
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/sensors"
    item = db.get_item(collection_path, sensor_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_sensors_sensor_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/sensors/{sensor_id}"
            static_val["Id"] = sensor_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/chassis/{chassi_id}/sensors/{sensor_id}", methods=["PATCH"])
def patch_redfish_v1_chassis_chassi_id_sensors_sensor_id(chassi_id: str, sensor_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/chassis/{chassi_id}/sensors/{sensor_id}
    Type: Sensor
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/sensors"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, sensor_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_chassis_chassi_id_sensors_sensor_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = sensor_id
            existing["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/sensors/{sensor_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, sensor_id, existing)
    return existing

@app.api_route("/redfish/v1/chassis/{chassi_id}/sensors/{sensor_id}", methods=["DELETE"])
def delete_redfish_v1_chassis_chassi_id_sensors_sensor_id(chassi_id: str, sensor_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/chassis/{chassi_id}/sensors/{sensor_id}
    Type: Sensor
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/sensors"
    deleted = db.delete_item(collection_path, sensor_id)
    if deleted:
        return {"message": "Deleted successfully", "id": sensor_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_chassis_chassi_id_sensors_senget_redfish_v1_chassis_chassi_id_sensors_sensor_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": sensor_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/chassis/{chassi_id}/thermal", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_thermal(chassi_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/thermal
    Type: Thermal
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/thermal"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_thermal", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/thermal/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/thermal", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_thermal(chassi_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/thermal
    Type: Thermal
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/thermal"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/thermal/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/thermalsubsystem", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_thermalsubsystem(chassi_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/thermalsubsystem
    Type: ThermalSubsystem
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_thermalsubsystem", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/thermalsubsystem", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_thermalsubsystem(chassi_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/thermalsubsystem
    Type: ThermalSubsystem
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_thermalsubsystem_fans(chassi_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans
    Type: Collection ofFan
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_thermalsubsystem_fans", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_thermalsubsystem_fans(chassi_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans
    Type: Collection ofFan
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans/{fan_id}", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_thermalsubsystem_fans_fan_id(chassi_id: str, fan_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans/{fan_id}
    Type: Fan
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans"
    item = db.get_item(collection_path, fan_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_thermalsubsystem_fans_fan_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans/{fan_id}"
            static_val["Id"] = fan_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans/{fan_id}", methods=["PATCH"])
def patch_redfish_v1_chassis_chassi_id_thermalsubsystem_fans_fan_id(chassi_id: str, fan_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans/{fan_id}
    Type: Fan
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, fan_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_chassis_chassi_id_thermalsubsystem_fans_fan_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = fan_id
            existing["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans/{fan_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, fan_id, existing)
    return existing

@app.api_route("/redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans/{fan_id}", methods=["DELETE"])
def delete_redfish_v1_chassis_chassi_id_thermalsubsystem_fans_fan_id(chassi_id: str, fan_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans/{fan_id}
    Type: Fan
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans"
    deleted = db.delete_item(collection_path, fan_id)
    if deleted:
        return {"message": "Deleted successfully", "id": fan_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_chassis_chassi_id_thermalsubsystem_fans_get_redfish_v1_chassis_chassi_id_thermalsubsystem_fans_fan_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": fan_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans/{fan_id}/assembly", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_thermalsubsystem_fans_fan_id_assembly(chassi_id: str, fan_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans/{fan_id}/assembly
    Type: Assembly
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans/{fan_id}/assembly"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_thermalsubsystem_fans_fan_id_assembly", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans/{fan_id}/assembly/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans/{fan_id}/assembly", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_thermalsubsystem_fans_fan_id_assembly(chassi_id: str, fan_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans/{fan_id}/assembly
    Type: Assembly
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans/{fan_id}/assembly"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem/fans/{fan_id}/assembly/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/thermalsubsystem/pumps", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_thermalsubsystem_pumps(chassi_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/thermalsubsystem/pumps
    Type: Collection ofPump
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem/pumps"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_thermalsubsystem_pumps", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem/pumps/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/thermalsubsystem/pumps", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_thermalsubsystem_pumps(chassi_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/thermalsubsystem/pumps
    Type: Collection ofPump
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem/pumps"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem/pumps/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/thermalsubsystem/pumps/{pump_id}/assembly", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_thermalsubsystem_pumps_pump_id_assembly(chassi_id: str, pump_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/thermalsubsystem/pumps/{pump_id}/assembly
    Type: Pump
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem/pumps/{pump_id}/assembly"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_thermalsubsystem_pumps_pump_id_assembly", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem/pumps/{pump_id}/assembly/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/thermalsubsystem/pumps/{pump_id}/assembly", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_thermalsubsystem_pumps_pump_id_assembly(chassi_id: str, pump_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/thermalsubsystem/pumps/{pump_id}/assembly
    Type: Pump
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem/pumps/{pump_id}/assembly"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem/pumps/{pump_id}/assembly/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/chassis/{chassi_id}/thermalsubsystem/thermalmetrics", methods=["GET"])
def get_redfish_v1_chassis_chassi_id_thermalsubsystem_thermalmetrics(chassi_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassi_id}/thermalsubsystem/thermalmetrics
    Type: ThermalMetrics
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem/thermalmetrics"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_chassis_chassi_id_thermalsubsystem_thermalmetrics", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem/thermalmetrics/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/chassis/{chassi_id}/thermalsubsystem/thermalmetrics", methods=["POST"])
def post_redfish_v1_chassis_chassi_id_thermalsubsystem_thermalmetrics(chassi_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/chassis/{chassi_id}/thermalsubsystem/thermalmetrics
    Type: ThermalMetrics
    """
    collection_path = f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem/thermalmetrics"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/chassis/{chassi_id}/thermalsubsystem/thermalmetrics/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/componentintegrity", methods=["GET"])
def get_redfish_v1_componentintegrity():
    """
    iLO Redfish Endpoint: GET /redfish/v1/componentintegrity
    Type: Collection ofComponentIntegrity
    """
    collection_path = "/redfish/v1/componentintegrity"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_componentintegrity", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/componentintegrity/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/componentintegrity", methods=["POST"])
def post_redfish_v1_componentintegrity(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/componentintegrity
    Type: Collection ofComponentIntegrity
    """
    collection_path = "/redfish/v1/componentintegrity"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/componentintegrity/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/componentintegrity/{componentintegrity_id}", methods=["GET"])
def get_redfish_v1_componentintegrity_componentintegrity_id(componentintegrity_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/componentintegrity/{componentintegrity_id}
    Type: ComponentIntegrity
    """
    collection_path = f"/redfish/v1/componentintegrity"
    item = db.get_item(collection_path, componentintegrity_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_componentintegrity_componentintegrity_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/componentintegrity/{componentintegrity_id}"
            static_val["Id"] = componentintegrity_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/componentintegrity/{componentintegrity_id}", methods=["PATCH"])
def patch_redfish_v1_componentintegrity_componentintegrity_id(componentintegrity_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/componentintegrity/{componentintegrity_id}
    Type: ComponentIntegrity
    """
    collection_path = f"/redfish/v1/componentintegrity"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, componentintegrity_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_componentintegrity_componentintegrity_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = componentintegrity_id
            existing["@odata.id"] = f"/redfish/v1/componentintegrity/{componentintegrity_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, componentintegrity_id, existing)
    return existing

@app.api_route("/redfish/v1/componentintegrity/{componentintegrity_id}", methods=["DELETE"])
def delete_redfish_v1_componentintegrity_componentintegrity_id(componentintegrity_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/componentintegrity/{componentintegrity_id}
    Type: ComponentIntegrity
    """
    collection_path = f"/redfish/v1/componentintegrity"
    deleted = db.delete_item(collection_path, componentintegrity_id)
    if deleted:
        return {"message": "Deleted successfully", "id": componentintegrity_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_componentintegrity_componentintegrget_redfish_v1_componentintegrity_componentintegrity_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": componentintegrity_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/eventservice", methods=["GET"])
def get_redfish_v1_eventservice():
    """
    iLO Redfish Endpoint: GET /redfish/v1/eventservice
    Type: EventService
    """
    collection_path = "/redfish/v1/eventservice"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_eventservice", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/eventservice/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/eventservice", methods=["POST"])
def post_redfish_v1_eventservice(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/eventservice
    Type: EventService
    """
    collection_path = "/redfish/v1/eventservice"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/eventservice/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/eventservice/cacertificates", methods=["GET"])
def get_redfish_v1_eventservice_cacertificates():
    """
    iLO Redfish Endpoint: GET /redfish/v1/eventservice/cacertificates
    Type: Collection ofHpeCertificate
    """
    collection_path = "/redfish/v1/eventservice/cacertificates"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_eventservice_cacertificates", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/eventservice/cacertificates/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/eventservice/cacertificates", methods=["POST"])
def post_redfish_v1_eventservice_cacertificates(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/eventservice/cacertificates
    Type: Collection ofHpeCertificate
    """
    collection_path = "/redfish/v1/eventservice/cacertificates"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/eventservice/cacertificates/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/eventservice/cacertificates/{cacertificat_id}", methods=["GET"])
def get_redfish_v1_eventservice_cacertificates_cacertificat_id(cacertificat_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/eventservice/cacertificates/{cacertificat_id}
    Type: HpeCertificate
    """
    collection_path = f"/redfish/v1/eventservice/cacertificates"
    item = db.get_item(collection_path, cacertificat_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_eventservice_cacertificates_cacertificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/eventservice/cacertificates/{cacertificat_id}"
            static_val["Id"] = cacertificat_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/eventservice/cacertificates/{cacertificat_id}", methods=["PATCH"])
def patch_redfish_v1_eventservice_cacertificates_cacertificat_id(cacertificat_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/eventservice/cacertificates/{cacertificat_id}
    Type: HpeCertificate
    """
    collection_path = f"/redfish/v1/eventservice/cacertificates"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, cacertificat_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_eventservice_cacertificates_cacertificat_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = cacertificat_id
            existing["@odata.id"] = f"/redfish/v1/eventservice/cacertificates/{cacertificat_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, cacertificat_id, existing)
    return existing

@app.api_route("/redfish/v1/eventservice/cacertificates/{cacertificat_id}", methods=["DELETE"])
def delete_redfish_v1_eventservice_cacertificates_cacertificat_id(cacertificat_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/eventservice/cacertificates/{cacertificat_id}
    Type: HpeCertificate
    """
    collection_path = f"/redfish/v1/eventservice/cacertificates"
    deleted = db.delete_item(collection_path, cacertificat_id)
    if deleted:
        return {"message": "Deleted successfully", "id": cacertificat_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_eventservice_cacertificates_cacertifiget_redfish_v1_eventservice_cacertificates_cacertificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": cacertificat_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/eventservice/subscriptions", methods=["GET"])
def get_redfish_v1_eventservice_subscriptions():
    """
    iLO Redfish Endpoint: GET /redfish/v1/eventservice/subscriptions
    Type: Collection ofEventDestination
    """
    collection_path = "/redfish/v1/eventservice/subscriptions"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_eventservice_subscriptions", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/eventservice/subscriptions/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/eventservice/subscriptions", methods=["POST"])
def post_redfish_v1_eventservice_subscriptions(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/eventservice/subscriptions
    Type: Collection ofEventDestination
    """
    collection_path = "/redfish/v1/eventservice/subscriptions"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/eventservice/subscriptions/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/eventservice/subscriptions/{subscription_id}", methods=["GET"])
def get_redfish_v1_eventservice_subscriptions_subscription_id(subscription_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/eventservice/subscriptions/{subscription_id}
    Type: EventDestination
    """
    collection_path = f"/redfish/v1/eventservice/subscriptions"
    item = db.get_item(collection_path, subscription_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_eventservice_subscriptions_subscription_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/eventservice/subscriptions/{subscription_id}"
            static_val["Id"] = subscription_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/eventservice/subscriptions/{subscription_id}", methods=["PATCH"])
def patch_redfish_v1_eventservice_subscriptions_subscription_id(subscription_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/eventservice/subscriptions/{subscription_id}
    Type: EventDestination
    """
    collection_path = f"/redfish/v1/eventservice/subscriptions"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, subscription_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_eventservice_subscriptions_subscription_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = subscription_id
            existing["@odata.id"] = f"/redfish/v1/eventservice/subscriptions/{subscription_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, subscription_id, existing)
    return existing

@app.api_route("/redfish/v1/eventservice/subscriptions/{subscription_id}", methods=["DELETE"])
def delete_redfish_v1_eventservice_subscriptions_subscription_id(subscription_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/eventservice/subscriptions/{subscription_id}
    Type: EventDestination
    """
    collection_path = f"/redfish/v1/eventservice/subscriptions"
    deleted = db.delete_item(collection_path, subscription_id)
    if deleted:
        return {"message": "Deleted successfully", "id": subscription_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_eventservice_subscriptions_subscriptget_redfish_v1_eventservice_subscriptions_subscription_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": subscription_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/fabrics", methods=["GET"])
def get_redfish_v1_fabrics():
    """
    iLO Redfish Endpoint: GET /redfish/v1/fabrics
    Type: Collection ofFabric
    """
    collection_path = "/redfish/v1/fabrics"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_fabrics", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/fabrics/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/fabrics", methods=["POST"])
def post_redfish_v1_fabrics(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/fabrics
    Type: Collection ofFabric
    """
    collection_path = "/redfish/v1/fabrics"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/fabrics/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/fabrics/{fabric_id}", methods=["GET"])
def get_redfish_v1_fabrics_fabric_id(fabric_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/fabrics/{fabric_id}
    Type: Fabric
    """
    collection_path = f"/redfish/v1/fabrics"
    item = db.get_item(collection_path, fabric_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_fabrics_fabric_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/fabrics/{fabric_id}"
            static_val["Id"] = fabric_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/fabrics/{fabric_id}", methods=["PATCH"])
def patch_redfish_v1_fabrics_fabric_id(fabric_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/fabrics/{fabric_id}
    Type: Fabric
    """
    collection_path = f"/redfish/v1/fabrics"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, fabric_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_fabrics_fabric_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = fabric_id
            existing["@odata.id"] = f"/redfish/v1/fabrics/{fabric_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, fabric_id, existing)
    return existing

@app.api_route("/redfish/v1/fabrics/{fabric_id}", methods=["DELETE"])
def delete_redfish_v1_fabrics_fabric_id(fabric_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/fabrics/{fabric_id}
    Type: Fabric
    """
    collection_path = f"/redfish/v1/fabrics"
    deleted = db.delete_item(collection_path, fabric_id)
    if deleted:
        return {"message": "Deleted successfully", "id": fabric_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_fabrics_fabget_redfish_v1_fabrics_fabric_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": fabric_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/fabrics/{fabric_id}/switches", methods=["GET"])
def get_redfish_v1_fabrics_fabric_id_switches(fabric_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/fabrics/{fabric_id}/switches
    Type: Collection ofSwitch
    """
    collection_path = f"/redfish/v1/fabrics/{fabric_id}/switches"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_fabrics_fabric_id_switches", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/fabrics/{fabric_id}/switches/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/fabrics/{fabric_id}/switches", methods=["POST"])
def post_redfish_v1_fabrics_fabric_id_switches(fabric_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/fabrics/{fabric_id}/switches
    Type: Collection ofSwitch
    """
    collection_path = f"/redfish/v1/fabrics/{fabric_id}/switches"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/fabrics/{fabric_id}/switches/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/fabrics/{fabric_id}/switches/{switch_id}", methods=["GET"])
def get_redfish_v1_fabrics_fabric_id_switches_switch_id(fabric_id: str, switch_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/fabrics/{fabric_id}/switches/{switch_id}
    Type: Switch
    """
    collection_path = f"/redfish/v1/fabrics/{fabric_id}/switches"
    item = db.get_item(collection_path, switch_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_fabrics_fabric_id_switches_switch_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/fabrics/{fabric_id}/switches/{switch_id}"
            static_val["Id"] = switch_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/fabrics/{fabric_id}/switches/{switch_id}", methods=["PATCH"])
def patch_redfish_v1_fabrics_fabric_id_switches_switch_id(fabric_id: str, switch_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/fabrics/{fabric_id}/switches/{switch_id}
    Type: Switch
    """
    collection_path = f"/redfish/v1/fabrics/{fabric_id}/switches"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, switch_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_fabrics_fabric_id_switches_switch_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = switch_id
            existing["@odata.id"] = f"/redfish/v1/fabrics/{fabric_id}/switches/{switch_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, switch_id, existing)
    return existing

@app.api_route("/redfish/v1/fabrics/{fabric_id}/switches/{switch_id}", methods=["DELETE"])
def delete_redfish_v1_fabrics_fabric_id_switches_switch_id(fabric_id: str, switch_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/fabrics/{fabric_id}/switches/{switch_id}
    Type: Switch
    """
    collection_path = f"/redfish/v1/fabrics/{fabric_id}/switches"
    deleted = db.delete_item(collection_path, switch_id)
    if deleted:
        return {"message": "Deleted successfully", "id": switch_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_fabrics_fabric_id_switches_swiget_redfish_v1_fabrics_fabric_id_switches_switch_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": switch_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/fabrics/{fabric_id}/switches/{switch_id}/ports", methods=["GET"])
def get_redfish_v1_fabrics_fabric_id_switches_switch_id_ports(fabric_id: str, switch_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/fabrics/{fabric_id}/switches/{switch_id}/ports
    Type: Collection ofPort
    """
    collection_path = f"/redfish/v1/fabrics/{fabric_id}/switches/{switch_id}/ports"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_fabrics_fabric_id_switches_switch_id_ports", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/fabrics/{fabric_id}/switches/{switch_id}/ports/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/fabrics/{fabric_id}/switches/{switch_id}/ports", methods=["POST"])
def post_redfish_v1_fabrics_fabric_id_switches_switch_id_ports(fabric_id: str, switch_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/fabrics/{fabric_id}/switches/{switch_id}/ports
    Type: Collection ofPort
    """
    collection_path = f"/redfish/v1/fabrics/{fabric_id}/switches/{switch_id}/ports"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/fabrics/{fabric_id}/switches/{switch_id}/ports/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/fabrics/{fabric_id}/switches/{switch_id}/ports/{port_id}", methods=["GET"])
def get_redfish_v1_fabrics_fabric_id_switches_switch_id_ports_port_id(fabric_id: str, switch_id: str, port_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/fabrics/{fabric_id}/switches/{switch_id}/ports/{port_id}
    Type: Port
    """
    collection_path = f"/redfish/v1/fabrics/{fabric_id}/switches/{switch_id}/ports"
    item = db.get_item(collection_path, port_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_fabrics_fabric_id_switches_switch_id_ports_port_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/fabrics/{fabric_id}/switches/{switch_id}/ports/{port_id}"
            static_val["Id"] = port_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/fabrics/{fabric_id}/switches/{switch_id}/ports/{port_id}", methods=["PATCH"])
def patch_redfish_v1_fabrics_fabric_id_switches_switch_id_ports_port_id(fabric_id: str, switch_id: str, port_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/fabrics/{fabric_id}/switches/{switch_id}/ports/{port_id}
    Type: Port
    """
    collection_path = f"/redfish/v1/fabrics/{fabric_id}/switches/{switch_id}/ports"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, port_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_fabrics_fabric_id_switches_switch_id_ports_port_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = port_id
            existing["@odata.id"] = f"/redfish/v1/fabrics/{fabric_id}/switches/{switch_id}/ports/{port_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, port_id, existing)
    return existing

@app.api_route("/redfish/v1/fabrics/{fabric_id}/switches/{switch_id}/ports/{port_id}", methods=["DELETE"])
def delete_redfish_v1_fabrics_fabric_id_switches_switch_id_ports_port_id(fabric_id: str, switch_id: str, port_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/fabrics/{fabric_id}/switches/{switch_id}/ports/{port_id}
    Type: Port
    """
    collection_path = f"/redfish/v1/fabrics/{fabric_id}/switches/{switch_id}/ports"
    deleted = db.delete_item(collection_path, port_id)
    if deleted:
        return {"message": "Deleted successfully", "id": port_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_fabrics_fabric_id_switches_switch_id_ports_pget_redfish_v1_fabrics_fabric_id_switches_switch_id_ports_port_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": port_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/jsonschemas", methods=["GET"])
def get_redfish_v1_jsonschemas():
    """
    iLO Redfish Endpoint: GET /redfish/v1/jsonschemas
    Type: Collection ofJsonSchemaFile
    """
    collection_path = "/redfish/v1/jsonschemas"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_jsonschemas", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/jsonschemas/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/jsonschemas", methods=["POST"])
def post_redfish_v1_jsonschemas(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/jsonschemas
    Type: Collection ofJsonSchemaFile
    """
    collection_path = "/redfish/v1/jsonschemas"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/jsonschemas/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/jsonschemas/{jsonschema_id}", methods=["GET"])
def get_redfish_v1_jsonschemas_jsonschema_id(jsonschema_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/jsonschemas/{jsonschema_id}
    Type: JsonSchemaFile
    """
    collection_path = f"/redfish/v1/jsonschemas"
    item = db.get_item(collection_path, jsonschema_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_jsonschemas_jsonschema_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/jsonschemas/{jsonschema_id}"
            static_val["Id"] = jsonschema_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/jsonschemas/{jsonschema_id}", methods=["PATCH"])
def patch_redfish_v1_jsonschemas_jsonschema_id(jsonschema_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/jsonschemas/{jsonschema_id}
    Type: JsonSchemaFile
    """
    collection_path = f"/redfish/v1/jsonschemas"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, jsonschema_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_jsonschemas_jsonschema_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = jsonschema_id
            existing["@odata.id"] = f"/redfish/v1/jsonschemas/{jsonschema_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, jsonschema_id, existing)
    return existing

@app.api_route("/redfish/v1/jsonschemas/{jsonschema_id}", methods=["DELETE"])
def delete_redfish_v1_jsonschemas_jsonschema_id(jsonschema_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/jsonschemas/{jsonschema_id}
    Type: JsonSchemaFile
    """
    collection_path = f"/redfish/v1/jsonschemas"
    deleted = db.delete_item(collection_path, jsonschema_id)
    if deleted:
        return {"message": "Deleted successfully", "id": jsonschema_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_jsonschemas_jsonschget_redfish_v1_jsonschemas_jsonschema_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": jsonschema_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers", methods=["GET"])
def get_redfish_v1_managers():
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers
    Type: Collection ofManager
    """
    collection_path = "/redfish/v1/managers"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers", methods=["POST"])
def post_redfish_v1_managers(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers
    Type: Collection ofManager
    """
    collection_path = "/redfish/v1/managers"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}", methods=["GET"])
def get_redfish_v1_managers_manager_id(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}
    Type: Manager
    """
    collection_path = f"/redfish/v1/managers"
    item = db.get_item(collection_path, manager_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_managers_manager_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/managers/{manager_id}"
            static_val["Id"] = manager_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}", methods=["PATCH"])
def patch_redfish_v1_managers_manager_id(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/managers/{manager_id}
    Type: Manager
    """
    collection_path = f"/redfish/v1/managers"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, manager_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_managers_manager_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = manager_id
            existing["@odata.id"] = f"/redfish/v1/managers/{manager_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, manager_id, existing)
    return existing

@app.api_route("/redfish/v1/managers/{manager_id}", methods=["DELETE"])
def delete_redfish_v1_managers_manager_id(manager_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/managers/{manager_id}
    Type: Manager
    """
    collection_path = f"/redfish/v1/managers"
    deleted = db.delete_item(collection_path, manager_id)
    if deleted:
        return {"message": "Deleted successfully", "id": manager_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_managers_managet_redfish_v1_managers_manager_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": manager_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/ManagerDiagnosticData", methods=["GET"])
def get_redfish_v1_managers_manager_id_managerdiagnosticdata(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/ManagerDiagnosticData
    Type: ManagerDiagnosticData
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/ManagerDiagnosticData"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_managerdiagnosticdata", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/ManagerDiagnosticData/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/ManagerDiagnosticData", methods=["POST"])
def post_redfish_v1_managers_manager_id_managerdiagnosticdata(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/ManagerDiagnosticData
    Type: ManagerDiagnosticData
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/ManagerDiagnosticData"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/ManagerDiagnosticData/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/activehealthsystem", methods=["GET"])
def get_redfish_v1_managers_manager_id_activehealthsystem(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/activehealthsystem
    Type: HpeiLOActiveHealthSystem
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/activehealthsystem"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_activehealthsystem", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/activehealthsystem/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/activehealthsystem", methods=["POST"])
def post_redfish_v1_managers_manager_id_activehealthsystem(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/activehealthsystem
    Type: HpeiLOActiveHealthSystem
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/activehealthsystem"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/activehealthsystem/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/backuprestoreservice", methods=["GET"])
def get_redfish_v1_managers_manager_id_backuprestoreservice(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/backuprestoreservice
    Type: HpeiLOBackupRestoreService
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/backuprestoreservice"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_backuprestoreservice", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/backuprestoreservice/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/backuprestoreservice", methods=["POST"])
def post_redfish_v1_managers_manager_id_backuprestoreservice(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/backuprestoreservice
    Type: HpeiLOBackupRestoreService
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/backuprestoreservice"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/backuprestoreservice/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/backuprestoreservice/backupfiles", methods=["GET"])
def get_redfish_v1_managers_manager_id_backuprestoreservice_backupfiles(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/backuprestoreservice/backupfiles
    Type: Collection ofHpeiLOBackupFile
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/backuprestoreservice/backupfiles"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_backuprestoreservice_backupfiles", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/backuprestoreservice/backupfiles/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/backuprestoreservice/backupfiles", methods=["POST"])
def post_redfish_v1_managers_manager_id_backuprestoreservice_backupfiles(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/backuprestoreservice/backupfiles
    Type: Collection ofHpeiLOBackupFile
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/backuprestoreservice/backupfiles"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/backuprestoreservice/backupfiles/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/backuprestoreservice/backupfiles/{backupfil_id}", methods=["GET"])
def get_redfish_v1_managers_manager_id_backuprestoreservice_backupfiles_backupfil_id(manager_id: str, backupfil_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/backuprestoreservice/backupfiles/{backupfil_id}
    Type: HpeiLOBackupFile
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/backuprestoreservice/backupfiles"
    item = db.get_item(collection_path, backupfil_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_managers_manager_id_backuprestoreservice_backupfiles_backupfil_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/managers/{manager_id}/backuprestoreservice/backupfiles/{backupfil_id}"
            static_val["Id"] = backupfil_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/backuprestoreservice/backupfiles/{backupfil_id}", methods=["PATCH"])
def patch_redfish_v1_managers_manager_id_backuprestoreservice_backupfiles_backupfil_id(manager_id: str, backupfil_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/managers/{manager_id}/backuprestoreservice/backupfiles/{backupfil_id}
    Type: HpeiLOBackupFile
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/backuprestoreservice/backupfiles"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, backupfil_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_managers_manager_id_backuprestoreservice_backupfiles_backupfil_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = backupfil_id
            existing["@odata.id"] = f"/redfish/v1/managers/{manager_id}/backuprestoreservice/backupfiles/{backupfil_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, backupfil_id, existing)
    return existing

@app.api_route("/redfish/v1/managers/{manager_id}/backuprestoreservice/backupfiles/{backupfil_id}", methods=["DELETE"])
def delete_redfish_v1_managers_manager_id_backuprestoreservice_backupfiles_backupfil_id(manager_id: str, backupfil_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/managers/{manager_id}/backuprestoreservice/backupfiles/{backupfil_id}
    Type: HpeiLOBackupFile
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/backuprestoreservice/backupfiles"
    deleted = db.delete_item(collection_path, backupfil_id)
    if deleted:
        return {"message": "Deleted successfully", "id": backupfil_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_managers_manager_id_backuprestoreservice_backupfiles_backupget_redfish_v1_managers_manager_id_backuprestoreservice_backupfiles_backupfil_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": backupfil_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/datetime", methods=["GET"])
def get_redfish_v1_managers_manager_id_datetime(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/datetime
    Type: HpeiLODateTime
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/datetime"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_datetime", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/datetime/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/datetime", methods=["POST"])
def post_redfish_v1_managers_manager_id_datetime(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/datetime
    Type: HpeiLODateTime
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/datetime"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/datetime/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/dedicatednetworkports", methods=["GET"])
def get_redfish_v1_managers_manager_id_dedicatednetworkports(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/dedicatednetworkports
    Type: Collection ofPort
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/dedicatednetworkports"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_dedicatednetworkports", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/dedicatednetworkports/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/dedicatednetworkports", methods=["POST"])
def post_redfish_v1_managers_manager_id_dedicatednetworkports(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/dedicatednetworkports
    Type: Collection ofPort
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/dedicatednetworkports"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/dedicatednetworkports/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/dedicatednetworkports/{dedicatednetworkport_id}", methods=["GET"])
def get_redfish_v1_managers_manager_id_dedicatednetworkports_dedicatednetworkport_id(manager_id: str, dedicatednetworkport_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/dedicatednetworkports/{dedicatednetworkport_id}
    Type: Port
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/dedicatednetworkports"
    item = db.get_item(collection_path, dedicatednetworkport_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_managers_manager_id_dedicatednetworkports_dedicatednetworkport_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/managers/{manager_id}/dedicatednetworkports/{dedicatednetworkport_id}"
            static_val["Id"] = dedicatednetworkport_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/dedicatednetworkports/{dedicatednetworkport_id}", methods=["PATCH"])
def patch_redfish_v1_managers_manager_id_dedicatednetworkports_dedicatednetworkport_id(manager_id: str, dedicatednetworkport_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/managers/{manager_id}/dedicatednetworkports/{dedicatednetworkport_id}
    Type: Port
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/dedicatednetworkports"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, dedicatednetworkport_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_managers_manager_id_dedicatednetworkports_dedicatednetworkport_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = dedicatednetworkport_id
            existing["@odata.id"] = f"/redfish/v1/managers/{manager_id}/dedicatednetworkports/{dedicatednetworkport_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, dedicatednetworkport_id, existing)
    return existing

@app.api_route("/redfish/v1/managers/{manager_id}/dedicatednetworkports/{dedicatednetworkport_id}", methods=["DELETE"])
def delete_redfish_v1_managers_manager_id_dedicatednetworkports_dedicatednetworkport_id(manager_id: str, dedicatednetworkport_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/managers/{manager_id}/dedicatednetworkports/{dedicatednetworkport_id}
    Type: Port
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/dedicatednetworkports"
    deleted = db.delete_item(collection_path, dedicatednetworkport_id)
    if deleted:
        return {"message": "Deleted successfully", "id": dedicatednetworkport_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_managers_manager_id_dedicatednetworkports_dedicatednetworkpget_redfish_v1_managers_manager_id_dedicatednetworkports_dedicatednetworkport_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": dedicatednetworkport_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/ethernetinterfaces", methods=["GET"])
def get_redfish_v1_managers_manager_id_ethernetinterfaces(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/ethernetinterfaces
    Type: Collection ofEthernetInterface
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/ethernetinterfaces"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_ethernetinterfaces", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/ethernetinterfaces/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/ethernetinterfaces", methods=["POST"])
def post_redfish_v1_managers_manager_id_ethernetinterfaces(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/ethernetinterfaces
    Type: Collection ofEthernetInterface
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/ethernetinterfaces"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/ethernetinterfaces/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/ethernetinterfaces/{ethernetinterfac_id}", methods=["GET"])
def get_redfish_v1_managers_manager_id_ethernetinterfaces_ethernetinterfac_id(manager_id: str, ethernetinterfac_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/ethernetinterfaces/{ethernetinterfac_id}
    Type: EthernetInterface
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/ethernetinterfaces"
    item = db.get_item(collection_path, ethernetinterfac_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_managers_manager_id_ethernetinterfaces_ethernetinterfac_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/managers/{manager_id}/ethernetinterfaces/{ethernetinterfac_id}"
            static_val["Id"] = ethernetinterfac_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/ethernetinterfaces/{ethernetinterfac_id}", methods=["PATCH"])
def patch_redfish_v1_managers_manager_id_ethernetinterfaces_ethernetinterfac_id(manager_id: str, ethernetinterfac_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/managers/{manager_id}/ethernetinterfaces/{ethernetinterfac_id}
    Type: EthernetInterface
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/ethernetinterfaces"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, ethernetinterfac_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_managers_manager_id_ethernetinterfaces_ethernetinterfac_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = ethernetinterfac_id
            existing["@odata.id"] = f"/redfish/v1/managers/{manager_id}/ethernetinterfaces/{ethernetinterfac_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, ethernetinterfac_id, existing)
    return existing

@app.api_route("/redfish/v1/managers/{manager_id}/ethernetinterfaces/{ethernetinterfac_id}", methods=["DELETE"])
def delete_redfish_v1_managers_manager_id_ethernetinterfaces_ethernetinterfac_id(manager_id: str, ethernetinterfac_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/managers/{manager_id}/ethernetinterfaces/{ethernetinterfac_id}
    Type: EthernetInterface
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/ethernetinterfaces"
    deleted = db.delete_item(collection_path, ethernetinterfac_id)
    if deleted:
        return {"message": "Deleted successfully", "id": ethernetinterfac_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_managers_manager_id_ethernetinterfaces_ethernetinterget_redfish_v1_managers_manager_id_ethernetinterfaces_ethernetinterfac_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": ethernetinterfac_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/hostinterfaces", methods=["GET"])
def get_redfish_v1_managers_manager_id_hostinterfaces(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/hostinterfaces
    Type: Collection ofHostInterface
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/hostinterfaces"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_hostinterfaces", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/hostinterfaces/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/hostinterfaces", methods=["POST"])
def post_redfish_v1_managers_manager_id_hostinterfaces(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/hostinterfaces
    Type: Collection ofHostInterface
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/hostinterfaces"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/hostinterfaces/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/hostinterfaces/{hostinterfac_id}", methods=["GET"])
def get_redfish_v1_managers_manager_id_hostinterfaces_hostinterfac_id(manager_id: str, hostinterfac_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/hostinterfaces/{hostinterfac_id}
    Type: HostInterface
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/hostinterfaces"
    item = db.get_item(collection_path, hostinterfac_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_managers_manager_id_hostinterfaces_hostinterfac_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/managers/{manager_id}/hostinterfaces/{hostinterfac_id}"
            static_val["Id"] = hostinterfac_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/hostinterfaces/{hostinterfac_id}", methods=["PATCH"])
def patch_redfish_v1_managers_manager_id_hostinterfaces_hostinterfac_id(manager_id: str, hostinterfac_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/managers/{manager_id}/hostinterfaces/{hostinterfac_id}
    Type: HostInterface
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/hostinterfaces"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, hostinterfac_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_managers_manager_id_hostinterfaces_hostinterfac_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = hostinterfac_id
            existing["@odata.id"] = f"/redfish/v1/managers/{manager_id}/hostinterfaces/{hostinterfac_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, hostinterfac_id, existing)
    return existing

@app.api_route("/redfish/v1/managers/{manager_id}/hostinterfaces/{hostinterfac_id}", methods=["DELETE"])
def delete_redfish_v1_managers_manager_id_hostinterfaces_hostinterfac_id(manager_id: str, hostinterfac_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/managers/{manager_id}/hostinterfaces/{hostinterfac_id}
    Type: HostInterface
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/hostinterfaces"
    deleted = db.delete_item(collection_path, hostinterfac_id)
    if deleted:
        return {"message": "Deleted successfully", "id": hostinterfac_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_managers_manager_id_hostinterfaces_hostinterget_redfish_v1_managers_manager_id_hostinterfaces_hostinterfac_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": hostinterfac_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/licenseservice", methods=["GET"])
def get_redfish_v1_managers_manager_id_licenseservice(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/licenseservice
    Type: Collection ofHpeiLOLicense
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/licenseservice"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_licenseservice", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/licenseservice/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/licenseservice", methods=["POST"])
def post_redfish_v1_managers_manager_id_licenseservice(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/licenseservice
    Type: Collection ofHpeiLOLicense
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/licenseservice"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/licenseservice/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/licenseservice/{licenseservice_id}", methods=["GET"])
def get_redfish_v1_managers_manager_id_licenseservice_licenseservice_id(manager_id: str, licenseservice_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/licenseservice/{licenseservice_id}
    Type: HpeiLOLicense
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/licenseservice"
    item = db.get_item(collection_path, licenseservice_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_managers_manager_id_licenseservice_licenseservice_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/managers/{manager_id}/licenseservice/{licenseservice_id}"
            static_val["Id"] = licenseservice_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/licenseservice/{licenseservice_id}", methods=["PATCH"])
def patch_redfish_v1_managers_manager_id_licenseservice_licenseservice_id(manager_id: str, licenseservice_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/managers/{manager_id}/licenseservice/{licenseservice_id}
    Type: HpeiLOLicense
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/licenseservice"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, licenseservice_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_managers_manager_id_licenseservice_licenseservice_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = licenseservice_id
            existing["@odata.id"] = f"/redfish/v1/managers/{manager_id}/licenseservice/{licenseservice_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, licenseservice_id, existing)
    return existing

@app.api_route("/redfish/v1/managers/{manager_id}/licenseservice/{licenseservice_id}", methods=["DELETE"])
def delete_redfish_v1_managers_manager_id_licenseservice_licenseservice_id(manager_id: str, licenseservice_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/managers/{manager_id}/licenseservice/{licenseservice_id}
    Type: HpeiLOLicense
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/licenseservice"
    deleted = db.delete_item(collection_path, licenseservice_id)
    if deleted:
        return {"message": "Deleted successfully", "id": licenseservice_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_managers_manager_id_licenseservice_licenseservget_redfish_v1_managers_manager_id_licenseservice_licenseservice_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": licenseservice_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/logservices", methods=["GET"])
def get_redfish_v1_managers_manager_id_logservices(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/logservices
    Type: Collection ofLogService
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/logservices"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_logservices", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/logservices/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/logservices", methods=["POST"])
def post_redfish_v1_managers_manager_id_logservices(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/logservices
    Type: Collection ofLogService
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/logservices"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/logservices/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/logservices/iel", methods=["GET"])
def get_redfish_v1_managers_manager_id_logservices_iel(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/logservices/iel
    Type: LogService
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/logservices/iel"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_logservices_iel", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/logservices/iel/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/logservices/iel", methods=["POST"])
def post_redfish_v1_managers_manager_id_logservices_iel(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/logservices/iel
    Type: LogService
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/logservices/iel"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/logservices/iel/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/logservices/iel/entries", methods=["GET"])
def get_redfish_v1_managers_manager_id_logservices_iel_entries(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/logservices/iel/entries
    Type: Collection ofLogEntry
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/logservices/iel/entries"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_logservices_iel_entries", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/logservices/iel/entries/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/logservices/iel/entries", methods=["POST"])
def post_redfish_v1_managers_manager_id_logservices_iel_entries(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/logservices/iel/entries
    Type: Collection ofLogEntry
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/logservices/iel/entries"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/logservices/iel/entries/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/logservices/iel/entries/{entry_id}", methods=["GET"])
def get_redfish_v1_managers_manager_id_logservices_iel_entries_entry_id(manager_id: str, entry_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/logservices/iel/entries/{entry_id}
    Type: LogEntry
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/logservices/iel/entries"
    item = db.get_item(collection_path, entry_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_managers_manager_id_logservices_iel_entries_entry_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/managers/{manager_id}/logservices/iel/entries/{entry_id}"
            static_val["Id"] = entry_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/logservices/iel/entries/{entry_id}", methods=["PATCH"])
def patch_redfish_v1_managers_manager_id_logservices_iel_entries_entry_id(manager_id: str, entry_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/managers/{manager_id}/logservices/iel/entries/{entry_id}
    Type: LogEntry
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/logservices/iel/entries"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, entry_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_managers_manager_id_logservices_iel_entries_entry_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = entry_id
            existing["@odata.id"] = f"/redfish/v1/managers/{manager_id}/logservices/iel/entries/{entry_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, entry_id, existing)
    return existing

@app.api_route("/redfish/v1/managers/{manager_id}/logservices/iel/entries/{entry_id}", methods=["DELETE"])
def delete_redfish_v1_managers_manager_id_logservices_iel_entries_entry_id(manager_id: str, entry_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/managers/{manager_id}/logservices/iel/entries/{entry_id}
    Type: LogEntry
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/logservices/iel/entries"
    deleted = db.delete_item(collection_path, entry_id)
    if deleted:
        return {"message": "Deleted successfully", "id": entry_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_managers_manager_id_logservices_iel_entries_enget_redfish_v1_managers_manager_id_logservices_iel_entries_entry_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": entry_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/networkprotocol", methods=["GET"])
def get_redfish_v1_managers_manager_id_networkprotocol(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/networkprotocol
    Type: ManagerNetworkProtocol
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/networkprotocol"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_networkprotocol", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/networkprotocol/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/networkprotocol", methods=["POST"])
def post_redfish_v1_managers_manager_id_networkprotocol(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/networkprotocol
    Type: ManagerNetworkProtocol
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/networkprotocol"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/networkprotocol/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/networkprotocol/HTTPS/certificates", methods=["GET"])
def get_redfish_v1_managers_manager_id_networkprotocol_https_certificates(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/networkprotocol/HTTPS/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/networkprotocol/HTTPS/certificates"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_networkprotocol_https_certificates", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/networkprotocol/HTTPS/certificates/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/networkprotocol/HTTPS/certificates", methods=["POST"])
def post_redfish_v1_managers_manager_id_networkprotocol_https_certificates(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/networkprotocol/HTTPS/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/networkprotocol/HTTPS/certificates"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/networkprotocol/HTTPS/certificates/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/networkprotocol/HTTPS/certificates/{certificat_id}", methods=["GET"])
def get_redfish_v1_managers_manager_id_networkprotocol_https_certificates_certificat_id(manager_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/networkprotocol/HTTPS/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/networkprotocol/HTTPS/certificates"
    item = db.get_item(collection_path, certificat_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_managers_manager_id_networkprotocol_https_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/managers/{manager_id}/networkprotocol/HTTPS/certificates/{certificat_id}"
            static_val["Id"] = certificat_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/networkprotocol/HTTPS/certificates/{certificat_id}", methods=["PATCH"])
def patch_redfish_v1_managers_manager_id_networkprotocol_https_certificates_certificat_id(manager_id: str, certificat_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/managers/{manager_id}/networkprotocol/HTTPS/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/networkprotocol/HTTPS/certificates"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, certificat_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_managers_manager_id_networkprotocol_https_certificates_certificat_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = certificat_id
            existing["@odata.id"] = f"/redfish/v1/managers/{manager_id}/networkprotocol/HTTPS/certificates/{certificat_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, certificat_id, existing)
    return existing

@app.api_route("/redfish/v1/managers/{manager_id}/networkprotocol/HTTPS/certificates/{certificat_id}", methods=["DELETE"])
def delete_redfish_v1_managers_manager_id_networkprotocol_https_certificates_certificat_id(manager_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/managers/{manager_id}/networkprotocol/HTTPS/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/networkprotocol/HTTPS/certificates"
    deleted = db.delete_item(collection_path, certificat_id)
    if deleted:
        return {"message": "Deleted successfully", "id": certificat_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_managers_manager_id_networkprotocol_https_certificates_certifiget_redfish_v1_managers_manager_id_networkprotocol_https_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": certificat_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/remotesupportservice", methods=["GET"])
def get_redfish_v1_managers_manager_id_remotesupportservice(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/remotesupportservice
    Type: HpeRemoteSupport
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/remotesupportservice"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_remotesupportservice", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/remotesupportservice/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/remotesupportservice", methods=["POST"])
def post_redfish_v1_managers_manager_id_remotesupportservice(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/remotesupportservice
    Type: HpeRemoteSupport
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/remotesupportservice"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/remotesupportservice/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/remotesupportservice/serviceeventlogs", methods=["GET"])
def get_redfish_v1_managers_manager_id_remotesupportservice_serviceeventlogs(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/remotesupportservice/serviceeventlogs
    Type: Collection ofLogEntry
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/remotesupportservice/serviceeventlogs"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_remotesupportservice_serviceeventlogs", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/remotesupportservice/serviceeventlogs/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/remotesupportservice/serviceeventlogs", methods=["POST"])
def post_redfish_v1_managers_manager_id_remotesupportservice_serviceeventlogs(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/remotesupportservice/serviceeventlogs
    Type: Collection ofLogEntry
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/remotesupportservice/serviceeventlogs"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/remotesupportservice/serviceeventlogs/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/remotesupportservice/serviceeventlogs/{serviceeventlog_id}", methods=["GET"])
def get_redfish_v1_managers_manager_id_remotesupportservice_serviceeventlogs_serviceeventlog_id(manager_id: str, serviceeventlog_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/remotesupportservice/serviceeventlogs/{serviceeventlog_id}
    Type: LogEntry
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/remotesupportservice/serviceeventlogs"
    item = db.get_item(collection_path, serviceeventlog_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_managers_manager_id_remotesupportservice_serviceeventlogs_serviceeventlog_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/managers/{manager_id}/remotesupportservice/serviceeventlogs/{serviceeventlog_id}"
            static_val["Id"] = serviceeventlog_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/remotesupportservice/serviceeventlogs/{serviceeventlog_id}", methods=["PATCH"])
def patch_redfish_v1_managers_manager_id_remotesupportservice_serviceeventlogs_serviceeventlog_id(manager_id: str, serviceeventlog_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/managers/{manager_id}/remotesupportservice/serviceeventlogs/{serviceeventlog_id}
    Type: LogEntry
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/remotesupportservice/serviceeventlogs"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, serviceeventlog_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_managers_manager_id_remotesupportservice_serviceeventlogs_serviceeventlog_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = serviceeventlog_id
            existing["@odata.id"] = f"/redfish/v1/managers/{manager_id}/remotesupportservice/serviceeventlogs/{serviceeventlog_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, serviceeventlog_id, existing)
    return existing

@app.api_route("/redfish/v1/managers/{manager_id}/remotesupportservice/serviceeventlogs/{serviceeventlog_id}", methods=["DELETE"])
def delete_redfish_v1_managers_manager_id_remotesupportservice_serviceeventlogs_serviceeventlog_id(manager_id: str, serviceeventlog_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/managers/{manager_id}/remotesupportservice/serviceeventlogs/{serviceeventlog_id}
    Type: LogEntry
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/remotesupportservice/serviceeventlogs"
    deleted = db.delete_item(collection_path, serviceeventlog_id)
    if deleted:
        return {"message": "Deleted successfully", "id": serviceeventlog_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_managers_manager_id_remotesupportservice_serviceeventlogs_serviceeventget_redfish_v1_managers_manager_id_remotesupportservice_serviceeventlogs_serviceeventlog_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": serviceeventlog_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice", methods=["GET"])
def get_redfish_v1_managers_manager_id_securityservice(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/securityservice
    Type: HpeSecurityService
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_securityservice", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/securityservice/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice", methods=["POST"])
def post_redfish_v1_managers_manager_id_securityservice(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/securityservice
    Type: HpeSecurityService
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/bmchpeldevid/certificates", methods=["GET"])
def get_redfish_v1_managers_manager_id_securityservice_bmchpeldevid_certificates(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/securityservice/bmchpeldevid/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/bmchpeldevid/certificates"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_securityservice_bmchpeldevid_certificates", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/securityservice/bmchpeldevid/certificates/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/bmchpeldevid/certificates", methods=["POST"])
def post_redfish_v1_managers_manager_id_securityservice_bmchpeldevid_certificates(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/securityservice/bmchpeldevid/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/bmchpeldevid/certificates"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/bmchpeldevid/certificates/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/bmchpeldevid/certificates/{certificat_id}", methods=["GET"])
def get_redfish_v1_managers_manager_id_securityservice_bmchpeldevid_certificates_certificat_id(manager_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/securityservice/bmchpeldevid/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/bmchpeldevid/certificates"
    item = db.get_item(collection_path, certificat_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_managers_manager_id_securityservice_bmchpeldevid_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/bmchpeldevid/certificates/{certificat_id}"
            static_val["Id"] = certificat_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/bmchpeldevid/certificates/{certificat_id}", methods=["PATCH"])
def patch_redfish_v1_managers_manager_id_securityservice_bmchpeldevid_certificates_certificat_id(manager_id: str, certificat_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/managers/{manager_id}/securityservice/bmchpeldevid/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/bmchpeldevid/certificates"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, certificat_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_managers_manager_id_securityservice_bmchpeldevid_certificates_certificat_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = certificat_id
            existing["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/bmchpeldevid/certificates/{certificat_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, certificat_id, existing)
    return existing

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/bmchpeldevid/certificates/{certificat_id}", methods=["DELETE"])
def delete_redfish_v1_managers_manager_id_securityservice_bmchpeldevid_certificates_certificat_id(manager_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/managers/{manager_id}/securityservice/bmchpeldevid/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/bmchpeldevid/certificates"
    deleted = db.delete_item(collection_path, certificat_id)
    if deleted:
        return {"message": "Deleted successfully", "id": certificat_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_managers_manager_id_securityservice_bmchpeldevid_certificates_certifiget_redfish_v1_managers_manager_id_securityservice_bmchpeldevid_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": certificat_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/bmciak/certificates", methods=["GET"])
def get_redfish_v1_managers_manager_id_securityservice_bmciak_certificates(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/securityservice/bmciak/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/bmciak/certificates"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_securityservice_bmciak_certificates", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/securityservice/bmciak/certificates/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/bmciak/certificates", methods=["POST"])
def post_redfish_v1_managers_manager_id_securityservice_bmciak_certificates(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/securityservice/bmciak/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/bmciak/certificates"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/bmciak/certificates/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/bmciak/certificates/{certificat_id}", methods=["GET"])
def get_redfish_v1_managers_manager_id_securityservice_bmciak_certificates_certificat_id(manager_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/securityservice/bmciak/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/bmciak/certificates"
    item = db.get_item(collection_path, certificat_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_managers_manager_id_securityservice_bmciak_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/bmciak/certificates/{certificat_id}"
            static_val["Id"] = certificat_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/bmciak/certificates/{certificat_id}", methods=["PATCH"])
def patch_redfish_v1_managers_manager_id_securityservice_bmciak_certificates_certificat_id(manager_id: str, certificat_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/managers/{manager_id}/securityservice/bmciak/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/bmciak/certificates"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, certificat_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_managers_manager_id_securityservice_bmciak_certificates_certificat_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = certificat_id
            existing["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/bmciak/certificates/{certificat_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, certificat_id, existing)
    return existing

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/bmciak/certificates/{certificat_id}", methods=["DELETE"])
def delete_redfish_v1_managers_manager_id_securityservice_bmciak_certificates_certificat_id(manager_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/managers/{manager_id}/securityservice/bmciak/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/bmciak/certificates"
    deleted = db.delete_item(collection_path, certificat_id)
    if deleted:
        return {"message": "Deleted successfully", "id": certificat_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_managers_manager_id_securityservice_bmciak_certificates_certifiget_redfish_v1_managers_manager_id_securityservice_bmciak_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": certificat_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/bmcidevidpca/certificates", methods=["GET"])
def get_redfish_v1_managers_manager_id_securityservice_bmcidevidpca_certificates(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/securityservice/bmcidevidpca/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/bmcidevidpca/certificates"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_securityservice_bmcidevidpca_certificates", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/securityservice/bmcidevidpca/certificates/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/bmcidevidpca/certificates", methods=["POST"])
def post_redfish_v1_managers_manager_id_securityservice_bmcidevidpca_certificates(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/securityservice/bmcidevidpca/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/bmcidevidpca/certificates"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/bmcidevidpca/certificates/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/bmcidevidpca/certificates/{certificat_id}", methods=["GET"])
def get_redfish_v1_managers_manager_id_securityservice_bmcidevidpca_certificates_certificat_id(manager_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/securityservice/bmcidevidpca/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/bmcidevidpca/certificates"
    item = db.get_item(collection_path, certificat_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_managers_manager_id_securityservice_bmcidevidpca_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/bmcidevidpca/certificates/{certificat_id}"
            static_val["Id"] = certificat_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/bmcidevidpca/certificates/{certificat_id}", methods=["PATCH"])
def patch_redfish_v1_managers_manager_id_securityservice_bmcidevidpca_certificates_certificat_id(manager_id: str, certificat_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/managers/{manager_id}/securityservice/bmcidevidpca/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/bmcidevidpca/certificates"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, certificat_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_managers_manager_id_securityservice_bmcidevidpca_certificates_certificat_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = certificat_id
            existing["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/bmcidevidpca/certificates/{certificat_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, certificat_id, existing)
    return existing

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/bmcidevidpca/certificates/{certificat_id}", methods=["DELETE"])
def delete_redfish_v1_managers_manager_id_securityservice_bmcidevidpca_certificates_certificat_id(manager_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/managers/{manager_id}/securityservice/bmcidevidpca/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/bmcidevidpca/certificates"
    deleted = db.delete_item(collection_path, certificat_id)
    if deleted:
        return {"message": "Deleted successfully", "id": certificat_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_managers_manager_id_securityservice_bmcidevidpca_certificates_certifiget_redfish_v1_managers_manager_id_securityservice_bmcidevidpca_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": certificat_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/bmclak/certificates", methods=["GET"])
def get_redfish_v1_managers_manager_id_securityservice_bmclak_certificates(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/securityservice/bmclak/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/bmclak/certificates"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_securityservice_bmclak_certificates", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/securityservice/bmclak/certificates/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/bmclak/certificates", methods=["POST"])
def post_redfish_v1_managers_manager_id_securityservice_bmclak_certificates(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/securityservice/bmclak/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/bmclak/certificates"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/bmclak/certificates/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/bmclak/certificates/{certificat_id}", methods=["GET"])
def get_redfish_v1_managers_manager_id_securityservice_bmclak_certificates_certificat_id(manager_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/securityservice/bmclak/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/bmclak/certificates"
    item = db.get_item(collection_path, certificat_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_managers_manager_id_securityservice_bmclak_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/bmclak/certificates/{certificat_id}"
            static_val["Id"] = certificat_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/bmclak/certificates/{certificat_id}", methods=["PATCH"])
def patch_redfish_v1_managers_manager_id_securityservice_bmclak_certificates_certificat_id(manager_id: str, certificat_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/managers/{manager_id}/securityservice/bmclak/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/bmclak/certificates"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, certificat_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_managers_manager_id_securityservice_bmclak_certificates_certificat_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = certificat_id
            existing["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/bmclak/certificates/{certificat_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, certificat_id, existing)
    return existing

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/bmclak/certificates/{certificat_id}", methods=["DELETE"])
def delete_redfish_v1_managers_manager_id_securityservice_bmclak_certificates_certificat_id(manager_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/managers/{manager_id}/securityservice/bmclak/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/bmclak/certificates"
    deleted = db.delete_item(collection_path, certificat_id)
    if deleted:
        return {"message": "Deleted successfully", "id": certificat_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_managers_manager_id_securityservice_bmclak_certificates_certifiget_redfish_v1_managers_manager_id_securityservice_bmclak_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": certificat_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/certificateauthentication", methods=["GET"])
def get_redfish_v1_managers_manager_id_securityservice_certificateauthentication(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/securityservice/certificateauthentication
    Type: HpeCertAuth
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/certificateauthentication"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_securityservice_certificateauthentication", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/securityservice/certificateauthentication/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/certificateauthentication", methods=["POST"])
def post_redfish_v1_managers_manager_id_securityservice_certificateauthentication(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/securityservice/certificateauthentication
    Type: HpeCertAuth
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/certificateauthentication"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/certificateauthentication/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/certificateauthentication/cacertificates", methods=["GET"])
def get_redfish_v1_managers_manager_id_securityservice_certificateauthentication_cacertificates(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/securityservice/certificateauthentication/cacertificates
    Type: Collection ofHpeCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/certificateauthentication/cacertificates"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_securityservice_certificateauthentication_cacertificates", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/securityservice/certificateauthentication/cacertificates/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/certificateauthentication/cacertificates", methods=["POST"])
def post_redfish_v1_managers_manager_id_securityservice_certificateauthentication_cacertificates(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/securityservice/certificateauthentication/cacertificates
    Type: Collection ofHpeCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/certificateauthentication/cacertificates"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/certificateauthentication/cacertificates/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/certificateauthentication/cacertificates/{cacertificat_id}", methods=["GET"])
def get_redfish_v1_managers_manager_id_securityservice_certificateauthentication_cacertificates_cacertificat_id(manager_id: str, cacertificat_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/securityservice/certificateauthentication/cacertificates/{cacertificat_id}
    Type: HpeCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/certificateauthentication/cacertificates"
    item = db.get_item(collection_path, cacertificat_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_managers_manager_id_securityservice_certificateauthentication_cacertificates_cacertificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/certificateauthentication/cacertificates/{cacertificat_id}"
            static_val["Id"] = cacertificat_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/certificateauthentication/cacertificates/{cacertificat_id}", methods=["PATCH"])
def patch_redfish_v1_managers_manager_id_securityservice_certificateauthentication_cacertificates_cacertificat_id(manager_id: str, cacertificat_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/managers/{manager_id}/securityservice/certificateauthentication/cacertificates/{cacertificat_id}
    Type: HpeCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/certificateauthentication/cacertificates"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, cacertificat_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_managers_manager_id_securityservice_certificateauthentication_cacertificates_cacertificat_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = cacertificat_id
            existing["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/certificateauthentication/cacertificates/{cacertificat_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, cacertificat_id, existing)
    return existing

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/certificateauthentication/cacertificates/{cacertificat_id}", methods=["DELETE"])
def delete_redfish_v1_managers_manager_id_securityservice_certificateauthentication_cacertificates_cacertificat_id(manager_id: str, cacertificat_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/managers/{manager_id}/securityservice/certificateauthentication/cacertificates/{cacertificat_id}
    Type: HpeCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/certificateauthentication/cacertificates"
    deleted = db.delete_item(collection_path, cacertificat_id)
    if deleted:
        return {"message": "Deleted successfully", "id": cacertificat_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_managers_manager_id_securityservice_certificateauthentication_cacertificates_cacertifiget_redfish_v1_managers_manager_id_securityservice_certificateauthentication_cacertificates_cacertificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": cacertificat_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/eskm", methods=["GET"])
def get_redfish_v1_managers_manager_id_securityservice_eskm(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/securityservice/eskm
    Type: HpeESKM
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/eskm"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_securityservice_eskm", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/securityservice/eskm/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/eskm", methods=["POST"])
def post_redfish_v1_managers_manager_id_securityservice_eskm(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/securityservice/eskm
    Type: HpeESKM
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/eskm"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/eskm/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/httpscert", methods=["GET"])
def get_redfish_v1_managers_manager_id_securityservice_httpscert(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/securityservice/httpscert
    Type: HpeHttpsCert
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/httpscert"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_securityservice_httpscert", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/securityservice/httpscert/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/httpscert", methods=["POST"])
def post_redfish_v1_managers_manager_id_securityservice_httpscert(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/securityservice/httpscert
    Type: HpeHttpsCert
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/httpscert"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/httpscert/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/platformcert/certificates", methods=["GET"])
def get_redfish_v1_managers_manager_id_securityservice_platformcert_certificates(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/securityservice/platformcert/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/platformcert/certificates"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_securityservice_platformcert_certificates", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/securityservice/platformcert/certificates/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/platformcert/certificates", methods=["POST"])
def post_redfish_v1_managers_manager_id_securityservice_platformcert_certificates(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/securityservice/platformcert/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/platformcert/certificates"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/platformcert/certificates/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/platformcert/certificates/{certificat_id}", methods=["GET"])
def get_redfish_v1_managers_manager_id_securityservice_platformcert_certificates_certificat_id(manager_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/securityservice/platformcert/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/platformcert/certificates"
    item = db.get_item(collection_path, certificat_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_managers_manager_id_securityservice_platformcert_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/platformcert/certificates/{certificat_id}"
            static_val["Id"] = certificat_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/platformcert/certificates/{certificat_id}", methods=["PATCH"])
def patch_redfish_v1_managers_manager_id_securityservice_platformcert_certificates_certificat_id(manager_id: str, certificat_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/managers/{manager_id}/securityservice/platformcert/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/platformcert/certificates"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, certificat_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_managers_manager_id_securityservice_platformcert_certificates_certificat_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = certificat_id
            existing["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/platformcert/certificates/{certificat_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, certificat_id, existing)
    return existing

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/platformcert/certificates/{certificat_id}", methods=["DELETE"])
def delete_redfish_v1_managers_manager_id_securityservice_platformcert_certificates_certificat_id(manager_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/managers/{manager_id}/securityservice/platformcert/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/platformcert/certificates"
    deleted = db.delete_item(collection_path, certificat_id)
    if deleted:
        return {"message": "Deleted successfully", "id": certificat_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_managers_manager_id_securityservice_platformcert_certificates_certifiget_redfish_v1_managers_manager_id_securityservice_platformcert_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": certificat_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/securitydashboard", methods=["GET"])
def get_redfish_v1_managers_manager_id_securityservice_securitydashboard(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/securityservice/securitydashboard
    Type: HpeiLOSecurityDashboard
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/securitydashboard"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_securityservice_securitydashboard", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/securityservice/securitydashboard/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/securitydashboard", methods=["POST"])
def post_redfish_v1_managers_manager_id_securityservice_securitydashboard(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/securityservice/securitydashboard
    Type: HpeiLOSecurityDashboard
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/securitydashboard"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/securitydashboard/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/securitydashboard/securityparams", methods=["GET"])
def get_redfish_v1_managers_manager_id_securityservice_securitydashboard_securityparams(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/securityservice/securitydashboard/securityparams
    Type: Collection ofHpeiLOSecurityParam
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/securitydashboard/securityparams"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_securityservice_securitydashboard_securityparams", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/securityservice/securitydashboard/securityparams/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/securitydashboard/securityparams", methods=["POST"])
def post_redfish_v1_managers_manager_id_securityservice_securitydashboard_securityparams(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/securityservice/securitydashboard/securityparams
    Type: Collection ofHpeiLOSecurityParam
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/securitydashboard/securityparams"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/securitydashboard/securityparams/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/securitydashboard/securityparams/{securityparam_id}", methods=["GET"])
def get_redfish_v1_managers_manager_id_securityservice_securitydashboard_securityparams_securityparam_id(manager_id: str, securityparam_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/securityservice/securitydashboard/securityparams/{securityparam_id}
    Type: HpeiLOSecurityParam
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/securitydashboard/securityparams"
    item = db.get_item(collection_path, securityparam_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_managers_manager_id_securityservice_securitydashboard_securityparams_securityparam_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/securitydashboard/securityparams/{securityparam_id}"
            static_val["Id"] = securityparam_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/securitydashboard/securityparams/{securityparam_id}", methods=["PATCH"])
def patch_redfish_v1_managers_manager_id_securityservice_securitydashboard_securityparams_securityparam_id(manager_id: str, securityparam_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/managers/{manager_id}/securityservice/securitydashboard/securityparams/{securityparam_id}
    Type: HpeiLOSecurityParam
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/securitydashboard/securityparams"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, securityparam_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_managers_manager_id_securityservice_securitydashboard_securityparams_securityparam_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = securityparam_id
            existing["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/securitydashboard/securityparams/{securityparam_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, securityparam_id, existing)
    return existing

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/securitydashboard/securityparams/{securityparam_id}", methods=["DELETE"])
def delete_redfish_v1_managers_manager_id_securityservice_securitydashboard_securityparams_securityparam_id(manager_id: str, securityparam_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/managers/{manager_id}/securityservice/securitydashboard/securityparams/{securityparam_id}
    Type: HpeiLOSecurityParam
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/securitydashboard/securityparams"
    deleted = db.delete_item(collection_path, securityparam_id)
    if deleted:
        return {"message": "Deleted successfully", "id": securityparam_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_managers_manager_id_securityservice_securitydashboard_securityparams_securitypaget_redfish_v1_managers_manager_id_securityservice_securitydashboard_securityparams_securityparam_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": securityparam_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/sso", methods=["GET"])
def get_redfish_v1_managers_manager_id_securityservice_sso(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/securityservice/sso
    Type: HpeiLOSSO
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/sso"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_securityservice_sso", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/securityservice/sso/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/sso", methods=["POST"])
def post_redfish_v1_managers_manager_id_securityservice_sso(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/securityservice/sso
    Type: HpeiLOSSO
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/sso"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/sso/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/systemiak/certificates", methods=["GET"])
def get_redfish_v1_managers_manager_id_securityservice_systemiak_certificates(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/securityservice/systemiak/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/systemiak/certificates"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_securityservice_systemiak_certificates", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/securityservice/systemiak/certificates/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/systemiak/certificates", methods=["POST"])
def post_redfish_v1_managers_manager_id_securityservice_systemiak_certificates(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/securityservice/systemiak/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/systemiak/certificates"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/systemiak/certificates/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/systemiak/certificates/{certificat_id}", methods=["GET"])
def get_redfish_v1_managers_manager_id_securityservice_systemiak_certificates_certificat_id(manager_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/securityservice/systemiak/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/systemiak/certificates"
    item = db.get_item(collection_path, certificat_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_managers_manager_id_securityservice_systemiak_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/systemiak/certificates/{certificat_id}"
            static_val["Id"] = certificat_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/systemiak/certificates/{certificat_id}", methods=["PATCH"])
def patch_redfish_v1_managers_manager_id_securityservice_systemiak_certificates_certificat_id(manager_id: str, certificat_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/managers/{manager_id}/securityservice/systemiak/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/systemiak/certificates"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, certificat_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_managers_manager_id_securityservice_systemiak_certificates_certificat_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = certificat_id
            existing["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/systemiak/certificates/{certificat_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, certificat_id, existing)
    return existing

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/systemiak/certificates/{certificat_id}", methods=["DELETE"])
def delete_redfish_v1_managers_manager_id_securityservice_systemiak_certificates_certificat_id(manager_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/managers/{manager_id}/securityservice/systemiak/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/systemiak/certificates"
    deleted = db.delete_item(collection_path, certificat_id)
    if deleted:
        return {"message": "Deleted successfully", "id": certificat_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_managers_manager_id_securityservice_systemiak_certificates_certifiget_redfish_v1_managers_manager_id_securityservice_systemiak_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": certificat_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/systemidevid/certificates", methods=["GET"])
def get_redfish_v1_managers_manager_id_securityservice_systemidevid_certificates(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/securityservice/systemidevid/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/systemidevid/certificates"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_securityservice_systemidevid_certificates", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/securityservice/systemidevid/certificates/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/systemidevid/certificates", methods=["POST"])
def post_redfish_v1_managers_manager_id_securityservice_systemidevid_certificates(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/securityservice/systemidevid/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/systemidevid/certificates"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/systemidevid/certificates/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/systemidevid/certificates/{certificat_id}", methods=["GET"])
def get_redfish_v1_managers_manager_id_securityservice_systemidevid_certificates_certificat_id(manager_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/securityservice/systemidevid/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/systemidevid/certificates"
    item = db.get_item(collection_path, certificat_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_managers_manager_id_securityservice_systemidevid_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/systemidevid/certificates/{certificat_id}"
            static_val["Id"] = certificat_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/systemidevid/certificates/{certificat_id}", methods=["PATCH"])
def patch_redfish_v1_managers_manager_id_securityservice_systemidevid_certificates_certificat_id(manager_id: str, certificat_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/managers/{manager_id}/securityservice/systemidevid/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/systemidevid/certificates"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, certificat_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_managers_manager_id_securityservice_systemidevid_certificates_certificat_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = certificat_id
            existing["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/systemidevid/certificates/{certificat_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, certificat_id, existing)
    return existing

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/systemidevid/certificates/{certificat_id}", methods=["DELETE"])
def delete_redfish_v1_managers_manager_id_securityservice_systemidevid_certificates_certificat_id(manager_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/managers/{manager_id}/securityservice/systemidevid/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/systemidevid/certificates"
    deleted = db.delete_item(collection_path, certificat_id)
    if deleted:
        return {"message": "Deleted successfully", "id": certificat_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_managers_manager_id_securityservice_systemidevid_certificates_certifiget_redfish_v1_managers_manager_id_securityservice_systemidevid_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": certificat_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/systemlak/certificates", methods=["GET"])
def get_redfish_v1_managers_manager_id_securityservice_systemlak_certificates(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/securityservice/systemlak/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/systemlak/certificates"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_securityservice_systemlak_certificates", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/securityservice/systemlak/certificates/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/systemlak/certificates", methods=["POST"])
def post_redfish_v1_managers_manager_id_securityservice_systemlak_certificates(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/securityservice/systemlak/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/systemlak/certificates"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/systemlak/certificates/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/systemlak/certificates/{certificat_id}", methods=["GET"])
def get_redfish_v1_managers_manager_id_securityservice_systemlak_certificates_certificat_id(manager_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/securityservice/systemlak/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/systemlak/certificates"
    item = db.get_item(collection_path, certificat_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_managers_manager_id_securityservice_systemlak_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/systemlak/certificates/{certificat_id}"
            static_val["Id"] = certificat_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/systemlak/certificates/{certificat_id}", methods=["PATCH"])
def patch_redfish_v1_managers_manager_id_securityservice_systemlak_certificates_certificat_id(manager_id: str, certificat_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/managers/{manager_id}/securityservice/systemlak/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/systemlak/certificates"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, certificat_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_managers_manager_id_securityservice_systemlak_certificates_certificat_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = certificat_id
            existing["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/systemlak/certificates/{certificat_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, certificat_id, existing)
    return existing

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/systemlak/certificates/{certificat_id}", methods=["DELETE"])
def delete_redfish_v1_managers_manager_id_securityservice_systemlak_certificates_certificat_id(manager_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/managers/{manager_id}/securityservice/systemlak/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/systemlak/certificates"
    deleted = db.delete_item(collection_path, certificat_id)
    if deleted:
        return {"message": "Deleted successfully", "id": certificat_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_managers_manager_id_securityservice_systemlak_certificates_certifiget_redfish_v1_managers_manager_id_securityservice_systemlak_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": certificat_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/systemldevid/certificates", methods=["GET"])
def get_redfish_v1_managers_manager_id_securityservice_systemldevid_certificates(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/securityservice/systemldevid/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/systemldevid/certificates"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_securityservice_systemldevid_certificates", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/securityservice/systemldevid/certificates/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/systemldevid/certificates", methods=["POST"])
def post_redfish_v1_managers_manager_id_securityservice_systemldevid_certificates(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/securityservice/systemldevid/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/systemldevid/certificates"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/systemldevid/certificates/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/systemldevid/certificates/{certificat_id}", methods=["GET"])
def get_redfish_v1_managers_manager_id_securityservice_systemldevid_certificates_certificat_id(manager_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/securityservice/systemldevid/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/systemldevid/certificates"
    item = db.get_item(collection_path, certificat_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_managers_manager_id_securityservice_systemldevid_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/systemldevid/certificates/{certificat_id}"
            static_val["Id"] = certificat_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/systemldevid/certificates/{certificat_id}", methods=["PATCH"])
def patch_redfish_v1_managers_manager_id_securityservice_systemldevid_certificates_certificat_id(manager_id: str, certificat_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/managers/{manager_id}/securityservice/systemldevid/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/systemldevid/certificates"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, certificat_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_managers_manager_id_securityservice_systemldevid_certificates_certificat_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = certificat_id
            existing["@odata.id"] = f"/redfish/v1/managers/{manager_id}/securityservice/systemldevid/certificates/{certificat_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, certificat_id, existing)
    return existing

@app.api_route("/redfish/v1/managers/{manager_id}/securityservice/systemldevid/certificates/{certificat_id}", methods=["DELETE"])
def delete_redfish_v1_managers_manager_id_securityservice_systemldevid_certificates_certificat_id(manager_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/managers/{manager_id}/securityservice/systemldevid/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/securityservice/systemldevid/certificates"
    deleted = db.delete_item(collection_path, certificat_id)
    if deleted:
        return {"message": "Deleted successfully", "id": certificat_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_managers_manager_id_securityservice_systemldevid_certificates_certifiget_redfish_v1_managers_manager_id_securityservice_systemldevid_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": certificat_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/sharednetworkports", methods=["GET"])
def get_redfish_v1_managers_manager_id_sharednetworkports(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/sharednetworkports
    Type: Collection ofPort
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/sharednetworkports"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_sharednetworkports", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/sharednetworkports/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/sharednetworkports", methods=["POST"])
def post_redfish_v1_managers_manager_id_sharednetworkports(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/sharednetworkports
    Type: Collection ofPort
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/sharednetworkports"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/sharednetworkports/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/sharednetworkports/{sharednetworkport_id}", methods=["GET"])
def get_redfish_v1_managers_manager_id_sharednetworkports_sharednetworkport_id(manager_id: str, sharednetworkport_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/sharednetworkports/{sharednetworkport_id}
    Type: Port
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/sharednetworkports"
    item = db.get_item(collection_path, sharednetworkport_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_managers_manager_id_sharednetworkports_sharednetworkport_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/managers/{manager_id}/sharednetworkports/{sharednetworkport_id}"
            static_val["Id"] = sharednetworkport_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/sharednetworkports/{sharednetworkport_id}", methods=["PATCH"])
def patch_redfish_v1_managers_manager_id_sharednetworkports_sharednetworkport_id(manager_id: str, sharednetworkport_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/managers/{manager_id}/sharednetworkports/{sharednetworkport_id}
    Type: Port
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/sharednetworkports"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, sharednetworkport_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_managers_manager_id_sharednetworkports_sharednetworkport_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = sharednetworkport_id
            existing["@odata.id"] = f"/redfish/v1/managers/{manager_id}/sharednetworkports/{sharednetworkport_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, sharednetworkport_id, existing)
    return existing

@app.api_route("/redfish/v1/managers/{manager_id}/sharednetworkports/{sharednetworkport_id}", methods=["DELETE"])
def delete_redfish_v1_managers_manager_id_sharednetworkports_sharednetworkport_id(manager_id: str, sharednetworkport_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/managers/{manager_id}/sharednetworkports/{sharednetworkport_id}
    Type: Port
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/sharednetworkports"
    deleted = db.delete_item(collection_path, sharednetworkport_id)
    if deleted:
        return {"message": "Deleted successfully", "id": sharednetworkport_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_managers_manager_id_sharednetworkports_sharednetworkpget_redfish_v1_managers_manager_id_sharednetworkports_sharednetworkport_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": sharednetworkport_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/snmpservice", methods=["GET"])
def get_redfish_v1_managers_manager_id_snmpservice(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/snmpservice
    Type: HpeiLOSnmpService
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/snmpservice"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_snmpservice", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/snmpservice/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/snmpservice", methods=["POST"])
def post_redfish_v1_managers_manager_id_snmpservice(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/snmpservice
    Type: HpeiLOSnmpService
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/snmpservice"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/snmpservice/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/snmpservice/snmpalertdestinations", methods=["GET"])
def get_redfish_v1_managers_manager_id_snmpservice_snmpalertdestinations(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/snmpservice/snmpalertdestinations
    Type: Collection ofHpeSNMPAlertDestination
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/snmpservice/snmpalertdestinations"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_snmpservice_snmpalertdestinations", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/snmpservice/snmpalertdestinations/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/snmpservice/snmpalertdestinations", methods=["POST"])
def post_redfish_v1_managers_manager_id_snmpservice_snmpalertdestinations(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/snmpservice/snmpalertdestinations
    Type: Collection ofHpeSNMPAlertDestination
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/snmpservice/snmpalertdestinations"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/snmpservice/snmpalertdestinations/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/snmpservice/snmpalertdestinations/{snmpalertdestination_id}", methods=["GET"])
def get_redfish_v1_managers_manager_id_snmpservice_snmpalertdestinations_snmpalertdestination_id(manager_id: str, snmpalertdestination_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/snmpservice/snmpalertdestinations/{snmpalertdestination_id}
    Type: HpeSNMPAlertDestination
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/snmpservice/snmpalertdestinations"
    item = db.get_item(collection_path, snmpalertdestination_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_managers_manager_id_snmpservice_snmpalertdestinations_snmpalertdestination_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/managers/{manager_id}/snmpservice/snmpalertdestinations/{snmpalertdestination_id}"
            static_val["Id"] = snmpalertdestination_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/snmpservice/snmpalertdestinations/{snmpalertdestination_id}", methods=["PATCH"])
def patch_redfish_v1_managers_manager_id_snmpservice_snmpalertdestinations_snmpalertdestination_id(manager_id: str, snmpalertdestination_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/managers/{manager_id}/snmpservice/snmpalertdestinations/{snmpalertdestination_id}
    Type: HpeSNMPAlertDestination
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/snmpservice/snmpalertdestinations"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, snmpalertdestination_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_managers_manager_id_snmpservice_snmpalertdestinations_snmpalertdestination_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = snmpalertdestination_id
            existing["@odata.id"] = f"/redfish/v1/managers/{manager_id}/snmpservice/snmpalertdestinations/{snmpalertdestination_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, snmpalertdestination_id, existing)
    return existing

@app.api_route("/redfish/v1/managers/{manager_id}/snmpservice/snmpalertdestinations/{snmpalertdestination_id}", methods=["DELETE"])
def delete_redfish_v1_managers_manager_id_snmpservice_snmpalertdestinations_snmpalertdestination_id(manager_id: str, snmpalertdestination_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/managers/{manager_id}/snmpservice/snmpalertdestinations/{snmpalertdestination_id}
    Type: HpeSNMPAlertDestination
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/snmpservice/snmpalertdestinations"
    deleted = db.delete_item(collection_path, snmpalertdestination_id)
    if deleted:
        return {"message": "Deleted successfully", "id": snmpalertdestination_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_managers_manager_id_snmpservice_snmpalertdestinations_snmpalertdestinatget_redfish_v1_managers_manager_id_snmpservice_snmpalertdestinations_snmpalertdestination_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": snmpalertdestination_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/snmpservice/snmpusers", methods=["GET"])
def get_redfish_v1_managers_manager_id_snmpservice_snmpusers(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/snmpservice/snmpusers
    Type: Collection ofHpeSNMPUser
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/snmpservice/snmpusers"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_snmpservice_snmpusers", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/snmpservice/snmpusers/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/snmpservice/snmpusers", methods=["POST"])
def post_redfish_v1_managers_manager_id_snmpservice_snmpusers(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/snmpservice/snmpusers
    Type: Collection ofHpeSNMPUser
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/snmpservice/snmpusers"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/snmpservice/snmpusers/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/snmpservice/snmpusers/{snmpuser_id}", methods=["GET"])
def get_redfish_v1_managers_manager_id_snmpservice_snmpusers_snmpuser_id(manager_id: str, snmpuser_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/snmpservice/snmpusers/{snmpuser_id}
    Type: HpeSNMPUser
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/snmpservice/snmpusers"
    item = db.get_item(collection_path, snmpuser_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_managers_manager_id_snmpservice_snmpusers_snmpuser_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/managers/{manager_id}/snmpservice/snmpusers/{snmpuser_id}"
            static_val["Id"] = snmpuser_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/snmpservice/snmpusers/{snmpuser_id}", methods=["PATCH"])
def patch_redfish_v1_managers_manager_id_snmpservice_snmpusers_snmpuser_id(manager_id: str, snmpuser_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/managers/{manager_id}/snmpservice/snmpusers/{snmpuser_id}
    Type: HpeSNMPUser
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/snmpservice/snmpusers"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, snmpuser_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_managers_manager_id_snmpservice_snmpusers_snmpuser_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = snmpuser_id
            existing["@odata.id"] = f"/redfish/v1/managers/{manager_id}/snmpservice/snmpusers/{snmpuser_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, snmpuser_id, existing)
    return existing

@app.api_route("/redfish/v1/managers/{manager_id}/snmpservice/snmpusers/{snmpuser_id}", methods=["DELETE"])
def delete_redfish_v1_managers_manager_id_snmpservice_snmpusers_snmpuser_id(manager_id: str, snmpuser_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/managers/{manager_id}/snmpservice/snmpusers/{snmpuser_id}
    Type: HpeSNMPUser
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/snmpservice/snmpusers"
    deleted = db.delete_item(collection_path, snmpuser_id)
    if deleted:
        return {"message": "Deleted successfully", "id": snmpuser_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_managers_manager_id_snmpservice_snmpusers_snmpuget_redfish_v1_managers_manager_id_snmpservice_snmpusers_snmpuser_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": snmpuser_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/virtualmedia", methods=["GET"])
def get_redfish_v1_managers_manager_id_virtualmedia(manager_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/virtualmedia
    Type: Collection ofVirtualMedia
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/virtualmedia"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_managers_manager_id_virtualmedia", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/managers/{manager_id}/virtualmedia/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/managers/{manager_id}/virtualmedia", methods=["POST"])
def post_redfish_v1_managers_manager_id_virtualmedia(manager_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/virtualmedia
    Type: Collection ofVirtualMedia
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/virtualmedia"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/managers/{manager_id}/virtualmedia/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/managers/{manager_id}/virtualmedia/{virtualmedia_id}", methods=["GET"])
def get_redfish_v1_managers_manager_id_virtualmedia_virtualmedia_id(manager_id: str, virtualmedia_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/managers/{manager_id}/virtualmedia/{virtualmedia_id}
    Type: VirtualMedia
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/virtualmedia"
    item = db.get_item(collection_path, virtualmedia_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_managers_manager_id_virtualmedia_virtualmedia_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/managers/{manager_id}/virtualmedia/{virtualmedia_id}"
            static_val["Id"] = virtualmedia_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/managers/{manager_id}/virtualmedia/{virtualmedia_id}", methods=["PATCH"])
def patch_redfish_v1_managers_manager_id_virtualmedia_virtualmedia_id(manager_id: str, virtualmedia_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/managers/{manager_id}/virtualmedia/{virtualmedia_id}
    Type: VirtualMedia
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/virtualmedia"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, virtualmedia_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_managers_manager_id_virtualmedia_virtualmedia_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = virtualmedia_id
            existing["@odata.id"] = f"/redfish/v1/managers/{manager_id}/virtualmedia/{virtualmedia_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, virtualmedia_id, existing)
    return existing

@app.api_route("/redfish/v1/managers/{manager_id}/virtualmedia/{virtualmedia_id}", methods=["DELETE"])
def delete_redfish_v1_managers_manager_id_virtualmedia_virtualmedia_id(manager_id: str, virtualmedia_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/managers/{manager_id}/virtualmedia/{virtualmedia_id}
    Type: VirtualMedia
    """
    collection_path = f"/redfish/v1/managers/{manager_id}/virtualmedia"
    deleted = db.delete_item(collection_path, virtualmedia_id)
    if deleted:
        return {"message": "Deleted successfully", "id": virtualmedia_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_managers_manager_id_virtualmedia_virtualmeget_redfish_v1_managers_manager_id_virtualmedia_virtualmedia_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": virtualmedia_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/registries", methods=["GET"])
def get_redfish_v1_registries():
    """
    iLO Redfish Endpoint: GET /redfish/v1/registries
    Type: Collection ofMessageRegistryFile
    """
    collection_path = "/redfish/v1/registries"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_registries", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/registries/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/registries", methods=["POST"])
def post_redfish_v1_registries(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/registries
    Type: Collection ofMessageRegistryFile
    """
    collection_path = "/redfish/v1/registries"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/registries/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/registries/{registry_id}", methods=["GET"])
def get_redfish_v1_registries_registry_id(registry_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/registries/{registry_id}
    Type: MessageRegistryFile
    """
    collection_path = f"/redfish/v1/registries"
    item = db.get_item(collection_path, registry_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_registries_registry_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/registries/{registry_id}"
            static_val["Id"] = registry_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/registries/{registry_id}", methods=["PATCH"])
def patch_redfish_v1_registries_registry_id(registry_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/registries/{registry_id}
    Type: MessageRegistryFile
    """
    collection_path = f"/redfish/v1/registries"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, registry_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_registries_registry_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = registry_id
            existing["@odata.id"] = f"/redfish/v1/registries/{registry_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, registry_id, existing)
    return existing

@app.api_route("/redfish/v1/registries/{registry_id}", methods=["DELETE"])
def delete_redfish_v1_registries_registry_id(registry_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/registries/{registry_id}
    Type: MessageRegistryFile
    """
    collection_path = f"/redfish/v1/registries"
    deleted = db.delete_item(collection_path, registry_id)
    if deleted:
        return {"message": "Deleted successfully", "id": registry_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_registries_regisget_redfish_v1_registries_registry_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": registry_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/resourcedirectory", methods=["GET"])
def get_redfish_v1_resourcedirectory():
    """
    iLO Redfish Endpoint: GET /redfish/v1/resourcedirectory
    Type: HpeiLOResourceDirectory
    """
    collection_path = "/redfish/v1/resourcedirectory"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_resourcedirectory", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/resourcedirectory/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/resourcedirectory", methods=["POST"])
def post_redfish_v1_resourcedirectory(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/resourcedirectory
    Type: HpeiLOResourceDirectory
    """
    collection_path = "/redfish/v1/resourcedirectory"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/resourcedirectory/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/sessionservice", methods=["GET"])
def get_redfish_v1_sessionservice():
    """
    iLO Redfish Endpoint: GET /redfish/v1/sessionservice
    Type: SessionService
    """
    collection_path = "/redfish/v1/sessionservice"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_sessionservice", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/sessionservice/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/sessionservice", methods=["POST"])
def post_redfish_v1_sessionservice(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/sessionservice
    Type: SessionService
    """
    collection_path = "/redfish/v1/sessionservice"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/sessionservice/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/sessionservice/sessions", methods=["GET"])
def get_redfish_v1_sessionservice_sessions():
    """
    iLO Redfish Endpoint: GET /redfish/v1/sessionservice/sessions
    Type: Collection ofSession
    """
    collection_path = "/redfish/v1/sessionservice/sessions"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_sessionservice_sessions", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/sessionservice/sessions/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/sessionservice/sessions", methods=["POST"])
def post_redfish_v1_sessionservice_sessions(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/sessionservice/sessions
    Type: Collection ofSession
    """
    collection_path = "/redfish/v1/sessionservice/sessions"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/sessionservice/sessions/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/sessionservice/sessions/{session_id}", methods=["GET"])
def get_redfish_v1_sessionservice_sessions_session_id(session_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/sessionservice/sessions/{session_id}
    Type: Session
    """
    collection_path = f"/redfish/v1/sessionservice/sessions"
    item = db.get_item(collection_path, session_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_sessionservice_sessions_session_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/sessionservice/sessions/{session_id}"
            static_val["Id"] = session_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/sessionservice/sessions/{session_id}", methods=["PATCH"])
def patch_redfish_v1_sessionservice_sessions_session_id(session_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/sessionservice/sessions/{session_id}
    Type: Session
    """
    collection_path = f"/redfish/v1/sessionservice/sessions"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, session_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_sessionservice_sessions_session_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = session_id
            existing["@odata.id"] = f"/redfish/v1/sessionservice/sessions/{session_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, session_id, existing)
    return existing

@app.api_route("/redfish/v1/sessionservice/sessions/{session_id}", methods=["DELETE"])
def delete_redfish_v1_sessionservice_sessions_session_id(session_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/sessionservice/sessions/{session_id}
    Type: Session
    """
    collection_path = f"/redfish/v1/sessionservice/sessions"
    deleted = db.delete_item(collection_path, session_id)
    if deleted:
        return {"message": "Deleted successfully", "id": session_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_sessionservice_sessions_sessget_redfish_v1_sessionservice_sessions_session_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": session_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems", methods=["GET"])
def get_redfish_v1_systems():
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems
    Type: Collection ofComputerSystem
    """
    collection_path = "/redfish/v1/systems"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems", methods=["POST"])
def post_redfish_v1_systems(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems
    Type: Collection ofComputerSystem
    """
    import uuid as _uuid
    from datetime import datetime, timezone
    collection_path = "/redfish/v1/systems"
    payload_dict = payload if payload is not None else {}

    # The server name/serial from the payload — used as search key, never as UUID
    name = (payload_dict.get("Name") or payload_dict.get("name")
            or payload_dict.get("serial_number") or payload_dict.get("SerialNumber"))

    # --- Always resolve UUID from PostgreSQL by serial_number ---
    device_uuid = None
    pg_ip = None
    pg_fqdn = None
    pg_device_type = None
    pg_source_device_id = None
    if name:
        try:
            import psycopg2
            pg_conn = psycopg2.connect(
                dbname="hpe_agentic_ai", user="postgres",
                password="mithles", host="localhost", connect_timeout=3
            )
            pg_cur = pg_conn.cursor()
            pg_cur.execute(
                "SELECT id, ip_address, fqdn, device_type, source_device_id FROM devices WHERE serial_number = %s LIMIT 1",
                (name,)
            )
            row = pg_cur.fetchone()
            if row:
                device_uuid        = str(row[0])
                pg_ip              = str(row[1]) if row[1] else None
                pg_fqdn            = row[2]
                pg_device_type     = row[3]
                pg_source_device_id = row[4]
            pg_conn.close()
        except Exception:
            pass  # PG unavailable

    # UUID = PG device id (real UUID) or fresh uuid4 — never the server name
    item_id  = device_uuid or str(_uuid.uuid4())
    now      = datetime.now(timezone.utc).isoformat()
    hostname = name or item_id
    fqdn     = pg_fqdn or f"{hostname}.server.local"

    # Build defaults — payload values override these
    defaults = {
        # Redfish standard fields
        "@odata.type"       : "#ComputerSystem.v1_17_0.ComputerSystem",
        "SystemType"        : "Physical",
        "Manufacturer"      : "HPE",
        "Model"             : "ProLiant DL360 Gen10",
        "SerialNumber"      : name or item_id,
        "serial_number"     : name or item_id,
        "UUID"              : item_id,
        "PowerState"        : "On",
        "Status"            : {"State": "Enabled", "Health": "OK"},
        "Bios"              : {"@odata.id": f"/redfish/v1/systems/{item_id}/bios"},
        "Processors"        : {"@odata.id": f"/redfish/v1/systems/{item_id}/processors"},
        "Memory"            : {"@odata.id": f"/redfish/v1/systems/{item_id}/memory"},
        "Storage"           : {"@odata.id": f"/redfish/v1/systems/{item_id}/storage"},
        # Custom tracking fields
        "name"              : hostname,
        "ip_address"        : pg_ip or "0.0.0.0",
        "fqdn"              : fqdn,
        "management_source" : "mock_server",
        "source_host"       : "mock-server-manager.local",
        "source_device_id"  : pg_source_device_id or item_id,
        "device_type"       : pg_device_type or "server",
        "last_seen"         : now,
        "created_at"        : now,
        "updated_at"        : now,
        "firmware_version"  : "iLO 5 v2.92",
        "health_status"     : "OK",
        "cpu_cores"         : 16,
        "total_capacity"    : 0,
        "free_capacity"     : 0,
        "temperature"       : 0.0,
        "temperature_celsius": 0.0,
        "storage_utilization": 0.0,
        "free_storage"      : 0,
        "memory_utilization": 0.0,
        "active_vms"        : 0,
        "allocated_cpu"     : 0,
        "allocated_memory"  : 0,
        "ports"             : 2,
        "configured_vlans"  : 1,
        "cpu_utilization"   : 0.0,
        "memory_usage"      : 0.0,
        "power_draw"        : 0.0,
    }

    # Merge: defaults first, then payload overrides
    merged = {**defaults, **payload_dict}

    # Always force-set these — payload must never override UUID/id
    merged["Id"]               = item_id
    merged["id"]               = item_id
    merged["UUID"]             = item_id
    merged["source_device_id"] = pg_source_device_id or item_id
    merged["@odata.id"]        = f"/redfish/v1/systems/{item_id}"
    merged["updated_at"]       = now

    db.upsert_item(collection_path, item_id, merged)
    
    # Auto-create linked manager and chassis for Redfish compliance
    db.upsert_item("/redfish/v1/managers", item_id, {
        "id": item_id,
        "UUID": item_id,
        "name": f"{hostname}-ilo",
        "source_device_id": pg_source_device_id or item_id,
        "@odata.id": f"/redfish/v1/Managers/{item_id}",
        "Links": {"ManagerForServers": [{"@odata.id": f"/redfish/v1/systems/{item_id}"}]}
    })
    db.upsert_item("/redfish/v1/chassis", item_id, {
        "id": item_id,
        "UUID": item_id,
        "name": f"{hostname}-chassis",
        "SerialNumber": name or item_id,
        "source_device_id": pg_source_device_id or item_id,
        "@odata.id": f"/redfish/v1/Chassis/{item_id}",
        "Links": {"ComputerSystems": [{"@odata.id": f"/redfish/v1/systems/{item_id}"}]}
    })
    
    return merged

@app.api_route("/redfish/v1/systems/{system_id}", methods=["GET"])
def get_redfish_v1_systems_system_id(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}
    Type: ComputerSystem
    """
    collection_path = f"/redfish/v1/systems"
    item = db.get_item(collection_path, system_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}"
            static_val["Id"] = system_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}
    Type: ComputerSystem
    """
    collection_path = f"/redfish/v1/systems"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, system_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = system_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, system_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id(system_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}
    Type: ComputerSystem
    """
    collection_path = f"/redfish/v1/systems"
    deleted = db.delete_item(collection_path, system_id)
    if deleted:
        # Auto-delete linked manager and chassis
        db.delete_item("/redfish/v1/managers", system_id)
        db.delete_item("/redfish/v1/chassis", system_id)
        return {"message": "Deleted successfully", "id": system_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_sysget_redfish_v1_systems_system_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": system_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/bios", methods=["GET"])
def get_redfish_v1_systems_system_id_bios(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/bios
    Type: Bios
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_bios", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/bios/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/bios", methods=["POST"])
def post_redfish_v1_systems_system_id_bios(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/bios
    Type: Bios
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/bios/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/bios/baseconfigs", methods=["GET"])
def get_redfish_v1_systems_system_id_bios_baseconfigs(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/bios/baseconfigs
    Type: HpeBaseConfigs
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/baseconfigs"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_bios_baseconfigs", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/bios/baseconfigs/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/bios/baseconfigs", methods=["POST"])
def post_redfish_v1_systems_system_id_bios_baseconfigs(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/bios/baseconfigs
    Type: HpeBaseConfigs
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/baseconfigs"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/bios/baseconfigs/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/bios/boot", methods=["GET"])
def get_redfish_v1_systems_system_id_bios_boot(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/bios/boot
    Type: HpeServerBootSettings
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/boot"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_bios_boot", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/bios/boot/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/bios/boot", methods=["POST"])
def post_redfish_v1_systems_system_id_bios_boot(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/bios/boot
    Type: HpeServerBootSettings
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/boot"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/bios/boot/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/bios/boot/baseconfigs", methods=["GET"])
def get_redfish_v1_systems_system_id_bios_boot_baseconfigs(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/bios/boot/baseconfigs
    Type: HpeBaseConfigs
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/boot/baseconfigs"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_bios_boot_baseconfigs", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/bios/boot/baseconfigs/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/bios/boot/baseconfigs", methods=["POST"])
def post_redfish_v1_systems_system_id_bios_boot_baseconfigs(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/bios/boot/baseconfigs
    Type: HpeBaseConfigs
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/boot/baseconfigs"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/bios/boot/baseconfigs/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/bios/boot/settings", methods=["GET"])
def get_redfish_v1_systems_system_id_bios_boot_settings(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/bios/boot/settings
    Type: HpeServerBootSettings
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/boot/settings"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_bios_boot_settings", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/bios/boot/settings/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/bios/boot/settings", methods=["POST"])
def post_redfish_v1_systems_system_id_bios_boot_settings(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/bios/boot/settings
    Type: HpeServerBootSettings
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/boot/settings"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/bios/boot/settings/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/bios/iscsi", methods=["GET"])
def get_redfish_v1_systems_system_id_bios_iscsi(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/bios/iscsi
    Type: HpeiSCSISoftwareInitiator
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/iscsi"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_bios_iscsi", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/bios/iscsi/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/bios/iscsi", methods=["POST"])
def post_redfish_v1_systems_system_id_bios_iscsi(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/bios/iscsi
    Type: HpeiSCSISoftwareInitiator
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/iscsi"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/bios/iscsi/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/bios/iscsi/baseconfigs", methods=["GET"])
def get_redfish_v1_systems_system_id_bios_iscsi_baseconfigs(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/bios/iscsi/baseconfigs
    Type: HpeBaseConfigs
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/iscsi/baseconfigs"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_bios_iscsi_baseconfigs", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/bios/iscsi/baseconfigs/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/bios/iscsi/baseconfigs", methods=["POST"])
def post_redfish_v1_systems_system_id_bios_iscsi_baseconfigs(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/bios/iscsi/baseconfigs
    Type: HpeBaseConfigs
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/iscsi/baseconfigs"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/bios/iscsi/baseconfigs/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/bios/iscsi/settings", methods=["GET"])
def get_redfish_v1_systems_system_id_bios_iscsi_settings(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/bios/iscsi/settings
    Type: HpeiSCSISoftwareInitiator
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/iscsi/settings"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_bios_iscsi_settings", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/bios/iscsi/settings/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/bios/iscsi/settings", methods=["POST"])
def post_redfish_v1_systems_system_id_bios_iscsi_settings(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/bios/iscsi/settings
    Type: HpeiSCSISoftwareInitiator
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/iscsi/settings"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/bios/iscsi/settings/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/bios/kmsconfig", methods=["GET"])
def get_redfish_v1_systems_system_id_bios_kmsconfig(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/bios/kmsconfig
    Type: HpeKmsConfig
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/kmsconfig"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_bios_kmsconfig", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/bios/kmsconfig/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/bios/kmsconfig", methods=["POST"])
def post_redfish_v1_systems_system_id_bios_kmsconfig(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/bios/kmsconfig
    Type: HpeKmsConfig
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/kmsconfig"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/bios/kmsconfig/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/bios/kmsconfig/baseconfigs", methods=["GET"])
def get_redfish_v1_systems_system_id_bios_kmsconfig_baseconfigs(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/bios/kmsconfig/baseconfigs
    Type: HpeBaseConfigs
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/kmsconfig/baseconfigs"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_bios_kmsconfig_baseconfigs", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/bios/kmsconfig/baseconfigs/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/bios/kmsconfig/baseconfigs", methods=["POST"])
def post_redfish_v1_systems_system_id_bios_kmsconfig_baseconfigs(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/bios/kmsconfig/baseconfigs
    Type: HpeBaseConfigs
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/kmsconfig/baseconfigs"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/bios/kmsconfig/baseconfigs/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/bios/kmsconfig/settings", methods=["GET"])
def get_redfish_v1_systems_system_id_bios_kmsconfig_settings(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/bios/kmsconfig/settings
    Type: HpeKmsConfig
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/kmsconfig/settings"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_bios_kmsconfig_settings", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/bios/kmsconfig/settings/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/bios/kmsconfig/settings", methods=["POST"])
def post_redfish_v1_systems_system_id_bios_kmsconfig_settings(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/bios/kmsconfig/settings
    Type: HpeKmsConfig
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/kmsconfig/settings"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/bios/kmsconfig/settings/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/bios/mappings", methods=["GET"])
def get_redfish_v1_systems_system_id_bios_mappings(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/bios/mappings
    Type: HpeBiosMapping
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/mappings"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_bios_mappings", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/bios/mappings/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/bios/mappings", methods=["POST"])
def post_redfish_v1_systems_system_id_bios_mappings(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/bios/mappings
    Type: HpeBiosMapping
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/mappings"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/bios/mappings/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig", methods=["GET"])
def get_redfish_v1_systems_system_id_bios_oem_hpe_tlsconfig(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig
    Type: HpeTlsConfig
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_bios_oem_hpe_tlsconfig", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig", methods=["POST"])
def post_redfish_v1_systems_system_id_bios_oem_hpe_tlsconfig(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig
    Type: HpeTlsConfig
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig/baseconfigs", methods=["GET"])
def get_redfish_v1_systems_system_id_bios_oem_hpe_tlsconfig_baseconfigs(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig/baseconfigs
    Type: HpeBaseConfigs
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig/baseconfigs"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_bios_oem_hpe_tlsconfig_baseconfigs", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig/baseconfigs/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig/baseconfigs", methods=["POST"])
def post_redfish_v1_systems_system_id_bios_oem_hpe_tlsconfig_baseconfigs(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig/baseconfigs
    Type: HpeBaseConfigs
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig/baseconfigs"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig/baseconfigs/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig/settings", methods=["GET"])
def get_redfish_v1_systems_system_id_bios_oem_hpe_tlsconfig_settings(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig/settings
    Type: HpeTlsConfig
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig/settings"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_bios_oem_hpe_tlsconfig_settings", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig/settings/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig/settings", methods=["POST"])
def post_redfish_v1_systems_system_id_bios_oem_hpe_tlsconfig_settings(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig/settings
    Type: HpeTlsConfig
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig/settings"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/bios/oem/hpe/tlsconfig/settings/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/bios/serverconfiglock", methods=["GET"])
def get_redfish_v1_systems_system_id_bios_serverconfiglock(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/bios/serverconfiglock
    Type: HpeServerConfigLock
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/serverconfiglock"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_bios_serverconfiglock", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/bios/serverconfiglock/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/bios/serverconfiglock", methods=["POST"])
def post_redfish_v1_systems_system_id_bios_serverconfiglock(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/bios/serverconfiglock
    Type: HpeServerConfigLock
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/serverconfiglock"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/bios/serverconfiglock/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/bios/serverconfiglock/baseconfigs", methods=["GET"])
def get_redfish_v1_systems_system_id_bios_serverconfiglock_baseconfigs(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/bios/serverconfiglock/baseconfigs
    Type: HpeBaseConfigs
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/serverconfiglock/baseconfigs"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_bios_serverconfiglock_baseconfigs", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/bios/serverconfiglock/baseconfigs/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/bios/serverconfiglock/baseconfigs", methods=["POST"])
def post_redfish_v1_systems_system_id_bios_serverconfiglock_baseconfigs(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/bios/serverconfiglock/baseconfigs
    Type: HpeBaseConfigs
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/serverconfiglock/baseconfigs"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/bios/serverconfiglock/baseconfigs/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/bios/serverconfiglock/settings", methods=["GET"])
def get_redfish_v1_systems_system_id_bios_serverconfiglock_settings(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/bios/serverconfiglock/settings
    Type: HpeServerConfigLock
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/serverconfiglock/settings"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_bios_serverconfiglock_settings", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/bios/serverconfiglock/settings/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/bios/serverconfiglock/settings", methods=["POST"])
def post_redfish_v1_systems_system_id_bios_serverconfiglock_settings(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/bios/serverconfiglock/settings
    Type: HpeServerConfigLock
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/serverconfiglock/settings"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/bios/serverconfiglock/settings/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/bios/settings", methods=["GET"])
def get_redfish_v1_systems_system_id_bios_settings(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/bios/settings
    Type: Bios
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/settings"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_bios_settings", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/bios/settings/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/bios/settings", methods=["POST"])
def post_redfish_v1_systems_system_id_bios_settings(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/bios/settings
    Type: Bios
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bios/settings"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/bios/settings/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/bootoptions", methods=["GET"])
def get_redfish_v1_systems_system_id_bootoptions(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/bootoptions
    Type: Collection ofBootOption
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bootoptions"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_bootoptions", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/bootoptions/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/bootoptions", methods=["POST"])
def post_redfish_v1_systems_system_id_bootoptions(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/bootoptions
    Type: Collection ofBootOption
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bootoptions"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/bootoptions/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/bootoptions/{bootoption_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_bootoptions_bootoption_id(system_id: str, bootoption_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/bootoptions/{bootoption_id}
    Type: BootOption
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bootoptions"
    item = db.get_item(collection_path, bootoption_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_bootoptions_bootoption_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/bootoptions/{bootoption_id}"
            static_val["Id"] = bootoption_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/bootoptions/{bootoption_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_bootoptions_bootoption_id(system_id: str, bootoption_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/bootoptions/{bootoption_id}
    Type: BootOption
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bootoptions"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, bootoption_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_bootoptions_bootoption_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = bootoption_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/bootoptions/{bootoption_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, bootoption_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/bootoptions/{bootoption_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_bootoptions_bootoption_id(system_id: str, bootoption_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/bootoptions/{bootoption_id}
    Type: BootOption
    """
    collection_path = f"/redfish/v1/systems/{system_id}/bootoptions"
    deleted = db.delete_item(collection_path, bootoption_id)
    if deleted:
        return {"message": "Deleted successfully", "id": bootoption_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_bootoptions_bootoptget_redfish_v1_systems_system_id_bootoptions_bootoption_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": bootoption_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/ethernetinterfaces", methods=["GET"])
def get_redfish_v1_systems_system_id_ethernetinterfaces(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/ethernetinterfaces
    Type: Collection ofEthernetInterface
    """
    collection_path = f"/redfish/v1/systems/{system_id}/ethernetinterfaces"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_ethernetinterfaces", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/ethernetinterfaces/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/ethernetinterfaces", methods=["POST"])
def post_redfish_v1_systems_system_id_ethernetinterfaces(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/ethernetinterfaces
    Type: Collection ofEthernetInterface
    """
    collection_path = f"/redfish/v1/systems/{system_id}/ethernetinterfaces"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/ethernetinterfaces/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/ethernetinterfaces/{ethernetinterfac_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_ethernetinterfaces_ethernetinterfac_id(system_id: str, ethernetinterfac_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/ethernetinterfaces/{ethernetinterfac_id}
    Type: EthernetInterface
    """
    collection_path = f"/redfish/v1/systems/{system_id}/ethernetinterfaces"
    item = db.get_item(collection_path, ethernetinterfac_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_ethernetinterfaces_ethernetinterfac_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/ethernetinterfaces/{ethernetinterfac_id}"
            static_val["Id"] = ethernetinterfac_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/ethernetinterfaces/{ethernetinterfac_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_ethernetinterfaces_ethernetinterfac_id(system_id: str, ethernetinterfac_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/ethernetinterfaces/{ethernetinterfac_id}
    Type: EthernetInterface
    """
    collection_path = f"/redfish/v1/systems/{system_id}/ethernetinterfaces"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, ethernetinterfac_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_ethernetinterfaces_ethernetinterfac_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = ethernetinterfac_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/ethernetinterfaces/{ethernetinterfac_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, ethernetinterfac_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/ethernetinterfaces/{ethernetinterfac_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_ethernetinterfaces_ethernetinterfac_id(system_id: str, ethernetinterfac_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/ethernetinterfaces/{ethernetinterfac_id}
    Type: EthernetInterface
    """
    collection_path = f"/redfish/v1/systems/{system_id}/ethernetinterfaces"
    deleted = db.delete_item(collection_path, ethernetinterfac_id)
    if deleted:
        return {"message": "Deleted successfully", "id": ethernetinterfac_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_ethernetinterfaces_ethernetinterget_redfish_v1_systems_system_id_ethernetinterfaces_ethernetinterfac_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": ethernetinterfac_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/keymanagement/KMIPcertificates", methods=["GET"])
def get_redfish_v1_systems_system_id_keymanagement_kmipcertificates(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/keymanagement/KMIPcertificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/systems/{system_id}/keymanagement/KMIPcertificates"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_keymanagement_kmipcertificates", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/keymanagement/KMIPcertificates/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/keymanagement/KMIPcertificates", methods=["POST"])
def post_redfish_v1_systems_system_id_keymanagement_kmipcertificates(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/keymanagement/KMIPcertificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/systems/{system_id}/keymanagement/KMIPcertificates"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/keymanagement/KMIPcertificates/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/keymanagement/KMIPcertificates/{kmipcertificat_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_keymanagement_kmipcertificates_kmipcertificat_id(system_id: str, kmipcertificat_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/keymanagement/KMIPcertificates/{kmipcertificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/keymanagement/KMIPcertificates"
    item = db.get_item(collection_path, kmipcertificat_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_keymanagement_kmipcertificates_kmipcertificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/keymanagement/KMIPcertificates/{kmipcertificat_id}"
            static_val["Id"] = kmipcertificat_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/keymanagement/KMIPcertificates/{kmipcertificat_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_keymanagement_kmipcertificates_kmipcertificat_id(system_id: str, kmipcertificat_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/keymanagement/KMIPcertificates/{kmipcertificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/keymanagement/KMIPcertificates"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, kmipcertificat_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_keymanagement_kmipcertificates_kmipcertificat_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = kmipcertificat_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/keymanagement/KMIPcertificates/{kmipcertificat_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, kmipcertificat_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/keymanagement/KMIPcertificates/{kmipcertificat_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_keymanagement_kmipcertificates_kmipcertificat_id(system_id: str, kmipcertificat_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/keymanagement/KMIPcertificates/{kmipcertificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/keymanagement/KMIPcertificates"
    deleted = db.delete_item(collection_path, kmipcertificat_id)
    if deleted:
        return {"message": "Deleted successfully", "id": kmipcertificat_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_keymanagement_kmipcertificates_kmipcertifiget_redfish_v1_systems_system_id_keymanagement_kmipcertificates_kmipcertificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": kmipcertificat_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/keymanagement/KMIPclientcertificates", methods=["GET"])
def get_redfish_v1_systems_system_id_keymanagement_kmipclientcertificates(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/keymanagement/KMIPclientcertificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/systems/{system_id}/keymanagement/KMIPclientcertificates"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_keymanagement_kmipclientcertificates", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/keymanagement/KMIPclientcertificates/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/keymanagement/KMIPclientcertificates", methods=["POST"])
def post_redfish_v1_systems_system_id_keymanagement_kmipclientcertificates(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/keymanagement/KMIPclientcertificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/systems/{system_id}/keymanagement/KMIPclientcertificates"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/keymanagement/KMIPclientcertificates/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/keymanagement/KMIPclientcertificates/{kmipclientcertificat_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_keymanagement_kmipclientcertificates_kmipclientcertificat_id(system_id: str, kmipclientcertificat_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/keymanagement/KMIPclientcertificates/{kmipclientcertificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/keymanagement/KMIPclientcertificates"
    item = db.get_item(collection_path, kmipclientcertificat_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_keymanagement_kmipclientcertificates_kmipclientcertificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/keymanagement/KMIPclientcertificates/{kmipclientcertificat_id}"
            static_val["Id"] = kmipclientcertificat_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/keymanagement/KMIPclientcertificates/{kmipclientcertificat_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_keymanagement_kmipclientcertificates_kmipclientcertificat_id(system_id: str, kmipclientcertificat_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/keymanagement/KMIPclientcertificates/{kmipclientcertificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/keymanagement/KMIPclientcertificates"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, kmipclientcertificat_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_keymanagement_kmipclientcertificates_kmipclientcertificat_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = kmipclientcertificat_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/keymanagement/KMIPclientcertificates/{kmipclientcertificat_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, kmipclientcertificat_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/keymanagement/KMIPclientcertificates/{kmipclientcertificat_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_keymanagement_kmipclientcertificates_kmipclientcertificat_id(system_id: str, kmipclientcertificat_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/keymanagement/KMIPclientcertificates/{kmipclientcertificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/keymanagement/KMIPclientcertificates"
    deleted = db.delete_item(collection_path, kmipclientcertificat_id)
    if deleted:
        return {"message": "Deleted successfully", "id": kmipclientcertificat_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_keymanagement_kmipclientcertificates_kmipclientcertifiget_redfish_v1_systems_system_id_keymanagement_kmipclientcertificates_kmipclientcertificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": kmipclientcertificat_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/logservices", methods=["GET"])
def get_redfish_v1_systems_system_id_logservices(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/logservices
    Type: Collection ofLogService
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_logservices", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/logservices/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/logservices", methods=["POST"])
def post_redfish_v1_systems_system_id_logservices(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/logservices
    Type: Collection ofLogService
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/logservices/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/logservices/dpu", methods=["GET"])
def get_redfish_v1_systems_system_id_logservices_dpu(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/logservices/dpu
    Type: LogService
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/dpu"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_logservices_dpu", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/logservices/dpu/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/logservices/dpu", methods=["POST"])
def post_redfish_v1_systems_system_id_logservices_dpu(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/logservices/dpu
    Type: LogService
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/dpu"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/logservices/dpu/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/logservices/dpu/entries", methods=["GET"])
def get_redfish_v1_systems_system_id_logservices_dpu_entries(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/logservices/dpu/entries
    Type: Collection ofLogEntry
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/dpu/entries"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_logservices_dpu_entries", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/logservices/dpu/entries/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/logservices/dpu/entries", methods=["POST"])
def post_redfish_v1_systems_system_id_logservices_dpu_entries(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/logservices/dpu/entries
    Type: Collection ofLogEntry
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/dpu/entries"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/logservices/dpu/entries/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/logservices/dpu/entries/{entry_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_logservices_dpu_entries_entry_id(system_id: str, entry_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/logservices/dpu/entries/{entry_id}
    Type: LogEntry
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/dpu/entries"
    item = db.get_item(collection_path, entry_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_logservices_dpu_entries_entry_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/logservices/dpu/entries/{entry_id}"
            static_val["Id"] = entry_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/logservices/dpu/entries/{entry_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_logservices_dpu_entries_entry_id(system_id: str, entry_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/logservices/dpu/entries/{entry_id}
    Type: LogEntry
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/dpu/entries"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, entry_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_logservices_dpu_entries_entry_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = entry_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/logservices/dpu/entries/{entry_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, entry_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/logservices/dpu/entries/{entry_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_logservices_dpu_entries_entry_id(system_id: str, entry_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/logservices/dpu/entries/{entry_id}
    Type: LogEntry
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/dpu/entries"
    deleted = db.delete_item(collection_path, entry_id)
    if deleted:
        return {"message": "Deleted successfully", "id": entry_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_logservices_dpu_entries_enget_redfish_v1_systems_system_id_logservices_dpu_entries_entry_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": entry_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/logservices/event", methods=["GET"])
def get_redfish_v1_systems_system_id_logservices_event(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/logservices/event
    Type: LogService
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/event"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_logservices_event", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/logservices/event/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/logservices/event", methods=["POST"])
def post_redfish_v1_systems_system_id_logservices_event(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/logservices/event
    Type: LogService
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/event"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/logservices/event/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/logservices/event/entries", methods=["GET"])
def get_redfish_v1_systems_system_id_logservices_event_entries(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/logservices/event/entries
    Type: Collection ofLogEntry
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/event/entries"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_logservices_event_entries", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/logservices/event/entries/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/logservices/event/entries", methods=["POST"])
def post_redfish_v1_systems_system_id_logservices_event_entries(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/logservices/event/entries
    Type: Collection ofLogEntry
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/event/entries"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/logservices/event/entries/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/logservices/event/entries/{entry_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_logservices_event_entries_entry_id(system_id: str, entry_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/logservices/event/entries/{entry_id}
    Type: LogEntry
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/event/entries"
    item = db.get_item(collection_path, entry_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_logservices_event_entries_entry_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/logservices/event/entries/{entry_id}"
            static_val["Id"] = entry_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/logservices/event/entries/{entry_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_logservices_event_entries_entry_id(system_id: str, entry_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/logservices/event/entries/{entry_id}
    Type: LogEntry
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/event/entries"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, entry_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_logservices_event_entries_entry_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = entry_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/logservices/event/entries/{entry_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, entry_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/logservices/event/entries/{entry_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_logservices_event_entries_entry_id(system_id: str, entry_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/logservices/event/entries/{entry_id}
    Type: LogEntry
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/event/entries"
    deleted = db.delete_item(collection_path, entry_id)
    if deleted:
        return {"message": "Deleted successfully", "id": entry_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_logservices_event_entries_enget_redfish_v1_systems_system_id_logservices_event_entries_entry_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": entry_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/logservices/iml", methods=["GET"])
def get_redfish_v1_systems_system_id_logservices_iml(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/logservices/iml
    Type: LogService
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/iml"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_logservices_iml", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/logservices/iml/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/logservices/iml", methods=["POST"])
def post_redfish_v1_systems_system_id_logservices_iml(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/logservices/iml
    Type: LogService
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/iml"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/logservices/iml/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/logservices/iml/entries", methods=["GET"])
def get_redfish_v1_systems_system_id_logservices_iml_entries(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/logservices/iml/entries
    Type: Collection ofLogEntry
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/iml/entries"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_logservices_iml_entries", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/logservices/iml/entries/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/logservices/iml/entries", methods=["POST"])
def post_redfish_v1_systems_system_id_logservices_iml_entries(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/logservices/iml/entries
    Type: Collection ofLogEntry
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/iml/entries"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/logservices/iml/entries/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/logservices/iml/entries/{entry_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_logservices_iml_entries_entry_id(system_id: str, entry_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/logservices/iml/entries/{entry_id}
    Type: LogEntry
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/iml/entries"
    item = db.get_item(collection_path, entry_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_logservices_iml_entries_entry_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/logservices/iml/entries/{entry_id}"
            static_val["Id"] = entry_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/logservices/iml/entries/{entry_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_logservices_iml_entries_entry_id(system_id: str, entry_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/logservices/iml/entries/{entry_id}
    Type: LogEntry
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/iml/entries"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, entry_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_logservices_iml_entries_entry_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = entry_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/logservices/iml/entries/{entry_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, entry_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/logservices/iml/entries/{entry_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_logservices_iml_entries_entry_id(system_id: str, entry_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/logservices/iml/entries/{entry_id}
    Type: LogEntry
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/iml/entries"
    deleted = db.delete_item(collection_path, entry_id)
    if deleted:
        return {"message": "Deleted successfully", "id": entry_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_logservices_iml_entries_enget_redfish_v1_systems_system_id_logservices_iml_entries_entry_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": entry_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/logservices/sl", methods=["GET"])
def get_redfish_v1_systems_system_id_logservices_sl(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/logservices/sl
    Type: LogService
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/sl"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_logservices_sl", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/logservices/sl/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/logservices/sl", methods=["POST"])
def post_redfish_v1_systems_system_id_logservices_sl(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/logservices/sl
    Type: LogService
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/sl"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/logservices/sl/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/logservices/sl/entries", methods=["GET"])
def get_redfish_v1_systems_system_id_logservices_sl_entries(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/logservices/sl/entries
    Type: Collection ofLogEntry
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/sl/entries"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_logservices_sl_entries", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/logservices/sl/entries/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/logservices/sl/entries", methods=["POST"])
def post_redfish_v1_systems_system_id_logservices_sl_entries(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/logservices/sl/entries
    Type: Collection ofLogEntry
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/sl/entries"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/logservices/sl/entries/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/logservices/sl/entries/{entry_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_logservices_sl_entries_entry_id(system_id: str, entry_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/logservices/sl/entries/{entry_id}
    Type: LogEntry
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/sl/entries"
    item = db.get_item(collection_path, entry_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_logservices_sl_entries_entry_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/logservices/sl/entries/{entry_id}"
            static_val["Id"] = entry_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/logservices/sl/entries/{entry_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_logservices_sl_entries_entry_id(system_id: str, entry_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/logservices/sl/entries/{entry_id}
    Type: LogEntry
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/sl/entries"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, entry_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_logservices_sl_entries_entry_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = entry_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/logservices/sl/entries/{entry_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, entry_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/logservices/sl/entries/{entry_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_logservices_sl_entries_entry_id(system_id: str, entry_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/logservices/sl/entries/{entry_id}
    Type: LogEntry
    """
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/sl/entries"
    deleted = db.delete_item(collection_path, entry_id)
    if deleted:
        return {"message": "Deleted successfully", "id": entry_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_logservices_sl_entries_enget_redfish_v1_systems_system_id_logservices_sl_entries_entry_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": entry_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/memory", methods=["GET"])
def get_redfish_v1_systems_system_id_memory(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/memory
    Type: Collection ofMemory
    """
    collection_path = f"/redfish/v1/systems/{system_id}/memory"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_memory", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/memory/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/memory", methods=["POST"])
def post_redfish_v1_systems_system_id_memory(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/memory
    Type: Collection ofMemory
    """
    collection_path = f"/redfish/v1/systems/{system_id}/memory"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/memory/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/memory/{memory_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_memory_memory_id(system_id: str, memory_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/memory/{memory_id}
    Type: Memory
    """
    collection_path = f"/redfish/v1/systems/{system_id}/memory"
    item = db.get_item(collection_path, memory_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_memory_memory_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/memory/{memory_id}"
            static_val["Id"] = memory_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/memory/{memory_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_memory_memory_id(system_id: str, memory_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/memory/{memory_id}
    Type: Memory
    """
    collection_path = f"/redfish/v1/systems/{system_id}/memory"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, memory_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_memory_memory_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = memory_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/memory/{memory_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, memory_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/memory/{memory_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_memory_memory_id(system_id: str, memory_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/memory/{memory_id}
    Type: Memory
    """
    collection_path = f"/redfish/v1/systems/{system_id}/memory"
    deleted = db.delete_item(collection_path, memory_id)
    if deleted:
        return {"message": "Deleted successfully", "id": memory_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_memory_memget_redfish_v1_systems_system_id_memory_memory_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": memory_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/memory/{memory_id}/memorymetrics", methods=["GET"])
def get_redfish_v1_systems_system_id_memory_memory_id_memorymetrics(system_id: str, memory_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/memory/{memory_id}/memorymetrics
    Type: MemoryMetrics
    """
    collection_path = f"/redfish/v1/systems/{system_id}/memory/{memory_id}/memorymetrics"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_memory_memory_id_memorymetrics", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/memory/{memory_id}/memorymetrics/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/memory/{memory_id}/memorymetrics", methods=["POST"])
def post_redfish_v1_systems_system_id_memory_memory_id_memorymetrics(system_id: str, memory_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/memory/{memory_id}/memorymetrics
    Type: MemoryMetrics
    """
    collection_path = f"/redfish/v1/systems/{system_id}/memory/{memory_id}/memorymetrics"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/memory/{memory_id}/memorymetrics/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/memorydomains", methods=["GET"])
def get_redfish_v1_systems_system_id_memorydomains(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/memorydomains
    Type: Collection ofMemoryDomain
    """
    collection_path = f"/redfish/v1/systems/{system_id}/memorydomains"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_memorydomains", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/memorydomains/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/memorydomains", methods=["POST"])
def post_redfish_v1_systems_system_id_memorydomains(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/memorydomains
    Type: Collection ofMemoryDomain
    """
    collection_path = f"/redfish/v1/systems/{system_id}/memorydomains"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/memorydomains/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_memorydomains_memorydomain_id(system_id: str, memorydomain_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}
    Type: MemoryDomain
    """
    collection_path = f"/redfish/v1/systems/{system_id}/memorydomains"
    item = db.get_item(collection_path, memorydomain_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_memorydomains_memorydomain_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}"
            static_val["Id"] = memorydomain_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_memorydomains_memorydomain_id(system_id: str, memorydomain_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}
    Type: MemoryDomain
    """
    collection_path = f"/redfish/v1/systems/{system_id}/memorydomains"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, memorydomain_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_memorydomains_memorydomain_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = memorydomain_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, memorydomain_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_memorydomains_memorydomain_id(system_id: str, memorydomain_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}
    Type: MemoryDomain
    """
    collection_path = f"/redfish/v1/systems/{system_id}/memorydomains"
    deleted = db.delete_item(collection_path, memorydomain_id)
    if deleted:
        return {"message": "Deleted successfully", "id": memorydomain_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_memorydomains_memorydomget_redfish_v1_systems_system_id_memorydomains_memorydomain_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": memorydomain_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}/memorychunks", methods=["GET"])
def get_redfish_v1_systems_system_id_memorydomains_memorydomain_id_memorychunks(system_id: str, memorydomain_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}/memorychunks
    Type: Collection ofMemoryChunks
    """
    collection_path = f"/redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}/memorychunks"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_memorydomains_memorydomain_id_memorychunks", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}/memorychunks/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}/memorychunks", methods=["POST"])
def post_redfish_v1_systems_system_id_memorydomains_memorydomain_id_memorychunks(system_id: str, memorydomain_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}/memorychunks
    Type: Collection ofMemoryChunks
    """
    collection_path = f"/redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}/memorychunks"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}/memorychunks/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}/memorychunks/{memorychunk_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_memorydomains_memorydomain_id_memorychunks_memorychunk_id(system_id: str, memorydomain_id: str, memorychunk_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}/memorychunks/{memorychunk_id}
    Type: MemoryChunks
    """
    collection_path = f"/redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}/memorychunks"
    item = db.get_item(collection_path, memorychunk_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_memorydomains_memorydomain_id_memorychunks_memorychunk_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}/memorychunks/{memorychunk_id}"
            static_val["Id"] = memorychunk_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}/memorychunks/{memorychunk_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_memorydomains_memorydomain_id_memorychunks_memorychunk_id(system_id: str, memorydomain_id: str, memorychunk_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}/memorychunks/{memorychunk_id}
    Type: MemoryChunks
    """
    collection_path = f"/redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}/memorychunks"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, memorychunk_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_memorydomains_memorydomain_id_memorychunks_memorychunk_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = memorychunk_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}/memorychunks/{memorychunk_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, memorychunk_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}/memorychunks/{memorychunk_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_memorydomains_memorydomain_id_memorychunks_memorychunk_id(system_id: str, memorydomain_id: str, memorychunk_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}/memorychunks/{memorychunk_id}
    Type: MemoryChunks
    """
    collection_path = f"/redfish/v1/systems/{system_id}/memorydomains/{memorydomain_id}/memorychunks"
    deleted = db.delete_item(collection_path, memorychunk_id)
    if deleted:
        return {"message": "Deleted successfully", "id": memorychunk_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_memorydomains_memorydomain_id_memorychunks_memorychget_redfish_v1_systems_system_id_memorydomains_memorydomain_id_memorychunks_memorychunk_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": memorychunk_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/networkinterfaces", methods=["GET"])
def get_redfish_v1_systems_system_id_networkinterfaces(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/networkinterfaces
    Type: Collection ofNetworkInterface
    """
    collection_path = f"/redfish/v1/systems/{system_id}/networkinterfaces"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_networkinterfaces", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/networkinterfaces/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/networkinterfaces", methods=["POST"])
def post_redfish_v1_systems_system_id_networkinterfaces(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/networkinterfaces
    Type: Collection ofNetworkInterface
    """
    collection_path = f"/redfish/v1/systems/{system_id}/networkinterfaces"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/networkinterfaces/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id(system_id: str, networkinterfac_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}
    Type: NetworkInterface
    """
    collection_path = f"/redfish/v1/systems/{system_id}/networkinterfaces"
    item = db.get_item(collection_path, networkinterfac_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}"
            static_val["Id"] = networkinterfac_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id(system_id: str, networkinterfac_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}
    Type: NetworkInterface
    """
    collection_path = f"/redfish/v1/systems/{system_id}/networkinterfaces"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, networkinterfac_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = networkinterfac_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, networkinterfac_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id(system_id: str, networkinterfac_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}
    Type: NetworkInterface
    """
    collection_path = f"/redfish/v1/systems/{system_id}/networkinterfaces"
    deleted = db.delete_item(collection_path, networkinterfac_id)
    if deleted:
        return {"message": "Deleted successfully", "id": networkinterfac_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_networkinterfaces_networkinterget_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": networkinterfac_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions", methods=["GET"])
def get_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id_networkdevicefunctions(system_id: str, networkinterfac_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions
    Type: Collection ofNetworkDeviceFunction
    """
    collection_path = f"/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id_networkdevicefunctions", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions", methods=["POST"])
def post_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id_networkdevicefunctions(system_id: str, networkinterfac_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions
    Type: Collection ofNetworkDeviceFunction
    """
    collection_path = f"/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions/{networkdevicefunction_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id_networkdevicefunctions_networkdevicefunction_id(system_id: str, networkinterfac_id: str, networkdevicefunction_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions/{networkdevicefunction_id}
    Type: NetworkDeviceFunction
    """
    collection_path = f"/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions"
    item = db.get_item(collection_path, networkdevicefunction_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id_networkdevicefunctions_networkdevicefunction_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions/{networkdevicefunction_id}"
            static_val["Id"] = networkdevicefunction_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions/{networkdevicefunction_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id_networkdevicefunctions_networkdevicefunction_id(system_id: str, networkinterfac_id: str, networkdevicefunction_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions/{networkdevicefunction_id}
    Type: NetworkDeviceFunction
    """
    collection_path = f"/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, networkdevicefunction_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id_networkdevicefunctions_networkdevicefunction_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = networkdevicefunction_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions/{networkdevicefunction_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, networkdevicefunction_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions/{networkdevicefunction_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id_networkdevicefunctions_networkdevicefunction_id(system_id: str, networkinterfac_id: str, networkdevicefunction_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions/{networkdevicefunction_id}
    Type: NetworkDeviceFunction
    """
    collection_path = f"/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions"
    deleted = db.delete_item(collection_path, networkdevicefunction_id)
    if deleted:
        return {"message": "Deleted successfully", "id": networkdevicefunction_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id_networkdevicefunctions_networkdevicefunctget_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id_networkdevicefunctions_networkdevicefunction_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": networkdevicefunction_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions/{networkdevicefunction_id}/settings", methods=["GET"])
def get_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id_networkdevicefunctions_networkdevicefunction_id_settings(system_id: str, networkinterfac_id: str, networkdevicefunction_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions/{networkdevicefunction_id}/settings
    Type: NetworkDeviceFunction
    """
    collection_path = f"/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions/{networkdevicefunction_id}/settings"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id_networkdevicefunctions_networkdevicefunction_id_settings", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions/{networkdevicefunction_id}/settings/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions/{networkdevicefunction_id}/settings", methods=["POST"])
def post_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id_networkdevicefunctions_networkdevicefunction_id_settings(system_id: str, networkinterfac_id: str, networkdevicefunction_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions/{networkdevicefunction_id}/settings
    Type: NetworkDeviceFunction
    """
    collection_path = f"/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions/{networkdevicefunction_id}/settings"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/networkdevicefunctions/{networkdevicefunction_id}/settings/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports", methods=["GET"])
def get_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id_ports(system_id: str, networkinterfac_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports
    Type: Collection ofPort
    """
    collection_path = f"/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id_ports", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports", methods=["POST"])
def post_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id_ports(system_id: str, networkinterfac_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports
    Type: Collection ofPort
    """
    collection_path = f"/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports/{port_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id_ports_port_id(system_id: str, networkinterfac_id: str, port_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports/{port_id}
    Type: Port
    """
    collection_path = f"/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports"
    item = db.get_item(collection_path, port_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id_ports_port_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports/{port_id}"
            static_val["Id"] = port_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports/{port_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id_ports_port_id(system_id: str, networkinterfac_id: str, port_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports/{port_id}
    Type: Port
    """
    collection_path = f"/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, port_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id_ports_port_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = port_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports/{port_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, port_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports/{port_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id_ports_port_id(system_id: str, networkinterfac_id: str, port_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports/{port_id}
    Type: Port
    """
    collection_path = f"/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports"
    deleted = db.delete_item(collection_path, port_id)
    if deleted:
        return {"message": "Deleted successfully", "id": port_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id_ports_pget_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id_ports_port_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": port_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports/{port_id}/settings", methods=["GET"])
def get_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id_ports_port_id_settings(system_id: str, networkinterfac_id: str, port_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports/{port_id}/settings
    Type: Port
    """
    collection_path = f"/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports/{port_id}/settings"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id_ports_port_id_settings", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports/{port_id}/settings/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports/{port_id}/settings", methods=["POST"])
def post_redfish_v1_systems_system_id_networkinterfaces_networkinterfac_id_ports_port_id_settings(system_id: str, networkinterfac_id: str, port_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports/{port_id}/settings
    Type: Port
    """
    collection_path = f"/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports/{port_id}/settings"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/networkinterfaces/{networkinterfac_id}/ports/{port_id}/settings/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/pcidevices", methods=["GET"])
def get_redfish_v1_systems_system_id_pcidevices(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/pcidevices
    Type: Collection ofHpeServerPciDevice
    """
    collection_path = f"/redfish/v1/systems/{system_id}/pcidevices"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_pcidevices", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/pcidevices/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/pcidevices", methods=["POST"])
def post_redfish_v1_systems_system_id_pcidevices(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/pcidevices
    Type: Collection ofHpeServerPciDevice
    """
    collection_path = f"/redfish/v1/systems/{system_id}/pcidevices"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/pcidevices/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/pcidevices/{pcidevic_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_pcidevices_pcidevic_id(system_id: str, pcidevic_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/pcidevices/{pcidevic_id}
    Type: HpeServerPciDevice
    """
    collection_path = f"/redfish/v1/systems/{system_id}/pcidevices"
    item = db.get_item(collection_path, pcidevic_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_pcidevices_pcidevic_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/pcidevices/{pcidevic_id}"
            static_val["Id"] = pcidevic_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/pcidevices/{pcidevic_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_pcidevices_pcidevic_id(system_id: str, pcidevic_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/pcidevices/{pcidevic_id}
    Type: HpeServerPciDevice
    """
    collection_path = f"/redfish/v1/systems/{system_id}/pcidevices"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, pcidevic_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_pcidevices_pcidevic_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = pcidevic_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/pcidevices/{pcidevic_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, pcidevic_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/pcidevices/{pcidevic_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_pcidevices_pcidevic_id(system_id: str, pcidevic_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/pcidevices/{pcidevic_id}
    Type: HpeServerPciDevice
    """
    collection_path = f"/redfish/v1/systems/{system_id}/pcidevices"
    deleted = db.delete_item(collection_path, pcidevic_id)
    if deleted:
        return {"message": "Deleted successfully", "id": pcidevic_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_pcidevices_pcideget_redfish_v1_systems_system_id_pcidevices_pcidevic_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": pcidevic_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/pcislots", methods=["GET"])
def get_redfish_v1_systems_system_id_pcislots(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/pcislots
    Type: Collection ofHpeServerPCISlot
    """
    collection_path = f"/redfish/v1/systems/{system_id}/pcislots"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_pcislots", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/pcislots/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/pcislots", methods=["POST"])
def post_redfish_v1_systems_system_id_pcislots(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/pcislots
    Type: Collection ofHpeServerPCISlot
    """
    collection_path = f"/redfish/v1/systems/{system_id}/pcislots"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/pcislots/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/pcislots/{pcislot_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_pcislots_pcislot_id(system_id: str, pcislot_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/pcislots/{pcislot_id}
    Type: HpeServerPCISlot
    """
    collection_path = f"/redfish/v1/systems/{system_id}/pcislots"
    item = db.get_item(collection_path, pcislot_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_pcislots_pcislot_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/pcislots/{pcislot_id}"
            static_val["Id"] = pcislot_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/pcislots/{pcislot_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_pcislots_pcislot_id(system_id: str, pcislot_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/pcislots/{pcislot_id}
    Type: HpeServerPCISlot
    """
    collection_path = f"/redfish/v1/systems/{system_id}/pcislots"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, pcislot_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_pcislots_pcislot_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = pcislot_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/pcislots/{pcislot_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, pcislot_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/pcislots/{pcislot_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_pcislots_pcislot_id(system_id: str, pcislot_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/pcislots/{pcislot_id}
    Type: HpeServerPCISlot
    """
    collection_path = f"/redfish/v1/systems/{system_id}/pcislots"
    deleted = db.delete_item(collection_path, pcislot_id)
    if deleted:
        return {"message": "Deleted successfully", "id": pcislot_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_pcislots_pcisget_redfish_v1_systems_system_id_pcislots_pcislot_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": pcislot_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/processors", methods=["GET"])
def get_redfish_v1_systems_system_id_processors(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/processors
    Type: Collection ofProcessor
    """
    collection_path = f"/redfish/v1/systems/{system_id}/processors"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_processors", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/processors/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/processors", methods=["POST"])
def post_redfish_v1_systems_system_id_processors(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/processors
    Type: Collection ofProcessor
    """
    collection_path = f"/redfish/v1/systems/{system_id}/processors"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/processors/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/processors/{processor_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_processors_processor_id(system_id: str, processor_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/processors/{processor_id}
    Type: Processor
    """
    collection_path = f"/redfish/v1/systems/{system_id}/processors"
    item = db.get_item(collection_path, processor_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_processors_processor_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/processors/{processor_id}"
            static_val["Id"] = processor_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/processors/{processor_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_processors_processor_id(system_id: str, processor_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/processors/{processor_id}
    Type: Processor
    """
    collection_path = f"/redfish/v1/systems/{system_id}/processors"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, processor_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_processors_processor_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = processor_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/processors/{processor_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, processor_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/processors/{processor_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_processors_processor_id(system_id: str, processor_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/processors/{processor_id}
    Type: Processor
    """
    collection_path = f"/redfish/v1/systems/{system_id}/processors"
    deleted = db.delete_item(collection_path, processor_id)
    if deleted:
        return {"message": "Deleted successfully", "id": processor_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_processors_procesget_redfish_v1_systems_system_id_processors_processor_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": processor_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/processors/{processor_id}/environmentmetrics", methods=["GET"])
def get_redfish_v1_systems_system_id_processors_processor_id_environmentmetrics(system_id: str, processor_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/processors/{processor_id}/environmentmetrics
    Type: EnvironmentMetrics
    """
    collection_path = f"/redfish/v1/systems/{system_id}/processors/{processor_id}/environmentmetrics"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_processors_processor_id_environmentmetrics", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/processors/{processor_id}/environmentmetrics/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/processors/{processor_id}/environmentmetrics", methods=["POST"])
def post_redfish_v1_systems_system_id_processors_processor_id_environmentmetrics(system_id: str, processor_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/processors/{processor_id}/environmentmetrics
    Type: EnvironmentMetrics
    """
    collection_path = f"/redfish/v1/systems/{system_id}/processors/{processor_id}/environmentmetrics"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/processors/{processor_id}/environmentmetrics/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/processors/{processor_id}/processormetrics", methods=["GET"])
def get_redfish_v1_systems_system_id_processors_processor_id_processormetrics(system_id: str, processor_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/processors/{processor_id}/processormetrics
    Type: ProcessorMetrics
    """
    collection_path = f"/redfish/v1/systems/{system_id}/processors/{processor_id}/processormetrics"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_processors_processor_id_processormetrics", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/processors/{processor_id}/processormetrics/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/processors/{processor_id}/processormetrics", methods=["POST"])
def post_redfish_v1_systems_system_id_processors_processor_id_processormetrics(system_id: str, processor_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/processors/{processor_id}/processormetrics
    Type: ProcessorMetrics
    """
    collection_path = f"/redfish/v1/systems/{system_id}/processors/{processor_id}/processormetrics"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/processors/{processor_id}/processormetrics/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot
    Type: SecureBoot
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot
    Type: SecureBoot
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases
    Type: Collection ofSecureBootDatabase
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases
    Type: Collection ofSecureBootDatabase
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_db(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db
    Type: SecureBootDatabase
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_db", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_db(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db
    Type: SecureBootDatabase
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/certificates", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_db_certificates(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/certificates"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_db_certificates", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/certificates/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/certificates", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_db_certificates(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/certificates"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/certificates/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/certificates/{certificat_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_db_certificates_certificat_id(system_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/certificates"
    item = db.get_item(collection_path, certificat_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_db_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/certificates/{certificat_id}"
            static_val["Id"] = certificat_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/certificates/{certificat_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_db_certificates_certificat_id(system_id: str, certificat_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/certificates"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, certificat_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_db_certificates_certificat_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = certificat_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/certificates/{certificat_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, certificat_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/certificates/{certificat_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_db_certificates_certificat_id(system_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/certificates"
    deleted = db.delete_item(collection_path, certificat_id)
    if deleted:
        return {"message": "Deleted successfully", "id": certificat_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_db_certificates_certifiget_redfish_v1_systems_system_id_secureboot_securebootdatabases_db_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": certificat_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/signatures", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_db_signatures(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/signatures
    Type: Collection ofSignature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/signatures"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_db_signatures", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/signatures/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/signatures", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_db_signatures(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/signatures
    Type: Collection ofSignature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/signatures"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/signatures/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/signatures/{signatur_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_db_signatures_signatur_id(system_id: str, signatur_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/signatures/{signatur_id}
    Type: Signature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/signatures"
    item = db.get_item(collection_path, signatur_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_db_signatures_signatur_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/signatures/{signatur_id}"
            static_val["Id"] = signatur_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/signatures/{signatur_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_db_signatures_signatur_id(system_id: str, signatur_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/signatures/{signatur_id}
    Type: Signature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/signatures"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, signatur_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_db_signatures_signatur_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = signatur_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/signatures/{signatur_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, signatur_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/signatures/{signatur_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_db_signatures_signatur_id(system_id: str, signatur_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/signatures/{signatur_id}
    Type: Signature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/db/signatures"
    deleted = db.delete_item(collection_path, signatur_id)
    if deleted:
        return {"message": "Deleted successfully", "id": signatur_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_db_signatures_signaget_redfish_v1_systems_system_id_secureboot_securebootdatabases_db_signatures_signatur_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": signatur_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbdefault(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault
    Type: SecureBootDatabase
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbdefault", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbdefault(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault
    Type: SecureBootDatabase
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/certificates", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbdefault_certificates(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/certificates"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbdefault_certificates", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/certificates/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/certificates", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbdefault_certificates(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/certificates"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/certificates/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/certificates/{certificat_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbdefault_certificates_certificat_id(system_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/certificates"
    item = db.get_item(collection_path, certificat_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbdefault_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/certificates/{certificat_id}"
            static_val["Id"] = certificat_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/certificates/{certificat_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbdefault_certificates_certificat_id(system_id: str, certificat_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/certificates"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, certificat_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbdefault_certificates_certificat_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = certificat_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/certificates/{certificat_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, certificat_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/certificates/{certificat_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbdefault_certificates_certificat_id(system_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/certificates"
    deleted = db.delete_item(collection_path, certificat_id)
    if deleted:
        return {"message": "Deleted successfully", "id": certificat_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbdefault_certificates_certifiget_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbdefault_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": certificat_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/signatures", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbdefault_signatures(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/signatures
    Type: Collection ofSignature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/signatures"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbdefault_signatures", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/signatures/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/signatures", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbdefault_signatures(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/signatures
    Type: Collection ofSignature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/signatures"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/signatures/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/signatures/{signatur_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbdefault_signatures_signatur_id(system_id: str, signatur_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/signatures/{signatur_id}
    Type: Signature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/signatures"
    item = db.get_item(collection_path, signatur_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbdefault_signatures_signatur_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/signatures/{signatur_id}"
            static_val["Id"] = signatur_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/signatures/{signatur_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbdefault_signatures_signatur_id(system_id: str, signatur_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/signatures/{signatur_id}
    Type: Signature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/signatures"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, signatur_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbdefault_signatures_signatur_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = signatur_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/signatures/{signatur_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, signatur_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/signatures/{signatur_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbdefault_signatures_signatur_id(system_id: str, signatur_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/signatures/{signatur_id}
    Type: Signature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbdefault/signatures"
    deleted = db.delete_item(collection_path, signatur_id)
    if deleted:
        return {"message": "Deleted successfully", "id": signatur_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbdefault_signatures_signaget_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbdefault_signatures_signatur_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": signatur_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbr(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr
    Type: SecureBootDatabase
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbr", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbr(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr
    Type: SecureBootDatabase
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/certificates", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbr_certificates(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/certificates"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbr_certificates", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/certificates/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/certificates", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbr_certificates(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/certificates"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/certificates/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/certificates/{certificat_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbr_certificates_certificat_id(system_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/certificates"
    item = db.get_item(collection_path, certificat_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbr_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/certificates/{certificat_id}"
            static_val["Id"] = certificat_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/certificates/{certificat_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbr_certificates_certificat_id(system_id: str, certificat_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/certificates"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, certificat_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbr_certificates_certificat_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = certificat_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/certificates/{certificat_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, certificat_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/certificates/{certificat_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbr_certificates_certificat_id(system_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/certificates"
    deleted = db.delete_item(collection_path, certificat_id)
    if deleted:
        return {"message": "Deleted successfully", "id": certificat_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbr_certificates_certifiget_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbr_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": certificat_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/signatures", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbr_signatures(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/signatures
    Type: Collection ofSignature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/signatures"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbr_signatures", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/signatures/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/signatures", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbr_signatures(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/signatures
    Type: Collection ofSignature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/signatures"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/signatures/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/signatures/{signatur_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbr_signatures_signatur_id(system_id: str, signatur_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/signatures/{signatur_id}
    Type: Signature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/signatures"
    item = db.get_item(collection_path, signatur_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbr_signatures_signatur_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/signatures/{signatur_id}"
            static_val["Id"] = signatur_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/signatures/{signatur_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbr_signatures_signatur_id(system_id: str, signatur_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/signatures/{signatur_id}
    Type: Signature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/signatures"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, signatur_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbr_signatures_signatur_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = signatur_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/signatures/{signatur_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, signatur_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/signatures/{signatur_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbr_signatures_signatur_id(system_id: str, signatur_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/signatures/{signatur_id}
    Type: Signature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbr/signatures"
    deleted = db.delete_item(collection_path, signatur_id)
    if deleted:
        return {"message": "Deleted successfully", "id": signatur_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbr_signatures_signaget_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbr_signatures_signatur_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": signatur_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbrdefault(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault
    Type: SecureBootDatabase
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbrdefault", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbrdefault(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault
    Type: SecureBootDatabase
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/certificates", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbrdefault_certificates(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/certificates"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbrdefault_certificates", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/certificates/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/certificates", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbrdefault_certificates(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/certificates"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/certificates/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/certificates/{certificat_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbrdefault_certificates_certificat_id(system_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/certificates"
    item = db.get_item(collection_path, certificat_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbrdefault_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/certificates/{certificat_id}"
            static_val["Id"] = certificat_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/certificates/{certificat_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbrdefault_certificates_certificat_id(system_id: str, certificat_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/certificates"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, certificat_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbrdefault_certificates_certificat_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = certificat_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/certificates/{certificat_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, certificat_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/certificates/{certificat_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbrdefault_certificates_certificat_id(system_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/certificates"
    deleted = db.delete_item(collection_path, certificat_id)
    if deleted:
        return {"message": "Deleted successfully", "id": certificat_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbrdefault_certificates_certifiget_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbrdefault_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": certificat_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/signatures", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbrdefault_signatures(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/signatures
    Type: Collection ofSignature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/signatures"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbrdefault_signatures", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/signatures/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/signatures", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbrdefault_signatures(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/signatures
    Type: Collection ofSignature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/signatures"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/signatures/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/signatures/{signatur_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbrdefault_signatures_signatur_id(system_id: str, signatur_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/signatures/{signatur_id}
    Type: Signature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/signatures"
    item = db.get_item(collection_path, signatur_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbrdefault_signatures_signatur_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/signatures/{signatur_id}"
            static_val["Id"] = signatur_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/signatures/{signatur_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbrdefault_signatures_signatur_id(system_id: str, signatur_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/signatures/{signatur_id}
    Type: Signature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/signatures"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, signatur_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbrdefault_signatures_signatur_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = signatur_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/signatures/{signatur_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, signatur_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/signatures/{signatur_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbrdefault_signatures_signatur_id(system_id: str, signatur_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/signatures/{signatur_id}
    Type: Signature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbrdefault/signatures"
    deleted = db.delete_item(collection_path, signatur_id)
    if deleted:
        return {"message": "Deleted successfully", "id": signatur_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbrdefault_signatures_signaget_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbrdefault_signatures_signatur_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": signatur_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbt(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt
    Type: SecureBootDatabase
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbt", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbt(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt
    Type: SecureBootDatabase
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/certificates", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbt_certificates(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/certificates"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbt_certificates", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/certificates/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/certificates", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbt_certificates(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/certificates"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/certificates/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/certificates/{certificat_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbt_certificates_certificat_id(system_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/certificates"
    item = db.get_item(collection_path, certificat_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbt_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/certificates/{certificat_id}"
            static_val["Id"] = certificat_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/certificates/{certificat_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbt_certificates_certificat_id(system_id: str, certificat_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/certificates"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, certificat_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbt_certificates_certificat_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = certificat_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/certificates/{certificat_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, certificat_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/certificates/{certificat_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbt_certificates_certificat_id(system_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/certificates"
    deleted = db.delete_item(collection_path, certificat_id)
    if deleted:
        return {"message": "Deleted successfully", "id": certificat_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbt_certificates_certifiget_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbt_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": certificat_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/signatures", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbt_signatures(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/signatures
    Type: Collection ofSignature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/signatures"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbt_signatures", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/signatures/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/signatures", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbt_signatures(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/signatures
    Type: Collection ofSignature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/signatures"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/signatures/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/signatures/{signatur_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbt_signatures_signatur_id(system_id: str, signatur_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/signatures/{signatur_id}
    Type: Signature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/signatures"
    item = db.get_item(collection_path, signatur_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbt_signatures_signatur_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/signatures/{signatur_id}"
            static_val["Id"] = signatur_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/signatures/{signatur_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbt_signatures_signatur_id(system_id: str, signatur_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/signatures/{signatur_id}
    Type: Signature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/signatures"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, signatur_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbt_signatures_signatur_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = signatur_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/signatures/{signatur_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, signatur_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/signatures/{signatur_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbt_signatures_signatur_id(system_id: str, signatur_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/signatures/{signatur_id}
    Type: Signature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbt/signatures"
    deleted = db.delete_item(collection_path, signatur_id)
    if deleted:
        return {"message": "Deleted successfully", "id": signatur_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbt_signatures_signaget_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbt_signatures_signatur_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": signatur_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbtdefault(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault
    Type: SecureBootDatabase
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbtdefault", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbtdefault(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault
    Type: SecureBootDatabase
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/certificates", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbtdefault_certificates(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/certificates"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbtdefault_certificates", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/certificates/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/certificates", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbtdefault_certificates(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/certificates"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/certificates/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/certificates/{certificat_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbtdefault_certificates_certificat_id(system_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/certificates"
    item = db.get_item(collection_path, certificat_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbtdefault_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/certificates/{certificat_id}"
            static_val["Id"] = certificat_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/certificates/{certificat_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbtdefault_certificates_certificat_id(system_id: str, certificat_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/certificates"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, certificat_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbtdefault_certificates_certificat_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = certificat_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/certificates/{certificat_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, certificat_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/certificates/{certificat_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbtdefault_certificates_certificat_id(system_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/certificates"
    deleted = db.delete_item(collection_path, certificat_id)
    if deleted:
        return {"message": "Deleted successfully", "id": certificat_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbtdefault_certificates_certifiget_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbtdefault_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": certificat_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/signatures", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbtdefault_signatures(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/signatures
    Type: Collection ofSignature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/signatures"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbtdefault_signatures", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/signatures/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/signatures", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbtdefault_signatures(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/signatures
    Type: Collection ofSignature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/signatures"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/signatures/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/signatures/{signatur_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbtdefault_signatures_signatur_id(system_id: str, signatur_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/signatures/{signatur_id}
    Type: Signature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/signatures"
    item = db.get_item(collection_path, signatur_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbtdefault_signatures_signatur_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/signatures/{signatur_id}"
            static_val["Id"] = signatur_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/signatures/{signatur_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbtdefault_signatures_signatur_id(system_id: str, signatur_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/signatures/{signatur_id}
    Type: Signature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/signatures"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, signatur_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbtdefault_signatures_signatur_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = signatur_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/signatures/{signatur_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, signatur_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/signatures/{signatur_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbtdefault_signatures_signatur_id(system_id: str, signatur_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/signatures/{signatur_id}
    Type: Signature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbtdefault/signatures"
    deleted = db.delete_item(collection_path, signatur_id)
    if deleted:
        return {"message": "Deleted successfully", "id": signatur_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbtdefault_signatures_signaget_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbtdefault_signatures_signatur_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": signatur_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbx(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx
    Type: SecureBootDatabase
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbx", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbx(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx
    Type: SecureBootDatabase
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/certificates", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbx_certificates(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/certificates"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbx_certificates", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/certificates/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/certificates", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbx_certificates(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/certificates"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/certificates/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/certificates/{certificat_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbx_certificates_certificat_id(system_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/certificates"
    item = db.get_item(collection_path, certificat_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbx_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/certificates/{certificat_id}"
            static_val["Id"] = certificat_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/certificates/{certificat_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbx_certificates_certificat_id(system_id: str, certificat_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/certificates"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, certificat_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbx_certificates_certificat_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = certificat_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/certificates/{certificat_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, certificat_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/certificates/{certificat_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbx_certificates_certificat_id(system_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/certificates"
    deleted = db.delete_item(collection_path, certificat_id)
    if deleted:
        return {"message": "Deleted successfully", "id": certificat_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbx_certificates_certifiget_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbx_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": certificat_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/signatures", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbx_signatures(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/signatures
    Type: Collection ofSignature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/signatures"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbx_signatures", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/signatures/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/signatures", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbx_signatures(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/signatures
    Type: Collection ofSignature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/signatures"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/signatures/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/signatures/{signatur_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbx_signatures_signatur_id(system_id: str, signatur_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/signatures/{signatur_id}
    Type: Signature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/signatures"
    item = db.get_item(collection_path, signatur_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbx_signatures_signatur_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/signatures/{signatur_id}"
            static_val["Id"] = signatur_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/signatures/{signatur_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbx_signatures_signatur_id(system_id: str, signatur_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/signatures/{signatur_id}
    Type: Signature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/signatures"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, signatur_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbx_signatures_signatur_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = signatur_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/signatures/{signatur_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, signatur_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/signatures/{signatur_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbx_signatures_signatur_id(system_id: str, signatur_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/signatures/{signatur_id}
    Type: Signature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbx/signatures"
    deleted = db.delete_item(collection_path, signatur_id)
    if deleted:
        return {"message": "Deleted successfully", "id": signatur_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbx_signatures_signaget_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbx_signatures_signatur_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": signatur_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbxdefault(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault
    Type: SecureBootDatabase
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbxdefault", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbxdefault(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault
    Type: SecureBootDatabase
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/certificates", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbxdefault_certificates(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/certificates"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbxdefault_certificates", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/certificates/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/certificates", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbxdefault_certificates(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/certificates"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/certificates/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/certificates/{certificat_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbxdefault_certificates_certificat_id(system_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/certificates"
    item = db.get_item(collection_path, certificat_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbxdefault_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/certificates/{certificat_id}"
            static_val["Id"] = certificat_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/certificates/{certificat_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbxdefault_certificates_certificat_id(system_id: str, certificat_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/certificates"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, certificat_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbxdefault_certificates_certificat_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = certificat_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/certificates/{certificat_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, certificat_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/certificates/{certificat_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbxdefault_certificates_certificat_id(system_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/certificates"
    deleted = db.delete_item(collection_path, certificat_id)
    if deleted:
        return {"message": "Deleted successfully", "id": certificat_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbxdefault_certificates_certifiget_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbxdefault_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": certificat_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/signatures", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbxdefault_signatures(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/signatures
    Type: Collection ofSignature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/signatures"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbxdefault_signatures", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/signatures/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/signatures", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbxdefault_signatures(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/signatures
    Type: Collection ofSignature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/signatures"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/signatures/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/signatures/{signatur_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbxdefault_signatures_signatur_id(system_id: str, signatur_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/signatures/{signatur_id}
    Type: Signature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/signatures"
    item = db.get_item(collection_path, signatur_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbxdefault_signatures_signatur_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/signatures/{signatur_id}"
            static_val["Id"] = signatur_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/signatures/{signatur_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbxdefault_signatures_signatur_id(system_id: str, signatur_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/signatures/{signatur_id}
    Type: Signature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/signatures"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, signatur_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbxdefault_signatures_signatur_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = signatur_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/signatures/{signatur_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, signatur_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/signatures/{signatur_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbxdefault_signatures_signatur_id(system_id: str, signatur_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/signatures/{signatur_id}
    Type: Signature
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/dbxdefault/signatures"
    deleted = db.delete_item(collection_path, signatur_id)
    if deleted:
        return {"message": "Deleted successfully", "id": signatur_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbxdefault_signatures_signaget_redfish_v1_systems_system_id_secureboot_securebootdatabases_dbxdefault_signatures_signatur_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": signatur_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_kek(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek
    Type: SecureBootDatabase
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_kek", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_kek(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek
    Type: SecureBootDatabase
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek/certificates", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_kek_certificates(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek/certificates"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_kek_certificates", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek/certificates/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek/certificates", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_kek_certificates(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek/certificates"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek/certificates/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek/certificates/{certificat_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_kek_certificates_certificat_id(system_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek/certificates"
    item = db.get_item(collection_path, certificat_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_kek_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek/certificates/{certificat_id}"
            static_val["Id"] = certificat_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek/certificates/{certificat_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_kek_certificates_certificat_id(system_id: str, certificat_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek/certificates"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, certificat_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_kek_certificates_certificat_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = certificat_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek/certificates/{certificat_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, certificat_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek/certificates/{certificat_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_kek_certificates_certificat_id(system_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kek/certificates"
    deleted = db.delete_item(collection_path, certificat_id)
    if deleted:
        return {"message": "Deleted successfully", "id": certificat_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_kek_certificates_certifiget_redfish_v1_systems_system_id_secureboot_securebootdatabases_kek_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": certificat_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_kekdefault(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault
    Type: SecureBootDatabase
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_kekdefault", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_kekdefault(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault
    Type: SecureBootDatabase
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault/certificates", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_kekdefault_certificates(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault/certificates"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_kekdefault_certificates", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault/certificates/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault/certificates", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_kekdefault_certificates(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault/certificates"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault/certificates/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault/certificates/{certificat_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_kekdefault_certificates_certificat_id(system_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault/certificates"
    item = db.get_item(collection_path, certificat_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_kekdefault_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault/certificates/{certificat_id}"
            static_val["Id"] = certificat_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault/certificates/{certificat_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_kekdefault_certificates_certificat_id(system_id: str, certificat_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault/certificates"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, certificat_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_kekdefault_certificates_certificat_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = certificat_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault/certificates/{certificat_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, certificat_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault/certificates/{certificat_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_kekdefault_certificates_certificat_id(system_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/kekdefault/certificates"
    deleted = db.delete_item(collection_path, certificat_id)
    if deleted:
        return {"message": "Deleted successfully", "id": certificat_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_kekdefault_certificates_certifiget_redfish_v1_systems_system_id_secureboot_securebootdatabases_kekdefault_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": certificat_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_pk(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk
    Type: SecureBootDatabase
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_pk", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_pk(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk
    Type: SecureBootDatabase
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk/certificates", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_pk_certificates(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk/certificates"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_pk_certificates", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk/certificates/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk/certificates", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_pk_certificates(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk/certificates"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk/certificates/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk/certificates/{certificat_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_pk_certificates_certificat_id(system_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk/certificates"
    item = db.get_item(collection_path, certificat_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_pk_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk/certificates/{certificat_id}"
            static_val["Id"] = certificat_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk/certificates/{certificat_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_pk_certificates_certificat_id(system_id: str, certificat_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk/certificates"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, certificat_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_pk_certificates_certificat_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = certificat_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk/certificates/{certificat_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, certificat_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk/certificates/{certificat_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_pk_certificates_certificat_id(system_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pk/certificates"
    deleted = db.delete_item(collection_path, certificat_id)
    if deleted:
        return {"message": "Deleted successfully", "id": certificat_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_pk_certificates_certifiget_redfish_v1_systems_system_id_secureboot_securebootdatabases_pk_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": certificat_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_pkdefault(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault
    Type: SecureBootDatabase
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_pkdefault", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_pkdefault(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault
    Type: SecureBootDatabase
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault/certificates", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_pkdefault_certificates(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault/certificates"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_pkdefault_certificates", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault/certificates/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault/certificates", methods=["POST"])
def post_redfish_v1_systems_system_id_secureboot_securebootdatabases_pkdefault_certificates(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault/certificates
    Type: CertificateCollection
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault/certificates"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault/certificates/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault/certificates/{certificat_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_secureboot_securebootdatabases_pkdefault_certificates_certificat_id(system_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault/certificates"
    item = db.get_item(collection_path, certificat_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureboot_securebootdatabases_pkdefault_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault/certificates/{certificat_id}"
            static_val["Id"] = certificat_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault/certificates/{certificat_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_pkdefault_certificates_certificat_id(system_id: str, certificat_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault/certificates"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, certificat_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_secureboot_securebootdatabases_pkdefault_certificates_certificat_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = certificat_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault/certificates/{certificat_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, certificat_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault/certificates/{certificat_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_pkdefault_certificates_certificat_id(system_id: str, certificat_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault/certificates/{certificat_id}
    Type: Collection ofCertificate
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureboot/securebootdatabases/pkdefault/certificates"
    deleted = db.delete_item(collection_path, certificat_id)
    if deleted:
        return {"message": "Deleted successfully", "id": certificat_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_secureboot_securebootdatabases_pkdefault_certificates_certifiget_redfish_v1_systems_system_id_secureboot_securebootdatabases_pkdefault_certificates_certificat_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": certificat_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureerasereportservice", methods=["GET"])
def get_redfish_v1_systems_system_id_secureerasereportservice(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureerasereportservice
    Type: HpeSecureEraseReportService
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureerasereportservice"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureerasereportservice", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureerasereportservice/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureerasereportservice", methods=["POST"])
def post_redfish_v1_systems_system_id_secureerasereportservice(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureerasereportservice
    Type: HpeSecureEraseReportService
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureerasereportservice"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureerasereportservice/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureerasereportservice/secureerasereportentries", methods=["GET"])
def get_redfish_v1_systems_system_id_secureerasereportservice_secureerasereportentries(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureerasereportservice/secureerasereportentries
    Type: Collection ofHpeSecureEraseReport
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureerasereportservice/secureerasereportentries"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureerasereportservice_secureerasereportentries", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/secureerasereportservice/secureerasereportentries/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/secureerasereportservice/secureerasereportentries", methods=["POST"])
def post_redfish_v1_systems_system_id_secureerasereportservice_secureerasereportentries(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/secureerasereportservice/secureerasereportentries
    Type: Collection ofHpeSecureEraseReport
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureerasereportservice/secureerasereportentries"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureerasereportservice/secureerasereportentries/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/secureerasereportservice/secureerasereportentries/{secureerasereportentry_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_secureerasereportservice_secureerasereportentries_secureerasereportentry_id(system_id: str, secureerasereportentry_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/secureerasereportservice/secureerasereportentries/{secureerasereportentry_id}
    Type: HpeSecureEraseReport
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureerasereportservice/secureerasereportentries"
    item = db.get_item(collection_path, secureerasereportentry_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_secureerasereportservice_secureerasereportentries_secureerasereportentry_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureerasereportservice/secureerasereportentries/{secureerasereportentry_id}"
            static_val["Id"] = secureerasereportentry_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/secureerasereportservice/secureerasereportentries/{secureerasereportentry_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_secureerasereportservice_secureerasereportentries_secureerasereportentry_id(system_id: str, secureerasereportentry_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/secureerasereportservice/secureerasereportentries/{secureerasereportentry_id}
    Type: HpeSecureEraseReport
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureerasereportservice/secureerasereportentries"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, secureerasereportentry_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_secureerasereportservice_secureerasereportentries_secureerasereportentry_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = secureerasereportentry_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/secureerasereportservice/secureerasereportentries/{secureerasereportentry_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, secureerasereportentry_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/secureerasereportservice/secureerasereportentries/{secureerasereportentry_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_secureerasereportservice_secureerasereportentries_secureerasereportentry_id(system_id: str, secureerasereportentry_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/secureerasereportservice/secureerasereportentries/{secureerasereportentry_id}
    Type: HpeSecureEraseReport
    """
    collection_path = f"/redfish/v1/systems/{system_id}/secureerasereportservice/secureerasereportentries"
    deleted = db.delete_item(collection_path, secureerasereportentry_id)
    if deleted:
        return {"message": "Deleted successfully", "id": secureerasereportentry_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_secureerasereportservice_secureerasereportentries_secureerasereportenget_redfish_v1_systems_system_id_secureerasereportservice_secureerasereportentries_secureerasereportentry_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": secureerasereportentry_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/storage", methods=["GET"])
def get_redfish_v1_systems_system_id_storage(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/storage
    Type: Collection ofStorage
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_storage", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/storage/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/storage", methods=["POST"])
def post_redfish_v1_systems_system_id_storage(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/storage
    Type: Collection ofStorage
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/storage/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/storage/{storage_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_storage_storage_id(system_id: str, storage_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/storage/{storage_id}
    Type: Storage
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage"
    item = db.get_item(collection_path, storage_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_storage_storage_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/storage/{storage_id}"
            static_val["Id"] = storage_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/storage/{storage_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_storage_storage_id(system_id: str, storage_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/storage/{storage_id}
    Type: Storage
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, storage_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_storage_storage_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = storage_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/storage/{storage_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, storage_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/storage/{storage_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_storage_storage_id(system_id: str, storage_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/storage/{storage_id}
    Type: Storage
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage"
    deleted = db.delete_item(collection_path, storage_id)
    if deleted:
        return {"message": "Deleted successfully", "id": storage_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_storage_storget_redfish_v1_systems_system_id_storage_storage_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": storage_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/", methods=["GET"])
def get_redfish_v1_systems_system_id_storage_storage_id_controllers(system_id: str, storage_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/
    Type: Collection ofStorageController
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_storage_storage_id_controllers", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers//{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/", methods=["POST"])
def post_redfish_v1_systems_system_id_storage_storage_id_controllers(system_id: str, storage_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/
    Type: Collection ofStorageController
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers//{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_storage_storage_id_controllers_controller_id(system_id: str, storage_id: str, controller_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}
    Type: StorageController
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers"
    item = db.get_item(collection_path, controller_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_storage_storage_id_controllers_controller_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}"
            static_val["Id"] = controller_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_storage_storage_id_controllers_controller_id(system_id: str, storage_id: str, controller_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}
    Type: StorageController
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, controller_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_storage_storage_id_controllers_controller_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = controller_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, controller_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_storage_storage_id_controllers_controller_id(system_id: str, storage_id: str, controller_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}
    Type: StorageController
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers"
    deleted = db.delete_item(collection_path, controller_id)
    if deleted:
        return {"message": "Deleted successfully", "id": controller_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_storage_storage_id_controllers_controlget_redfish_v1_systems_system_id_storage_storage_id_controllers_controller_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": controller_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/assembly", methods=["GET"])
def get_redfish_v1_systems_system_id_storage_storage_id_controllers_controller_id_assembly(system_id: str, storage_id: str, controller_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/assembly
    Type: Assembly
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/assembly"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_storage_storage_id_controllers_controller_id_assembly", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/assembly/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/assembly", methods=["POST"])
def post_redfish_v1_systems_system_id_storage_storage_id_controllers_controller_id_assembly(system_id: str, storage_id: str, controller_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/assembly
    Type: Assembly
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/assembly"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/assembly/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/ports", methods=["GET"])
def get_redfish_v1_systems_system_id_storage_storage_id_controllers_controller_id_ports(system_id: str, storage_id: str, controller_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/ports
    Type: Collection ofPort
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/ports"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_storage_storage_id_controllers_controller_id_ports", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/ports/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/ports", methods=["POST"])
def post_redfish_v1_systems_system_id_storage_storage_id_controllers_controller_id_ports(system_id: str, storage_id: str, controller_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/ports
    Type: Collection ofPort
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/ports"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/ports/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/ports/{port_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_storage_storage_id_controllers_controller_id_ports_port_id(system_id: str, storage_id: str, controller_id: str, port_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/ports/{port_id}
    Type: Port
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/ports"
    item = db.get_item(collection_path, port_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_storage_storage_id_controllers_controller_id_ports_port_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/ports/{port_id}"
            static_val["Id"] = port_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/ports/{port_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_storage_storage_id_controllers_controller_id_ports_port_id(system_id: str, storage_id: str, controller_id: str, port_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/ports/{port_id}
    Type: Port
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/ports"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, port_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_storage_storage_id_controllers_controller_id_ports_port_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = port_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/ports/{port_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, port_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/ports/{port_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_storage_storage_id_controllers_controller_id_ports_port_id(system_id: str, storage_id: str, controller_id: str, port_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/ports/{port_id}
    Type: Port
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/controllers/{controller_id}/ports"
    deleted = db.delete_item(collection_path, port_id)
    if deleted:
        return {"message": "Deleted successfully", "id": port_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_storage_storage_id_controllers_controller_id_ports_pget_redfish_v1_systems_system_id_storage_storage_id_controllers_controller_id_ports_port_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": port_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/storage/{storage_id}/drives/{driv_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_storage_storage_id_drives_driv_id(system_id: str, storage_id: str, driv_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/storage/{storage_id}/drives/{driv_id}
    Type: Drive
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/drives"
    item = db.get_item(collection_path, driv_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_storage_storage_id_drives_driv_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/drives/{driv_id}"
            static_val["Id"] = driv_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/storage/{storage_id}/drives/{driv_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_storage_storage_id_drives_driv_id(system_id: str, storage_id: str, driv_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/storage/{storage_id}/drives/{driv_id}
    Type: Drive
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/drives"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, driv_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_storage_storage_id_drives_driv_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = driv_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/drives/{driv_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, driv_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/storage/{storage_id}/drives/{driv_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_storage_storage_id_drives_driv_id(system_id: str, storage_id: str, driv_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/storage/{storage_id}/drives/{driv_id}
    Type: Drive
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/drives"
    deleted = db.delete_item(collection_path, driv_id)
    if deleted:
        return {"message": "Deleted successfully", "id": driv_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_storage_storage_id_drives_dget_redfish_v1_systems_system_id_storage_storage_id_drives_driv_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": driv_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/storage/{storage_id}/storagecontrollers/{storagecontroller_id}/ports", methods=["GET"])
def get_redfish_v1_systems_system_id_storage_storage_id_storagecontrollers_storagecontroller_id_ports(system_id: str, storage_id: str, storagecontroller_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/storage/{storage_id}/storagecontrollers/{storagecontroller_id}/ports
    Type: Collection ofPort
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/storagecontrollers/{storagecontroller_id}/ports"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_storage_storage_id_storagecontrollers_storagecontroller_id_ports", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/storage/{storage_id}/storagecontrollers/{storagecontroller_id}/ports/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/storage/{storage_id}/storagecontrollers/{storagecontroller_id}/ports", methods=["POST"])
def post_redfish_v1_systems_system_id_storage_storage_id_storagecontrollers_storagecontroller_id_ports(system_id: str, storage_id: str, storagecontroller_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/storage/{storage_id}/storagecontrollers/{storagecontroller_id}/ports
    Type: Collection ofPort
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/storagecontrollers/{storagecontroller_id}/ports"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/storagecontrollers/{storagecontroller_id}/ports/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/storage/{storage_id}/storagecontrollers/{storagecontroller_id}/ports/{port_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_storage_storage_id_storagecontrollers_storagecontroller_id_ports_port_id(system_id: str, storage_id: str, storagecontroller_id: str, port_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/storage/{storage_id}/storagecontrollers/{storagecontroller_id}/ports/{port_id}
    Type: Port
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/storagecontrollers/{storagecontroller_id}/ports"
    item = db.get_item(collection_path, port_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_storage_storage_id_storagecontrollers_storagecontroller_id_ports_port_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/storagecontrollers/{storagecontroller_id}/ports/{port_id}"
            static_val["Id"] = port_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/storage/{storage_id}/storagecontrollers/{storagecontroller_id}/ports/{port_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_storage_storage_id_storagecontrollers_storagecontroller_id_ports_port_id(system_id: str, storage_id: str, storagecontroller_id: str, port_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/storage/{storage_id}/storagecontrollers/{storagecontroller_id}/ports/{port_id}
    Type: Port
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/storagecontrollers/{storagecontroller_id}/ports"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, port_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_storage_storage_id_storagecontrollers_storagecontroller_id_ports_port_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = port_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/storagecontrollers/{storagecontroller_id}/ports/{port_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, port_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/storage/{storage_id}/storagecontrollers/{storagecontroller_id}/ports/{port_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_storage_storage_id_storagecontrollers_storagecontroller_id_ports_port_id(system_id: str, storage_id: str, storagecontroller_id: str, port_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/storage/{storage_id}/storagecontrollers/{storagecontroller_id}/ports/{port_id}
    Type: Port
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/storagecontrollers/{storagecontroller_id}/ports"
    deleted = db.delete_item(collection_path, port_id)
    if deleted:
        return {"message": "Deleted successfully", "id": port_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_storage_storage_id_storagecontrollers_storagecontroller_id_ports_pget_redfish_v1_systems_system_id_storage_storage_id_storagecontrollers_storagecontroller_id_ports_port_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": port_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/storage/{storage_id}/volumes", methods=["GET"])
def get_redfish_v1_systems_system_id_storage_storage_id_volumes(system_id: str, storage_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/storage/{storage_id}/volumes
    Type: Collection ofVolume
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/volumes"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_storage_storage_id_volumes", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/storage/{storage_id}/volumes/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/storage/{storage_id}/volumes", methods=["POST"])
def post_redfish_v1_systems_system_id_storage_storage_id_volumes(system_id: str, storage_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/storage/{storage_id}/volumes
    Type: Collection ofVolume
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/volumes"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/volumes/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/storage/{storage_id}/volumes/{volum_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_storage_storage_id_volumes_volum_id(system_id: str, storage_id: str, volum_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/storage/{storage_id}/volumes/{volum_id}
    Type: Volume
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/volumes"
    item = db.get_item(collection_path, volum_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_storage_storage_id_volumes_volum_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/volumes/{volum_id}"
            static_val["Id"] = volum_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/storage/{storage_id}/volumes/{volum_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_storage_storage_id_volumes_volum_id(system_id: str, storage_id: str, volum_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/storage/{storage_id}/volumes/{volum_id}
    Type: Volume
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/volumes"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, volum_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_storage_storage_id_volumes_volum_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = volum_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/volumes/{volum_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, volum_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/storage/{storage_id}/volumes/{volum_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_storage_storage_id_volumes_volum_id(system_id: str, storage_id: str, volum_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/storage/{storage_id}/volumes/{volum_id}
    Type: Volume
    """
    collection_path = f"/redfish/v1/systems/{system_id}/storage/{storage_id}/volumes"
    deleted = db.delete_item(collection_path, volum_id)
    if deleted:
        return {"message": "Deleted successfully", "id": volum_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_storage_storage_id_volumes_voget_redfish_v1_systems_system_id_storage_storage_id_volumes_volum_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": volum_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/usbdevices", methods=["GET"])
def get_redfish_v1_systems_system_id_usbdevices(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/usbdevices
    Type: Collection ofHpeUSBDevice
    """
    collection_path = f"/redfish/v1/systems/{system_id}/usbdevices"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_usbdevices", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/usbdevices/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/usbdevices", methods=["POST"])
def post_redfish_v1_systems_system_id_usbdevices(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/usbdevices
    Type: Collection ofHpeUSBDevice
    """
    collection_path = f"/redfish/v1/systems/{system_id}/usbdevices"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/usbdevices/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/usbdevices/{usbdevic_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_usbdevices_usbdevic_id(system_id: str, usbdevic_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/usbdevices/{usbdevic_id}
    Type: HpeUSBDevice
    """
    collection_path = f"/redfish/v1/systems/{system_id}/usbdevices"
    item = db.get_item(collection_path, usbdevic_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_usbdevices_usbdevic_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/usbdevices/{usbdevic_id}"
            static_val["Id"] = usbdevic_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/usbdevices/{usbdevic_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_usbdevices_usbdevic_id(system_id: str, usbdevic_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/usbdevices/{usbdevic_id}
    Type: HpeUSBDevice
    """
    collection_path = f"/redfish/v1/systems/{system_id}/usbdevices"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, usbdevic_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_usbdevices_usbdevic_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = usbdevic_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/usbdevices/{usbdevic_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, usbdevic_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/usbdevices/{usbdevic_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_usbdevices_usbdevic_id(system_id: str, usbdevic_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/usbdevices/{usbdevic_id}
    Type: HpeUSBDevice
    """
    collection_path = f"/redfish/v1/systems/{system_id}/usbdevices"
    deleted = db.delete_item(collection_path, usbdevic_id)
    if deleted:
        return {"message": "Deleted successfully", "id": usbdevic_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_usbdevices_usbdeget_redfish_v1_systems_system_id_usbdevices_usbdevic_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": usbdevic_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/usbports", methods=["GET"])
def get_redfish_v1_systems_system_id_usbports(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/usbports
    Type: Collection ofHpeUSBPort
    """
    collection_path = f"/redfish/v1/systems/{system_id}/usbports"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_usbports", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/usbports/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/usbports", methods=["POST"])
def post_redfish_v1_systems_system_id_usbports(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/usbports
    Type: Collection ofHpeUSBPort
    """
    collection_path = f"/redfish/v1/systems/{system_id}/usbports"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/usbports/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/usbports/{usbport_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_usbports_usbport_id(system_id: str, usbport_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/usbports/{usbport_id}
    Type: HpeUSBPort
    """
    collection_path = f"/redfish/v1/systems/{system_id}/usbports"
    item = db.get_item(collection_path, usbport_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_usbports_usbport_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/usbports/{usbport_id}"
            static_val["Id"] = usbport_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/usbports/{usbport_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_usbports_usbport_id(system_id: str, usbport_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/usbports/{usbport_id}
    Type: HpeUSBPort
    """
    collection_path = f"/redfish/v1/systems/{system_id}/usbports"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, usbport_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_usbports_usbport_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = usbport_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/usbports/{usbport_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, usbport_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/usbports/{usbport_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_usbports_usbport_id(system_id: str, usbport_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/usbports/{usbport_id}
    Type: HpeUSBPort
    """
    collection_path = f"/redfish/v1/systems/{system_id}/usbports"
    deleted = db.delete_item(collection_path, usbport_id)
    if deleted:
        return {"message": "Deleted successfully", "id": usbport_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_usbports_usbpget_redfish_v1_systems_system_id_usbports_usbport_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": usbport_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/workloadperformanceadvisor", methods=["GET"])
def get_redfish_v1_systems_system_id_workloadperformanceadvisor(system_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/workloadperformanceadvisor
    Type: Collection ofHpeWorkloadPerformanceAdvisor
    """
    collection_path = f"/redfish/v1/systems/{system_id}/workloadperformanceadvisor"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_systems_system_id_workloadperformanceadvisor", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/systems/{system_id}/workloadperformanceadvisor/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/systems/{system_id}/workloadperformanceadvisor", methods=["POST"])
def post_redfish_v1_systems_system_id_workloadperformanceadvisor(system_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/workloadperformanceadvisor
    Type: Collection ofHpeWorkloadPerformanceAdvisor
    """
    collection_path = f"/redfish/v1/systems/{system_id}/workloadperformanceadvisor"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/systems/{system_id}/workloadperformanceadvisor/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/systems/{system_id}/workloadperformanceadvisor/{workloadperformanceadvisor_id}", methods=["GET"])
def get_redfish_v1_systems_system_id_workloadperformanceadvisor_workloadperformanceadvisor_id(system_id: str, workloadperformanceadvisor_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/workloadperformanceadvisor/{workloadperformanceadvisor_id}
    Type: HpeWorkloadPerformanceAdvisor
    """
    collection_path = f"/redfish/v1/systems/{system_id}/workloadperformanceadvisor"
    item = db.get_item(collection_path, workloadperformanceadvisor_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_systems_system_id_workloadperformanceadvisor_workloadperformanceadvisor_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/systems/{system_id}/workloadperformanceadvisor/{workloadperformanceadvisor_id}"
            static_val["Id"] = workloadperformanceadvisor_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/systems/{system_id}/workloadperformanceadvisor/{workloadperformanceadvisor_id}", methods=["PATCH"])
def patch_redfish_v1_systems_system_id_workloadperformanceadvisor_workloadperformanceadvisor_id(system_id: str, workloadperformanceadvisor_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/systems/{system_id}/workloadperformanceadvisor/{workloadperformanceadvisor_id}
    Type: HpeWorkloadPerformanceAdvisor
    """
    collection_path = f"/redfish/v1/systems/{system_id}/workloadperformanceadvisor"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, workloadperformanceadvisor_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_systems_system_id_workloadperformanceadvisor_workloadperformanceadvisor_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = workloadperformanceadvisor_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}/workloadperformanceadvisor/{workloadperformanceadvisor_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, workloadperformanceadvisor_id, existing)
    return existing

@app.api_route("/redfish/v1/systems/{system_id}/workloadperformanceadvisor/{workloadperformanceadvisor_id}", methods=["DELETE"])
def delete_redfish_v1_systems_system_id_workloadperformanceadvisor_workloadperformanceadvisor_id(system_id: str, workloadperformanceadvisor_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/systems/{system_id}/workloadperformanceadvisor/{workloadperformanceadvisor_id}
    Type: HpeWorkloadPerformanceAdvisor
    """
    collection_path = f"/redfish/v1/systems/{system_id}/workloadperformanceadvisor"
    deleted = db.delete_item(collection_path, workloadperformanceadvisor_id)
    if deleted:
        return {"message": "Deleted successfully", "id": workloadperformanceadvisor_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_systems_system_id_workloadperformanceadvisor_workloadperformanceadviget_redfish_v1_systems_system_id_workloadperformanceadvisor_workloadperformanceadvisor_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": workloadperformanceadvisor_id}
    raise HTTPException(status_code=404, detail="Resource not found")

# ══════════════════════════════════════════════════════════════════════════════
# IML / LogServices — Event Logs
# ══════════════════════════════════════════════════════════════════════════════

_SAMPLE_IML_ENTRIES = [
    {"Id": "1", "Severity": "OK",       "Message": "Server power on at 2026-06-28T10:00:00Z", "Created": "2026-06-28T10:00:00Z"},
    {"Id": "2", "Severity": "Warning",  "Message": "Memory training deviation detected on DIMM slot 4A", "Created": "2026-06-28T11:15:00Z"},
    {"Id": "3", "Severity": "Critical", "Message": "Fan redundancy lost: Fan 4 failed, speed reading 0 RPM", "Created": "2026-06-28T12:30:00Z"},
    {"Id": "4", "Severity": "OK",       "Message": "iLO reset: firmware update completed successfully", "Created": "2026-06-28T13:00:00Z"},
    {"Id": "5", "Severity": "Warning",  "Message": "CPU 1 correctable error threshold reached", "Created": "2026-06-28T14:20:00Z"},
    {"Id": "6", "Severity": "Critical", "Message": "Drive 2 (slot 1) predictive failure detected", "Created": "2026-06-28T15:45:00Z"},
    {"Id": "7", "Severity": "OK",       "Message": "Automatic server recovery initiated by watchdog", "Created": "2026-06-28T16:00:00Z"},
]

@app.api_route("/redfish/v1/systems/{system_id}/logservices", methods=["GET"])
def get_logservices(system_id: str):
    """iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/logservices"""
    return {
        "@odata.type": "#LogServiceCollection.LogServiceCollection",
        "@odata.id": f"/redfish/v1/systems/{system_id}/logservices",
        "Name": "Log Services Collection",
        "Members@odata.count": 1,
        "Members": [{"@odata.id": f"/redfish/v1/systems/{system_id}/logservices/iml"}]
    }

@app.api_route("/redfish/v1/systems/{system_id}/logservices/iml", methods=["GET"])
def get_iml_logservice(system_id: str):
    """iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/logservices/iml"""
    return {
        "@odata.type": "#LogService.v1_1_0.LogService",
        "@odata.id": f"/redfish/v1/systems/{system_id}/logservices/iml",
        "Id": "IML",
        "Name": "Integrated Management Log",
        "MaxNumberOfRecords": 1000,
        "OverWritePolicy": "WrapsWhenFull",
        "Entries": {"@odata.id": f"/redfish/v1/systems/{system_id}/logservices/iml/entries"},
        "Actions": {
            "#LogService.ClearLog": {
                "target": f"/redfish/v1/systems/{system_id}/logservices/iml/actions/logservice.clearlog"
            }
        }
    }

@app.api_route("/redfish/v1/systems/{system_id}/logservices/iml/entries", methods=["GET"])
def get_iml_entries(system_id: str, severity: str = None):
    """iLO Redfish Endpoint: GET /redfish/v1/systems/{system_id}/logservices/iml/entries"""
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/iml/entries"
    dynamic_items = db.get_all(collection_path)
    entries = dynamic_items if dynamic_items else list(_SAMPLE_IML_ENTRIES)
    if severity:
        entries = [e for e in entries if str(e.get("Severity", "")).lower() == severity.lower()]
    return {
        "@odata.type": "#LogEntryCollection.LogEntryCollection",
        "@odata.id": f"/redfish/v1/systems/{system_id}/logservices/iml/entries",
        "Name": "Integrated Management Log Entries",
        "Members@odata.count": len(entries),
        "Members": entries
    }

@app.api_route("/redfish/v1/systems/{system_id}/logservices/iml/actions/logservice.clearlog", methods=["POST"])
def clear_iml_log(system_id: str, payload: dict = None):
    """iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/logservices/iml/actions/logservice.clearlog"""
    collection_path = f"/redfish/v1/systems/{system_id}/logservices/iml/entries"
    db._dynamic.pop(collection_path, None)
    return {"message": f"IML log cleared for system {system_id}", "Members@odata.count": 0, "Members": []}

# ══════════════════════════════════════════════════════════════════════════════
# Chassis — Thermal and Power sensors
# ══════════════════════════════════════════════════════════════════════════════

@app.api_route("/redfish/v1/chassis", methods=["GET"])
def get_chassis_collection():
    """iLO Redfish Endpoint: GET /redfish/v1/chassis"""
    return {
        "@odata.type": "#ChassisCollection.ChassisCollection",
        "@odata.id": "/redfish/v1/chassis",
        "Name": "Chassis Collection",
        "Members@odata.count": 1,
        "Members": [{"@odata.id": "/redfish/v1/chassis/1"}]
    }

@app.api_route("/redfish/v1/chassis/{chassis_id}", methods=["GET"])
def get_chassis(chassis_id: str):
    """iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassis_id}"""
    return {
        "@odata.type": "#Chassis.v1_14_0.Chassis",
        "@odata.id": f"/redfish/v1/chassis/{chassis_id}",
        "Id": chassis_id,
        "Name": f"Computer System Chassis {chassis_id}",
        "ChassisType": "RackMount",
        "Thermal": {"@odata.id": f"/redfish/v1/chassis/{chassis_id}/thermal"},
        "Power":   {"@odata.id": f"/redfish/v1/chassis/{chassis_id}/power"},
    }

@app.api_route("/redfish/v1/chassis/{chassis_id}/thermal", methods=["GET"])
def get_chassis_thermal(chassis_id: str):
    """iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassis_id}/thermal"""
    return {
        "@odata.type": "#Thermal.v1_6_1.Thermal",
        "@odata.id": f"/redfish/v1/chassis/{chassis_id}/thermal",
        "Id": "Thermal",
        "Name": "Thermal Metrics",
        "Temperatures": [
            {"MemberId": "0", "Name": "01-Inlet Ambient", "ReadingCelsius": 24, "UpperThresholdCritical": 42, "Status": {"State": "Enabled", "Health": "OK"}},
            {"MemberId": "1", "Name": "02-CPU 1",          "ReadingCelsius": 48, "UpperThresholdCritical": 70, "Status": {"State": "Enabled", "Health": "OK"}},
            {"MemberId": "2", "Name": "03-CPU 2",          "ReadingCelsius": 46, "UpperThresholdCritical": 70, "Status": {"State": "Enabled", "Health": "OK"}},
            {"MemberId": "3", "Name": "04-P1 DIMM 1-6",   "ReadingCelsius": 36, "UpperThresholdCritical": 85, "Status": {"State": "Enabled", "Health": "OK"}},
        ],
        "Fans": [
            {"MemberId": "0", "Name": "Fan 1", "Reading": 4200, "ReadingUnits": "RPM", "Status": {"State": "Enabled", "Health": "OK"}},
            {"MemberId": "1", "Name": "Fan 2", "Reading": 4100, "ReadingUnits": "RPM", "Status": {"State": "Enabled", "Health": "OK"}},
            {"MemberId": "2", "Name": "Fan 3", "Reading": 4150, "ReadingUnits": "RPM", "Status": {"State": "Enabled", "Health": "OK"}},
            {"MemberId": "3", "Name": "Fan 4", "Reading": 0,    "ReadingUnits": "RPM", "Status": {"State": "Enabled", "Health": "Critical"}},
        ]
    }

@app.api_route("/redfish/v1/chassis/{chassis_id}/power", methods=["GET"])
def get_chassis_power(chassis_id: str):
    """iLO Redfish Endpoint: GET /redfish/v1/chassis/{chassis_id}/power"""
    return {
        "@odata.type": "#Power.v1_6_1.Power",
        "@odata.id": f"/redfish/v1/chassis/{chassis_id}/power",
        "Id": "Power",
        "Name": "Power Metrics",
        "PowerControl": [
            {"MemberId": "0", "Name": "Server Power Control", "PowerConsumedWatts": 320, "PowerCapacityWatts": 800,
             "Status": {"State": "Enabled", "Health": "OK"}}
        ],
        "PowerSupplies": [
            {"MemberId": "0", "Name": "HpeServerPowerSupply 1", "PowerInputWatts": 165, "PowerOutputWatts": 160,
             "Status": {"State": "Enabled", "Health": "OK"}, "Redundancy": [{"@odata.id": f"/redfish/v1/chassis/{chassis_id}/power#/Redundancy/0"}]},
            {"MemberId": "1", "Name": "HpeServerPowerSupply 2", "PowerInputWatts": 160, "PowerOutputWatts": 155,
             "Status": {"State": "Enabled", "Health": "OK"}, "Redundancy": [{"@odata.id": f"/redfish/v1/chassis/{chassis_id}/power#/Redundancy/0"}]},
        ],
        "Redundancy": [
            {"MemberId": "0", "Name": "PowerSupply Redundancy Group 1", "Mode": "Failover",
             "Status": {"State": "Enabled", "Health": "OK"}, "RedundancyEnabled": True}
        ]
    }

# ══════════════════════════════════════════════════════════════════════════════
# ComputerSystem Actions — Reset (Power On/Off/Restart)
# ══════════════════════════════════════════════════════════════════════════════

@app.api_route("/redfish/v1/systems/{system_id}/actions/computersystem.reset", methods=["POST"])
def system_reset_action(system_id: str, payload: dict = None):
    """iLO Redfish Endpoint: POST /redfish/v1/systems/{system_id}/actions/computersystem.reset"""
    payload_dict = payload or {}
    reset_type = payload_dict.get("ResetType", "GracefulRestart")
    # Update system power state accordingly
    collection_path = "/redfish/v1/systems"
    item = db.get_item(collection_path, system_id) or {}
    new_state = {
        "On": "On", "ForceOff": "Off", "GracefulShutdown": "Off",
        "GracefulRestart": "On", "ForceRestart": "On", "PowerCycle": "On"
    }.get(reset_type, "On")
    item.update({"PowerState": new_state, "Id": system_id})
    db.upsert_item(collection_path, system_id, item)
    return {
        "message": f"Reset action '{reset_type}' accepted for system {system_id}",
        "PowerState": new_state,
        "ResetType": reset_type,
        "@odata.id": f"/redfish/v1/systems/{system_id}"
    }

# ══════════════════════════════════════════════════════════════════════════════
# VirtualMedia — InsertMedia and EjectMedia Actions
# ══════════════════════════════════════════════════════════════════════════════

@app.api_route("/redfish/v1/managers/{manager_id}/virtualmedia/{media_id}/actions/virtualmedia.insertmedia", methods=["POST"])
def insert_virtual_media(manager_id: str, media_id: str, payload: dict = None):
    """iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/virtualmedia/{media_id}/actions/virtualmedia.insertmedia"""
    payload_dict = payload or {}
    image_url = payload_dict.get("Image", "")
    transfer_protocol = payload_dict.get("TransferProtocolType", "HTTP")
    collection_path = f"/redfish/v1/managers/{manager_id}/virtualmedia"
    existing = db.get_item(collection_path, media_id) or {}
    existing.update({
        "Id": media_id,
        "@odata.id": f"/redfish/v1/managers/{manager_id}/virtualmedia/{media_id}",
        "Inserted": True,
        "WriteProtected": payload_dict.get("WriteProtected", True),
        "Image": image_url,
        "TransferProtocolType": transfer_protocol,
        "MediaTypes": ["CD", "DVD"] if "iso" in image_url.lower() else ["USBStick"],
        "ConnectedVia": "URI",
    })
    db.upsert_item(collection_path, media_id, existing)
    return {
        "message": f"Virtual media inserted successfully on manager {manager_id}, slot {media_id}",
        "Image": image_url,
        "Inserted": True,
        "TransferProtocolType": transfer_protocol,
        "@odata.id": f"/redfish/v1/managers/{manager_id}/virtualmedia/{media_id}"
    }

@app.api_route("/redfish/v1/managers/{manager_id}/virtualmedia/{media_id}/actions/virtualmedia.ejectmedia", methods=["POST"])
def eject_virtual_media(manager_id: str, media_id: str, payload: dict = None):
    """iLO Redfish Endpoint: POST /redfish/v1/managers/{manager_id}/virtualmedia/{media_id}/actions/virtualmedia.ejectmedia"""
    collection_path = f"/redfish/v1/managers/{manager_id}/virtualmedia"
    existing = db.get_item(collection_path, media_id) or {}
    existing.update({"Id": media_id, "Inserted": False, "Image": "", "ConnectedVia": "NotConnected"})
    db.upsert_item(collection_path, media_id, existing)
    return {"message": f"Virtual media ejected from manager {manager_id}, slot {media_id}", "Inserted": False}



@app.api_route("/redfish/v1/taskservice", methods=["GET"])
def get_redfish_v1_taskservice():
    """
    iLO Redfish Endpoint: GET /redfish/v1/taskservice
    Type: TaskService
    """
    collection_path = "/redfish/v1/taskservice"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_taskservice", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/taskservice/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/taskservice", methods=["POST"])
def post_redfish_v1_taskservice(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/taskservice
    Type: TaskService
    """
    collection_path = "/redfish/v1/taskservice"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/taskservice/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/taskservice/tasks", methods=["GET"])
def get_redfish_v1_taskservice_tasks():
    """
    iLO Redfish Endpoint: GET /redfish/v1/taskservice/tasks
    Type: Collection ofTask
    """
    collection_path = "/redfish/v1/taskservice/tasks"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_taskservice_tasks", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/taskservice/tasks/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/taskservice/tasks", methods=["POST"])
def post_redfish_v1_taskservice_tasks(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/taskservice/tasks
    Type: Collection ofTask
    """
    collection_path = "/redfish/v1/taskservice/tasks"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/taskservice/tasks/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/taskservice/tasks/{task_id}", methods=["GET"])
def get_redfish_v1_taskservice_tasks_task_id(task_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/taskservice/tasks/{task_id}
    Type: Task
    """
    collection_path = f"/redfish/v1/taskservice/tasks"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_taskservice_tasks_task_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/taskservice/tasks/{task_id}"
            static_val["Id"] = task_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/taskservice/tasks/{task_id}", methods=["PATCH"])
def patch_redfish_v1_taskservice_tasks_task_id(task_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/taskservice/tasks/{task_id}
    Type: Task
    """
    collection_path = f"/redfish/v1/taskservice/tasks"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, task_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_taskservice_tasks_task_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = task_id
            existing["@odata.id"] = f"/redfish/v1/taskservice/tasks/{task_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, task_id, existing)
    return existing

@app.api_route("/redfish/v1/taskservice/tasks/{task_id}", methods=["DELETE"])
def delete_redfish_v1_taskservice_tasks_task_id(task_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/taskservice/tasks/{task_id}
    Type: Task
    """
    collection_path = f"/redfish/v1/taskservice/tasks"
    deleted = db.delete_item(collection_path, task_id)
    if deleted:
        return {"message": "Deleted successfully", "id": task_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_taskservice_tasks_tget_redfish_v1_taskservice_tasks_task_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": task_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/telemetryservice", methods=["GET"])
def get_redfish_v1_telemetryservice():
    """
    iLO Redfish Endpoint: GET /redfish/v1/telemetryservice
    Type: TelemetryService
    """
    collection_path = "/redfish/v1/telemetryservice"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_telemetryservice", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/telemetryservice/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/telemetryservice", methods=["POST"])
def post_redfish_v1_telemetryservice(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/telemetryservice
    Type: TelemetryService
    """
    collection_path = "/redfish/v1/telemetryservice"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/telemetryservice/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/telemetryservice/metricdefinitions", methods=["GET"])
def get_redfish_v1_telemetryservice_metricdefinitions():
    """
    iLO Redfish Endpoint: GET /redfish/v1/telemetryservice/metricdefinitions
    Type: Collection ofMetricDefinition
    """
    collection_path = "/redfish/v1/telemetryservice/metricdefinitions"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_telemetryservice_metricdefinitions", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/telemetryservice/metricdefinitions/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/telemetryservice/metricdefinitions", methods=["POST"])
def post_redfish_v1_telemetryservice_metricdefinitions(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/telemetryservice/metricdefinitions
    Type: Collection ofMetricDefinition
    """
    collection_path = "/redfish/v1/telemetryservice/metricdefinitions"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/telemetryservice/metricdefinitions/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/telemetryservice/metricdefinitions/{metricdefinition_id}", methods=["GET"])
def get_redfish_v1_telemetryservice_metricdefinitions_metricdefinition_id(metricdefinition_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/telemetryservice/metricdefinitions/{metricdefinition_id}
    Type: MetricDefinition
    """
    collection_path = f"/redfish/v1/telemetryservice/metricdefinitions"
    item = db.get_item(collection_path, metricdefinition_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_telemetryservice_metricdefinitions_metricdefinition_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/telemetryservice/metricdefinitions/{metricdefinition_id}"
            static_val["Id"] = metricdefinition_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/telemetryservice/metricdefinitions/{metricdefinition_id}", methods=["PATCH"])
def patch_redfish_v1_telemetryservice_metricdefinitions_metricdefinition_id(metricdefinition_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/telemetryservice/metricdefinitions/{metricdefinition_id}
    Type: MetricDefinition
    """
    collection_path = f"/redfish/v1/telemetryservice/metricdefinitions"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, metricdefinition_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_telemetryservice_metricdefinitions_metricdefinition_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = metricdefinition_id
            existing["@odata.id"] = f"/redfish/v1/telemetryservice/metricdefinitions/{metricdefinition_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, metricdefinition_id, existing)
    return existing

@app.api_route("/redfish/v1/telemetryservice/metricdefinitions/{metricdefinition_id}", methods=["DELETE"])
def delete_redfish_v1_telemetryservice_metricdefinitions_metricdefinition_id(metricdefinition_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/telemetryservice/metricdefinitions/{metricdefinition_id}
    Type: MetricDefinition
    """
    collection_path = f"/redfish/v1/telemetryservice/metricdefinitions"
    deleted = db.delete_item(collection_path, metricdefinition_id)
    if deleted:
        return {"message": "Deleted successfully", "id": metricdefinition_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_telemetryservice_metricdefinitions_metricdefinitget_redfish_v1_telemetryservice_metricdefinitions_metricdefinition_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": metricdefinition_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/telemetryservice/metricreportdefinitions", methods=["GET"])
def get_redfish_v1_telemetryservice_metricreportdefinitions():
    """
    iLO Redfish Endpoint: GET /redfish/v1/telemetryservice/metricreportdefinitions
    Type: Collection ofMetricReportDefinition
    """
    collection_path = "/redfish/v1/telemetryservice/metricreportdefinitions"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_telemetryservice_metricreportdefinitions", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/telemetryservice/metricreportdefinitions/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/telemetryservice/metricreportdefinitions", methods=["POST"])
def post_redfish_v1_telemetryservice_metricreportdefinitions(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/telemetryservice/metricreportdefinitions
    Type: Collection ofMetricReportDefinition
    """
    collection_path = "/redfish/v1/telemetryservice/metricreportdefinitions"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/telemetryservice/metricreportdefinitions/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/telemetryservice/metricreportdefinitions/{metricreportdefinition_id}", methods=["GET"])
def get_redfish_v1_telemetryservice_metricreportdefinitions_metricreportdefinition_id(metricreportdefinition_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/telemetryservice/metricreportdefinitions/{metricreportdefinition_id}
    Type: MetricReportDefinition
    """
    collection_path = f"/redfish/v1/telemetryservice/metricreportdefinitions"
    item = db.get_item(collection_path, metricreportdefinition_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_telemetryservice_metricreportdefinitions_metricreportdefinition_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/telemetryservice/metricreportdefinitions/{metricreportdefinition_id}"
            static_val["Id"] = metricreportdefinition_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/telemetryservice/metricreportdefinitions/{metricreportdefinition_id}", methods=["PATCH"])
def patch_redfish_v1_telemetryservice_metricreportdefinitions_metricreportdefinition_id(metricreportdefinition_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/telemetryservice/metricreportdefinitions/{metricreportdefinition_id}
    Type: MetricReportDefinition
    """
    collection_path = f"/redfish/v1/telemetryservice/metricreportdefinitions"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, metricreportdefinition_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_telemetryservice_metricreportdefinitions_metricreportdefinition_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = metricreportdefinition_id
            existing["@odata.id"] = f"/redfish/v1/telemetryservice/metricreportdefinitions/{metricreportdefinition_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, metricreportdefinition_id, existing)
    return existing

@app.api_route("/redfish/v1/telemetryservice/metricreportdefinitions/{metricreportdefinition_id}", methods=["DELETE"])
def delete_redfish_v1_telemetryservice_metricreportdefinitions_metricreportdefinition_id(metricreportdefinition_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/telemetryservice/metricreportdefinitions/{metricreportdefinition_id}
    Type: MetricReportDefinition
    """
    collection_path = f"/redfish/v1/telemetryservice/metricreportdefinitions"
    deleted = db.delete_item(collection_path, metricreportdefinition_id)
    if deleted:
        return {"message": "Deleted successfully", "id": metricreportdefinition_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_telemetryservice_metricreportdefinitions_metricreportdefinitget_redfish_v1_telemetryservice_metricreportdefinitions_metricreportdefinition_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": metricreportdefinition_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/telemetryservice/metricreports", methods=["GET"])
def get_redfish_v1_telemetryservice_metricreports():
    """
    iLO Redfish Endpoint: GET /redfish/v1/telemetryservice/metricreports
    Type: Collection ofMetricReport
    """
    collection_path = "/redfish/v1/telemetryservice/metricreports"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_telemetryservice_metricreports", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/telemetryservice/metricreports/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/telemetryservice/metricreports", methods=["POST"])
def post_redfish_v1_telemetryservice_metricreports(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/telemetryservice/metricreports
    Type: Collection ofMetricReport
    """
    collection_path = "/redfish/v1/telemetryservice/metricreports"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/telemetryservice/metricreports/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/telemetryservice/metricreports/{metricreport_id}", methods=["GET"])
def get_redfish_v1_telemetryservice_metricreports_metricreport_id(metricreport_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/telemetryservice/metricreports/{metricreport_id}
    Type: MetricReport
    """
    collection_path = f"/redfish/v1/telemetryservice/metricreports"
    item = db.get_item(collection_path, metricreport_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_telemetryservice_metricreports_metricreport_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/telemetryservice/metricreports/{metricreport_id}"
            static_val["Id"] = metricreport_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/telemetryservice/metricreports/{metricreport_id}", methods=["PATCH"])
def patch_redfish_v1_telemetryservice_metricreports_metricreport_id(metricreport_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/telemetryservice/metricreports/{metricreport_id}
    Type: MetricReport
    """
    collection_path = f"/redfish/v1/telemetryservice/metricreports"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, metricreport_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_telemetryservice_metricreports_metricreport_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = metricreport_id
            existing["@odata.id"] = f"/redfish/v1/telemetryservice/metricreports/{metricreport_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, metricreport_id, existing)
    return existing

@app.api_route("/redfish/v1/telemetryservice/metricreports/{metricreport_id}", methods=["DELETE"])
def delete_redfish_v1_telemetryservice_metricreports_metricreport_id(metricreport_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/telemetryservice/metricreports/{metricreport_id}
    Type: MetricReport
    """
    collection_path = f"/redfish/v1/telemetryservice/metricreports"
    deleted = db.delete_item(collection_path, metricreport_id)
    if deleted:
        return {"message": "Deleted successfully", "id": metricreport_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_telemetryservice_metricreports_metricrepget_redfish_v1_telemetryservice_metricreports_metricreport_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": metricreport_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/telemetryservice/triggers", methods=["GET"])
def get_redfish_v1_telemetryservice_triggers():
    """
    iLO Redfish Endpoint: GET /redfish/v1/telemetryservice/triggers
    Type: Collection ofTriggers
    """
    collection_path = "/redfish/v1/telemetryservice/triggers"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_telemetryservice_triggers", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/telemetryservice/triggers/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/telemetryservice/triggers", methods=["POST"])
def post_redfish_v1_telemetryservice_triggers(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/telemetryservice/triggers
    Type: Collection ofTriggers
    """
    collection_path = "/redfish/v1/telemetryservice/triggers"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/telemetryservice/triggers/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/telemetryservice/triggers/{trigger_id}", methods=["GET"])
def get_redfish_v1_telemetryservice_triggers_trigger_id(trigger_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/telemetryservice/triggers/{trigger_id}
    Type: Triggers
    """
    collection_path = f"/redfish/v1/telemetryservice/triggers"
    item = db.get_item(collection_path, trigger_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_telemetryservice_triggers_trigger_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/telemetryservice/triggers/{trigger_id}"
            static_val["Id"] = trigger_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/telemetryservice/triggers/{trigger_id}", methods=["PATCH"])
def patch_redfish_v1_telemetryservice_triggers_trigger_id(trigger_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/telemetryservice/triggers/{trigger_id}
    Type: Triggers
    """
    collection_path = f"/redfish/v1/telemetryservice/triggers"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, trigger_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_telemetryservice_triggers_trigger_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = trigger_id
            existing["@odata.id"] = f"/redfish/v1/telemetryservice/triggers/{trigger_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, trigger_id, existing)
    return existing

@app.api_route("/redfish/v1/telemetryservice/triggers/{trigger_id}", methods=["DELETE"])
def delete_redfish_v1_telemetryservice_triggers_trigger_id(trigger_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/telemetryservice/triggers/{trigger_id}
    Type: Triggers
    """
    collection_path = f"/redfish/v1/telemetryservice/triggers"
    deleted = db.delete_item(collection_path, trigger_id)
    if deleted:
        return {"message": "Deleted successfully", "id": trigger_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_telemetryservice_triggers_trigget_redfish_v1_telemetryservice_triggers_trigger_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": trigger_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/updateservice", methods=["GET"])
def get_redfish_v1_updateservice():
    """
    iLO Redfish Endpoint: GET /redfish/v1/updateservice
    Type: UpdateService
    """
    collection_path = "/redfish/v1/updateservice"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_updateservice", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/updateservice/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/updateservice", methods=["POST"])
def post_redfish_v1_updateservice(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/updateservice
    Type: UpdateService
    """
    collection_path = "/redfish/v1/updateservice"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/updateservice/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/updateservice/componentrepository", methods=["GET"])
def get_redfish_v1_updateservice_componentrepository():
    """
    iLO Redfish Endpoint: GET /redfish/v1/updateservice/componentrepository
    Type: Collection ofHpeComponent
    """
    collection_path = "/redfish/v1/updateservice/componentrepository"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_updateservice_componentrepository", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/updateservice/componentrepository/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/updateservice/componentrepository", methods=["POST"])
def post_redfish_v1_updateservice_componentrepository(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/updateservice/componentrepository
    Type: Collection ofHpeComponent
    """
    collection_path = "/redfish/v1/updateservice/componentrepository"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/updateservice/componentrepository/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/updateservice/componentrepository/{componentrepository_id}", methods=["GET"])
def get_redfish_v1_updateservice_componentrepository_componentrepository_id(componentrepository_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/updateservice/componentrepository/{componentrepository_id}
    Type: HpeComponent
    """
    collection_path = f"/redfish/v1/updateservice/componentrepository"
    item = db.get_item(collection_path, componentrepository_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_updateservice_componentrepository_componentrepository_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/updateservice/componentrepository/{componentrepository_id}"
            static_val["Id"] = componentrepository_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/updateservice/componentrepository/{componentrepository_id}", methods=["PATCH"])
def patch_redfish_v1_updateservice_componentrepository_componentrepository_id(componentrepository_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/updateservice/componentrepository/{componentrepository_id}
    Type: HpeComponent
    """
    collection_path = f"/redfish/v1/updateservice/componentrepository"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, componentrepository_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_updateservice_componentrepository_componentrepository_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = componentrepository_id
            existing["@odata.id"] = f"/redfish/v1/updateservice/componentrepository/{componentrepository_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, componentrepository_id, existing)
    return existing

@app.api_route("/redfish/v1/updateservice/componentrepository/{componentrepository_id}", methods=["DELETE"])
def delete_redfish_v1_updateservice_componentrepository_componentrepository_id(componentrepository_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/updateservice/componentrepository/{componentrepository_id}
    Type: HpeComponent
    """
    collection_path = f"/redfish/v1/updateservice/componentrepository"
    deleted = db.delete_item(collection_path, componentrepository_id)
    if deleted:
        return {"message": "Deleted successfully", "id": componentrepository_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_updateservice_componentrepository_componentrepositget_redfish_v1_updateservice_componentrepository_componentrepository_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": componentrepository_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/updateservice/firmwareinventory", methods=["GET"])
def get_redfish_v1_updateservice_firmwareinventory():
    """
    iLO Redfish Endpoint: GET /redfish/v1/updateservice/firmwareinventory
    Type: Collection ofSoftwareInventory
    """
    collection_path = "/redfish/v1/updateservice/firmwareinventory"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_updateservice_firmwareinventory", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/updateservice/firmwareinventory/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/updateservice/firmwareinventory", methods=["POST"])
def post_redfish_v1_updateservice_firmwareinventory(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/updateservice/firmwareinventory
    Type: Collection ofSoftwareInventory
    """
    collection_path = "/redfish/v1/updateservice/firmwareinventory"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/updateservice/firmwareinventory/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/updateservice/firmwareinventory/{firmwareinventory_id}", methods=["GET"])
def get_redfish_v1_updateservice_firmwareinventory_firmwareinventory_id(firmwareinventory_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/updateservice/firmwareinventory/{firmwareinventory_id}
    Type: SoftwareInventory
    """
    collection_path = f"/redfish/v1/updateservice/firmwareinventory"
    item = db.get_item(collection_path, firmwareinventory_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_updateservice_firmwareinventory_firmwareinventory_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/updateservice/firmwareinventory/{firmwareinventory_id}"
            static_val["Id"] = firmwareinventory_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/updateservice/firmwareinventory/{firmwareinventory_id}", methods=["PATCH"])
def patch_redfish_v1_updateservice_firmwareinventory_firmwareinventory_id(firmwareinventory_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/updateservice/firmwareinventory/{firmwareinventory_id}
    Type: SoftwareInventory
    """
    collection_path = f"/redfish/v1/updateservice/firmwareinventory"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, firmwareinventory_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_updateservice_firmwareinventory_firmwareinventory_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = firmwareinventory_id
            existing["@odata.id"] = f"/redfish/v1/updateservice/firmwareinventory/{firmwareinventory_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, firmwareinventory_id, existing)
    return existing

@app.api_route("/redfish/v1/updateservice/firmwareinventory/{firmwareinventory_id}", methods=["DELETE"])
def delete_redfish_v1_updateservice_firmwareinventory_firmwareinventory_id(firmwareinventory_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/updateservice/firmwareinventory/{firmwareinventory_id}
    Type: SoftwareInventory
    """
    collection_path = f"/redfish/v1/updateservice/firmwareinventory"
    deleted = db.delete_item(collection_path, firmwareinventory_id)
    if deleted:
        return {"message": "Deleted successfully", "id": firmwareinventory_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_updateservice_firmwareinventory_firmwareinventget_redfish_v1_updateservice_firmwareinventory_firmwareinventory_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": firmwareinventory_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/updateservice/installsets", methods=["GET"])
def get_redfish_v1_updateservice_installsets():
    """
    iLO Redfish Endpoint: GET /redfish/v1/updateservice/installsets
    Type: Collection ofHpeComponentInstallSet
    """
    collection_path = "/redfish/v1/updateservice/installsets"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_updateservice_installsets", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/updateservice/installsets/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/updateservice/installsets", methods=["POST"])
def post_redfish_v1_updateservice_installsets(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/updateservice/installsets
    Type: Collection ofHpeComponentInstallSet
    """
    collection_path = "/redfish/v1/updateservice/installsets"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/updateservice/installsets/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/updateservice/installsets/{installset_id}", methods=["GET"])
def get_redfish_v1_updateservice_installsets_installset_id(installset_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/updateservice/installsets/{installset_id}
    Type: HpeComponentInstallSet
    """
    collection_path = f"/redfish/v1/updateservice/installsets"
    item = db.get_item(collection_path, installset_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_updateservice_installsets_installset_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/updateservice/installsets/{installset_id}"
            static_val["Id"] = installset_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/updateservice/installsets/{installset_id}", methods=["PATCH"])
def patch_redfish_v1_updateservice_installsets_installset_id(installset_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/updateservice/installsets/{installset_id}
    Type: HpeComponentInstallSet
    """
    collection_path = f"/redfish/v1/updateservice/installsets"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, installset_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_updateservice_installsets_installset_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = installset_id
            existing["@odata.id"] = f"/redfish/v1/updateservice/installsets/{installset_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, installset_id, existing)
    return existing

@app.api_route("/redfish/v1/updateservice/installsets/{installset_id}", methods=["DELETE"])
def delete_redfish_v1_updateservice_installsets_installset_id(installset_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/updateservice/installsets/{installset_id}
    Type: HpeComponentInstallSet
    """
    collection_path = f"/redfish/v1/updateservice/installsets"
    deleted = db.delete_item(collection_path, installset_id)
    if deleted:
        return {"message": "Deleted successfully", "id": installset_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_updateservice_installsets_installget_redfish_v1_updateservice_installsets_installset_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": installset_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/updateservice/invalidimagerepository", methods=["GET"])
def get_redfish_v1_updateservice_invalidimagerepository():
    """
    iLO Redfish Endpoint: GET /redfish/v1/updateservice/invalidimagerepository
    Type: Collection ofHpeInvalidImage
    """
    collection_path = "/redfish/v1/updateservice/invalidimagerepository"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_updateservice_invalidimagerepository", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/updateservice/invalidimagerepository/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/updateservice/invalidimagerepository", methods=["POST"])
def post_redfish_v1_updateservice_invalidimagerepository(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/updateservice/invalidimagerepository
    Type: Collection ofHpeInvalidImage
    """
    collection_path = "/redfish/v1/updateservice/invalidimagerepository"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/updateservice/invalidimagerepository/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/updateservice/invalidimagerepository/{invalidimagerepository_id}", methods=["GET"])
def get_redfish_v1_updateservice_invalidimagerepository_invalidimagerepository_id(invalidimagerepository_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/updateservice/invalidimagerepository/{invalidimagerepository_id}
    Type: HpeInvalidImage
    """
    collection_path = f"/redfish/v1/updateservice/invalidimagerepository"
    item = db.get_item(collection_path, invalidimagerepository_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_updateservice_invalidimagerepository_invalidimagerepository_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/updateservice/invalidimagerepository/{invalidimagerepository_id}"
            static_val["Id"] = invalidimagerepository_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/updateservice/invalidimagerepository/{invalidimagerepository_id}", methods=["PATCH"])
def patch_redfish_v1_updateservice_invalidimagerepository_invalidimagerepository_id(invalidimagerepository_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/updateservice/invalidimagerepository/{invalidimagerepository_id}
    Type: HpeInvalidImage
    """
    collection_path = f"/redfish/v1/updateservice/invalidimagerepository"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, invalidimagerepository_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_updateservice_invalidimagerepository_invalidimagerepository_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = invalidimagerepository_id
            existing["@odata.id"] = f"/redfish/v1/updateservice/invalidimagerepository/{invalidimagerepository_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, invalidimagerepository_id, existing)
    return existing

@app.api_route("/redfish/v1/updateservice/invalidimagerepository/{invalidimagerepository_id}", methods=["DELETE"])
def delete_redfish_v1_updateservice_invalidimagerepository_invalidimagerepository_id(invalidimagerepository_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/updateservice/invalidimagerepository/{invalidimagerepository_id}
    Type: HpeInvalidImage
    """
    collection_path = f"/redfish/v1/updateservice/invalidimagerepository"
    deleted = db.delete_item(collection_path, invalidimagerepository_id)
    if deleted:
        return {"message": "Deleted successfully", "id": invalidimagerepository_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_updateservice_invalidimagerepository_invalidimagerepositget_redfish_v1_updateservice_invalidimagerepository_invalidimagerepository_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": invalidimagerepository_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/updateservice/maintenancewindows", methods=["GET"])
def get_redfish_v1_updateservice_maintenancewindows():
    """
    iLO Redfish Endpoint: GET /redfish/v1/updateservice/maintenancewindows
    Type: Collection ofHpeMaintenanceWindow
    """
    collection_path = "/redfish/v1/updateservice/maintenancewindows"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_updateservice_maintenancewindows", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/updateservice/maintenancewindows/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/updateservice/maintenancewindows", methods=["POST"])
def post_redfish_v1_updateservice_maintenancewindows(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/updateservice/maintenancewindows
    Type: Collection ofHpeMaintenanceWindow
    """
    collection_path = "/redfish/v1/updateservice/maintenancewindows"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/updateservice/maintenancewindows/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/updateservice/maintenancewindows/{maintenancewindow_id}", methods=["GET"])
def get_redfish_v1_updateservice_maintenancewindows_maintenancewindow_id(maintenancewindow_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/updateservice/maintenancewindows/{maintenancewindow_id}
    Type: HpeMaintenanceWindow
    """
    collection_path = f"/redfish/v1/updateservice/maintenancewindows"
    item = db.get_item(collection_path, maintenancewindow_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_updateservice_maintenancewindows_maintenancewindow_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/updateservice/maintenancewindows/{maintenancewindow_id}"
            static_val["Id"] = maintenancewindow_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/updateservice/maintenancewindows/{maintenancewindow_id}", methods=["PATCH"])
def patch_redfish_v1_updateservice_maintenancewindows_maintenancewindow_id(maintenancewindow_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/updateservice/maintenancewindows/{maintenancewindow_id}
    Type: HpeMaintenanceWindow
    """
    collection_path = f"/redfish/v1/updateservice/maintenancewindows"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, maintenancewindow_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_updateservice_maintenancewindows_maintenancewindow_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = maintenancewindow_id
            existing["@odata.id"] = f"/redfish/v1/updateservice/maintenancewindows/{maintenancewindow_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, maintenancewindow_id, existing)
    return existing

@app.api_route("/redfish/v1/updateservice/maintenancewindows/{maintenancewindow_id}", methods=["DELETE"])
def delete_redfish_v1_updateservice_maintenancewindows_maintenancewindow_id(maintenancewindow_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/updateservice/maintenancewindows/{maintenancewindow_id}
    Type: HpeMaintenanceWindow
    """
    collection_path = f"/redfish/v1/updateservice/maintenancewindows"
    deleted = db.delete_item(collection_path, maintenancewindow_id)
    if deleted:
        return {"message": "Deleted successfully", "id": maintenancewindow_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_updateservice_maintenancewindows_maintenancewinget_redfish_v1_updateservice_maintenancewindows_maintenancewindow_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": maintenancewindow_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/updateservice/runningsoftwareinventory", methods=["GET"])
def get_redfish_v1_updateservice_runningsoftwareinventory():
    """
    iLO Redfish Endpoint: GET /redfish/v1/updateservice/runningsoftwareinventory
    Type: Collection ofHpeiLORunningSoftwareInventory
    """
    collection_path = "/redfish/v1/updateservice/runningsoftwareinventory"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_updateservice_runningsoftwareinventory", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/updateservice/runningsoftwareinventory/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/updateservice/runningsoftwareinventory", methods=["POST"])
def post_redfish_v1_updateservice_runningsoftwareinventory(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/updateservice/runningsoftwareinventory
    Type: Collection ofHpeiLORunningSoftwareInventory
    """
    collection_path = "/redfish/v1/updateservice/runningsoftwareinventory"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/updateservice/runningsoftwareinventory/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/updateservice/runningsoftwareinventory/{runningsoftwareinventory_id}", methods=["GET"])
def get_redfish_v1_updateservice_runningsoftwareinventory_runningsoftwareinventory_id(runningsoftwareinventory_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/updateservice/runningsoftwareinventory/{runningsoftwareinventory_id}
    Type: HpeiLORunningSoftwareInventory
    """
    collection_path = f"/redfish/v1/updateservice/runningsoftwareinventory"
    item = db.get_item(collection_path, runningsoftwareinventory_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_updateservice_runningsoftwareinventory_runningsoftwareinventory_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/updateservice/runningsoftwareinventory/{runningsoftwareinventory_id}"
            static_val["Id"] = runningsoftwareinventory_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/updateservice/runningsoftwareinventory/{runningsoftwareinventory_id}", methods=["PATCH"])
def patch_redfish_v1_updateservice_runningsoftwareinventory_runningsoftwareinventory_id(runningsoftwareinventory_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/updateservice/runningsoftwareinventory/{runningsoftwareinventory_id}
    Type: HpeiLORunningSoftwareInventory
    """
    collection_path = f"/redfish/v1/updateservice/runningsoftwareinventory"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, runningsoftwareinventory_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_updateservice_runningsoftwareinventory_runningsoftwareinventory_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = runningsoftwareinventory_id
            existing["@odata.id"] = f"/redfish/v1/updateservice/runningsoftwareinventory/{runningsoftwareinventory_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, runningsoftwareinventory_id, existing)
    return existing

@app.api_route("/redfish/v1/updateservice/runningsoftwareinventory/{runningsoftwareinventory_id}", methods=["DELETE"])
def delete_redfish_v1_updateservice_runningsoftwareinventory_runningsoftwareinventory_id(runningsoftwareinventory_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/updateservice/runningsoftwareinventory/{runningsoftwareinventory_id}
    Type: HpeiLORunningSoftwareInventory
    """
    collection_path = f"/redfish/v1/updateservice/runningsoftwareinventory"
    deleted = db.delete_item(collection_path, runningsoftwareinventory_id)
    if deleted:
        return {"message": "Deleted successfully", "id": runningsoftwareinventory_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_updateservice_runningsoftwareinventory_runningsoftwareinventget_redfish_v1_updateservice_runningsoftwareinventory_runningsoftwareinventory_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": runningsoftwareinventory_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/updateservice/softwareinventory", methods=["GET"])
def get_redfish_v1_updateservice_softwareinventory():
    """
    iLO Redfish Endpoint: GET /redfish/v1/updateservice/softwareinventory
    Type: Collection ofSoftwareInventory
    """
    collection_path = "/redfish/v1/updateservice/softwareinventory"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_updateservice_softwareinventory", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/updateservice/softwareinventory/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/updateservice/softwareinventory", methods=["POST"])
def post_redfish_v1_updateservice_softwareinventory(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/updateservice/softwareinventory
    Type: Collection ofSoftwareInventory
    """
    collection_path = "/redfish/v1/updateservice/softwareinventory"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/updateservice/softwareinventory/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/updateservice/softwareinventory/{softwareinventory_id}", methods=["GET"])
def get_redfish_v1_updateservice_softwareinventory_softwareinventory_id(softwareinventory_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/updateservice/softwareinventory/{softwareinventory_id}
    Type: SoftwareInventory
    """
    collection_path = f"/redfish/v1/updateservice/softwareinventory"
    item = db.get_item(collection_path, softwareinventory_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_updateservice_softwareinventory_softwareinventory_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/updateservice/softwareinventory/{softwareinventory_id}"
            static_val["Id"] = softwareinventory_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/updateservice/softwareinventory/{softwareinventory_id}", methods=["PATCH"])
def patch_redfish_v1_updateservice_softwareinventory_softwareinventory_id(softwareinventory_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/updateservice/softwareinventory/{softwareinventory_id}
    Type: SoftwareInventory
    """
    collection_path = f"/redfish/v1/updateservice/softwareinventory"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, softwareinventory_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_updateservice_softwareinventory_softwareinventory_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = softwareinventory_id
            existing["@odata.id"] = f"/redfish/v1/updateservice/softwareinventory/{softwareinventory_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, softwareinventory_id, existing)
    return existing

@app.api_route("/redfish/v1/updateservice/softwareinventory/{softwareinventory_id}", methods=["DELETE"])
def delete_redfish_v1_updateservice_softwareinventory_softwareinventory_id(softwareinventory_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/updateservice/softwareinventory/{softwareinventory_id}
    Type: SoftwareInventory
    """
    collection_path = f"/redfish/v1/updateservice/softwareinventory"
    deleted = db.delete_item(collection_path, softwareinventory_id)
    if deleted:
        return {"message": "Deleted successfully", "id": softwareinventory_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_updateservice_softwareinventory_softwareinventget_redfish_v1_updateservice_softwareinventory_softwareinventory_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": softwareinventory_id}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/updateservice/updatetaskqueue", methods=["GET"])
def get_redfish_v1_updateservice_updatetaskqueue():
    """
    iLO Redfish Endpoint: GET /redfish/v1/updateservice/updatetaskqueue
    Type: Collection ofHpeComponentUpdateTask
    """
    collection_path = "/redfish/v1/updateservice/updatetaskqueue"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_redfish_v1_updateservice_updatetaskqueue", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        if "Members" not in res:
            res["Members"] = []
        res["Members"] = list(res["Members"])
        existing = {m.get("@odata.id") for m in res["Members"] if isinstance(m, dict)}
        for item in dynamic_items:
            item_id = item.get("id") or item.get("Id")
            item_url = item.get("@odata.id") or f"/redfish/v1/updateservice/updatetaskqueue/{item_id}"
            if item_url not in existing:
                res["Members"].append({"@odata.id": item_url})
        res["Members@odata.count"] = len(res["Members"])
        return res
    return static_val

@app.api_route("/redfish/v1/updateservice/updatetaskqueue", methods=["POST"])
def post_redfish_v1_updateservice_updatetaskqueue(payload: dict = None):
    """
    iLO Redfish Endpoint: POST /redfish/v1/updateservice/updatetaskqueue
    Type: Collection ofHpeComponentUpdateTask
    """
    collection_path = "/redfish/v1/updateservice/updatetaskqueue"
    payload_dict = payload if payload is not None else {}
    item_id = str(payload_dict.get("Id") or payload_dict.get("id") or payload_dict.get("UserName") or payload_dict.get("Name") or len(db.get_all(collection_path)) + 1)
    payload_dict["Id"] = item_id
    payload_dict["id"] = item_id
    payload_dict["@odata.id"] = f"/redfish/v1/updateservice/updatetaskqueue/{item_id}"
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/redfish/v1/updateservice/updatetaskqueue/{updatetaskqueue_id}", methods=["GET"])
def get_redfish_v1_updateservice_updatetaskqueue_updatetaskqueue_id(updatetaskqueue_id: str):
    """
    iLO Redfish Endpoint: GET /redfish/v1/updateservice/updatetaskqueue/{updatetaskqueue_id}
    Type: HpeComponentUpdateTask
    """
    collection_path = f"/redfish/v1/updateservice/updatetaskqueue"
    item = db.get_item(collection_path, updatetaskqueue_id)
    if item:
        return item
    static_val = db.get_static("get_redfish_v1_updateservice_updatetaskqueue_updatetaskqueue_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            static_val["@odata.id"] = f"/redfish/v1/updateservice/updatetaskqueue/{updatetaskqueue_id}"
            static_val["Id"] = updatetaskqueue_id
            return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/redfish/v1/updateservice/updatetaskqueue/{updatetaskqueue_id}", methods=["PATCH"])
def patch_redfish_v1_updateservice_updatetaskqueue_updatetaskqueue_id(updatetaskqueue_id: str, payload: dict = None):
    """
    iLO Redfish Endpoint: PATCH /redfish/v1/updateservice/updatetaskqueue/{updatetaskqueue_id}
    Type: HpeComponentUpdateTask
    """
    collection_path = f"/redfish/v1/updateservice/updatetaskqueue"
    payload_dict = payload if payload is not None else {}
    existing = db.get_item(collection_path, updatetaskqueue_id) or {}
    if not existing:
        static_val = db.get_static("patch_redfish_v1_updateservice_updatetaskqueue_updatetaskqueue_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = updatetaskqueue_id
            existing["@odata.id"] = f"/redfish/v1/updateservice/updatetaskqueue/{updatetaskqueue_id}"
    existing.update(payload_dict)
    db.upsert_item(collection_path, updatetaskqueue_id, existing)
    return existing

@app.api_route("/redfish/v1/updateservice/updatetaskqueue/{updatetaskqueue_id}", methods=["DELETE"])
def delete_redfish_v1_updateservice_updatetaskqueue_updatetaskqueue_id(updatetaskqueue_id: str):
    """
    iLO Redfish Endpoint: DELETE /redfish/v1/updateservice/updatetaskqueue/{updatetaskqueue_id}
    Type: HpeComponentUpdateTask
    """
    collection_path = f"/redfish/v1/updateservice/updatetaskqueue"
    deleted = db.delete_item(collection_path, updatetaskqueue_id)
    if deleted:
        return {"message": "Deleted successfully", "id": updatetaskqueue_id, "item": deleted}
    # If not in dynamic store, try static check (simulated deletion)
    static_val = db.get_static("delete_redfish_v1_updateservice_updatetaskqueue_updatetaskquget_redfish_v1_updateservice_updatetaskqueue_updatetaskqueue_id")
    if static_val:
        static_val = dict(static_val)
        if True: # Bypass strict ID check
            return {"message": "Deleted successfully (static default removal simulated)", "id": updatetaskqueue_id}
    raise HTTPException(status_code=404, detail="Resource not found")


@app.post("/redfish/v1/systems/{system_id}")
@app.post("/redfish/v1/systems/{system_id}/actions/computersystem.reset")
@app.post("/redfish/v1/systems/{system_id}/Actions/ComputerSystem.Reset")
def post_redfish_v1_systems_system_id(system_id: str, payload: dict = None):
    collection_path = f"/redfish/v1/systems"
    payload_dict = payload if payload is not None else {}
    reset_type = payload_dict.get("ResetType") or payload_dict.get("powerState") or "On"

    # Map ResetType to PowerState
    if reset_type.lower() in ("forceoff", "gracefulshutdown", "off"):
        new_power_state = "Off"
    else:
        new_power_state = "On"

    # Simulate hardware power transition delay
    import time
    time.sleep(5)

    existing = db.get_item(collection_path, system_id) or {}
    if not existing:
        static_val = db.get_static("get_redfish_v1_systems_system_id")
        if static_val:
            existing = dict(static_val)
            existing["Id"] = system_id
            existing["@odata.id"] = f"/redfish/v1/systems/{system_id}"

    existing["PowerState"] = new_power_state   # Redfish standard field — single source of truth
    existing.pop("power_state", None)           # Remove stale duplicate if present
    db.upsert_item(collection_path, system_id, existing)
    return {"status": "success", "ResetType": reset_type, "PowerState": new_power_state}

