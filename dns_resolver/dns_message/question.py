from dataclasses import dataclass


@dataclass
class DNSQuestion:
    qname: str
    qtype: int
    qclass: int
