
import socket
import struct

class scope:
    port = 5025

    class params:
        def __init__(self):
            self.format = ''
            self.dtype = ''
            self.points = 0
            self.count = 0
            self.xincrement = 0
            self.xorigin = 0
            self.xreference = 0
            self.yincrement = 0
            self.yorigin = 0
            self.yreference = 0
        
    def __init__(self, host, port=port):
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(2)        
        self.s.connect((host,port))
        print 'device info:'
        print self.sendRecvString('*IDN?\n')
        self.s.send('WAV:POIN:MODE RAW\n')
        self.s.send('WAV:FORM WORD\n')
        self.getParams(disp=1)

    def getData(self):
        self.getParams()
        self.s.send('STOP\n')
        self.s.send('WAV:DATA?\n') 
        rawdata = struct.unpack('<'+str(self.settings.points)+'H',self.s.recv(2**15)[10:-1])
        #self.data = [0.0]*self.settings.points
        self.rawdata = [0.0]*self.settings.points
        for i in xrange(self.settings.points):
            self.rawdata[i] = rawdata[i]
            #self.data[i] = self.settings.yincrement * (rawdata[i] - self.settings.yreference) + self.settings.yorigin
        self.s.send('RUN\n')
        return self.rawdata

    def sendString(self,string):
        self.s.send(string)

    def sendRecvString(self,string):
        try:
            self.s.send(string)
            return self.s.recv(2048)
        except socket.timeout:
            print 'socket timed out on '+string
            return None

    def getParams(self,disp=0):
        self.settings = self.params()
        preamble = self.sendRecvString('WAV:PRE?\n').split(',')
        field = int(preamble[0])
        if field == 0:
            self.settings.format = 'byte'
        elif field == 1:
            self.settings.format = 'word'
        elif field == 2:
            self.settings.format = 'ascii'
        field = int(preamble[1])
        if field == 0:
            self.settings.dtype = 'normal'
        elif field == 1:
            self.settings.dtype = 'peak'
        elif field == 2:
            self.settings.dtype = 'average'
        self.settings.points = int(preamble[2])
        self.settings.count = 1
        if int(preamble[3]) > 1:
            self.settings.count = int(preamble[3])
        self.settings.xincrement = float(preamble[4])
        self.settings.xorigin = float(preamble[5])
        self.settings.xreference = int(preamble[6])
        self.settings.yincrement = float(preamble[7])
        self.settings.yorigin = float(preamble[8])
        self.settings.yreference = float(preamble[9])
        if disp == 1:
            print 'format is                '+self.settings.format
            print 'aquisition type is       '+self.settings.dtype
            print 'number of data points is '+str(self.settings.points)
            print 'count is (always 1)      '+str(self.settings.count)
            print 'time step is             '+str(self.settings.xincrement)
            print 'time origin is           '+str(self.settings.xorigin)
            print 'time reference is        '+str(self.settings.xreference)
            print 'voltage step is          '+str(self.settings.yincrement)
            print 'voltage origin is        '+str(self.settings.yorigin)
            print 'voltage reference is     '+str(self.settings.yreference)
            print ''


