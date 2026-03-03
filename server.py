# server.py
import socket
import threading
from auth_db import init_db, register_user, login_user

HOST = "0.0.0.0"
PORT = 5050

clients_lock = threading.Lock()
clients = {}  # {conn: username}

def send_line(conn: socket.socket, msg: str):
    conn.sendall((msg + "\n").encode("utf-8"))

def broadcast(msg: str, exclude_conn: socket.socket | None = None):
    with clients_lock:
        conns = list(clients.keys())

    for c in conns:
        if exclude_conn is not None and c == exclude_conn:
            continue
        try:
            send_line(c, msg)
        except Exception:
            remove_client(c)

def remove_client(conn: socket.socket):
    with clients_lock:
        username = clients.pop(conn, None)

    try:
        conn.close()
    except Exception:
        pass

    if username:
        broadcast(f"[SERVER] {username} left the chat.")

def handle_client(conn: socket.socket, addr):
    # makefile gives reliable line-based reading
    f = conn.makefile("r", encoding="utf-8", newline="\n")

    try:
        send_line(conn, "WELCOME Multiuser Chat System")
        send_line(conn, "AUTH Choose: REGISTER or LOGIN")

        authed_user = None

        while authed_user is None:
            send_line(conn, "PROMPT Type REGISTER or LOGIN:")
            choice = f.readline()
            if not choice:
                return
            choice = choice.strip().upper()

            if choice not in ("REGISTER", "LOGIN"):
                send_line(conn, "ERROR Invalid choice. Type REGISTER or LOGIN.")
                continue

            send_line(conn, "PROMPT Username:")
            username = f.readline()
            if not username:
                return
            username = username.strip()

            send_line(conn, "PROMPT Password:")
            password = f.readline()
            if not password:
                return
            password = password.strip()

            if choice == "REGISTER":
                ok, msg = register_user(username, password)
                send_line(conn, ("OK " if ok else "ERROR ") + msg)
                if ok:
                    send_line(conn, "INFO Now LOGIN to enter chat.")
            else:
                ok, msg = login_user(username, password)
                send_line(conn, ("OK " if ok else "ERROR ") + msg)
                if ok:
                    authed_user = username

        # Add authenticated user
        with clients_lock:
            clients[conn] = authed_user

        send_line(conn, f"OK Welcome {authed_user}! Type /quit to exit.")
        broadcast(f"[SERVER] {authed_user} joined the chat.", exclude_conn=conn)

        # Chat loop
        while True:
            line = f.readline()
            if not line:
                return
            msg = line.strip()

            if msg.lower() == "/quit":
                send_line(conn, "OK Bye.")
                return

            broadcast(f"{authed_user}: {msg}")

    except Exception as e:
        try:
            send_line(conn, f"ERROR Server exception: {e}")
        except Exception:
            pass
    finally:
        try:
            f.close()
        except Exception:
            pass
        remove_client(conn)

def main():
    init_db()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(100)

    print(f"[SERVER] Listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        print(f"[SERVER] Connection from {addr}")
        t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        t.start()

if __name__ == "__main__":
    main()