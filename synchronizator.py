#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Cron automated synchronization script.

Desc: Synchronize remote folder into local machine. Duplicate processes 
      are disallowed until running process finished.

Usage:
    :: Change required variables (_user, _password, _domain etc.)
    :: Edit crontab 
    # crontab -e

    :: Append line below.
    */30 * * * * python synchronizator.py 2>&1 &

Author: Sencer HAMARAT (RecNes)
E-Mail: sencerhamarat@gmail.com
"""

import shlex
from subprocess import Popen, PIPE
import logging as log
import sys

__author__ = "Sencer HAMARAT"

_user = 'username'
_password = 'password'
_domain = 'example.com'

_expectation = "Enter passphrase for key \'/home/%s/.ssh/id_rsa\':" % _user
_rsync = '/usr/bin/rsync --partial --progress -avvz -e'
_pub_key = '/home/%s/.ssh/id_rsa.pub' % _user
_ssh = '/usr/bin/ssh -i %s' % _pub_key
_remoteDir = '/home/%s/backup/' % _user
_localDir = '/home/%s/backup/' % _user
_command = '%s %s %s@%s:%s %s' % (_rsync, _ssh, _user, _domain, _remoteDir, _localDir)
run_command = shlex.split(_command)

_logFile = "logfile.log"
_logFormat = "%(asctime)s %(levelname)s %(name)s %(process)d %(threadName)s %(module)s:%(lineno)d %(funcName)s() " \
             "%(message)s\n"
log.basicConfig(filename=_logFile, level=log.DEBUG, format=_logFormat)

log.debug(u'Command will run: %s' % _command)

try:
    running_command = Popen(run_command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    if running_command.poll():
        log.debug(repr(running_command.poll()))
        sys.exit()
    if _expectation in running_command.communicate():
        running_command.communicate(_password)
    print running_command.communicate()
except Exception as e:
    log.debug(repr(e))
finally:
    sys.exit()
