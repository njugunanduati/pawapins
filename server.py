import sys
import os

from twisted.application import internet, service
from twisted.web import server, resource, wsgi, static
from twisted.python import threadpool
from twisted.internet import reactor
from twisted.python.logfile import DailyLogFile
from twisted.python.log import ILogObserver, FileLogObserver
from django.core.handlers.wsgi import WSGIHandler
from config.wsgi import application as djapp

PORT = 9010


def wsgi_resource():
    pool = threadpool.ThreadPool()
    pool.start()
    # wsgi_resource = wsgi.WSGIResource(reactor, pool, WSGIHandler())
    wsgi_resource = wsgi.WSGIResource(reactor, pool, djapp)
    return wsgi_resource


# Twisted Application Framework setup:
application = service.Application('twisted-django')

root = wsgi.WSGIResource(reactor, reactor.getThreadPool(), djapp)
logfile = DailyLogFile("gui.log", "logs")
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
# Serve it up:
main_site = server.Site(root)
internet.TCPServer(PORT, main_site).setServiceParent(application)
