import unittest
from lru_cache.lru_cache import LRUcache


class LRUcacheBasicTestCase(unittest.TestCase):
    def test_basic(self):
        cache = LRUcache(max=10)
        cache.set("key", "value")
        self.assertEquals(cache.get("key"), "value")
        self.assertEquals(cache.get("nada"), None)
        self.assertEquals(cache.length, 1)
        self.assertEquals(cache.max, 10)

    def test_least_recently_set(self):
        cache = LRUcache(max=2)
        cache.set("A", "a")
        cache.set("B", "b")
        cache.set("C", "c")
        self.assertEquals(cache.get("A"), None)
        self.assertEquals(cache.get("C"), "c")

    def test_lru_recently_gotten(self):
        cache = LRUcache(max=2)
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
        cache = LRUcache(max=3)
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

    def test_reset(self):
        cache = LRUcache(max=10)
        cache.set("A", "a")
        cache.set("B", "b")
        cache.reset()
        self.assertEquals(cache.length, 0)
        self.assertEquals(cache.get("A"), None)
        self.assertEquals(cache.get("B"), None)

    def test_calculate_length(self):
        cache = LRUcache(max=100, length=lambda x: x.get("size"))
        cache.set("key", {"val": "value", "size": 50})
        self.assertEquals(cache.get("key").get("val"), "value")
        self.assertEquals(cache.get("none"), None)
        self.assertEquals(cache.length_calculator(cache.get("key")), 50)
        self.assertEquals(cache.length, 50)
        self.assertEquals(cache.max, 100)

    def test_calculate_length_too_long(self):
        cache = LRUcache(max=10, length=lambda x: x.get("size"))
        cache.set("key", {"val": "value", "size": 50})
        self.assertEquals(cache.length, 0)
        self.assertEquals(cache.get("key"), None)

    def test_least_recently_set_with_weighted_length(self):
        cache = LRUcache(max=8, length=lambda x: len(x))
        cache.set("A", "a")
        cache.set("B", "bb")
        cache.set("C", "ccc")
        cache.set("D", "dddd")
        self.assertEquals(cache.get("D"), "dddd")
        self.assertEquals(cache.get("C"), "ccc")
        self.assertEquals(cache.get("B"), None)
        self.assertEquals(cache.get("A"), None)

    def test_lru_recently_gotten_with_weighed_length(self):
        cache = LRUcache(max=8, length=lambda a: len(a))
        cache.set("A", "a")
        cache.set("B", "bb")
        cache.set("C", "ccc")
        cache.get("A")
        cache.get("B")
        cache.set("D", "dddd")
        self.assertEquals(cache.get("C"), None)
        self.assertEquals(cache.get("D"), "dddd")
        self.assertEquals(cache.get("B"), "bb")
        self.assertEquals(cache.get("A"), "a")

if __name__ == "__main__":
    unittest.main()


