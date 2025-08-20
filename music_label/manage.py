#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_label.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Impossibile importare Django. Assicurati che sia installato e che l'ambiente virtuale sia attivo."
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
