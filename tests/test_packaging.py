# Guards against the packaging being wrong: without src on the path, everything
# downstream fails in ways that look like analysis bugs.
import pricediscovery


def test_package_imports():
    assert pricediscovery.__doc__
