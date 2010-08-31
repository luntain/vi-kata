#!/usr/bin/env python
#
# fakemail (Python version)
#
# $Id: fakemail.py,v 1.1 2005/08/29 22:04:55 lastcraft Exp $


import asyncore
import getopt
import os
import signal
import smtpd
import socket
import sys


class FakeServer(smtpd.SMTPServer):

    def __init__(self, localaddr, remoteaddr):
        smtpd.SMTPServer.__init__(self, localaddr, remoteaddr)

    def process_message(self, peer, mailfrom, rcpttos, data):
        message("*************")
        message("Incoming mail")
        message(data)
        message("Incoming mail dispatched")


def usage():
    print "Usage: %s [OPTIONS]" % os.path.basename(sys.argv[0])
    print """
OPTIONS
        --host=<localdomain>
        --port=<port number>
        --log=<optional file to append messages to>
        --background"""


def quit(reason=None):
    global progname
    text = "Stopping %s" % progname
    if reason is not None:
        text += ": %s" % reason
    message(text)
    sys.exit()


log_file = None


def message(text):
    global log_file
    if log_file is not None:
        f = file(log_file, "a")
        f.write(text + "\n")
        f.close()
    else:
        print text


def handle_signals():

    def signal_handler(signum, frame):
        quit()

    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        signal.signal(sig, signal_handler)


def read_command_line():
    global log_file
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "",
            ["host=", "port=", "log=", "background"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    # Set defaults
    host = "localhost"
    port = 25
    background = False
    for opt, arg in optlist:
        if opt == "--host":
            host = arg
        elif opt == "--port":
            port = int(arg)
        elif opt == "--log":
            log_file = arg
        elif opt == "--background":
            background = True
    return host, port, background


def become_daemon():
    # See "Python Standard Library", pg. 29, O'Reilly, for more
    # info on the following.
    pid = os.fork()
    if pid:  # we're the parent if pid is set
        os._exit(0)
    os.setpgrp()
    os.umask(0)

    class DevNull:
        def write(self, message):
            pass

    sys.stdin.close()
    sys.stdout = DevNull()
    sys.stderr = DevNull()


def main():
    global progname
    handle_signals()
    host, port, background = read_command_line()
    message("Starting %s" % progname)
    if background:
        become_daemon()
    try:
        server = FakeServer((host, port), None)
    except socket.error, e:
        quit(str(e))
    message("Listening on port %d" % port)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        quit()


if __name__ == "__main__":
    progname = os.path.basename(sys.argv[0])
    main()
