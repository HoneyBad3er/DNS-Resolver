import socket
import time
from collections import defaultdict
from cachetools import LRUCache

from dns_message.message import DNSMessage
from dns_message.answer import DNSAnswer
from consts import RRType, UDP_MESSAGE_SIZE, DEFAULT_TTL


class DNSResolver:
    def __init__(self, bind_path="data/bind.txt", remote_ip='1.1.1.1', remote_port=53, cache_size=10000) -> None:
        self.bind_path = bind_path
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.cache = LRUCache(maxsize=cache_size)
        self._load_static_records()

    def listen(self, host_ip: str, port=53) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            try:
                s.bind((host_ip, port))
                print(f"DNS Resolver listening on {host_ip}:{port}")
                while True:
                    try:
                        data, client_addr = s.recvfrom(UDP_MESSAGE_SIZE)
                        message = DNSMessage(data)

                        answers = []
                        for q in message.questions:
                            if q.qtype == 1 and q.qname in self._domain_to_ip:
                                answers.extend(self._resolve_local(q.qname))
                            else:
                                answers.extend(self._resolve_remote(q.qname, data))

                        message.build_response(answers)
                        s.sendto(message.to_bytes(), client_addr)

                    except Exception as e:
                        print(f'Error receiving data: {e}')
                        break

            except socket.error as e:
                print(f"Error binding socket: {e}")

    def _resolve_local(self, domain: str):
        print("Resolve local...")
        return [
            DNSAnswer(
                name=domain,
                rtype=1,
                rclass=1,
                ttl=DEFAULT_TTL,
                rdlength=4,
                rdata=socket.inet_aton(ip)
                )
            for ip in self._domain_to_ip[domain]]

    def _resolve_remote(self, domain: str, data: bytes):
        print("Resolve remote...")
        if domain in self.cache:
            answers, exp_time = self.cache[domain]
            if time.time() < exp_time:
                return answers

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.settimeout(5)
                s.sendto(data, (self.remote_ip, self.remote_port))
                remote_data, _ = s.recvfrom(UDP_MESSAGE_SIZE)
                message = DNSMessage(remote_data)
                answers = message.answers
                exp_time = time.time() + min([a.ttl for a in answers])
                self.cache[domain] = (answers, exp_time)
                return answers

        except socket.timeout:
            print(f"Timeout occurred while querying {self.remote_ip}:{self.remote_port}")
            return []

        except Exception as e:
            print(f"Error: {e}")
            return []

    def _load_static_records(self) -> None:
        self._domain_to_ip = defaultdict(list)
        with open(self.bind_path, 'r') as f:
            for rr in f:
                rr = rr.strip()
                if not rr or rr.startswith(';'):
                    continue

                try:
                    rr_parts = rr.split()
                    if len(rr_parts) < 4:
                        raise ValueError(f"Malformed record (not enough parts): {rr}")
                    
                    domain, rr_class, rr_type = rr_parts[:3]
                    rr_type = RRType(rr_type)

                    match rr_type:
                        case RRType.A:
                            value = rr_parts[3]
                            if not self._is_valid_ipv4(value):
                                raise ValueError(f"Invalid IPv4 address '{value}' for domain '{domain}'")
                        case _:
                            raise ValueError(f"Unsupported record type '{rr_type}' for domain '{domain}'")

                    self._domain_to_ip[domain].append(value)

                except ValueError as ve:
                    print(f"ValueError: {ve}")

                except Exception as e:
                    print(f"Unexpected error while processing static bind file record: {rr} -> {e}")

    def _is_valid_ipv4(self, ip):
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False
