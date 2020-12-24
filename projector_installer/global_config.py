# Copyright 2000-2020 JetBrains s.r.o.
# Use of this source code is governed by the Apache 2.0 license that can be found
# in the LICENSE file.


"""
Global configuration constants, variables and functions.
"""

import sys
from typing import List
from shutil import rmtree
from os.path import dirname, join, expanduser, abspath

from .installable_app import InstallableApp, load_compatible_apps
from .utils import create_dir_if_not_exist

USER_HOME: str = expanduser('~')
INSTALL_DIR: str = dirname(abspath(__file__))
DEF_PROJECTOR_PORT: int = 9999
COMPATIBLE_IDE_FILE: str = join(INSTALL_DIR, 'compatible_ide.json')
DEF_CONFIG_DIR: str = '.projector'
SSL_PROPERTIES_FILE = 'ssl.properties'
BUNDLED_DIR: str = 'bundled'
SERVER_DIR: str = 'server'
config_dir: str = join(USER_HOME, DEF_CONFIG_DIR)
cache_dir: str = ''
CHANGELOG_URL = 'https://github.com/JetBrains/projector-installer/blob/master/CHANGELOG.md'


def get_changelog_url(ver: str) -> str:
    """Returns URL to changelog for specified version"""
    ver_ref = ver.replace('.', '')
    return f'{CHANGELOG_URL}#{ver_ref}'


def get_path_to_license() -> str:
    """Returns full path to license file"""
    return join(INSTALL_DIR, 'LICENSE.txt')


def get_apps_dir() -> str:
    """Returns full path to applications directory."""
    return join(config_dir, 'apps')


def get_run_configs_dir() -> str:
    """Returns full path to run configs directory."""
    return join(config_dir, 'configs')


def get_ssl_properties_file(config_name: str) -> str:
    """Returns full path to ssl.properties file"""
    return join(get_run_configs_dir(), config_name, SSL_PROPERTIES_FILE)


def get_download_cache_dir() -> str:
    """Returns full path to download cache directory."""

    if cache_dir:
        return cache_dir

    return join(config_dir, 'cache')


def get_ssl_dir() -> str:
    """Returns full path to ssl directory."""
    return join(config_dir, 'ssl')


COMPATIBLE_APPS: List[InstallableApp] = []


class RunConfig:
    """Run config dataclass"""

    # pylint: disable=too-many-instance-attributes
    def __init__(self, own_name: str, path_to_app: str, projector_port: int,
                 token: str, password: str, ro_password: str, toolbox: bool,
                 custom_fqdns: str) -> None:
        self.name: str = own_name
        self.path_to_app: str = path_to_app
        self.projector_port: int = projector_port
        self.token: str = token
        self.password: str = password
        self.ro_password: str = ro_password
        self.toolbox = toolbox
        self.fqdns = custom_fqdns

    def is_secure(self) -> bool:
        """Checks if secure configuration"""
        return self.token != ''

    def is_password_protected(self) -> bool:
        """Checks if run config is password protected"""
        return self.password != ''


def init_compatible_apps() -> List[InstallableApp]:
    """Initializes compatible apps list."""
    try:
        return load_compatible_apps(COMPATIBLE_IDE_FILE)
    except IOError as error:
        print(f'Cannot load compatible ide file: {str(error)}. Exiting...')
        sys.exit(2)


def get_projector_server_dir() -> str:
    """Returns directory with projector server jar"""
    return join(INSTALL_DIR, BUNDLED_DIR, SERVER_DIR)


def init_cache_dir() -> None:
    """Initialize download cache dir"""
    create_dir_if_not_exist(get_download_cache_dir())


def init_config_dir() -> None:
    """Initializes global config directory."""
    # pylint: disable=W0703
    try:
        create_dir_if_not_exist(config_dir)
        create_dir_if_not_exist(get_apps_dir())
        create_dir_if_not_exist(get_run_configs_dir())
        init_cache_dir()
    except Exception as exception:
        print(f'Error during initialization: {str(exception)}, cleanup ...')
        rmtree(config_dir)
        sys.exit(1)
