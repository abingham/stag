# pylint: disable=C0103

"""Top-level application for stag.
"""

import logging
import os
import re
import sys

import baker
from eagertools import emap
import pkg_resources
from pykka.registry import ActorRegistry

from stag.actor import DispatcherActor, ParserActor, StorageActor
from stag.storage.manager import StorageManager
from stag.storage.sqlalchemy_storage import SqlAlchemyStorage as Storage

log = logging.getLogger(__file__)

def init_logging(verbose):
    """Initialize the logging system.

    Args:
      verbose: Whether detailed logging should be enabled.

    """

    if verbose:
        level = logging.INFO
    else:
        level = logging.WARNING

    logging.basicConfig(
        level=level,
        stream=sys.stdout)

def parser_plugins():
    """Generate the sequence of 'stag.parser' plugins."""

    log.info('Loading parser plugins.')

    for entry_point in pkg_resources.iter_entry_points('stag.parser'):
        plugin_class = entry_point.load()

        log.info('Plugin detected: {}'.format(plugin_class))

        plugin = plugin_class()
        yield plugin

@baker.command(
    name='scan',
    params={
        'directory': 'The directory to scan',
        'tagfile': 'The output file.',
        'verbose': 'Whether to generate verbose logging output.'})
def scan_command(directory, tagfile='STAG.sqlite', verbose=False):
    """Scan a directory tree for definitions and references."""

    init_logging(verbose)

    with StorageManager(Storage(tagfile)) as s:
        s.clear_defs()

        storage = StorageActor.start(s)
        parser_map = [
            (list(p.patterns()),
             ParserActor.start(p.create_parser(), storage))
            for p in parser_plugins()]

        dispatcher = DispatcherActor.start(parser_map)

        def dispatch_file(args):
            "Send results of os.walk to the dispatcher."
            dirpath, _, filenames = args
            for fname in filenames:
                dispatcher.tell({
                    'command': 'dispatch',
                    'filename': os.path.join(dirpath, fname)
        })

        emap(dispatch_file, os.walk(directory))

        # Shut everything down.
        ActorRegistry.stop_all()

@baker.command(
    name='find_defs',
    params={
        'name': 'The name to search.',
        'tagfile': 'The file containing tag information',
        'verbose': 'Whether to generate verbose logging output.'})
def find_definitions_command(name, tagfile='STAG.sqlite', verbose=False):
    """Find definitions for a name."""

    init_logging(verbose)

    with StorageManager(Storage(tagfile)) as s:
        for name, filename, lineno, source in s.find_definitions(name):
            print('{}:{}: {}'.format(
                filename, lineno, source))

@baker.command(
    name='match_defs',
    params={
        'pattern': 'The pattern for which to search.',
        'tagfile': 'The file containing the tag information.',
        'verbose': 'Whether to generate verbose logging output.'})
def match_definitions_command(pattern, tagfile='STAG.sqlite', verbose=False):
    """Find definitions matching a regular expression."""

    init_logging(verbose)

    with StorageManager(Storage(tagfile)) as s:
        for name, filename, lineno, source in s.definitions():
            if re.match(pattern, name):
                print('{}:{}: {}'.format(
                    filename, lineno, source))

@baker.command(
    name='find_refs',
    params={
        'name': 'The name to search.',
        'tagfile': 'The file containing tag information',
        'verbose': 'Whether to generate verbose logging output.'})
def find_references_command(name, tagfile='STAG.sqlite', verbose=False):
    """Find references to a name."""

    init_logging(verbose)

    with StorageManager(Storage(tagfile)) as s:
        for name, filename, lineno, source in s.find_references(name):
            print('{}:{}: {}'.format(
                filename, lineno, source))

@baker.command(
    name='match_refs',
    params={
        'pattern': 'The pattern for which to search.',
        'tagfile': 'The file containing the tag information.',
        'verbose': 'Whether to generate verbose logging output.'})
def match_references_command(pattern, tagfile='STAG.sqlite', verbose=False):
    """Find references matching a regular expression."""

    init_logging(verbose)

    with StorageManager(Storage(tagfile)) as s:
        for name, filename, lineno, source in s.references():
            if re.match(pattern, name):
                print('{}:{}: {}'.format(
                    filename, lineno, source))

def main():
    """Application main."""
    baker.run()

if __name__ == '__main__':
    main()
