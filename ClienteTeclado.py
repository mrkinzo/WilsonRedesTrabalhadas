# ClienteTeclado.py - Com reconexão automática
import socket
import time

HOST = "127.0.0.1"
PORT = 9002

def conectar_servidor():
    """Tenta conectar ao servidor com retry"""
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            print(" Conectado ao servidor!")
            return s
        except ConnectionRefusedError:
            print(" Aguardando servidor... Tentando novamente em 2 segundos")
            time.sleep(2)
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            time.sleep(2)

def main():
    socket_cliente = conectar_servidor()
    print("Digite suas mensagens (ou 'sair' para encerrar):")
    
    while True:
        try:
            mensagem = input("> ")
            
            if mensagem.lower() == 'sair':
                print("Encerrando...")
                break
            
            if not mensagem.strip():  # Ignora mensagens vazias
                continue
                
            # Envia a mensagem
            socket_cliente.sendall(mensagem.encode("utf-8"))
            print(f"✓ Enviado: {mensagem}")
            
        except (BrokenPipeError, ConnectionResetError):
            print(" Conexão perdida. Tentando reconectar...")
            socket_cliente.close()
            socket_cliente = conectar_servidor()
        except Exception as e:
            print(f"Erro: {e}")
            break
    
    socket_cliente.close()

if __name__ == "__main__":
    main()