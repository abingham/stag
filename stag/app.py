from itertools import chain
import fnmatch
import logging
import os
import re
import sys

import baker
from eagertools import emap
import pkg_resources
from pykka.actor import Actor
from pykka.gevent import GeventActor
from pykka.registry import ActorRegistry

from stag.storage.sqlalchemy_storage import SqlAlchemyStorage as Storage
from stag.util import consume

log = logging.getLogger(__file__)

class DispatcherActor(GeventActor):
    """Actor for dispatching filenames to the proper parser."""

    def __init__(self, parser_map):
        super(DispatcherActor, self).__init__()
        self.parser_map = parser_map

    def find_parser(self, filename):
        for patterns, parser in self.parser_map:
            for pattern in patterns:
                if fnmatch.fnmatch(filename, pattern):
                    log.info('{} matched pattern {} for parser {}'.format(
                        filename, pattern, parser))
                    return parser

    def dispatch(self, filename):
        parser = self.find_parser(filename)
        if parser:
            parser.tell({
                'command': 'parse',
                'filename': filename
                })
        else:
            log.info('No parser for filename: {}'.format(filename))

    def on_receive(self, message):
        if message.get('command') == 'dispatch':
            self.dispatch(message['filename'])

        else:
            log.error('Dispatcher received unexpected message type: {}'.format(
                message))

class ParserActor(GeventActor):
    """Actor for parsing files."""

    def __init__(self, parser, storage):
        super(ParserActor, self).__init__()
        self.parser = parser
        self.storage = storage

    def on_receive(self, message):
        if message.get('command') == 'parse':
            fname = message['filename']
            self.parser.set_file(fname)
            for d in self.parser.definitions():
                self.storage.tell({
                    'command': 'store_def',
                    'name': d[0],
                    'filename': fname,
                    'lineno': d[1]
                })
            for r in self.parser.references():
                self.storage.tell({
                    'command': 'store_ref',
                    'name': r[0],
                    'filename': fname,
                    'lineno': r[1]
                })
        else:
            log.error('ParserActor received unexpected message: {}'.format(
                message))

class StorageActor(GeventActor):
    """Actor for managing storage."""

    def __init__(self, storage):
        super(StorageActor, self).__init__()
        self.storage = storage

    def on_receive(self, message):
        if message.get('command') == 'store_def':
            self.storage.add_def(
                message['name'],
                message['filename'],
                message['lineno'])
        elif message.get('command') == 'store_ref':
            self.storage.add_ref(
                message['name'],
                message['filename'],
                message['lineno'])
        else:
            log.error('StorageActor received unexpeted message: {}'.format(
                message))

def init_logging(verbose):
    if verbose:
        level = logging.INFO
    else:
        level = logging.WARNING

    logging.basicConfig(
        level=level,
        stream=sys.stdout)

def parser_plugins():
    log.info('Loading parser plugins.')

    for entry_point in pkg_resources.iter_entry_points('stag.parser'):
        plugin_class = entry_point.load()

        log.info('Plugin detected: {}'.format(plugin_class))

        plugin = plugin_class()
        yield plugin

@baker.command(name='scan')
def scan_command(dir, filename='STAG', verbose=False):
    init_logging(verbose)

    with Storage(filename) as s:
        s.clear_defs()

        storage = StorageActor.start(s)
        parser_map = [
            (list(p.patterns()),
             ParserActor.start(p.create_parser(), storage))
            for p in parser_plugins()]

        dispatcher = DispatcherActor.start(parser_map)

        # Send results of os.walk to the dispatcher
        def dispatch_file(args):
            dirpath, dirnames, filenames = args
            for fname in filenames:
                dispatcher.tell({
                    'command': 'dispatch',
                    'filename': os.path.join(dirpath, fname)
        })

        emap(dispatch_file, os.walk(dir))

        # Shut everything down.
        ActorRegistry.stop_all()

@baker.command(name='find_defs')
def find_definitions_command(name, filename='STAG', verbose=False):
    init_logging(verbose)

    with Storage(filename) as s:
        for name, filename, lineno in s.find_definitions(name):
            print('{}:{}: {}'.format(
                filename, lineno, name))

@baker.command(name='match_defs')
def match_definitions_command(pattern, filename='STAG', verbose=False):
    init_logging(verbose)

    with Storage(filename) as s:
        for name, filename, lineno in s.definitions():
            if re.match(pattern, name):
                print('{}:{}: {}'.format(
                    filename, lineno, name))

@baker.command(name='find_refs')
def find_references_command(name, filename='STAG', verbose=False):
    init_logging(verbose)

    with Storage(filename) as s:
        for name, filename, lineno in s.find_references(name):
            print('{}:{}: {}'.format(
                filename, lineno, name))

@baker.command(name='match_refs')
def match_references_command(pattern, filename='STAG', verbose=False):
    init_logging(verbose)

    with Storage(filename) as s:
        for name, filename, lineno in s.references():
            if re.match(pattern, name):
                print('{}:{}: {}'.format(
                    filename, lineno, name))

def main():
    baker.run()

if __name__ == '__main__':
    main()
