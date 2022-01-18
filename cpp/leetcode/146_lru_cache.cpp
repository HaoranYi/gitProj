#include <algorithm>
#include <iostream>
#include <vector>
#include <map>

struct lru_cache {
  std::map<int, int> storage;
  int capacity;

  std::vector<int> recent_accesses;
  // tree O(log(n))
  // hash + linklist O(N) -- sorted hashmap
  // std::list<int> recent_accesses;
  // using NodePtr = std::list<int>::iterator;
  // std::map<int, NodePtr> look_up;

  lru_cache(int cap) : capacity(cap) {}

  void update_recent_accesses(int key) {
    auto iter = std::find(recent_accesses.begin(), recent_accesses.end(), key);
    if (iter == recent_accesses.end()) {
      recent_accesses.insert(recent_accesses.begin(), key);
    }
    else {
      std::rotate(recent_accesses.begin(), iter, iter+1);
    }
  }

  int get(int key)
  {
    if (storage.find(key) != storage.end()) {
      update_recent_accesses(key);
      return storage[key];
    } else {
      return -1;
    }
  }

  void put(int key, int value) {
    if (storage.find(key) != storage.end()) {
      storage[key] = value;
      update_recent_accesses(key);
    }
    else {
      if (storage.size() < capacity) {
	storage[key] = value;
	update_recent_accesses(key);
      }
      else {
	auto del = recent_accesses.back();
	recent_accesses.pop_back();
	storage.erase(del);
	storage[key] = value;
	update_recent_accesses(key);
      }
    }
  }
};

int main() {
  lru_cache c{5};

  c.put(1, 1);
  c.put(2, 2);
  c.put(3, 3);

  std::cout << c.get(1) << "\n";
  std::cout << c.get(2) << "\n";
  std::cout << c.get(3) << "\n";
}
