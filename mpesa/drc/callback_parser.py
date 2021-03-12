"""Callback Parser Module.

To parse the callbacks of b2c and c2b.
    rootKey="soapenv:Envelope"
    bodyKey="soapenv:Body"
    resKey="gen:getGenericResult"
    reqKey="Request"#>>dataItem
"""
import xmltodict
import json


def data_items_to_map(data):
    """Convert Data Items to map."""
    if isinstance(data, dict):
        return {data.get("name"): data.get("value")}
    elif isinstance(data, list):
        out = {}
        for d in data:
            out.update({d.get("name"): d.get("value")})
        return out


def prepare_callback(content: bytes) -> dict:
    """Prepare callback as dict."""
    rootKey = "soapenv:Envelope"
    bodyKey = "soapenv:Body"
    resKey = "gen:getGenericResult"
    reqKey = "Request"  # >>dataItem
    if not isinstance(content, bytes):
        content = content.encode()
    payload = json.loads(json.dumps(xmltodict.parse(content)))
    request = payload.get(rootKey).get(bodyKey).get(
        resKey).get(reqKey).get("dataItem")
    return data_items_to_map(request)
