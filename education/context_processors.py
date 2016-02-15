from education import __version__, __commit__


def version(request):
    return {
        'version': __version__,
        'commit': __commit__,
    }
