import collections
import configparser
import logging
import os
import sys
import traceback
from collections import OrderedDict
from pathlib import Path

import yaml

#meaningless change10

def __json_error_generator(error, trace):
    """A generator function used to capture the exception and its stack trace."""

    def d(*args, **kwargs):
        """
        This is a scoped function that will be added to the exception object.
        This function allows the DSLogger to print exceptions into the logs
        in a way that is consistent with the intended design of the DSLogger.
        """
        return {
            "error": True,
            "type": error.__class__.__name__,
            "message": error.message if hasattr(error, "message") else str(error),
            "trace": trace,
        }

    return d


def safe_wrap(*a, fn=None, verbose=True, log_fn=logging.error, exceptions=None, **kw):
    """
    Call a function, with parameters, returning an object that can be re-ran
    """

    def c():
        try:
            return True, fn(*a, **kw), None
        except Exception as e:
            # Send stack trace to the logs, if logging.
            stacktrace = []
            if verbose:
                exc_type, _, exc_traceback = sys.exc_info()
                # sending whole stack trace on a single line
                stacktrace = traceback.format_tb(exc_traceback)
                stacktrace.append(f"{e.__class__.__name__}({e})")
                if exceptions and (
                    exc_type == exceptions
                    or (hasattr(exceptions, "__iter__") and exc_type in exceptions)
                ):
                    safe_log(stacktrace, log_fn)
                else:
                    logging.error(stacktrace)

            e.__json__ = __json_error_generator(e, stacktrace)
            return False, None, e

    c.success, c.value, c.error = c()
    return c


def safe_call(*a, fn=None, verbose=True, log_fn=logging.error, exceptions=None, **kw):
    """
    Call a function, return only (success, value || error)
    """
    e = safe_wrap(
        *a, fn=fn, verbose=verbose, log_fn=log_fn, exceptions=exceptions, **kw
    )
    return (e.success, e.value) if e.success else (e.success, e.error)


def safe_execute(*a, fn=None, default=None, exception=Exception, **kw):
    """Call a function without raising"""
    try:
        return fn(*a, **kw)
    except exception:
        return default


def safe_unpack(fn, value, kw=None):
    """unpacks the value and passes it to the function"""

    if isinstance(value, dict):
        return fn(**value)

    if isinstance(value, str) and isinstance(kw, dict):
        value_dict = kw.get(value) or {}
        return safe_unpack(fn, value_dict)

    return fn()


def safe_log(trace, log_fn):
    """Logs traceback based on preferred log function."""
    try:
        if log_fn.__module__ == "logging" and log_fn.__qualname__ in (
            "debug",
            "info",
            "warning",
            "error",
            "critical",
        ):
            log_fn(trace)
        else:
            logging.error(
                "Invalid function passed to safe_log. Please only pass logging functions."
            )
            logging.error(trace)
    except Exception as e:
        logging.error(e)
        logging.error(trace)


def listify(o):
    """Create lists from objects"""
    if o is None:
        return []
    if isinstance(o, list):
        return o
    if isinstance(o, str):
        return [o]
    if isinstance(o, dict):
        return [o]
    if isinstance(o, Iterable):
        return list(o)
    return [o]


def d_merge(a, b, *others):
    """Recursive dictionary merge."""
    c = a.copy()
    for k, v in b.items():
        if (
            k in c
            and isinstance(b.get(k), dict)
            and isinstance(c[k], collections.Mapping)
        ):
            c[k] = d_merge(c[k], b[k])
        elif not k in c:
            c[k] = b[k]
    return d_merge(c, *others) if bool(others) else c


def lower_key(d):
    """Convert a dictionary to lower-case string keys."""
    return {str(k).lower(): v for k, v in d.items()}


def filter_dictionary(keys, d):
    """Reduce a dictionary to items in a white list."""
    d = lower_key(d)
    output = OrderedDict()
    for key in keys:
        key = str(key).lower()
        if key in d:
            output[key] = d[key]
    return dict(output)


def path_yield(*paths):
    """Convert strings to paths and yield them if they exist."""
    for path in paths:
        path = Path(path)
        if path.exists():
            yield path


def contents(path, mode="r"):
    """Read and return the path or return None."""
    try:
        return open(path, mode).read()
    except:
        return None


def path_contents(*paths, mode="r"):
    """For all paths, yield the contents."""
    for path in path_yield(*paths):
        yield contents(path)


def yaml_read(path, allowed_terms: list):
    """Safely read a YAML path."""
    try:
        result = yaml.load(contents(path), Loader=yaml.FullLoader)
        return filter_dictionary(keys=allowed_terms, d=result) if bool(result) else {}
    except:
        return {}


def config_read(path, allowed_terms: list):
    """Read an ini file, prepending the keys with the section name."""
    config = configparser.ConfigParser()
    config.read(path)
    d = {}
    for section in config.sections():
        d1 = {f"{section}_{k}": v for k, v in dict(config[section]).items()}
        d1 = filter_dictionary(allowed_terms, d1)
        d = d_merge(d, d1)
    return d


def is_ini(path):
    return ".ini" in Path(path).suffixes


def parse(path):
    """Read an ini or yaml file, returning a dictionary of key value pairs."""
    return config_read(path) if is_ini(path) else yaml_read(path)


def get_config(*paths):
    """Read all configuration files, merging the results."""
    d = {}
    for path in path_yield(*paths):
        d = d_merge(d, parse(path))
    return d


def delete_directory_contents(dir_path: str):
    """Delete all files from a specified directory."""
    for file in os.listdir(dir_path):
        os.remove(os.path.join(dir_path, file))
