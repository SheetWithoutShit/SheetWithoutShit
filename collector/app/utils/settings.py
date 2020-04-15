"""This module provides utils for parsing config."""

import argparse
import os

DEFAULT_HOST = os.getenv('DEFAULT_HOST')
DEFAULT_PORT = os.getenv('DEFAULT_PORT')


def get_config(argv=None):
    """Parse configs from command line."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str,
                        help="Setup application host")
    parser.add_argument("--port", type=int,
                        help="Setup application port")

    # ignore unknown options
    options, _ = parser.parse_known_args(argv)
    config = {
        'host': options.host if options.host is not None else DEFAULT_HOST,
        'port': options.port if options.port is not None else DEFAULT_PORT
    }
    return config
