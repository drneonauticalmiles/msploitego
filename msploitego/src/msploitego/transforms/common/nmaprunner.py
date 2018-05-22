#!/usr/bin/env python

from libnmap.parser import NmapParser
from libnmap.process import NmapProcess
from pprint import pprint

from corelib import static_var

import sys

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, Metasploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'
# nmap -vv -p 139,445 --script=$(ls /usr/share/nmap/scripts/smb-vuln* | cut -d"/" -f6 | tr '\n' ',' | sed 's/.$//') --script-args=unsafe=1
# scripts = "smb-vuln-conficker,smb-vuln-cve-2017-7494,smb-vuln-cve2009-3103,smb-vuln-ms06-025,smb-vuln-ms07-029,smb-vuln-ms08-067,smb-vuln-ms10-054,smb-vuln-ms10-061,smb-vuln-ms17-010,smb-vuln-regsvc-dos,smb2-vuln-uptime"

@static_var("TCP_SYN", "-sS")

class Nmaprunner(object):
    def __init__(self, ip, port, callback, safemode=False):
        self.scantype = self.TCP_SYN
        self.options = "-vv {} -p {} {}".format(self.scantype, port, ip)
        self.ip = ip
        self.port = port
        self.callback = callback
        self.nmap_proc = NmapProcess(targets=self.ip,
                                    options=self.options,
                                    event_callback=self.callback,
                                     safe_mode=safemode)
    def runnmap(self):
        self.nmap_proc.run()
        return NmapParser.parse(self.nmap_proc.stdout)

    def getproc(self):
        return self.nmap_proc

if __name__ == "__main__":
    def mycallback(nmaptask):
        if nmaptask:
            print "Task {0} ({1}): ETC: {2} DONE: {3}%".format(nmaptask.name,nmaptask.status,nmaptask.etc,nmaptask.progress)

    nrunner = Nmaprunner("10.10.10.74", "445", mycallback)
    nrunner.runnmap()
    pprint(nrunner)