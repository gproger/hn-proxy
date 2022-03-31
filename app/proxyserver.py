from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib import request
from urllib.error import HTTPError, URLError
from functools import partial
import ssl
import gzip
#import time
from config import ProxyConfig
from patchhtml import patch_html


# for mac OS with not by Brew installation python we need create ssl context
ssl._create_default_https_context = ssl._create_unverified_context



class ProxyHandler(BaseHTTPRequestHandler):
    """ ProxyHandler for ThreadingHTTPServer instance """
    def __init__(self, config: ProxyConfig, *args, **kwargs):
        self.config=config
        super().__init__(*args, **kwargs)


    def do_GET(self):
        """ Process HTTP GET request """
        url=self.path[1:]
        url = self.config.target_url + self.path[1:]
        try:
            result = request.urlopen(url)
        except HTTPError as err:
            self.send_response(code=int(err.code),message=err.reason)
            data=''.encode('utf-8')
        except URLError as err:
            self.send_response(code=500,message='No internet connection')
            data=''.encode('utf-8')
        else:
            self.send_response(result.status)
            data = result.read()
            for att, val in result.getheaders():
                self.send_header(att, val)
                if att == 'Content-Type' and 'text/html' in val:
#                start_time = time.time()
                    data = patch_html(data,
                                      self.config
                                     )
 #               print("--- %s seconds ---" % (time.time() - start_time))
        finally:
            self.end_headers()
            self.wfile.write(data)

    def do_POST(self):
        """ Process HTTP POST request """
        headers = self.headers
        print(type(headers))
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        url = self.config.target_url + self.path[1:]
        result = ''
        data = ''
        try:
            req = request.Request(url, headers=headers, data=post_data)     
            result = request.urlopen(req)   
        except HTTPError as err:
            self.send_response(code=int(err.code),message=err.reason)
            data=''.encode('utf-8')
        except URLError as err:
            self.send_response(code=500,message='No internet connection')
            data=''.encode('utf-8')
        else:
            self.send_response(result.status)
            data = result.read()
            gz = False
            for att, val in result.getheaders():
                if att == 'Content-Encoding' and val == 'gzip':
                    data = gzip.decompress(data)
                    gz = True
            for att, val in result.getheaders():
                self.send_header(att, val)
                if att == 'Content-Type' and 'text/html' in val:
                    data = patch_html(data,
                                      self.config
                                     )
                    if gz:
                        data = gzip.compress(data)
 
        finally:
            self.end_headers()
            self.wfile.write(data)


class ProxyServer(object):
    """ Proxy server instance""" 
    def __init__(self, config: ProxyConfig) -> None:
        self.config=config

    def run(self):
        """ Main work loop """   
        handler = partial(ProxyHandler, self.config)

        httpd = ThreadingHTTPServer((self.config.source_ipv4, 
                                     self.config.port),
                                     handler
                                    )
        print("Now serving at http://{}:{}".format(self.config.source_ipv4, 
                                                    self.config.port))
        httpd.serve_forever()