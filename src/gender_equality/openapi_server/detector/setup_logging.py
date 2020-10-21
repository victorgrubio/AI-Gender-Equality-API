# -*- coding: utf-8 -*-
# @Author: Victor Garcia
# @Date:   2018-12-10 13:39:15
# @Last Modified by:   Victor Garcia
# @Last Modified time: 2018-12-10 13:42:04
from os import getenv
from os.path import dirname, join, sep, exists, abspath
import logging.config
import yaml


def setup_logging(
    default_path='log/logging.yaml',
    default_level=logging.DEBUG,
    env_key='LOG_CFG'):
    """
    Setup logging configuration
    """
    dir_path = dirname(abspath(__file__))
    path = join(sep, dir_path, default_path)
    value = getenv(env_key, None)
    if value:
        path = value
    if exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
