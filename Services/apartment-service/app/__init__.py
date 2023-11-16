import sys

if 'test' not in sys.argv[0]:
    from app.app import app

    __all__= [app]