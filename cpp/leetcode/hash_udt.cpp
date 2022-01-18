#include <iostream>
#include <unordered_set>
#include <string>
#include <functional>

struct S {
  std::string first_name;
  std::string last_name;
};

bool operator==(const S& lhs, const S& rhs) {
  return (lhs.first_name == rhs.first_name) && (lhs.last_name == rhs.last_name);
}

struct MyHash {
  std::size_t operator()(S const& s) const noexcept {
    auto h1 = std::hash<std::string>{}(s.first_name);
    auto h2 = std::hash<std::string>{}(s.last_name);
    return h1 & (h2 << 1);
  }
};

template<>
struct std::hash<S> {
  std::size_t operator()(S const& s) const {
    return MyHash{}(s);
  }
};

int main() {
  std::unordered_set<S> s;
  s.insert({"aa", "bb"});
  s.insert({"cc", "dd"});

  for (auto x : s) {
    std::cout << x.first_name << ' ' << x.last_name << "\n";
  }
}
