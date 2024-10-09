import socket
from resolver import DNSResolver


def run(host_ip=None, port=1053):
    print("Starting UDP server...")

    if not host_ip:
        localhost = socket.gethostname()
        host_ip = socket.gethostbyname(localhost)

    resolver = DNSResolver(bind_path="data/fake_dns_records_10k.txt")
    resolver.listen(host_ip=host_ip, port=port)


if __name__ == "__main__":
    run()
