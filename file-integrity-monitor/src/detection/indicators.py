import ipaddress
import re


IPV4_PATTERN = re.compile(r"\b" r"(?:" r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)" r"\." r"){3}" r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)" r"\b")


def extract_ipv4_addresses(text: str) -> list[str]:

    addresses = IPV4_PATTERN.findall(text)

    return list(dict.fromkeys(addresses))


def classify_ipv4(address: str) -> str:


    ip = ipaddress.ip_address(address)

    if ip.is_private:
        return "private"

    if ip.is_loopback:
        return "loopback"

    if ip.is_link_local:
        return "link_local"

    if ip.is_reserved:
        return "reserved"

    return "public"


def extract_public_ipv4_addresses(text: str) -> list[str]:

    addresses = extract_ipv4_addresses(text)

    return [
        address
        for address in addresses
        if classify_ipv4(address) == "public"
    ]