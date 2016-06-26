import os,sys,thread,socket, time, select, string, numpy, pickle

#********* CONSTANT VARIABLES *********
BACKLOG = 50            # how many pending connections queue will hold
MAX_DATA_RECV = 999999  # max number of bytes we receive at once
DEBUG = True            # set to True to see the debug msgs
BLOCKED = []            # just an example. Remove with [""] for no blocking at all.


class event_list():

    def __init__(self):
        self.tail = -1
        self.head = 0
        self.event_lst = []

    def push(self, item):
        self.tail += 1
        self.event_lst.append(item)
        return self.tail

    def pop(self, indx):
        if indx <= self.tail:
            return self.event_lst[indx]

    def fifo(self):
        if self.head <= self.tail:
            tmpp = self.event_lst[self.head]
            self.head += 1
            return tmpp


def store(event_):
    print "store."
    global eList
    if eList.push(event_) >= 100:
        with open('/var/lib/apk_cache/cache.apk', 'wb') as output:
            pickle.dump(eList, output, pickle.HIGHEST_PROTOCOL)
        eList = event_list()


def process(event_):
    pring "deciede for store or forward"
    global plan
    global conn_server

    if plan == 1:
        if old_event_exist:
            store(event_)
        else:
            conn_server.send(event_)
    else:
        store(event_)


def main():

    # check the length of command running
    if (len(sys.argv)<2):
        print "No port given, using :5002 " 
        port = 5002
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

        if not ser:
            thread.start_new_thread(proxy_thread_ser)
        # connect to remote host
        # create a thread to handle request
        thread.start_new_thread(proxy_thread, (conn, client_addr))
        
    s.close()


def proxy_thread_ser():
    host = "192.168.4.2"
    port = 23
    
    conn_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn_server.settimeout(2)
    try:
        conn_server.connect((host, port))
    except:
        print 'Unable to connect'
        # sys.exit()
        return
     
    print 'Connected to '+host

    read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
    send event intervally to server
    based on plan Value




def proxy_thread(conn, client_addr):
    host = "192.168.4.2"
    port = 23
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try:
        s.connect((host, port))
    except:
        print 'Unable to connect'
        # sys.exit()
        return
     
    print 'Connected to '+host
     
    while 1:
        socket_list = [conn, s]
         
        if not s or not conn:
            if s:
                s.close()
            if conn:
                conn.close()
            return

        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:
            #incoming message from remote server
            print "in for"
            if sock == s:
                # s1 = numpy.ndarray(4096)
                # nby , addr = sock.recvfrom_into(s1.data)
                # print str(nby) + str(addr)
                data = sock.recv(4096)
                print data
                # if not int(nby) <1 :
                if not data:
                    print 'Connection server closed'
                    # sys.exit()
                    if s:
                        s.close()
                    if conn:
                        conn.close()
                    return
                else:
                    print "s data"
                    # sys.stdout.write(data)
                    process(data)
             
            #user entered a message
            else:
                msg = conn.recv(4096)
                if not msg:
                    print 'Connection agent closed'
                    # sys.exit()
                    if s:
                        s.close()
                    if conn:
                        conn.close()
                    return
                else :
                    print "conn data"
                    s.send(msg)
    
if __name__ == '__main__':
    main()

eList = event_list()            # a list for soring 100 event and save/load them at once
old_event_exist = False         # True: we have some events in cache
plan = 1                        # 1: send without delay. 2: send event in 100 event per second. 3: Dont send any thing
fname_head = 10                 # this numbers addet at the end of cache files
fname_tail = 9                  # this numbers addet at the end of cache files