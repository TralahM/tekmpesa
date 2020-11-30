"""Handle Parsing of XML Content into JSON."""
from lxml import etree


def parse_login_response(content):
    """Return python `dict` from parsed Login response XML content."""
    print(content)
    base = etree.fromstring(content)
    header, root = base.getchildren()
    event_id = header.getchildren()[0].text.split("\n")[0]
    code = root.xpath("//eventInfo/code")[0]
    description = root.xpath("//eventInfo/description")[0]
    detail = root.xpath("//eventInfo/detail")[0]
    transactionID = root.xpath("//eventInfo/transactionID")[0]
    token = base.xpath("//response/dataItem/value")[0]
    js_out = {k.tag: k.text for k in [
        code, description, detail, transactionID]}
    js_out.update({"token": token.text})
    js_out.update({"event_id": event_id})
    return js_out


def parse_c2b_response(content):
    """Return python `dict` from parsed C2B response XML content."""
    print(content)
    root = etree.fromstring(content)
    header, body = root.getchildren()
    event_id = header.getchildren()[0].text.split("\n")[0]
    code = body.xpath("//eventInfo/code")[0]
    description = root.xpath("//eventInfo/description")[0]
    detail = body.xpath("//eventInfo/detail")[0]
    transactionID = root.xpath("//eventInfo/transactionID")[0]
    js_out = {"event_id": event_id}
    keys = []
    for dataItem in root.xpath("//dataItem"):
        name, t, value = dataItem.getchildren()
        keys.append({name.text: value.text})
    oks = [{i.tag: i.text} for i in [code, description, detail, transactionID]]
    new = oks + keys
    [js_out.update(ks) for ks in new]
    return js_out


def parse_b2c_response(content):
    """Return python `dict` from parsed B2C response XML content."""
    print(content)
    root = etree.fromstring(content)
    header, body = root.getchildren()
    event_id = header.getchildren()[0].text.split("\n")[0]
    code = body.xpath("//eventInfo/code")[0]
    description = root.xpath("//eventInfo/description")[0]
    detail = body.xpath("//eventInfo/detail")[0]
    transactionID = root.xpath("//eventInfo/transactionID")[0]
    js_out = {"event_id": event_id}
    keys = []
    for dataItem in root.xpath("//dataItem"):
        name, t, value = dataItem.getchildren()
        keys.append({name.text: value.text})
    oks = [{i.tag: i.text} for i in [code, description, detail, transactionID]]
    new = oks + keys
    [js_out.update(ks) for ks in new]
    return js_out


def parse_c2b_callback(content):
    """Return python `dict` from parsed C2B Callback XML content."""
    print(content)
    root = etree.fromstring(content)
    js_out = {}
    keys = []
    for dataItem in root.xpath("//dataItem"):
        name, t, value = dataItem.getchildren()
        keys.append({name.text: t.text})
    [js_out.update(ks) for ks in keys]
    return js_out


def parse_b2c_callback(content):
    """Return python `dict` from parsed B2C Callback XML content."""
    print(content)
    root = etree.fromstring(content)
    js_out = {}
    keys = []
    for dataItem in root.xpath("//dataItem"):
        name, t, value = dataItem.getchildren()
        keys.append({name.text: t.text})
    [js_out.update(ks) for ks in keys]
    return js_out
