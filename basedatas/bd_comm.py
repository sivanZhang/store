from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render

import pdb


class Common():
    
    PRIVATE_IPS_PREFIX = ('10.', '172.', '192.', )
    def get_client_ip(self,request):
        """get the client ip from the request
        """
        remote_address = request.META.get('REMOTE_ADDR')
        # set the default value of the ip to be the REMOTE_ADDR if available
        # else None
        ip = remote_address
        # try to get the first non-proxy ip (not a private ip) from the
        # HTTP_X_FORWARDED_FOR
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            proxies = x_forwarded_for.split(',')
            # remove the private ips from the beginning
            while (len(proxies) > 0 and
                    proxies[0].startswith(PRIVATE_IPS_PREFIX)):
                proxies.pop(0)
            # take the first ip which is not a private one (of a proxy)
            if len(proxies) > 0:
                ip = proxies[0]

        return ip

    
    def redirect_login(self, isMobile, request):
        next_url = request.GET.get('next')
        context  = {'next':next_url}
        if isMobile:
            return render(request, 'registration/m_login.html', context)
        else:
            return render(request, 'registration/login.html', context)
    
    #user is not login, and redirect by server side.
    #we need the next parameter to direct the URL after login
    def redirect_login_path(self, isMobile, request):
        next_url = request.path
        context  = {'next':next_url}
        if isMobile:
            return render(request, 'registration/m_login.html', context)
        else:
            return render(request, 'registration/login.html', context)
    
 