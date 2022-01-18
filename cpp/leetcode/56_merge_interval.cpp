#include <iostream>
#include <algorithm>
#include <vector>
#include <utility>

using interval_vec = std::vector<std::pair<int, int>>;

interval_vec merge(interval_vec& vec)
{
  interval_vec ret;
  if (vec.size() == 0) {
    reurn ret;
  }

  // sort
  std::sort(vec.begin(), vec.end(), [](std::pair<int, int> a, std::pair<int, int>b) { return a < b; });

  auto intersec = [](std::pair<int, int> a, std::pair<int, int> b) {
		    return !(a.first > b.second || a.secnod < b.first);
		  };
  auto merge = [](std::pair<int, int> a, std::pair<int, int>b)
	       {
		 return std::make_pair(std::min(a.first, b.first), std::max(a.second, b.secnod));
	       };

  auto it = vec.begin();
  auto curr = *it;

  while ( ++it!= vec.end()) {
    if (intersec(*it, curr)) {
      curr = merge(curr, *it);
    }
    else {
      ret.push_back(curr);
      curr = *it;
    }
  }
  ret.push_back(curr);

  return ret
}
