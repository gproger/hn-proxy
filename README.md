Hacker™ News proxy
=================

Code for test application for 
https://github.com/ivelum/job/blob/master/challenges/python.md




```
usage: proxy.py [-h] [-l [WORD_LEN]] [-t [WORD_APP]] [-u [TARGET_URL]]
              [-p [PORT]] [-a [SOURCE_IPV4]] [--regex | --no-regex]

Hacker News proxy

options:
  -h, --help            show this help message and exit
  -l [WORD_LEN], --length [WORD_LEN]
                        specifies the length of the word to add characters
  -t [WORD_APP], --text [WORD_APP]
                        Text appended to matched by length words
  -u [TARGET_URL], --url [TARGET_URL]
                        Proxyfied server URL (e.g. 'https://test.com/')
  -p [PORT], --port [PORT]
                        HTTP proxy server listen port
  -a [SOURCE_IPV4], --addr [SOURCE_IPV4]
                        HTTP proxy server binded address
```

How create Docker container

```
docker build -t hacker-proxy -f Dockerfile .
```


Run Hacker proxy

```
docker run -it --rm -p 8232:8232 hacker-proxy
```
