# coding=utf-8
# Reference: https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py
import os
import multiprocessing

bind = "127.0.0.1:8000"

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_VAR = os.path.join(_ROOT, "var")
_ETC = os.path.join(_ROOT, "etc")

loglevel = "info"
errorlog = "-"
accesslog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'


bind = "0.0.0.0:5000"
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 4

timeout = 3 * 60  # 3 minutes
keepalive = 24 * 60 * 60  # 1 day

capture_output = True
