"""Tests for mcp-server-unifi/main.py resources."""
import asyncio

import main


def _run(coro):
    return asyncio.run(coro)


class TestListSites:
    def test_delegates_to_paginate(self, mock_transport):
        mock_transport.paginate.return_value = [{"id": "default", "name": "Default"}]
        result = _run(main.list_sites())
        mock_transport.paginate.assert_called_once_with("/sites")
        assert result == [{"id": "default", "name": "Default"}]

    def test_returns_empty_list_when_no_sites(self, mock_transport):
        mock_transport.paginate.return_value = []
        assert _run(main.list_sites()) == []


class TestListDevices:
    def test_delegates_to_paginate(self, mock_transport):
        mock_transport.paginate.return_value = [{"id": "d1", "model": "UAP"}]
        result = _run(main.list_devices("abc123"))
        mock_transport.paginate.assert_called_once_with("/sites/abc123/devices")
        assert result == [{"id": "d1", "model": "UAP"}]

    def test_site_id_in_path(self, mock_transport):
        _run(main.list_devices("site42"))
        call_path = mock_transport.paginate.call_args[0][0]
        assert "site42" in call_path


class TestGetDeviceDetails:
    def test_delegates_to_request(self, mock_transport):
        mock_transport.request.return_value = {"id": "d1", "name": "UDM Pro"}
        result = _run(main.get_device_details("site1", "d1"))
        mock_transport.request.assert_called_once_with("/sites/site1/devices/d1")
        assert result == {"id": "d1", "name": "UDM Pro"}

    def test_returns_empty_dict_on_transport_none(self, mock_transport):
        mock_transport.request.return_value = None
        result = _run(main.get_device_details("site1", "d1"))
        assert result == {}


class TestGetDeviceStatistics:
    def test_delegates_to_request(self, mock_transport):
        mock_transport.request.return_value = {"cpu": 5.2, "mem": 38.0}
        result = _run(main.get_device_statistics("site1", "d1"))
        mock_transport.request.assert_called_once_with(
            "/sites/site1/devices/d1/statistics/latest"
        )
        assert result == {"cpu": 5.2, "mem": 38.0}

    def test_returns_empty_dict_on_transport_none(self, mock_transport):
        mock_transport.request.return_value = None
        result = _run(main.get_device_statistics("site1", "d1"))
        assert result == {}


class TestListClients:
    def test_delegates_to_paginate(self, mock_transport):
        mock_transport.paginate.return_value = [{"id": "c1", "ip": "10.0.0.5"}]
        result = _run(main.list_clients("site1"))
        mock_transport.paginate.assert_called_once_with("/sites/site1/clients")
        assert result == [{"id": "c1", "ip": "10.0.0.5"}]

    def test_returns_empty_list_on_empty_result(self, mock_transport):
        mock_transport.paginate.return_value = []
        assert _run(main.list_clients("site1")) == []
