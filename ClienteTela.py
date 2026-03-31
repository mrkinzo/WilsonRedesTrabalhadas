# Cliente
import socket

HOST = "127.0.0.1"
PORT = 9003
mensagem = ()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    #recebe as mensagens do servidor e imprime na tela
    while True:
        data = s.recv(1024)
        if not data:
            break
        print("Mensagem recebida:", data.decode("utf-8"))
