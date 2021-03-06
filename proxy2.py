#****************************************************
#                                                   *
#               HTTP PROXY                          *
#               Version: 1.0                        *
#               Author: Luu Gia Thuy                *
#                                                   *
#****************************************************

import os,sys,thread,socket, time, select , string

#********* CONSTANT VARIABLES *********
BACKLOG = 50            # how many pending connections queue will hold
MAX_DATA_RECV = 999999  # max number of bytes we receive at once
DEBUG = True            # set to True to see the debug msgs
BLOCKED = []            # just an example. Remove with [""] for no blocking at all.

#**************************************
#********* MAIN PROGRAM ***************
#**************************************
def main():

    # check the length of command running
    if (len(sys.argv)<2):
        print "No port given, using :5001 " 
        port = 5001
    else:
        port = int(sys.argv[1]) # port from argument

    # host and port info.
    host = ''               # blank for localhost
    
    print "Proxy Server Running on ",host,":",port

    try:
        # create a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # associate the socket to host and port
        s.bind((host, port))

        # listenning
        s.listen(BACKLOG)
    
    except socket.error, (value, message):
        if s:
            s.close()
        print "Could not open socket:", message
        sys.exit(1)

    # get the connection from client
    while 1:
        conn, client_addr = s.accept()

        # create a thread to handle request
        thread.start_new_thread(proxy_thread, (conn, client_addr))
        
    s.close()
#************** END MAIN PROGRAM ***************


#*******************************************
#********* PROXY_THREAD FUNC ***************
# A thread to handle request from browser
#*******************************************
def proxy_thread(conn, client_addr):
    host = "192.168.4.2"
    port = 23
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        # sys.exit()
        return
     
    print 'Connected to '+ host
     
    while 1:
        socket_list = [conn, s]
         
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:
            #incoming message from remote server
            print "in for"
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print 'Connection closed'
                    # sys.exit()
                    if s:
                        s.close()
                    if conn:
                        conn.close()
                    return
                else :
                    print "s data"
                    # sys.stdout.write(data)
                    conn.send(data)
             
            #user entered a message
            else :
                print "conn data"
                msg = conn.recv(4096)
                s.send(msg)

    
if __name__ == '__main__':
    main()


