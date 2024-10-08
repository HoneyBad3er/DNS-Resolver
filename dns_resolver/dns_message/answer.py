from dataclasses import dataclass
import struct


@dataclass
class DNSAnswer:
    name: str
    rtype: int
    rclass: int
    ttl: int
    rdlength: int
    rdata: bytes

    @staticmethod
    def from_bytes(data: bytes, offset: int):
        name, offset = DNSAnswer._read_name(data, offset)
        rtype, rclass, ttl, rdlength = struct.unpack("!HHIH", data[offset:offset + 10])
        offset += 10
        rdata = data[offset:offset + rdlength]
        offset += rdlength
        return DNSAnswer(name=name, rtype=rtype, rclass=rclass, ttl=ttl, rdlength=rdlength, rdata=rdata), offset

    @staticmethod
    def _read_name(data: bytes, offset: int):
        name = []
        jumped, original_offset = False, offset

        while True:
            if (data[offset] & 0xC0) == 0xC0:
                pointer = struct.unpack('!H', data[offset:offset + 2])[0] & 0x3FFF
                offset, jumped  = pointer, True
            else:
                length = data[offset]
                if length == 0:
                    offset += 1
                    break
                name.append(data[offset + 1: offset + 1 + length].decode())
                offset += length + 1

        if jumped:
            return '.'.join(name), original_offset + 2
        else:
            return '.'.join(name), offset

    def to_bytes(self) -> bytes:
        name_bytes = DNSAnswer._name_to_bytes(self.name)
        header_bytes = struct.pack("!HHIH", self.rtype, self.rclass, self.ttl, self.rdlength)
        return name_bytes + header_bytes + self.rdata

    @staticmethod
    def _name_to_bytes(name: str) -> bytes:
        parts = name.split('.')
        return b''.join([len(part).to_bytes(1, 'big') + part.encode() for part in parts]) + b'\x00'
