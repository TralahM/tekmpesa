"""Request Parser Module.

Parse XML Responses to Json that is structured and more useful.
+ process_b2c_request
+ process_c2b_request
+ process_login_request
root key is S:Envelope
both have S:Header,S:Body
S:Header>ns3:eventid>#text
S:Body>ns2:getGenericResultResponse>SOAPAPIResult
from SOAPAPIResult we have eventInfo, request,response
All request have dataItem as List
both c2b and b2c response have dataItem as List
login response has dataItem as Dict
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


def prepare_content(content: bytes) -> dict:
    """Prepare Content for consumption."""
    root_key = "S:Envelope"
    body_key = "S:Body"
    header_key = "S:Header"
    bodyResResponse = "ns2:getGenericResultResponse"
    bodySoapResult = "SOAPAPIResult"
    if not isinstance(content, bytes):
        content = content.encode()
    payload = json.loads(json.dumps(xmltodict.parse(content)))
    event_id = payload.get(root_key).get(
        header_key).get("ns3:eventid").get("#text")
    mainBody = (
        payload.get(root_key).get(body_key).get(
            bodyResResponse).get(bodySoapResult)
    )
    eventInfo = mainBody.get("eventInfo")
    request = mainBody.get("request").get("dataItem")
    response = mainBody.get("response").get("dataItem")
    eventInfo["event_id"] = event_id
    output = {}
    output.update(eventInfo)
    output.update(data_items_to_map(request))
    output.update(data_items_to_map(response))
    return output
