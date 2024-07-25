import socket


def get_ips():
    local_hostname = socket.gethostname()
    ip_addresses = socket.gethostbyname_ex(local_hostname)[2]
    return [ip for ip in ip_addresses if not ip.startswith("127.")]


if __name__ == '__main__':
    print('\n'.join(get_ips()))
