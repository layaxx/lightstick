###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Crossbar.io Technologies GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

import uuid, sys

from twisted.python import log
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource

from flask import Flask, render_template

from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol

from autobahn.twisted.resource import WebSocketResource, WSGIRootResource

import subprocess, psutil, argparse, os, signal


def cleanUp():
    children = psutil.Process().children()
    for child in children:
        print('Child: {}'.format(child.cmdline()))
    for process in psutil.process_iter():
        if "python" in process.name() and "led-action" in "".join(process.cmdline()):
            # os.killpg(os.getpgid(process.pid), signal.SIGABRT)
            process.terminate()
            log.msg("terminated " + "".join(process.cmdline()))
    return


# Our WebSocket Server protocol
class EchoServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        cleanUp()
        return super().onConnect(request)

    def onClose(self, a, b, c):
        cleanUp()
        return super().onClose()

    def onMessage(self, payload, isBinary):
        if payload == b"test":
            cleanUp()
            subprocess.Popen(
                ["sudo", "python3", "/home/pi/lightstick/led-action/test.py"])
        elif payload == b"stop":
            print("stopping")
            cleanUp()
        elif payload.decode('utf-8').startswith("solid "):
            color = payload.decode("utf-8")[6:12]
            print("solid: " + color)
            subprocess.Popen(
                ["sudo", "python3", "/home/pi/lightstick/led-action/solid.py", color])
        else:
            print("unrecognized command")
        self.sendMessage(bytes(hallo) + payload, isBinary)


# Our WSGI application .. in this case Flask based
app = Flask(__name__)
app.secret_key = str(uuid.uuid4())


@app.route('/')
def page_home():
    return render_template('index.html')


if __name__ == "__main__":

    def str2bool(v):
        if isinstance(v, bool):
            return v
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')

    hallo = "sadjfoidsfhpiöf"

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--prod", help="activate prod mode",
                        type=str2bool, nargs="?", const=True, default=False)
    args = parser.parse_args()

    if args.prod:
        print("prod mode")
        log.startLogging(open('/var/log/wsserver.log', 'w'))
    else:
        print("dev mode")
        log.startLogging(sys.stdout)

    # create a Twisted Web resource for our WebSocket server
    wsFactory = WebSocketServerFactory("ws://127.0.0.1:8080")
    wsFactory.protocol = EchoServerProtocol
    wsResource = WebSocketResource(wsFactory)

    # create a Twisted Web WSGI resource for our Flask server
    wsgiResource = WSGIResource(reactor, reactor.getThreadPool(), app)

    # create a root resource serving everything via WSGI/Flask, but
    # the path "/ws" served by our WebSocket stuff
    rootResource = WSGIRootResource(wsgiResource, {b'ws': wsResource})

    # create a Twisted Web Site and run everything
    site = Site(rootResource)

    reactor.listenTCP(8080, site)
    reactor.run()
