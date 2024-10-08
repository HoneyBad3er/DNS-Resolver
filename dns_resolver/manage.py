import socket
from resolver import DNSResolver


def run(host_ip=None, port=1053):
    print("Starting UDP server...")

    if not host_ip:
        localhost = socket.gethostname()
        host_ip = socket.gethostbyname(localhost)

    resolver = DNSResolver(bind_path="./bind.example.txt")
    resolver.listen(host_ip=host_ip, port=port)


if __name__ == "__main__":
    run()
