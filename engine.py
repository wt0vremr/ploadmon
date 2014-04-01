__author__ = 'wt0vremr'

import platform
import psutil
import subprocess
import os
from datetime import timedelta
import time


class ProcParser:
    """/proc data collector"""
    def getcpuinfo(self):
        temp = subprocess.check_output("cat /proc/cpuinfo | grep 'model name' -m 1", shell=True).split(': ')[1]
        cpu = temp.split(' @ ')
        model = cpu[0].replace("(R)", "").replace("(TM)", "").replace("CPU", "")
        speed = cpu[1].replace("\n", "").replace("GHz", " GHz")
        curspeed = subprocess.check_output("cat /proc/cpuinfo | grep 'cpu MHz' -m 1", shell=True).split(': ')[1]
        curspeed = str(round(float(curspeed) / 1000, 2)) + " GHz"
        return [model, speed, curspeed]

    def getuptime(self):
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            uptime_string = str(timedelta(seconds=uptime_seconds)).split('.')[0]
        return uptime_string



class ServerCPU:
    """Represents CPU"""
    #    @profiler.timed
    def __init__(self):
        proc = ProcParser().getcpuinfo()
        self.arch = platform.processor()
        self.cores = psutil.NUM_CPUS
        self.name = proc[0]
        self.speed = proc[1]
        self.curspeed = proc[2]

    def getcpuinfo(self):
        return [["Model", self.name],
                ["Cores", self.cores],
                ["Architecture", self.arch],
                ["Default speed", self.speed],
                ["Current speed", self.curspeed]]


class ServerOS:
    """Represents server OS"""
    def __init__(self):
        self.kernel = platform.release()
        self.dist = platform.linux_distribution()[0]
        self.distversion = platform.linux_distribution()[1]

    def getserveros(self):
        return [["Distribution", self.dist],
                ["Release", self.distversion],
                ["Kernel version", self.kernel]]


class ServerStatus:
    """Represents server status"""
    def __init__(self):
        self.memfree = int(psutil.avail_phymem()) / (1024 * 1024)
        self.memused = int(psutil.used_phymem()) / (1024 * 1024)
        self.memcached = int(psutil.cached_phymem()) / (1024 * 1024)
        self.memtotal = self.memfree + self.memused
        self.memload = psutil.phymem_usage()[3]
        self.load = os.getloadavg()
        self.uptime = ProcParser().getuptime()
        self.coresload = psutil.cpu_percent(0.7, True)
        self.time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        statvfs = os.statvfs('/')
        self.hddtotal = statvfs.f_frsize * statvfs.f_blocks / 1024 / 1024  # Size of filesystem in bytes
        self.hddfree = statvfs.f_frsize * statvfs.f_bfree / 1024 / 1024  # Actual number of free bytes
        self.hddused = self.hddtotal - self.hddfree

    def gethddload(self):
        return {"Free": self.hddfree, "Used": self.hddused}

    def getmemload(self):
        return {"Free": self.memfree, "Used": self.memused - self.memcached, "Cached": self.memcached}

    def getstatstable(self):
        return [["Time & Date", self.time],
                ["Uptime", self.uptime],
                ["Load average", str(self.load)],
                ["Total RAM", str(self.memtotal) + "Mb"],
                ["HDD capacity", str(self.hddtotal) + "Mb"]]


class Dognut:
    """Represents little dognut chart"""

    def __init__(self, element, datadict):
        self.element = element
        self.datadict = datadict
        self.dataset = []

        for key, value in self.datadict.iteritems():
            self.dataset.append({"label": key, "value": float(value)})

        self.chart = {'element': self.element, 'data': self.dataset}


class LineChart:
    """Represents big chart generally"""

    def __init__(self, element, ykeys, labels):
        self.chart = {
        "ymax": 100,
        "ymin": 0,
        "xkey": 'time',
        "element": element,
        "ykeys": ykeys,
        "labels": labels,
        "data": []
        #        "hideHover":True
        }

    def addnewdata(self, stat):
        pass

    def getchart(self):
        self.addnewdata(ServerStatus())
        self.chart['data'] = self.chart['data'][1:10] if len(self.chart['data']) == 10 else self.chart['data']
        return self.chart


class MemChart(LineChart):
    """Memory load chart"""

    def __init__(self):
        LineChart.__init__(self, "memgraph", ["memused"], ["Memory Usage"])

    def addnewdata(self, stat):
        self.chart['data'].append({"time": stat.time, "memused": stat.memload})


class CoresChart(LineChart):
    """CPU load chart"""

    def __init__(self):
        cores = ServerCPU().cores
        corelist = []
        corenames = []
        for a in xrange(cores):

            corelist.append(str(a))
            corenames.append("Core " + str(a + 1))

        LineChart.__init__(self, "coresgraph", corelist, corenames)

    def addnewdata(self, stat):
        cores = dict(enumerate(stat.coresload))
        cores['time'] = stat.time
        self.chart['data'].append(cores)




if __name__ == "__main__":

    cpu = ServerCPU()
    servos = ServerOS()
    status = ServerStatus()

    print status.__dict__
    print servos.__dict__
    print cpu.__dict__
    m = MemChart()
    print m.getchart()
    print m.getchart()
    print m.getchart()
