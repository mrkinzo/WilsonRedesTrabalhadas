# Cliente
import socket

HOST = "127.0.0.1"
PORT = 9002
mensagem = input()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(mensagem.encode("utf-8"))
    