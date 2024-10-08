from dataclasses import dataclass
import struct

@dataclass
class DNSHeader:
    id: int
    qr: int
    opcode: int
    aa: int
    tc: int
    rd: int
    ra: int
    z:int
    rcode:int
    qdcount: int
    ancount: int
    nscount: int
    arcount: int

    @staticmethod
    def from_bytes(data: bytes):
        id, flags, qdcount, ancount, nscount, arcount = struct.unpack('!HHHHHH', data[:12])
        return DNSHeader(
            id=id,
            qr=(flags >> 15) & 0x1,
            opcode=(flags >> 11) & 0xF,
            aa=(flags >> 10) & 0x1,
            tc=(flags >> 9) & 0x1,
            rd=(flags >> 8) & 0x1,
            ra=(flags >> 7) & 0x1,
            z=(flags >> 4) & 0x7,
            rcode = flags & 0xF,
            qdcount=qdcount,
            ancount=ancount,
            nscount=nscount,
            arcount=arcount
        )

    def to_bytes(self) -> bytes:
        flags = (self.qr << 15) \
        | (self.opcode << 11) \
        | (self.aa << 10) \
        | (self.tc << 9) \
        | (self.rd << 8) \
        | (self.ra << 7) \
        | (self.z << 4) \
        | (self.rcode)

        return struct.pack('!HHHHHH', self.id, flags, self.qdcount, self.ancount, self.nscount, self.arcount)
