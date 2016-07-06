__author__ = 'denonw'

import unittest
from lru_cache.lru_cache import LRUcache


class LRUcacheForEachTestCase(unittest.TestCase):
    def test_foreach(self):
        cache = LRUcache(5)
        for i in range(10):
            cache.set(str(i), str(i))

        i = 9
        for item in cache:
            self.assertEquals(item.get("key"), str(i))
            self.assertEquals(item.get("value"), str(i))
            i -= 1

        cache.get("6")
        cache.get("8")
        order = [8, 6, 9, 7, 5]
        i = 0
        for item in cache:
            j = order[i]
            self.assertEquals(item.get("key"), str(j))
            self.assertEquals(item.get("value"), str(j))

    def test_keys_and_values(self):
        cache = LRUcache(5)
        for i in range(10):
            cache.set(i, str(i))

        self.assertEquals(cache.keys, [9, 8, 7, 6, 5])
        self.assertEquals(cache.values, ["9", "8", "7", "6", "5"])
