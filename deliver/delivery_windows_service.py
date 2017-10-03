# -*- coding:utf-8 -*-
import win32serviceutil
import win32service 
import win32event
import os
import servicemanager
import sys
basedir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(basedir)
from deliver import Delivery


class DeliveryService(win32serviceutil.ServiceFramework):
    """
   u(Usage: 'PythonService.py [options] install|update|remove|start [...]|stop|restart [...]|debug [...]'
    Options for 'install' and 'update' commands only:
     --username domain/username : The Username the service is to run under
     --password password : The password for the username
     --startup [manual|auto|disabled|delayed] : How the service starts, default = manual
     --interactive : Allow the service to interact with the desktop.
     --perfmonini file: .ini file to use for registering performance monitor data
     --perfmondll file: .dll file to use when querying the service for
       performance data, default = perfmondata.dll
    Options for 'start' and 'stop' commands only:
     --wait seconds: Wait for the service to actually start or stop.If you specify --wait with the 'stop' option,the service
                     and all dependent services will be stopped,each waiting
                     the specified period.)"""

    # service name
    _svc_name_ = 'Delivery'

    # service display name
    _svc_display_name_ = 'Simcube server delivery'

    # service description
    _svc_description_name_ = 'this is simcube server delivery'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args) 
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.delivery = Delivery(os.path.join(basedir, 'server.conf'))
      
    def SvcDoRun(self):
        import time
        import servicemanager  
        self.delivery.run_consume(2, 2)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.delivery.stop_consume()
        # set event
        win32event.SetEvent(self.hWaitStop)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        try:
            evtsrc_dll = os.path.abspath(servicemanager.__file__)
            servicemanager.PrepareToHostSingle(DeliveryService)
            servicemanager.Initialize('DeliveryService', evtsrc_dll)
            servicemanager.StartServiceCtrlDispatcher()
        except win32service.error as details:
            if details[0] == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                win32serviceutil.usage()
    else:
        win32serviceutil.HandleCommandLine(DeliveryService)
 

