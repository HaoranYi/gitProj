#include<iostream>
#include<array>
#include<algorithm>

void count_sort(std::array<int, 5>& a)
{
  std::fill(a.begin(), a.end(), []{return 10;}());
  for (auto x : a)
    std::cout << x << std::endl;
}

int main()
{
  std::array<int, 5> a;
  count_sort(a);
}
