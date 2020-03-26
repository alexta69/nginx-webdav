from wsgidav.fs_dav_provider import FilesystemProvider
from wsgidav.wsgidav_app import WsgiDAVApp
from wsgidav.util import init_logging

import os


def parse_dn(dn):
    res = {}
    for pair in dn.split(','):
        k,v = pair.split('=')
        res[k] = v
    return res


class Files(FilesystemProvider):
    ROOT_PATH = '/data'

    def __init__(self):
        super().__init__(self.ROOT_PATH)

    def _loc_to_file_path(self, path, environ=None):
        if not environ:
            raise Exception('no environ in filesystem access')
        if 'SSL_CLIENT_S_DN' not in environ:
            raise Exception('no SSL_CLIENT_S_DN in environ in filesystem access')
        dn = parse_dn(environ['SSL_CLIENT_S_DN'])
        if 'CN' not in dn:
            raise Exception('CN not in certificate')
        new_root = self.ROOT_PATH + '/' + dn['CN']
        assert new_root == os.path.abspath(new_root)  # no funny ".." business in CN
        p = super()._loc_to_file_path(path, environ)
        assert p.startswith(self.ROOT_PATH)
        return os.path.join(new_root, p[len(self.ROOT_PATH)+1:])


config = {
    "provider_mapping": {"/": Files()},
    "simple_dc": {"user_mapping": {"*": True}},  # anonymous access
    "verbose": 3,
}

init_logging(config)
app = WsgiDAVApp(config)
