# client.py
import socket
import threading
import sys

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5050

def recv_loop(sock: socket.socket):
    f = sock.makefile("r", encoding="utf-8", newline="\n")
    try:
        while True:
            line = f.readline()
            if not line:
                print("[DISCONNECTED]")
                return
            print(line.rstrip())
    except Exception:
        print("[RECV ERROR]")
    finally:
        try:
            f.close()
        except Exception:
            pass
        try:
            sock.close()
        except Exception:
            pass

def main():
    host = DEFAULT_HOST
    port = DEFAULT_PORT

    # Optional: python client.py 192.168.x.x 5050
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        port = int(sys.argv[2])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    t = threading.Thread(target=recv_loop, args=(sock,), daemon=True)
    t.start()

    try:
        while True:
            msg = input()
            sock.sendall((msg + "\n").encode("utf-8"))
            if msg.lower() == "/quit":
                break
    except KeyboardInterrupt:
        try:
            sock.sendall(b"/quit\n")
        except Exception:
            pass
    finally:
        try:
            sock.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()