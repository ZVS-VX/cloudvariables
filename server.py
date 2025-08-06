from threading import Thread
from cloudvars import Server
import socket as sk
import http.client
import json
hc = http.client.HTTPConnection("ifconfig.me")
hc.request("GET", "/ip")

n = Server()
glob = json.loads(n.get_base(7))
is_last_thread_busy = True
exceptions = []
threads = []
try:
    if not glob["_LOGS"]:
        glob["_LOGS"] = exceptions
except KeyError:
    glob["_LOGS"] = exceptions
s = n.start()

print(f"Global ip: {hc.getresponse().read().decode()}\nLocal ip: {sk.gethostbyname(sk.gethostname())}\nPort: {n.get_port()}")

def connect():
    print("New thread")
    global exceptions
    global is_last_thread_busy
    global glob
    global threads
    try:
        conn, addr_full = s.accept()
        is_last_thread_busy = True
        (addr, client_port) = addr_full
        print("Connected to " + addr + ":" + str(client_port))
        ca = False
        close = False


        def send(val, ra=False):
            conn.send(str(len(val.encode(n.codec))).encode(n.codec))
            conn.recv(12)
            conn.send(str(val).encode(n.codec))
            if not ra:
                conn.recv(12)

        def recv(buffer=64, er=True):
            rs = conn.recv(buffer).decode(n.codec)
            v = ""
            if not rs == "":
                conn.send("1".encode(n.codec))
                v = conn.recv(int(rs)).decode(n.codec)
            if er:
                conn.send("1".encode(n.codec))
            return str(v)

        while True:
            if close:
                break
            if not ca:
                conn.recv(12)
                conn.send(n.codec.encode("UTF-8"))
                conn.recv(100)
                ca = True
            mode = recv()
            if mode == "create":
                password = recv(er = False)
                new_token = n.gen_token(glob)
                send(new_token)
                glob[new_token] = {"pw": password, "variables": {}}
            else:
                token = recv()
                password = recv(er=False)
                if glob[token]:
                    if password == glob[token]["pw"]:
                        conn.send("1".encode(n.codec))
                        if mode == "write":
                            variable = recv()
                            value = recv()
                            glob[token]["variables"][variable] = value
                        elif mode == "read":
                            variable = recv(er = False)
                            v = glob[token]["variables"].get(variable)
                            send(v)
                        elif mode == "delete variable":
                            variable = recv()
                            del glob[token]["variables"][variable]
                            print(glob)
                        elif mode == "delete project":
                            passw = recv()
                            if passw == glob[token]["pw"]:
                                del glob[token]
                        print(f"Backup: {glob}")
                        n.backup(7, glob)
                    else:
                        print("ERROR 02: Wrong password")
                        conn.send("ER2".encode(n.codec))
                else:
                    print("ERROR 01: Token not found")
                    conn.send("ER1".encode(n.codec))

    except Exception as e:
        exceptions.append(str(e))
        print(e)
        is_last_thread_busy = True
        glob["_LOGS"] = exceptions
        n.backup(7, glob)

while True:
    if is_last_thread_busy:
        threads.append(Thread(target=connect))
        threads[-1].start()
        is_last_thread_busy = False
