import sys, os
from PySide.QtCore import *
from PySide.QtNetwork import *
from cmd_listener import CMD

PORT = 12345

amg_root = os.getenv('AMG_ROOT')
if amg_root:
    if not amg_root in sys.path:
        sys.path.append(amg_root)
    import amg_config
    PORT = amg_config.conf['amg_tray_port']

SIZEOF_UINT32 = 4
server = 'localhost'
global snd

class AMGSender(QObject):
    responseSignal = Signal(str)
    def __init__(self, parent=None):
        super(AMGSender, self).__init__(parent)
        # Ititialize socket
        self.socket = QTcpSocket()
        # Initialize data IO variables
        self.nextBlockSize = 0
        self.request = None
        # self.socket.readyRead.connect(self.readFromServer)
        self.socket.disconnected.connect(self.serverHasStopped)
        self.socket.error.connect(self.serverHasError)

    def connectToServer(self):
        self.socket.connectToHost(server, PORT)

    def send_message(self, msg, wait_response=False):
        self.connectToServer()
        self.request = QByteArray()
        stream = QDataStream(self.request, QIODevice.WriteOnly)
        stream.setVersion(QDataStream.Qt_4_2)
        stream.writeUInt32(0)
        stream.writeQString(msg)
        stream.device().seek(0)
        stream.writeUInt32(self.request.size() - SIZEOF_UINT32)
        self.socket.write(self.request)
        self.nextBlockSize = 0
        self.request = None
        if not wait_response:
            self.socket.close()
            return
        self.socket.waitForReadyRead()
        resp = str(self.readFromServer())
        self.socket.close()
        self.responseSignal.emit(resp)
        return resp

    @classmethod
    def send(cls, message, command_type=CMD.POPUP_MESSAGE,  wait_response=False):
        global snd
        snd = cls()
        print 'Send message'
        res = snd.send_message(command_type + '::' + message, wait_response)
        return res

    def readFromServer(self):
        stream = QDataStream(self.socket)
        stream.setVersion(QDataStream.Qt_4_2)
        while True:
            if self.nextBlockSize == 0:
                if self.socket.bytesAvailable() < SIZEOF_UINT32:
                    break
                self.nextBlockSize = stream.readUInt32()
            if self.socket.bytesAvailable() < self.nextBlockSize:
                break
            textFromServer = stream.readQString()
            # print textFromServer
            self.nextBlockSize = 0
            return textFromServer
        # self.socket.close()

    def serverHasStopped(self):
        self.socket.close()

    def serverHasError(self):
        print ("Error: {}".format(self.socket.errorString()))
        self.socket.close()
