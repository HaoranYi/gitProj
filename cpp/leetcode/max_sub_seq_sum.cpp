#include <iostream>
#include <array>
#include <algorithm>

std::array<int, 9> a = {-2, 1, -3, 4, -1, 2, 1, -5, 4};

template<int N>
void max_sub_seq_sum(std::array<int, N>& a)
{
  std::array<int, N> dp;
  std::fill(dp.begin(), dp.end(), 0);

  dp[0] = a[0];
  for (auto i = 1; i < N; i++)
  {
    dp[i] = std::max(dp[i-1] + a[i], a[i]);
  }

  auto p = std::max_element(dp.begin(), dp.end());
  std::cout << *p << std::endl;
}

int main()
{
  max_sub_seq_sum<9>(a);
}
