import contextlib
import socket

import socks
try:
    import stem.process
except ImportError:
    stem = None

from pyreto import defaults


@contextlib.contextmanager
@defaults(port=1080, username=None, password=None)
def proxy(host, port, username, password):
    old_socket = socket.socket
    try:
        socks.set_default_proxy(socks.SOCKS5, host, port, True, username, password)
        socket.socket = socks.socksocket
        yield
    finally:
        socket.socket = old_socket


@contextlib.contextmanager
@defaults(port=7000, country=None, tor_config=None)
def tor_proxy(port, country, tor_config):
    if stem is None:
        raise RuntimeError('stem is not available')
    if tor_config is None:
        tor_config = {}
    tor_config['SocksPort'] = str(port)
    if country is not None:
        tor_config['ExitNodes'] = '{' + country + '}'
    tor_process = stem.process.launch_tor_with_config(config=tor_config)
    try:
        with proxy(host='127.0.0.1', port=port):
            yield
    finally:
        tor_process.kill()
