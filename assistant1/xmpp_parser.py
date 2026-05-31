import re


def extract_message(xml):

    body = re.search(
        r"<body>(.*?)</body>",
        xml,
        re.DOTALL
    )

    if not body:
        return None

    msg_id = re.search(
        r"id='([^']+)'",
        xml
    )

    sender = re.search(
        r"from='([^']+)'",
        xml
    )

    return {
        "id": msg_id.group(1) if msg_id else None,
        "from": sender.group(1) if sender else None,
        "body": body.group(1)
    }