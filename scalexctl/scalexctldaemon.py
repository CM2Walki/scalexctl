#!/usr/bin/env python


import gevent.monkey, base64, os
from gevent.pywsgi import WSGIServer
from daemon import Daemon
from mongodb import MongoDatabase
from storage import Storage
from daemoncommands import DaemonCommands
from flask import Flask, request
from flask_classy import FlaskView, route


gevent.monkey.patch_all()

mongodbORM = MongoDatabase(os.environ['MONGODB_HOST'], 27017)
userStorage = Storage()
commandList = DaemonCommands(mongodbORM, userStorage)


class V1View(FlaskView):
    route_prefix = '/api/'

    @route('/')
    def index(self):
        return ""

    @route('/get_active_user')
    def get_username(self):
        return commandList.get_active_user()

    @route('/setup_user')
    def setup_user(self):
        username = str(request.args.get('username'))
        return commandList.setup_user(username)

    @route('/cluster_run')
    def cluster_run(self):
        timestart = str(request.args.get('timestart'))
        timeend = str(request.args.get('timeend'))
        timestep = str(request.args.get('timestep'))
        target = str(request.args.get('target'))
        func = str(base64.b64decode(request.args.get('func')))
        clustersize = str(request.args.get('clustersize'))
        instancetype = str(request.args.get('instancetype'))
        return commandList.cluster_run(timestart, timeend, timestep, target, func, clustersize, instancetype)

    @route('/cluster_remove')
    def cluster_remove(self):
        return commandList.cluster_remove()


class ScaleXCtlDaemon(Daemon):
    app = None

    def __init__(self, pidfile, name, host, port):
        Daemon.__init__(self, pidfile)
        self.app = None
        self.host = host
        self.port = port
        self.name = name

    def run(self):
        self.app = Flask(self.name)
        V1View.register(self.app)
        http_server = WSGIServer((self.host, self.port), self.app)
        http_server.serve_forever()
