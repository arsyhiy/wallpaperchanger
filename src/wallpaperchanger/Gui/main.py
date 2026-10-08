import socket

from wallpaperchanger.Ipc.protocol import encode, decode


SOCKET_PATH = "/tmp/wallpaperchanger.sock"


class IPCClient:
    def __init__(self, socket_path: str):
        self.socket_path = socket_path

    def request(self, message: dict) -> dict:
        with socket.socket(
            socket.AF_UNIX,
            socket.SOCK_STREAM,
        ) as sock:

            sock.connect(self.socket_path)

            sock.sendall(encode(message))

            data = sock.recv(4096)

        return decode(data)

    def next(self):
        return self.request({
            "action": "next",
        })

    def previous(self):
        return self.request({
            "action": "previous",
        })

    def status(self):
        return self.request({
            "action": "status",
        })


def main():
    client = IPCClient(SOCKET_PATH)

    print("STATUS:")
    print(client.status())

    print()

    print("NEXT:")
    print(client.next())

    print()

    print("PREVIOUS:")
    print(client.previous())


if __name__ == "__main__":
    main()
