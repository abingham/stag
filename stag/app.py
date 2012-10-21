from itertools import chain
import fnmatch
import logging
import os

import baker
from pykka.actor import Actor, ThreadingActor
from pykka.registry import ActorRegistry

# TODO: This will go away when we move to a plugin-parser system
import stag.python_ast_parser
from stag.storage import PrintStorage as Storage
from stag.util import consume

log = logging.getLogger(__file__)

class DispatcherActor(ThreadingActor):
    """Actor for dispatching filenames to the proper parser."""

    def __init__(self, parser_map):
        self.parser_map = parser_map

    def find_parser(self, filename):
        for pattern, parser in self.parser_map.items():
            if fnmatch.fnmatch(filename, pattern):
                return parser

    def dispatch(self, filename):
        parser = self.find_parser(filename)
        if parser:
            parser.tell({
                'command': 'parse',
                'filename': filename
                })
        else:
            log.warning('No parser for filename: {}'.format(filename))

    def on_receive(self, message):
        if message.get('command') == 'dispatch':
            self.dispatch(message['filename'])

        else:
            log.error('Dispatcher received unexpected message type: {}'.format(
                message))

class ParserActor(ThreadingActor):
    """Actor for parsing files."""

    def __init__(self, parser, storage):
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

        else:
            log.error('ParserActor received unexpected message: {}'.format(
                message))

class StorageActor(ThreadingActor):
    """Actor for managing storage."""

    def __init__(self, storage):
        self.storage = storage

    def on_receive(self, message):
        if message.get('command') == 'store_def':
            self.storage.add_def(
                message['name'],
                message['filename'],
                message['lineno'])

        else:
            log.error('StorageActor received unexpeted message: {}'.format(
                message))

@baker.command(name='scan_defs')
def scan_definitions_command(dir, filename):
    with Storage() as s:
        s.clear_defs()

        storage = StorageActor.start(s)

        parser_map = {
            '*.py': ParserActor.start(stag.python_ast_parser.Parser(), storage),
        }

        dispatcher = DispatcherActor.start(parser_map)

        # Send results of os.walk to the dispatcher
        def dispatch_file(args):
            dirpath, dirnames, filenames = args
            for fname in filenames:
                dispatcher.tell({
                    'command': 'dispatch',
                    'filename': os.path.join(dirpath, fname)
        })

        consume(map(dispatch_file, os.walk(dir)))

        # Shut everything down.
        ActorRegistry.stop_all()

if __name__ == '__main__':
    import sys
    logging.basicConfig(
        level=logging.DEBUG,
        stream=sys.stdout)
    baker.run()