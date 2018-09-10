#!/usr/bin/env python

import sys
from tunexdaemon import TunexDaemon
from tunexclient import TunexClient


# Setup variables
alias = 'tunex'
api = 'api/v1/'
host = 'localhost'
port = 8081


if __name__ == "__main__":
    # Setup tunexclient
    tunexclient = TunexClient(alias, port, api)
    tunexclient.setup_hostfile()

    # Setup tunexdaemon (if not already running)
    tunexdaemon = TunexDaemon('/tmp/%s-daemon.pid' % alias, 'TunexAPI', host, port)

    # Argument handling (client)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            tunexdaemon.start()
        elif 'stop' == sys.argv[1]:
            tunexdaemon.stop()
        elif 'restart' == sys.argv[1]:
            tunexdaemon.restart()
        elif 'setup' == sys.argv[1]:
            print '"%s %s" requires exactly 1 argument\n' % (sys.argv[0], sys.argv[1])
            print 'Usage: %s %s [USERNAME]\n' % (sys.argv[0], sys.argv[1])
            print 'Fetch the AWS data from the ScaleX database for [USERNAME]\n'
            print 'Options:'
            print '  --force      Reinitialize %s with provided user', alias
        elif 'cluster' == sys.argv[1]:
            print 'Usage: %s %s COMMAND\n' % (sys.argv[0], sys.argv[1])
            print 'Commands: '
            print '  status     Prints status information and metrics for cluster'
            print '  run        Creates a new AWS autoscaling group that runs the provided k8s deployment'
            print '  remove     Removes an AWS autoscaling group'
            print '  apply      Creates or replaces the deployment on a cluster'
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    elif len(sys.argv) == 3:
        if 'cluster' == sys.argv[1]:
            if 'status' == sys.argv[2]:
                print '"%s %s %s" requires at least 1 argument\n' % (sys.argv[0], sys.argv[1], sys.argv[2])
                print 'Usage: %s %s %s [OPTIONS] [CLUSTER]\n' % (sys.argv[0], sys.argv[1], sys.argv[2])
                print 'Retrieve the status and metrics of a or all running cluster/s\n'
                print 'Options:'
                print '  --all      Displays all running clusters and their metrics'
            elif 'run' == sys.argv[2]:
                print '"%s %s %s" requires at least 1 argument\n' % (sys.argv[0], sys.argv[1], sys.argv[2])
                print 'Usage: %s %s %s [OPTIONS] [DEPLOYMENT]\n' % (sys.argv[0], sys.argv[1], sys.argv[2])
                print 'Creates a new autoscaling cluster with the provided parameters on AWS\n'
                print 'Options:'
                print '  --name             Set a name for the new cluster'
                print '  --cpuscaleutil     Set the average cpu utilization scaling threshold'
                print '  --loadbalancer     Create a loadbalancer attached to the scaling group'
            elif 'remove' == sys.argv[2]:
                print '"%s %s %s" requires at least 1 argument\n' % (sys.argv[0], sys.argv[1], sys.argv[2])
                print 'Usage: %s %s %s [OPTIONS] [CLUSTER] \n' % (sys.argv[0], sys.argv[1], sys.argv[2])
                print 'Removes a given cluster or removes all of them\n'
                print 'Options:'
                print '  --all      Remove all clusters'
            elif 'apply' == sys.argv[2]:
                print '"%s %s %s" requires at least 2 argument\n' % (sys.argv[0], sys.argv[1], sys.argv[2])
                print 'Usage: %s %s %s CLUSTER DEPLOYMENT \n' % (sys.argv[0], sys.argv[1], sys.argv[2])
                print 'Creates or replaces the deployment on a cluster\n'
            else:
                print "Unknown command"
                sys.exit(2)
        elif 'setup' == sys.argv[1]:
            response = tunexclient.get_active_user()
            if response == "False":
                print 'No active user detected! Setting up %s' % sys.argv[2]
                response = tunexclient.setup_user(sys.argv[2])
                print response
            else:
                print '%s already setup for user %s\n' % (alias, response)
                print 'Use --force to overwrite!'
                sys.exit(2)
        sys.exit(0)
    elif len(sys.argv) == 4:
        if 'setup' == sys.argv[1] and '--force' == sys.argv[2]:
            print 'Setting up %s' % sys.argv[3]
            response = tunexclient.setup_user(sys.argv[3])
            print response
        sys.exit(0)
    else:
        print 'Usage: %s COMMAND\n' % sys.argv[0]
        print 'Commands: '
        print '  start		Starts the %s-daemon' % alias
        print '  stop		Stops the %s-daemon' % alias
        print '  restart	Restarts the %s-daemon' % alias
        print '  setup		Fetches AWS information from the ScaleX database'
        print '  cluster	Controls and Creates AWS autoscaling clusters'
        sys.exit(2)
