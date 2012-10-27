# pylint: disable=C0103, R0904

"""The various actors used in stag.

"""

import fnmatch
import logging

from pykka.gevent import GeventActor

log = logging.getLogger(__file__)

class DispatcherActor(GeventActor):
    """Actor for dispatching filenames to the proper parser.

    ``parser_map`` should be a sequence of tuples of the form
    (list-of-patterns, ParserActor) which defines how filename
    patterns are mapped to Parsers.

    """

    def __init__(self, parser_map):
        super(DispatcherActor, self).__init__()
        self.parser_map = parser_map

    def find_parser(self, filename):
        """Given a filename, find a parser registered for it. Returns
        a ``Parser`` instance or ``None``.

        """
        for patterns, parser in self.parser_map:
            for pattern in patterns:
                if fnmatch.fnmatch(filename, pattern):
                    log.info('{} matched pattern {} for parser {}'.format(
                        filename, pattern, parser))
                    return parser

    def dispatch(self, filename):
        """Map ``filename`` to a parser and tell the parser to parse
        it.

        """
        parser = self.find_parser(filename)
        if parser:
            parser.tell({
                'command': 'parse',
                'filename': filename
                })
        else:
            log.info('No parser for filename: {}'.format(filename))

    def on_receive(self, message):
        """Process a pykka message."""
        if message.get('command') == 'dispatch':
            self.dispatch(message['filename'])

        else:
            log.error('Dispatcher received unexpected message type: {}'.format(
                message))

class ParserActor(GeventActor):
    """Actor for parsing files.

    ``parser`` is a Parser subclass used to parse input files. The
    results of the parse are stored using ``storage``, a
    StorageActor.

    """

    def __init__(self, parser, storage):
        super(ParserActor, self).__init__()
        self.parser = parser
        self.storage = storage

    def on_receive(self, message):
        """Process a pykka message."""
        if message.get('command') == 'parse':
            fname = message['filename']
            self.parser.set_file(fname)
            for defn in self.parser.definitions():
                self.storage.tell({
                    'command': 'store_def',
                    'name': defn[0],
                    'filename': fname,
                    'lineno': defn[1]
                })
            for refn in self.parser.references():
                self.storage.tell({
                    'command': 'store_ref',
                    'name': refn[0],
                    'filename': fname,
                    'lineno': refn[1]
                })
        else:
            log.error('ParserActor received unexpected message: {}'.format(
                message))

class StorageActor(GeventActor):
    """Actor for managing storage.

    ``storage`` is a Storage subclass.
    """

    def __init__(self, storage):
        super(StorageActor, self).__init__()
        self.storage = storage

    def on_receive(self, message):
        """Process a pykka message."""
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