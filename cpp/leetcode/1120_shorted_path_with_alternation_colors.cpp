#include <vector>
#include <pair>
#include <algorithm>
#include <deque>
#include <unordered_map>

using std::vector<std::pair<int, int>> edges_t;

std::vector<int> get_neighbors_sorted(int n, edge_t& edges)
{
  std::vector<int> ret;

  auto it1 = std::lower_bound(edges.begin(), edges.end(), n, [](auto& x, auto n){ return x.first < n; });
  auto it2 = std::upper_bound(edges.begin(), edges.end(), n, [](auto& x, auto n){ return x.first < n; });

  for (auto it = it1; it != it2; ++it) {
    ret.push_back((*it).second);
  }
  return ret;
}

std::vector<int> get_neighbors(int n, edge_t& edges)
{
  std::vector<int> ret;
  for (auto& e : edges) {
    if (e.first == n) {
      ret.push_back(e.second);
    }
  }
  return ret;
}

std::unordered_map<int, std::vector<int>> build_neighbor_map(edge_t& edges)
{
  std::unordered_map<int, std::vector<int>> m;
  for (auto& e : edges) {
    if (m.find(e.first) == m.end()) {
      //m[e.first] = {e.second};
      m.emplace(e.first, {e.second});
    }
    else {
      m[e.first].push_back(e.second);
    }
  }
  return m;
}

std::vector<int> shortest_alternate_path(edges_t& red, edges_t& blue, int n)
{
  std::vector<int> result(n, -1);
  std::set<std::pair<int, bool>> visisted;  // remember (node, color)

  std::sort(red.begin(), red.end(), [](auto& x, auto& y) { return x.first < y.first; });
  std::sort(blue.begin(), blue.end(), [](auto& x, auto& y) { return x.first < y.first; });

  auto red_neighbor_map = build_neighbor_map(red);
  auto blue_neighbor_map = build_neighbor_map(blue);

  result[0] = 0;
  bool curr_color = false; // false: red; true: blue
  std::deque<int> working;
  working.push_back(0);
  working.push_back(-1); // sentinal
  int len = 0;

  while (working.size() > 1) {
    auto curr = working[0];
    working.pop_front();
    if (curr == -1) {
      len += 1;
      working.push_back(-1);
      curr_color = !curr_color;
      continue;
    }

    result[n] = result[n] == -1 ? len : std::min(result[n], len);
    visited.insert(std::make_pair(curr, curr_color));
    // edges_t& curr_edge = curr_color ? blue : red;
    // auto neighbors = get_neighbors_sorted(curr, curr_edges);

    auto& curr_map = curr_color ? blue_neighbor_map : red_neighbor_map;
    if (curr_map.find(curr) == curr_map.end()) {
      continue;
    }
    auto neighbors = curr_map[curr];

    for (auto n : neighbors) {
      if (visited.find(std::make_pair(n, !curr_color)) != visited.end()) {
	working.push_back(n);
      }
    }
  }
  return result;
}
