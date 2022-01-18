// find the smallest 11...1, N, such that it mod K
// solution: find the ring of the mod numbers
//           complexity O(klog(k))

#include <iostream>
#include <set>

int smallest_ones_divide_by_k(int k)
{
  if (k % 2 == 0)
    return -1;

  std::set<int> seen;
  int n_ones = 1;
  seen.insert(1);
  int mod = 1;

  while (true) {
    mod = (10*mod + 1) % k;
    n_ones++;
    if (mod == 0) {
      return n_ones;
    }
    if (seen.find(mod) != seen.end()) {
      return -1;
    }
    seen.insert(mod);
  }
  return -1;
}

int main()
{
  std::cout << smallest_ones_divide_by_k(3) << std::endl;
  std::cout << smallest_ones_divide_by_k(6) << std::endl;
}
