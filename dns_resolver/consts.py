from enum import Enum


UDP_MESSAGE_SIZE = 512

class RRType(Enum):
    A = 'A'
    CNAME = 'CNAME'
    MX = 'MX'
    TXT = 'TXT'
