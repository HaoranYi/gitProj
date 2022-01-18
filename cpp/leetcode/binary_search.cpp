#include <iostream>
#include <array>
#include <numeric>


// we could also use std::array

int binary_search(int* arr, int start, int end, int k)
{
  if (start == (end - 1))
    return arr[start] == k ? start : -1;

  int m = (start + end + 1)/2;
  if (arr[m] == k)
    return m;

  if (arr[m] > k)
    return binary_search(arr, start, m, k);
  else
    return binary_search(arr, m, end, k);
}

int main()
{
  int a[4] = {1, 2, 3, 4};
  int ans = binary_search(a, 0, 4, 5);

  std::cout << ans << "\n";
}
