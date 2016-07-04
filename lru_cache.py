from datetime import datetime

INFINITY = float('inf')


class LRUcache(object):
    def __init__(self, max=float('inf'), length=None, state=False, age=None, dispose=None):
        self._max = max
        if not isinstance(self._max, int):
            self._max = INFINITY
        self._length_calculator = length
        if not hasattr(length, '__call__'):
            self._length_calculator = lambda x: 1
        self._allowStale = state
        self._maxAge = age
        self._dispose = dispose
        self.reset()

    # didn't check yet
    def __iter__(self):
        k = self._mru - 1
        i = 0
        while k >= 0 and i < self._item_count:
            if self._lrulist[k]:
                i += 1
                hit = self._lrulist[k]
                if self._maxAge and datetime.now()-hit.get("now") > self._maxAge:
                    self._del(hit)
                if not self._allowStale:
                    hit = None
                if hit:
                    yield hit

    def reset(self):
        if self._dispose and hasattr(self, "_cache"):
            for key in self._cache.iteritems():
                self._dispose(key, self._cache[key].get("value"))
        self._cache = dict()
        self._lrulist = dict()
        self._mru = 0
        self._lru = 0
        self._length = 0
        self._item_count = 0

    @property
    def length(self):
        return self._length

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, max_len):
        if not max_len or not isinstance(max_len, int) or max_len < 0:
            max_len = INFINITY
        self._max = max_len

        if self._length > self._max:
            self.trim()

    # didn't check yet
    @property
    def length_calculator(self):
        return self._length_calculator

    @length_calculator.setter
    def length_calculator(self, lc):
        if not hasattr(self._length_calculator, '__call__'):
            self._length_calculator = lambda x: 1
            self._length = self._item_count
            for key in self._cache.iteritems():
                self._cache[key]["length"] = 1
        else:
            self._length_calculator = lc
            self._length = 0
            for key in self._cache.iteritems():
                self._cache[key]["length"] = self._length_calculator(self._cache[key].get("value"))
                self._length += self._cache[key].get("length")

        if self._length > self._max:
            self.trim()

    def set(self, key, value):
        if self._cache.has_key(key):
            if self._dispose:
                self._dispose(key, self._cache[key].get("value"))
            if self._maxAge:
                self._cache[key]["now"] = datetime.now()
            self._cache[key]["value"] = value
            self.get(key)
            return True

        value_len = self._length_calculator(value)
        age = datetime.now if self._maxAge else 0
        hit = dict([
            ("key", key),
            ("value", value),
            ("lu", self._mru),
            ("len", value_len),
            ("age", age)
        ])
        self._mru += 1

        if hit.get("len") > self._max:
            if self._dispose:
                self._dispose(key, self._cache[key].get("value"))
            return False

        self._length += hit.get("len")
        self._lrulist[hit.get("lu")] = self._cache[key] = hit
        self._item_count += 1

        if self._length > self._max:
            self.trim()
        return True

    def has(self, key):
        if not hasattr(self._cache, key):
            return False
        hit = self._cache[key]
        if self._maxAge and datetime.now() - hit.get("age") > self._maxAge:
            return False
        return True

    def get(self, key, need_update=True):
        hit = self._cache.get(key)
        if hit:
            if self._maxAge and datetime.now() - hit.get("age") > self._maxAge:
                self._del(hit)
                if not self._allowStale:
                    hit = None
            else:
                if need_update:
                    self.use(hit)
            hit = hit.get("value", "")
        return hit

    def delete(self, key):
        self._del(self._cache.get(key))

    def use(self, hit):
        self.shift_lu(hit)
        hit["lu"] = self._mru
        self._mru += 1
        self._lrulist[hit["lu"]] = hit

    def trim(self):
        while self._lru < self._mru and self._length > self._max:
            self._del(self._lrulist[self._lru])

    def shift_lu(self, hit):
        self._lrulist.pop(hit.get("lu"))
        while self._lru < self._mru and not self._lrulist.get(self._lru):
            self._lru += 1

    def _del(self, hit):
        if hit:
            if self._dispose:
                self._dispose(hit.get("key"), hit.get("value"))
            self._length -= hit.get("len")
            self._item_count -= 1
            self._cache.pop(hit.get("key"))
            self.shift_lu(hit)
