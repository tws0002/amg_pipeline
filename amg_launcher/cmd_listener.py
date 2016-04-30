import sys, os, json
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtNetwork import *

PORT = 12345

amg_root = os.getenv('AMG_ROOT')
if amg_root:
    if not amg_root in sys.path:
        sys.path.append(amg_root)
    import amg_config
    PORT = amg_config.get()['amg_tray_port']

SIZEOF_UINT32 = 4

class AMGListener(QObject):
    messageSignal = Signal(str)
    def __init__(self, parent=None):
        super(AMGListener, self).__init__(parent)
        self.tcpServer = QTcpServer(self)
        self.tcpServer.listen(QHostAddress("0.0.0.0"), PORT)
        self.tcpServer.newConnection.connect(self.addConnection)

    def addConnection(self):
        self.con = self.tcpServer.nextPendingConnection()
        self.con.nextBlockSize = 0

        self.connect(self.con, SIGNAL("readyRead()"),
                self.receiveMessage)
        self.connect(self.con, SIGNAL("disconnected()"),
                self.removeConnection)

        self.con.error.connect(self.socketError)

    def receiveMessage(self):
        if self.con.bytesAvailable() > 0:
            stream = QDataStream(self.con)
            stream.setVersion(QDataStream.Qt_4_2)

            if self.con.nextBlockSize == 0:
                if self.con.bytesAvailable() < SIZEOF_UINT32:
                    return
                self.con.nextBlockSize = stream.readUInt32()
            if self.con.bytesAvailable() < self.con.nextBlockSize:
                return

            textFromClient = stream.readQString()
            self.con.nextBlockSize = 0
            result = self.parse_msg(textFromClient)
            self.sendMessage(result)
                # self.cons.nextBlockSize = 0

    def sendMessage(self, text):
            reply = QByteArray()
            stream = QDataStream(reply, QIODevice.WriteOnly)
            stream.setVersion(QDataStream.Qt_4_2)
            stream.writeUInt32(0)
            stream.writeQString(text)
            stream.device().seek(0)
            stream.writeUInt32(reply.size() - SIZEOF_UINT32)
            self.con.write(reply)

    def removeConnection(self):
        pass

    def socketError(self, *args):
        pass

    def parse_msg(self, msg):
        self.messageSignal.emit(msg)
        file = 'c:/messages.json'
        if os.path.exists(file):
            data = json.load(open(file))
        else:
            data = []
        data.append(msg)
        json.dump(data, open(file,'w'), indent=2)
        return 'OK'


class CMD():
    WATCH_RENDER_RESULT = 'WRRES'
    EXECUTE_COMMAND = 'EXCMD',
    POPUP_MESSAGE = "MSG"




if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = AMGListener()
    app.exec_()