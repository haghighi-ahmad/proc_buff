#****************************************************
#                                                   *
#               HTTP PROXY                          *
#               Version: 1.0                        *
#               Author: Luu Gia Thuy                *
#                                                   *
#****************************************************

import os,sys,thread,socket, time

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
        print "No port given, using :5000 " 
        port = 5000
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
	
    print "client connected" + str(client_addr)
    webserver = "google.com"
    port = 80

    while (True):
	    # get the request from browser
	    request = conn.recv(MAX_DATA_RECV)
	    print "request is:" + str(request)

	    if len(request) < 2:
	    	print "empty request"
	    	time.sleep(1)
	    	continue
	    
	    try:
	        # create a socket to connect to the web server
	        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
	        s.connect((webserver, port))
	        s.send(request)         # send request to webserver
	        
	        while 1:
	            # receive data from web server
	            data = s.recv(MAX_DATA_RECV)
	            print "data is " + str(data)
	            if (len(data) > 0):
	                # send to browser
	                conn.send(data)
	            else:
	                break

	        # s.close()
	        # conn.close()

	    except socket.error, (value, message):
	        if s:
	            s.close()
	        if conn:
	            conn.close()

	        print "Peer Reset"
	        sys.exit(1)
    if s:
        s.close()
    if conn:
        conn.close()
#********** END PROXY_THREAD ***********
    
if __name__ == '__main__':
    main()


