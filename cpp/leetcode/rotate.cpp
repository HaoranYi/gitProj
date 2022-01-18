#include <iostream>
#include <vector>
#include <algorithm>
#include <iterator>

void print_vec(std::vector<int>& v)
{
  for (auto& x : v)
    std::cout << x << ",";
  std::cout << "\n";
}

void insertion_sort(std::vector<int>& v)
{
  for (auto i = v.begin(); i != v.end(); i++) {
    std::rotate(std::upper_bound(v.begin(), i, *i), i, i+1);
  }
}

int main()
{
  std::vector<int> a = {1,2,3,4,5,6,7,8,9,10};
  print_vec(a);

  std::random_shuffle(a.begin(), a.end());  // reverse, swap, rotate
  print_vec(a);
  insertion_sort(a);
  print_vec(a);

  auto p = std::find(a.begin(), a.end(), 4);

  //std::rotate(a.begin(), p, a.end());
  auto n = std::distance(a.begin(), p);

  // std::vector<int> tmp(n);
  // std::copy(a.begin(), p, tmp.begin());
  // std::copy(p, a.end(), a.begin());
  // std::copy(tmp.begin(), tmp.end(), a.end() - n );

  print_vec(a);
}
