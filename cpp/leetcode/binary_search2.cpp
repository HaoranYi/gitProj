#include <iostream>

int main()
{
  int a[5] = {1, 2, 3, 4, 5};
  // hi -> point to one pass the last element, when returning hi, it means the element could not be found.
  auto bin_search = [](int* a, int lo, int hi, int v)
		    {
		      while (lo < hi) {
			auto mid = (lo+hi)/2;
			if (a[mid] == v) {
			  return mid;
			}
			else if (a[mid] > v) {
			  hi = mid;
			}
			else {
			  lo = mid + 1;
			}
		      }
		      return lo;
		    };
  std::cout << "bin_search: " << bin_search(a, 0, 5, 5) << "\n";
  std::cout << "bin_search: " << bin_search(a, 0, 5, 6) << "\n";
  std::cout << "bin_search: " << bin_search(a, 0, 5, 2) << "\n";
}
