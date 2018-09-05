#!/usr/bin/env python

import sys, time, boto3
from daemon import Daemon
from pymongo import MongoClient

class TunexDaemon(Daemon):
	def run(self):
		while True:
			time.sleep(1)

class MongoDatabase():
	def __init__(self):
		self.client = MongoClient('localhost', 27017)

if __name__ == "__main__":
	daemon = TunexDaemon('/tmp/tunex-daemon.pid')
	mongodb = MongoDatabase()
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		elif 'setup' == sys.argv[1]:
			print '"%s setup" requires exactly 1 argument\n'
			print 'Usage: %s setup [USERNAME]\n' % sys.argv[0]
			print 'Fetch the AWS data from the ScaleX database for [USERNAME]'
		elif 'cluster' == sys.argv[1]:
			print 'Usage: %s cluster COMMAND\n' % sys.argv[0]
			print 'Commands: '
			print '  status		Prints status information and metrics for cluster'
			print '  run			Creates a new AWS autoscaling group that runs the provided k8s deployment'
			print '  remove		Removes a AWS autoscaling group'
			print '  change		Changes deployment running on AWS autoscaling group'
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	if len(sys.argv) == 3:
		if 'cluster' == sys.argv[1]:
			if 'status' == sys.argv[2]:
				print 'TODO: AUTOSCALING STATUS'

	else:
		print 'Usage: %s COMMAND\n' % sys.argv[0]
		print 'Commands: '
		print '  start		Starts the tunex-daemon'
		print '  stop		Stops the tunex-daemon'
		print '  restart	Restarts the tunex-daemon'
		print '  setup		Fetches AWS information from the ScaleX database'
		print '  cluster	Controls and Creates AWS autoscaling clusters'
		sys.exit(2)
