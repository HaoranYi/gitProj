#include <iostream>
#include <array>
#include <vector>
#include <map>
#include <set>
#include <unordered_set>
#include <deque>
#include <algorithm>


template<int N>
int jump_game(std::array<int, N>& a)
{
  std::map<int, std::vector<int>> val_index_map;
  for (int i = 0; i < N; i++) {
    auto v = a[i];
    val_index_map.insert(std::make_pair(v, std::vector<int>{}));
    val_index_map[v].push_back(i);
  }

  std::map<int, std::vector<int>> neighbors;
  auto build_neighbors = [&]() {
			   for (int i = 0; i < N; i++)
			   {
			     neighbors[i] = {};
			     if (i-1 > 0) {
			       neighbors[i].push_back(i-1);
			     }
			     if (i+1 < N) {
			       neighbors[i].push_back(i+1);
			     }
			     for (auto indx : val_index_map[a[i]]) {
			       if (indx != i && indx != i-1 && indx != i+1) {
				 neighbors[i].push_back(indx);
			       }
			     }
			   }
			 };
  build_neighbors();

  auto bfs = [&](int start, int target) {
	       std::unordered_set<int> visited;
	       std::vector<int> bag;
	       std::vector<int> next_bag;
	       int step = 0;
	       bag.push_back(start);

	       while (true) {
		 if (std::find(bag.begin(), bag.end(), target) != bag.end()) {
		   return step;
		 }

		 for (auto curr : bag) {
		   visited.insert(curr);
		   if (neighbors.find(curr) == neighbors.end()) {
		     continue;
		   }
		   for (auto n : neighbors[curr]) {
		     if (visited.find(n) == visited.end()) {
		       next_bag.push_back(n);
		     }
		   }
		   neighbors.erase(curr); // cut away the neighbors, to save time for the fully connected graph
		 }
		 bag.swap(next_bag);
		 next_bag.clear();
		 step++;
	       }
	       return step;
	     };

  return bfs(0, N-1);
}

int main()
{
  std::array<int, 8> a{7,6,9,6,9,6,9,7};
  std::cout << jump_game<8>(a) << "\n";

  std::array<int, 8> b{7,7,7,7,7,7,7,7};
  std::cout << jump_game<8>(b) << "\n";

  std::array<int, 3> c{6,1, 9};
  std::cout << jump_game<3>(c) << "\n";

}
