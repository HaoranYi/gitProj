#include <iostream>
#include <map>
#include <functional>  //std::less
#include <utility>     //std::forward

template<typename T1, typename T2>
struct key_comp {
  bool operator()(const T1& x, T2 const& y)
  {
    return x > y;
  }
};

// perfect forwarding: forward lvaue as either lvalue or rvalue depending on T
template<typename... Ts>
struct ff {
  bool operator()(Ts&&... args) {
    return key_comp<Ts...>{}(std::forward<Ts>(args)...);
  }
};

int main()
{
  std::map<int, int, key_comp<int, int>> m;
  for (int i = 0; i < 10; i++)
  {
    m[i] = i;
  }

  // desending order
  for (const auto& x :m)
    std::cout << x.first << ' ' << x.second << '\n';

  auto f = [](auto x, auto y) { return x + y; };
  std::cout << f(1.0, 2.0) << "\n";

  std::cout << std::boolalpha << ff<int, int>{}(1.0, 2.0) << "\n";
}
