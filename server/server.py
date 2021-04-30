import uuid
import sys
import subprocess
import psutil
import argparse
import os
import base64
from twisted.python import log
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
from flask import Flask, render_template
from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol
from autobahn.twisted.resource import WebSocketResource, WSGIRootResource


def cleanUp(thorough=False):
    if thorough:
        log.msg("Thorough Cleanup initiated")
        for process in psutil.process_iter():
            if "python" in process.name() and "led-action" in "".join(process.cmdline()):
                process.terminate()
                log.msg("terminated " + "".join(process.cmdline()))
    else:
        for child in psutil.Process().children():
            child.terminate()
            log.msg("terminated " + "".join(child.cmdline()))
    log.msg("Cleanup completed")


class EchoServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        cleanUp(thorough=True)
        return super().onConnect(request)

    def onClose(self, a, b, c):
        cleanUp(thorough=True)
        return super().onClose(a, b, c)

    def onMessage(self, payload, isBinary):
        decoded = payload.decode('utf-8')
        [command, *arguments] = decoded.split(" ")

        if command == "test":
            cleanUp()
            subprocess.Popen(
                ["sudo", "python3", "/home/pi/lightstick/led-action/test.py"])

        elif command == "stop":
            print("stopping")
            cleanUp()
            self.sendMessage(
                bytes("executed non-thorough cleanup", "utf-8"), isBinary)

        elif command == "clean" or command == "cleanup":
            print("thorough cleanup requested")
            cleanUp(thorough=True)
            self.sendMessage(
                bytes("executed thorough cleanup", "utf-8"), isBinary)

        elif command == "solid":
            cleanUp()
            if len(arguments) > 0:
                color = arguments[0]
            else:
                color = "bb0000"
            print("solid: " + color)
            subprocess.Popen(
                ["sudo", "python3", "/home/pi/lightstick/led-action/solid.py", color])
            self.sendMessage(
                bytes("starting solid LED-Action", "utf-8"), isBinary)

        elif command == "brightness":
            if len(arguments) > 0:
                brightness = arguments[0]
            else:
                brightness = ".50"
            os.environ["ls_c_brightness"] = brightness
            self.sendMessage(
                bytes("updated brightness", "utf-8"), isBinary)

        elif command == "rainbow static":
            cleanUp()
            subprocess.Popen(
                ["sudo", "python3", "/home/pi/lightstick/led-action/rainbow_static.py"])
            self.sendMessage(
                bytes("starting rainbow static LED-Action", "utf-8"), isBinary)

        elif command == "rainbow active":
            cleanUp()
            if len(arguments) > 0:
                duration = arguments[0]
            else:
                duration = "60"
            subprocess.Popen(
                ["sudo", "python3", "/home/pi/lightstick/led-action/rainbow_active.py", duration])
            self.sendMessage(
                bytes("starting rainbow active LED-Action", "utf-8"), isBinary)

        elif command == "image-update":
            if len(arguments) > 1:
                type = arguments[0]
                image = arguments[1]
            else:
                self.sendMessage(
                    bytes("failed to updated image. Missing arguments", "utf-8"), isBinary)
                return
            with open("/home/pi/lightstick/led-action/image/test." + type, "wb") as handle:
                handle.write(base64.b64decode(image))
            self.sendMessage(
                bytes("updated image", "utf-8"), isBinary)

        elif command == "fix":
            subprocess.Popen(
                ["sudo", "bash", "/home/pi/s.sh"])
            self.sendMessage(
                bytes("executing startup-fix utility", "utf-8"), isBinary)

        else:
            print("unrecognized command - " + command)
            self.sendMessage(
                bytes("unrecognized command - " + command, "utf-8"), isBinary)


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

    wsFactory = WebSocketServerFactory("ws://127.0.0.1:8080")
    wsFactory.protocol = EchoServerProtocol
    wsResource = WebSocketResource(wsFactory)

    wsgiResource = WSGIResource(reactor, reactor.getThreadPool(), app)

    rootResource = WSGIRootResource(wsgiResource, {b'ws': wsResource})

    site = Site(rootResource)

    reactor.listenTCP(8080, site)
    reactor.run()
