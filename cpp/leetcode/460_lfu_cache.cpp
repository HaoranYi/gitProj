#include <iostream>
#include <vector>
#include <chrono

struct Freq {
  int key;
  int counts;
  int ts;
};

bool operator<(Freq& x, Freq& y) {
  if (x.couts < y.counts)
    return true;
  if (x.count == y.counts) {
    return x.ts > y.ts;
  }
  return false;
}

template<typename V, int S>
struct LFU_cache {
  std::map<int, V> _cache;
  std::vector<Freq> _freq_counts;

  V get(int k) {
    return _cache.at(k);
  }

  void put(int k, V& v) {
    auto add_entry = [this](auto k, auto v) {
			_cache.emplace(std::make_pair(k, v));
			auto ts = std::chrono::system_clock::now();
			Freq fq{k, 1, ts};
			auto iter = std::lower_bound(_freq_counts.begin(), _freq_count.end(), fq);
			_freq_counts.insert(iter, fq);
		     };

    if (_cache.find(k) == _cache.end()) {
      if (_cache.size() < S) {
	add_entry(k, v);
      }
      else {
	auto replace_key = _freq_counts[0].key;
	_cache.erase(replace_key);
	_freq_counts.erase(_freq_counts.begin());
	add_entry(k, v);
      }
    }
    else {
      // update
      _cache[k] = v;
      auto iter = std::find_if(_freq_counts.begin(), _freq_counts.end(), [k](auto& x) { return x.key == k; });
      auto fq = (*iter);
      fq.count++;
      fq.ts = std::chrono::system_clock::now();
      _freq_counts.erase(iter);
      auto iter = std::lower_bound(_cache.begin(), _cache.end(), fq);
      _freq_counts.insert(iter, fq);
    }
  }
};
