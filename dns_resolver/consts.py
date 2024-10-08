from enum import Enum

DEFAULT_TTL = 600
UDP_MESSAGE_SIZE = 512

class RRType(Enum):
    A = 'A'
    CNAME = 'CNAME'
    MX = 'MX'
    TXT = 'TXT'
