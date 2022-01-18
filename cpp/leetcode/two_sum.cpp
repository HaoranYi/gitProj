#include <array>
#include <map>
#include <iostream>

constexpr int target = 9;

const int arr[] = {2, 7, 11, 15};

int main()
{
  std::map<int, int> m;

  for (auto x : arr) {
    auto l = target - x;
    if (m.find(l) == m.end())
    {
      m[x] = 0;
    }
    else
    {
      std::cout << x << " " << l << "\n";
      return 0;
    }
  }
}
