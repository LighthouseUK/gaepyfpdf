"""
This is a stripped down version of cachepy: https://github.com/scidam/cachepy

I have removed the function value caching code and exposed just the methods for storing and fetching data.

.. codeauthor:: Dmitry Kislov <kislov@easydan.com>
.. codeauthor:: Matt Badger <foss@lighthouseuk.net>

"""
import warnings
import datetime
import base64
import sys

try:
    basestring = basestring
except NameError:
    basestring = str


try:
    import cPickle as pickle
except ImportError:
    import pickle

__all__ = ('Cache', 'memcache')


def _validate_key(key):
    """Returns validated key or None"""

    if not isinstance(key, basestring):
        return None
    elif len(key) > 1000:
        return None
    else:
        return key


def _load_safely_or_none(sdata):
    result = None
    try:
        result = pickle.loads(base64.b64decode(sdata))
    except:
        warnings.warn("Could not load data.", RuntimeWarning)
    return result


def _dump_safely_or_none(data):
    result = ''
    try:
        result = base64.b64encode(pickle.dumps(data))
    except:
        warnings.warn("Data could be serialized.", RuntimeWarning)
    return result


class RamDisk(object):
    """
    Simple cache for storing data in memory.

    .. note::
            - dict-like object, that performs storing and retrieving data via backend['chash']
            (e.g. `__getitem__, __setitem__`)
    """

    def __init__(self):
        self._cache = {}

    def _tostring(self, data, expired=None, noc=0, ncalls=0):
        """
        Serialize data to string.

        Cache expiration date and the number of querying cache
        is stored in this string.

        **Parameters**

        :param data: any python serializable (by pickle) object
        :param expired: data of cache expiration or None (default)
        :param noc:  number of calls
        :type expired: datetime,  None
        :type noc: int
        :type ncalls: int
        :returns: serialized data
        :rtype: str
        """
        return _dump_safely_or_none((data, expired, noc, ncalls))

    def _fromstring(self, sdata):
        """
        Deserialize (and decrypt if key is provided) cached
        data stored in the sdata (string).

        :param sdata: a string
        :returns: a python object
        """
        if sys.version_info >= (3, 0):
            sdata = sdata.decode('utf-8')
        if not isinstance(sdata, basestring):
            warnings.warn("Input data must be a string", RuntimeWarning)
            return

        return _load_safely_or_none(sdata)

    def store_data(self, cache_key, data, ttl=0, noc=0, ncalls=0):
        if ttl:
            expired = datetime.datetime.now() + datetime.timedelta(seconds=ttl)
        else:
            expired = datetime.datetime.now()

        self._cache[cache_key] = self._tostring(data, expired=expired, noc=noc, ncalls=ncalls)

    def get_data(self, cache_key, ttl=0, noc=0):
        """
        Get data from cache.

        :param cache_key: a string
        :param ttl: time-to-live in seconds
        :param noc: maximum number of cached data retrieving
        :type ttl: int
        :type noc: int
        :returns: a python object (representing sotred data)
        """
        res = None
        if cache_key in self._cache:
            res = self._fromstring(self._cache[cache_key])
        if isinstance(res, tuple):
            updated = (res[0], res[1], res[2], res[3]+1)
            self._cache[cache_key] = self._tostring(updated[0], expired=updated[1], noc=updated[2], ncalls=updated[3])
            if noc and updated[3] >= noc:
                res = None
                del self._cache[cache_key]
            if res is not None:
                if ttl and datetime.datetime.now() > res[1]:
                    res = None
                    del self._cache[cache_key]
        return res[0] if res else None