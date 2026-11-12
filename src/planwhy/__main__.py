"""Support ``python -m planwhy`` by delegating to the safe CLI entry point."""

import sys

from .cli import main


if __name__ == "__main__":
    sys.exit(main())
