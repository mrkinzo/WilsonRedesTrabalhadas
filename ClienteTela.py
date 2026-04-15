# ClienteTela.py
import socket
 
HOST = "127.0.0.1"
PORT = 9003
 
# Conecta ao servidor e fica aguardando mensagens para exibir na tela
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Aguardando mensagens do grupo...\n")
 
    while True:
        # Bloqueia até receber dados do servidor
        data = s.recv(1024)
 
        if not data:
            # Servidor encerrou a conexão
            print("Conexão encerrada pelo servidor.")
            break
 
        print("Mensagem recebida:", data.decode("utf-8"))
 