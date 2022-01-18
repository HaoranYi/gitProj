#include <iostream>
#include <atomic>

int main()
{
  std::atomic<int> x{5};

  auto y = x.fetch_add(1);  // useful for threads to parallel comsume the items in the array

  std::cout << x << ' ' << y << std::endl;

  y = 6;

  auto b = x.compare_exchange_strong(y, 7);
  std::cout << b << ' ' << x << std::endl;
}
