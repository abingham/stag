#pylint: disable=W0232

"""Provides the interface for Parser plugins."""

class ParserPlugin:
    """This defines the interface for plugins that provide parsers for
    stag.

    Plugins do not need to subclass from this (though they are free
    to), but they must adhere to the interface.

    A parser plugin provides the following:

      * A name to which users can refer

      * A set of regular expressions describing the default set of
        filenames for which the parser operats (these can be
        overridden by users.)

      * A factory function for constructing Parser instances.

    """

    @property
    def name(self):
        """The name of this plugin."""

        raise NotImplementedError(
            'Parser plugins must implement the `name` property.')

    def patterns(self):
        """Get an iterable of regular expressions which determine the
        filenames for which this plugin's parser apply.

        """

        raise NotImplementedError(
            'Parser plugins must implement `patterns()`.')

    def create_parser(self):
        """Construct a new parser instance.

        stag may instantiate more than one parser instance for a given
        plugin. Each call to this function should return a new parser
        instance, one which is able to operate in a potentially
        different thread from all other instances.

        """

        raise NotImplementedError(
            'Parser plugins must implement `create_parser()`.')
