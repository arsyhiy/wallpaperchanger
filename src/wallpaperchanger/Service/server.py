import os
import socket

from wallpaperchanger.Ipc.protocol import decode, encode


class IPCServer:
    def __init__(self, socket_path: str):
        self.socket_path = socket_path

        self.socket = socket.socket(
            socket.AF_UNIX,
            socket.SOCK_STREAM,
        )

    def start(self):
        # Если socket остался от предыдущего запуска
        if os.path.exists(self.socket_path):
            os.remove(self.socket_path)

        self.socket.bind(self.socket_path)
        self.socket.listen()

        print(f"IPC server listening on {self.socket_path}")

        try:
            while True:
                connection, _ = self.socket.accept()

                with connection:
                    data = connection.recv(4096)

                    if not data:
                        continue

                    request = decode(data)

                    print(f"Request: {request}")

                    response = self.handle(request)

                    print(f"Response: {response}")

                    connection.sendall(encode(response))

        finally:
            self.stop()

    def stop(self):
        self.socket.close()

        if os.path.exists(self.socket_path):
            os.remove(self.socket_path)

    def handle(self, request: dict) -> dict:
        action = request.get("action")

        if action == "next":
            print("Changing to next wallpaper")

            return {
                "ok": True,
                "action": "next",
            }

        if action == "previous":
            print("Changing to previous wallpaper")

            return {
                "ok": True,
                "action": "previous",
            }

        if action == "status":
            return {
                "ok": True,
                "status": "running",
            }

        return {
            "ok": False,
            "error": "unknown_action",
        }
