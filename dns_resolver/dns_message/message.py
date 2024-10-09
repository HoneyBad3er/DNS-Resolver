import struct
from typing import List

from dns_message.header import DNSHeader
from dns_message.question import DNSQuestion
from dns_message.answer import DNSAnswer


class DNSMessage:
    HEADER_SIZE: int = 12

    def __init__(self, raw_data: bytes) -> None:
        self.raw_data: bytes = raw_data
        self.header: DNSHeader = DNSHeader.from_bytes(self.raw_data[:self.HEADER_SIZE])
        self.questions: List[DNSQuestion] = []
        self.answers: List[DNSAnswer] = []
        self._parse_message()

    def _parse_message(self) -> None:
        # Parse questions
        offset = self.HEADER_SIZE
        for _ in range(self.header.qdcount):
            question, offset = self._parse_question(self.raw_data, offset)
            self.questions.append(question)

        # Parse answers
        for _ in range(self.header.ancount):
            answer, offset = DNSAnswer.from_bytes(self.raw_data, offset)
            self.answers.append(answer)

    def _parse_question(self, data: bytes, offset: int) -> DNSQuestion:
        qname = []
        while True:
            length = data[offset]
            if length == 0:
                offset += 1
                break
            qname.append(data[offset + 1: offset + 1 + length].decode())
            offset += length + 1

        qname = '.'.join(qname)
        qtype, qclass = struct.unpack('!HH', data[offset:offset + 4])
        offset += 4

        return DNSQuestion(qname=qname, qtype=qtype, qclass=qclass), offset

    def to_bytes(self) -> bytes:
        header_bytes = self.header.to_bytes()
        question_bytes = b''.join(
            self._qname_to_bytes(q.qname) + struct.pack('!HH', q.qtype, q.qclass)
            for q in self.questions
        )
        answer_bytes = b''.join(a.to_bytes() for a in self.answers)

        return b''.join([header_bytes, question_bytes, answer_bytes])

    def build_response(self, answers: List[DNSAnswer]) -> None:
        self.answers = answers
        self.header.ancount = len(answers)
        self.header.qr = 1
        self.header.ra = 1
        self.header.rcode = 0

    @staticmethod
    def _qname_to_bytes(name: str) -> bytes:
        parts = name.split('.')
        return b''.join([len(part).to_bytes(1, 'big') + part.encode() for part in parts]) + b'\x00'
