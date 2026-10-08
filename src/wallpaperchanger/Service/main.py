from wallpaperchanger.Service.server import IPCServer


SOCKET_PATH = "/tmp/wallpaperchanger.sock"


def main():
    server = IPCServer(SOCKET_PATH)

    try:
        server.start()
    except KeyboardInterrupt:
        print("\nStopping server...")


if __name__ == "__main__":
    main()
