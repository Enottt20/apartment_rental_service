import sys

if 'tests' not in sys.argv[0]:
    import app

    __all__= [app]