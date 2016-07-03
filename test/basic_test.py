import unittest
from lru_cache.lru_cache import LRUcache


class LRUcacheBasicTestCase(unittest.TestCase):
    def test_basic(self):
        cache = LRUcache(10)
        cache.set("key", "value")
        self.assertEquals(cache.get("key"), "value")
        self.assertEquals(cache.get("nada"), None)
        self.assertEquals(cache.length, 1)
        self.assertEquals(cache.max, 10)

    def test_least_recently_set(self):
        cache = LRUcache(2)
        cache.set("A", "a")
        cache.set("B", "b")
        cache.set("C", "c")
        self.assertEquals(cache.get("A"), None)
        self.assertEquals(cache.get("C"), "c")

    def test_lru_recently_gotten(self):
        cache = LRUcache(2)
        cache.set("A", "a")
        cache.set("B", "b")
        cache.get("A")
        cache.set("C", "c")
        self.assertEquals(cache.get("C"), "c")
        self.assertEquals(cache.get("B"), None)
        self.assertEquals(cache.get("A"), "a")

    def test_del(self):
        cache = LRUcache(2)
        cache.set("A", "a")
        cache.delete("A")
        self.assertEquals(cache.get("A"), None)

    def test_max(self):
        cache = LRUcache(3)
        cache.max = 100
        for i in range(100):
            cache.set(i,i)
        self.assertEquals(cache.length, 100)
        for i in range(100):
            self.assertEquals(cache.get(i), i)
        cache.max = 3
        self.assertEquals(cache.length, 3)
        for i in range(97):
            self.assertEquals(cache.get(i), None)
        for i in range(98, 100):
            self.assertEquals(cache.get(i), i)

        cache.max = "Hello"
        for i in range(100):
            cache.set(i, i)
        self.assertEquals(cache.length, 100)
        for i in range(100):
            self.assertEquals(cache.get(i), i)
        cache.max = 3
        self.assertEquals(cache.length, 3)
        for i in range(97):
            self.assertEquals(cache.get(i), None)
        for i in range(98, 100):
            self.assertEquals(cache.get(i), i)

if __name__ == "__main__":
    unittest.main()


