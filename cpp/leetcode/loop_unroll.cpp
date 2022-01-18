#include <utility>
#include <iostream>

template<int... Is>
void for_helper(std::integer_sequence<int, Is...> const&)
{
  using unused = int[];
  (void)unused{0, (std::cout << Is << std::endl, 0)... };
}

int main()
{
  for_helper(std::make_integer_sequence<int, 42>{});
}
