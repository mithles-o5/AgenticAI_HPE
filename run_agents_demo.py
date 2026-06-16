#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_agents_demo.py — Local validation demo for all three OASF agent microservices.

What this does:
  1. Installs required packages (fastapi, uvicorn, httpx, tenacity, pydantic-settings).
  2. Starts Cloud Agent  (:8005), Network Agent (:8006), Storage Agent (:8007) as subprocesses.
  3. Runs a suite of HTTP tests against each agent's endpoints.
  4. Prints a summary and exits.

Usage:
  python run_agents_demo.py
"""

import os
import sys
import time
import json
import subprocess
import signal
import threading

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import httpx

# ── Settings ──────────────────────────────────────────────────────────────────
AGENTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents")

AGENTS = [
    {"name": "cloud-agent",   "dir": "cloud_agent",   "port": 8005, "prefix": "/cloud-agent"},
    {"name": "network-agent", "dir": "network_agent",  "port": 8006, "prefix": "/network-agent"},
    {"name": "storage-agent", "dir": "storage_agent",  "port": 8007, "prefix": "/storage-agent"},
]

STARTUP_WAIT = 6      # seconds to wait for agents to start
REQUEST_TIMEOUT = 10  # seconds


# ── Colours ───────────────────────────────────────────────────────────────────
def _green(s): return f"\033[92m{s}\033[0m"
def _red(s):   return f"\033[91m{s}\033[0m"
def _cyan(s):  return f"\033[96m{s}\033[0m"
def _bold(s):  return f"\033[1m{s}\033[0m"


# ── Install dependencies ───────────────────────────────────────────────────────
def install_deps():
    packages = [
        "fastapi", "uvicorn[standard]", "httpx", "tenacity",
        "pydantic-settings", "apscheduler", "networkx",
    ]
    print(_cyan("[INFO] Installing/verifying dependencies ..."))
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--quiet", *packages],
        stdout=subprocess.DEVNULL,
    )
    print(_green("[OK] Dependencies ready.\n"))


# ── Start agents ───────────────────────────────────────────────────────────────
_procs: list[subprocess.Popen] = []


def start_agents():
    for agent in AGENTS:
        agent_dir = os.path.join(AGENTS_DIR, agent["dir"])
        cmd = [
            sys.executable, "-m", "uvicorn",
            "main:app",
            "--host", "127.0.0.1",
            "--port", str(agent["port"]),
            "--log-level", "warning",
        ]
        proc = subprocess.Popen(
            cmd,
            cwd=agent_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        _procs.append(proc)
        print(f"  [>] Started {_bold(agent['name'])} (PID {proc.pid}) on :{agent['port']}")

    print(f"\n[INFO] Waiting {STARTUP_WAIT}s for agents to initialize ...\n")
    time.sleep(STARTUP_WAIT)


def stop_agents():
    for proc in _procs:
        try:
            proc.terminate()
            proc.wait(timeout=3)
        except Exception:
            proc.kill()
    print("\n[STOP] All agent processes stopped.")


# ── Test runner ────────────────────────────────────────────────────────────────

def run_test(label: str, method: str, url: str, payload: dict = None) -> bool:
    try:
        with httpx.Client(timeout=REQUEST_TIMEOUT) as client:
            if method == "GET":
                resp = client.get(url)
            else:
                resp = client.post(url, json=payload)

        ok = resp.status_code == 200
        body = resp.json()
        icon = _green("[OK]") if ok else _red("[FAIL]")
        print(f"  {icon}  {label}")
        if not ok:
            print(f"       Status: {resp.status_code} | Body: {body}")
        else:
            # Print key result fields
            for field in ["status", "status_level", "protocols", "providers"]:
                if field in body:
                    print(f"       {field}: {body[field]}")
        return ok
    except Exception as exc:
        print(f"  {_red('[FAIL]')}  {label} - ERROR: {exc}")
        return False


def run_all_tests() -> tuple[int, int]:
    passed = failed = 0

    print(_bold(_cyan("\n══════════════════════════════════════════════════")))
    print(_bold(_cyan("  Cloud Agent Tests  (port 8005)")))
    print(_bold(_cyan("══════════════════════════════════════════════════")))

    tests = [
        ("Health check",           "GET",  "http://127.0.0.1:8005/cloud-agent/health"),
        ("List providers",         "GET",  "http://127.0.0.1:8005/cloud-agent/providers"),
        ("fetch_metrics (mock)",   "POST", "http://127.0.0.1:8005/cloud-agent/execute-task", {
            "task_id": "demo-c1", "task_type": "monitoring", "resource_type": "vm",
            "resource_id": "demo-vm-001", "provider": "mock", "action": "fetch_metrics"}),
        ("health_check (mock)",    "POST", "http://127.0.0.1:8005/cloud-agent/execute-task", {
            "task_id": "demo-c2", "task_type": "health_check", "resource_type": "vm",
            "resource_id": "demo-vm-002", "provider": "mock", "action": "health_check"}),
        ("discover_resources",     "POST", "http://127.0.0.1:8005/cloud-agent/execute-task", {
            "task_id": "demo-c3", "task_type": "discovery", "resource_type": "vm",
            "resource_id": "n/a", "provider": "mock", "action": "discover_resources",
            "parameters": {"limit": 3}}),
        ("detect_anomaly",         "POST", "http://127.0.0.1:8005/cloud-agent/execute-task", {
            "task_id": "demo-c4", "task_type": "anomaly", "resource_type": "vm",
            "resource_id": "demo-vm-003", "provider": "mock", "action": "detect_anomaly"}),
        ("Bad provider - failed",  "POST", "http://127.0.0.1:8005/cloud-agent/execute-task", {
            "task_id": "demo-c5", "task_type": "monitoring", "resource_type": "vm",
            "resource_id": "x", "provider": "nonexistent", "action": "fetch_metrics"}),
    ]
    for args in tests:
        label, method, url, *rest = args
        result = run_test(label, method, url, rest[0] if rest else None)
        if result:
            passed += 1
        else:
            failed += 1

    print(_bold(_cyan("\n══════════════════════════════════════════════════")))
    print(_bold(_cyan("  Network Agent Tests  (port 8006)")))
    print(_bold(_cyan("══════════════════════════════════════════════════")))

    net_tests = [
        ("Health check",                 "GET",  "http://127.0.0.1:8006/network-agent/health"),
        ("List protocols",               "GET",  "http://127.0.0.1:8006/network-agent/protocols"),
        ("fetch_metrics (mock)",         "POST", "http://127.0.0.1:8006/network-agent/execute-task", {
            "task_id": "demo-n1", "task_type": "monitoring", "resource_type": "switch",
            "resource_id": "sw-demo-001", "protocol": "mock", "action": "fetch_metrics"}),
        ("discover_topology",            "POST", "http://127.0.0.1:8006/network-agent/execute-task", {
            "task_id": "demo-n2", "task_type": "discovery", "resource_type": "switch",
            "resource_id": "sw-demo-002", "protocol": "mock", "action": "discover_topology"}),
        ("execute_config_push",          "POST", "http://127.0.0.1:8006/network-agent/execute-task", {
            "task_id": "demo-n3", "task_type": "config_push", "resource_type": "switch",
            "resource_id": "sw-demo-003", "protocol": "mock", "action": "execute_config_push",
            "parameters": {"config": {"vlan": 100, "name": "DEMO-VLAN"}}}),
        ("health_check",                 "POST", "http://127.0.0.1:8006/network-agent/execute-task", {
            "task_id": "demo-n4", "task_type": "health_check", "resource_type": "router",
            "resource_id": "r-demo-001", "protocol": "mock", "action": "health_check"}),
        ("detect_fault",                 "POST", "http://127.0.0.1:8006/network-agent/execute-task", {
            "task_id": "demo-n5", "task_type": "fault_detection", "resource_type": "switch",
            "resource_id": "sw-demo-004", "protocol": "mock", "action": "detect_fault"}),
    ]
    for args in net_tests:
        label, method, url, *rest = args
        result = run_test(label, method, url, rest[0] if rest else None)
        if result:
            passed += 1
        else:
            failed += 1

    print(_bold(_cyan("\n══════════════════════════════════════════════════")))
    print(_bold(_cyan("  Storage Agent Tests  (port 8007)")))
    print(_bold(_cyan("══════════════════════════════════════════════════")))

    stor_tests = [
        ("Health check",           "GET",  "http://127.0.0.1:8007/storage-agent/health"),
        ("List providers",         "GET",  "http://127.0.0.1:8007/storage-agent/providers"),
        ("fetch_capacity (mock)",  "POST", "http://127.0.0.1:8007/storage-agent/execute-task", {
            "task_id": "demo-s1", "task_type": "monitoring", "resource_type": "volume",
            "resource_id": "vol-demo-001", "provider": "mock", "action": "fetch_capacity"}),
        ("fetch_performance",      "POST", "http://127.0.0.1:8007/storage-agent/execute-task", {
            "task_id": "demo-s2", "task_type": "monitoring", "resource_type": "volume",
            "resource_id": "vol-demo-002", "provider": "mock", "action": "fetch_performance"}),
        ("discover_arrays",        "POST", "http://127.0.0.1:8007/storage-agent/execute-task", {
            "task_id": "demo-s3", "task_type": "discovery", "resource_type": "array",
            "resource_id": "n/a", "provider": "mock", "action": "discover_arrays",
            "parameters": {"limit": 3}}),
        ("poll (cap+perf+anomaly)","POST", "http://127.0.0.1:8007/storage-agent/execute-task", {
            "task_id": "demo-s4", "task_type": "poll", "resource_type": "volume",
            "resource_id": "vol-demo-003", "provider": "mock", "action": "poll"}),
        ("health_check",           "POST", "http://127.0.0.1:8007/storage-agent/execute-task", {
            "task_id": "demo-s5", "task_type": "health_check", "resource_type": "array",
            "resource_id": "arr-demo-001", "provider": "mock", "action": "health_check"}),
    ]
    for args in stor_tests:
        label, method, url, *rest = args
        result = run_test(label, method, url, rest[0] if rest else None)
        if result:
            passed += 1
        else:
            failed += 1

    return passed, failed


# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(_bold("\n*** OASF Agent Microservices - Local Demo ***\n"))

    install_deps()

    print(_cyan("[INFO] Starting agent microservices ...\n"))
    start_agents()

    try:
        passed, failed = run_all_tests()
    finally:
        stop_agents()

    total = passed + failed
    print(_bold(_cyan("\n══════════════════════════════════════════════════")))
    print(_bold(f"  Results: {_green(str(passed))} passed / {_red(str(failed))} failed / {total} total"))
    print(_bold(_cyan("══════════════════════════════════════════════════\n")))

    sys.exit(0 if failed == 0 else 1)
