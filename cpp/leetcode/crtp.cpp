#include <iostream>
#include <vector>
#include <string>

template<typename T>
struct Base
{
  void print()
  {
    T& derived = static_cast<T&>(*this);
    std::cout << derived.get_name() << "\n";
  }
};

struct Derived : Base<Derived>
{
  std::string get_name()
  {
    return "haha";
  }
};

struct Derived2 : Base<Derived2>
{
  std::string get_name()
  {
    return "hoho";
  }
};

int main()
{
  Derived d1;
  Derived2 d2;

  d1.print();
  d2.print();
}
