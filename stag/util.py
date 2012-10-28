from pathlib import Path

def seek_file_up(filename):
    """Look for ``filename`` in the current directory and all ancestor
    directories in turn until it's found.

    Args:
      filename: The name of the file to find. This should be a simple
        filename with no directory component.

    Return: The abslute path to ``filename`` (as a string) or None if
      it's not found.

    """

    def seek_rec(filename, dirpath):
        "Recursive seek method."

        filepath = dirpath[filename]

        # Look in the current directory
        if filepath.exists() and filepath.is_file():
            return filepath

        # If we've reached root, terminate.
        elif dirpath == Path(dirpath.root):
            return None

        # Else check the parent directory.
        else:
            return seek_rec(filename, dirpath.parent())

    return seek_rec(filename, Path('.').absolute())
