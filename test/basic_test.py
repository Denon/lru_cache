__author__ = 'denonw'

import unittest
import time
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

    def test_dump(self):
        pass

    def test_set_returns_proper_booleans(self):
        cache = LRUcache(max=5, length=lambda x: len(x))
        self.assertEquals(cache.set("A", "a"), True)
        self.assertEquals(cache.set("B", "bbbbbb"), False)
        self.assertEquals(cache.set("B", "b"), True)
        self.assertEquals(cache.set("C", "c"), True)

    def test_drop_the_old_items(self):
        cache = LRUcache(max=5, max_age=3)
        cache.set("A", "a")
        time.sleep(1)
        cache.set("B", "b")
        self.assertEquals(cache.get("A"), "a")
        time.sleep(3)
        cache.set("C", "c")
        self.assertEquals(cache.get("A"), None)
        time.sleep(2)
        self.assertEquals(cache.get("B"), None)
        self.assertEquals(cache.get("C"), "c")
        time.sleep(3)
        self.assertEquals(cache.get("C"), None)

    def test_disposal_function(self):
        dispose = [False]
        def helper(k, v):
            dispose[0] = v
        cache = LRUcache(max=1, dispose=helper)
        cache.set(1, 1)
        cache.set(2, 2)
        self.assertEquals(dispose[0], 1)
        cache.set(3, 3)
        self.assertEquals(dispose[0], 2)
        cache.reset()
        self.assertEquals(dispose[0], 3)

    def test_disposal_function_on_too_big_of_item(self):
        dispose = [False]
        def helper(k, v):
            dispose[0] = v
        cache = LRUcache(max=1, length=lambda x: len(x), dispose=helper)
        self.assertEquals(dispose[0], False)
        obj = [1, 2]
        cache.set("obj", obj)
        self.assertEquals(dispose[0], obj)

    def test_has(self):
        cache = LRUcache(max=1, max_age=3)
        cache.set("foo", "bar")
        self.assertEquals(cache.has("foo"), True)
        cache.set('blu', 'baz')
        self.assertEquals(cache.has("foo"), False)
        self.assertEquals(cache.has("blu"), True)
        time.sleep(4)
        self.assertEquals(cache.has("blu"), False)

    def test_stale(self):
        cache = LRUcache(max_age=2, stale=True)
        cache.set("foo", "bar")
        self.assertEquals(cache.get("foo"), "bar")
        self.assertEquals(cache.has("foo"), True)
        time.sleep(3)
        self.assertEquals(cache.has("foo"), False)
        self.assertEquals(cache.get("foo"), "bar")
        self.assertEquals(cache.get("foo"), None)

    def test_lru_update_via_set(self):
        cache = LRUcache(max=2)
        cache.set('foo', 1)
        cache.set('bar', 2)
        cache.delete('bar')
        cache.set('baz', 3)
        cache.set('qux', 4)
        self.assertEquals(cache.get("foo"), None)
        self.assertEquals(cache.get("bar"), None)
        self.assertEquals(cache.get("baz"), 3)
        self.assertEquals(cache.get("qux"), 4)

    def test_least_recently_set_peek(self):
        cache = LRUcache(2)
        cache.set("A", "a")
        cache.set("B", "b")
        self.assertEquals(cache.peek("A"), "a")
        cache.set("C", "c")
        self.assertEquals(cache.get("C"), "c")
        self.assertEquals(cache.get("B"), "b")
        self.assertEquals(cache.get("A"), None)

    def test_pop_the_least_used_item(self):
        cache = LRUcache(3)
        cache.set("A", "a")
        cache.set("B", "b")
        cache.set("C", "c")
        self.assertEquals(cache.length, 3)
        self.assertEquals(cache.max, 3)
        cache.get("B")
        last = cache.pop()
        self.assertEquals(last.get("key"), "A")
        self.assertEquals(last.get("value"), "a")
        self.assertEquals(cache.length, 2)
        self.assertEquals(cache.max, 3)

        last = cache.pop()
        self.assertEquals(last.get("key"), "C")
        self.assertEquals(last.get("value"), "c")
        self.assertEquals(cache.length, 1)
        self.assertEquals(cache.max, 3)

        last = cache.pop()
        self.assertEquals(last.get("key"), "B")
        self.assertEquals(last.get("value"), "b")
        self.assertEquals(cache.length, 0)
        self.assertEquals(cache.max, 3)

        last = cache.pop()
        self.assertEquals(last, None)
        self.assertEquals(cache.length, 0)
        self.assertEquals(cache.max, 3)

if __name__ == "__main__":
    unittest.main()


