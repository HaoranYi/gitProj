#include <iostream>
#include <variant>
#include <vector>
#include <string>

// C++17

template<typename... Bases>
struct overloaded : Bases...
{
  using Bases::operator()...;
};

// deduction guide (can be ommitted in c++ 20)
template<typename... Bases>
overloaded(Bases...) -> overloaded<Bases...>;

overloaded printer = {
  [](auto arg) { std::cout << arg << ' '; },
  [](int arg) { std::cout << arg << ' '; },
  [](double arg) { std::cout << arg << ' '; },
  [](const char* arg) { std::cout << arg << ' '; }
  [](std::string arg) { std::cout << arg << ' '; }
};

int main()
{
  using var_t = std::variant<int, std::string, double>;

  std::vector<var_t> v = {1, "hello world"};

  for (auto& t : v) {
    std::visit(printer, t);
  }

  std::cout << "\n";
  printer("hello world!");

}
