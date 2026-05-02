from typing import Any, List, Dict
import os
import sys
import urllib3
from pathlib import Path

import requests
from mcp.server.fastmcp import FastMCP

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from unifi.transport import IntegrationTransport  # noqa: E402

# Configuration
UNIFI_API_KEY = os.getenv("UNIFI_API_KEY", "CHANGEME")
UNIFI_GATEWAY_HOST = os.getenv("UNIFI_GATEWAY_HOST", "192.168.1.1")
UNIFI_GATEWAY_PORT = os.getenv("UNIFI_GATEWAY_PORT", "443")

# Suppress TLS warnings for self-signed UniFi gateway cert
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_session = requests.Session()
_session.verify = False

_transport = IntegrationTransport(
    host=f"https://{UNIFI_GATEWAY_HOST}:{UNIFI_GATEWAY_PORT}",
    api_key=UNIFI_API_KEY,
    session=_session,
)

# Initialize FastMCP server
mcp = FastMCP("unifi")


@mcp.resource("sites://")
async def list_sites() -> List[Dict[str, Any]]:
    """List all sites in the Unifi controller"""
    return _transport.paginate("/sites")


@mcp.resource("sites://{site_id}/devices")
async def list_devices(site_id: str) -> List[Dict[str, Any]]:
    """List all devices in a specific Unifi site"""
    return _transport.paginate(f"/sites/{site_id}/devices")


@mcp.resource("sites://{site_id}/devices/{device_id}")
async def get_device_details(site_id: str, device_id: str) -> Dict[str, Any]:
    """Get details for a specific device in a Unifi site"""
    return _transport.request(f"/sites/{site_id}/devices/{device_id}") or {}


@mcp.resource("sites://{site_id}/devices/{device_id}/statistics")
async def get_device_statistics(site_id: str, device_id: str) -> Dict[str, Any]:
    """Get the latest statistics for a specific device in a Unifi site"""
    return _transport.request(f"/sites/{site_id}/devices/{device_id}/statistics/latest") or {}


@mcp.resource("sites://{site_id}/clients")
async def list_clients(site_id: str) -> List[Dict[str, Any]]:
    """List all connected clients in a specific Unifi site.

    Clients can be physical devices (computers, smartphones) or active VPN connections.
    """
    return _transport.paginate(f"/sites/{site_id}/clients")


if __name__ == "__main__":
    mcp.run(transport='stdio')
