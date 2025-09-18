
import socket
import threading
import struct

# 配置
HOST = '0.0.0.0'      # 本机 IP
PORT = 12345          # 端口
PEER_HOST = '192.168.243.197'   # 对方主机 IP
PEER_PORT = 12345

def recvall(conn, n):
    """确保一次性接收 n 字节"""
    data = b''
    while len(data) < n:
        packet = conn.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def recv_thread(conn):
    """接收消息线程"""
    while True:
        try:
            length_bytes = recvall(conn, 4)
            if not length_bytes:
                print("[连接已关闭]")
                break
            length = struct.unpack('!I', length_bytes)[0]
            data = recvall(conn, length)
            if not data:
                print("[连接已关闭]")
                break
            # 按三段解析
            parts = data.decode().split(':')
            if len(parts) != 3:
                print("[收到未知格式数据]", data.decode())
                continue
            msg_str, msg_int, msg_float = parts
            msg_int = int(msg_int)
            msg_float = float(msg_float)
            print(f"\n[收到] 字符串: {msg_str}, 整数: {msg_int}, 浮点数: {msg_float}")
        except Exception as e:
            print("[接收异常]", e)
            break

def send_thread(conn):
    """发送消息线程"""
    while True:
        try:
            user_input = input("请输入消息 (格式: str:int:float) -> ")
            if not user_input:
                continue
            msg_bytes = user_input.encode()
            conn.sendall(struct.pack('!I', len(msg_bytes)))
            conn.sendall(msg_bytes)
            print("[已发送]", user_input)
        except Exception as e:
            print("[发送异常]", e)
            break

# 创建 TCP 套接字监听
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen()

print(f"[INFO] 正在监听 {PORT} 端口...")

# 尝试主动连接对方
connection = None
try:
    peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer.connect((PEER_HOST, PEER_PORT))
    connection = peer
    print(f"[INFO] 已主动连接到 {PEER_HOST}:{PEER_PORT}")
except Exception as e:
    print("[INFO] 未能主动连接到对方，等待对方连接...")

if connection is None:
    conn, addr = s.accept()
    connection = conn
    print(f"[INFO] 已接受来自 {addr} 的连接")

# 启动发送和接收线程
threading.Thread(target=recv_thread, args=(connection,), daemon=True).start()
threading.Thread(target=send_thread, args=(connection,), daemon=True).start()

# 主线程保持运行
while True:
    pass