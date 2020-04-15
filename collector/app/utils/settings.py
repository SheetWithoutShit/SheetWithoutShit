"""This module provides utils for parsing config."""
import argparse
import pathlib

import trafaret as T
from trafaret_config import commandline

TRAFARET = T.Dict({
    T.Key('host'): T.IP,
    T.Key('port'): T.Int(),
})

BASE_DIR = pathlib.Path(__file__).parent.parent
DEFAULT_CONFIG_PATH = BASE_DIR / 'config' / 'default.yaml'


def get_config(argv=None):
    """Parse configs from command line."""
    arg_parser = argparse.ArgumentParser()
    commandline.standard_argparse_options(
        arg_parser,
        default_config=DEFAULT_CONFIG_PATH
    )

    # ignore unknown options
    options, _ = arg_parser.parse_known_args(argv)

    config = commandline.config_from_options(options, TRAFARET)
    return config
