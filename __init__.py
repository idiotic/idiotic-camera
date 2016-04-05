"""camera -- interface with video cameras in idiotic

"""

import logging
from idiotic import utils, item

MODULE_NAME = "camera"

log = logging.getLogger("module.camera")

DRIVERS = {}
CREDENTIALS = None

def configure(config, api, assets):
    global CREDENTIALS
    CREDENTIALS = config['credentials']
    log.info(DRIVERS)

def register(c, name):
    global DRIVERS
    if name in DRIVERS:
        log.warn('driver {} declared twice, {} replacing {}'.format(
            name, c, DRIVERS[name]))
    DRIVERS[name] = c


class Camera(item.BaseItem):
    class UnknownCredentialsError(Exception): pass
    class UnsupportedCameraError(Exception): pass

    def __init__(self, name, uri, driver, *args, credentials_name=None, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.uri = uri

        if credentials_name:
            try:
                credentials = CREDENTIALS[credentials_name]
            except KeyError:
                raise UnknownCredentialsError(credentials_name)
        else:
            credentials = None

        if driver not in DRIVERS:
            raise UnsupportedCameraError(driver)
        else:
            self.driver = DRIVERS[driver](uri, credentials)

class CameraDriver:
    def __init__(self):
        pass

class FI8910EDriver(CameraDriver):
    def __init__(self, uri, credentials = None):
        self.uri = uri
        self.credentials = credentials

register(FI8910EDriver, 'FI8910E')
