import socket
from _thread import *
import pickle
from player import Player


server = "10.200.14.142"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

players = [Player(), Player()]

def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))  # how many bits received show
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1: reply = players[0]
                else: reply = players[1]
                print("Received: ", data)
                print("Sending: ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break
    
    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()  # accept connection
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1