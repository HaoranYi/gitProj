class Solution {
public:
    int numBusesToDestination(vector<vector<int>>& routes, int source, int target) {

	// stop-> bus_routes_index!!! one level of indirection
	std::map<int, std::vector<int>> stop_route_map;

	std::set<int> stops;

	auto build_routes = [&]() {
	    int index = 0;
	    for (auto& r : routes) {
		for (auto s : r) {
		    if (stop_route_map.find(s) == stop_route_map.end()) {
			stop_route_map[s] = {index};
		    }
		    else {
			stop_route_map[s].push_back(index);
		    }
		}

		for (auto s : r) {
		    stops.insert(s);
		}
		index++;
	    }
	};
	build_routes();

	auto bfs = [&](int start, int target) {
	    if (start == target)
		return 0;

	    if (stops.find(start) == stops.end() || stops.find(target) == stops.end()) {
		return -1;
	    }

	    std::set<int> curr;
	    std::set<int> next;
	    std::set<int> visited; // bus index!!! this increase the pruning

	    curr.insert(start);
	    int step = 1;
	    while (!curr.empty()) {
		for (auto& s : curr) {
		    //if (visited.find(s) != visited.end())
		    //    continue;

		    if (stop_route_map.find(s) == stop_route_map.end()) {
			continue;
		    }

		    auto& r = stop_route_map[s];
		    for (auto& i : r) {
			auto bus = routes[i];
			if (visited.find(i) == visited.end()) {
			    for (auto& x : bus) {
				next.insert(x);
			    }
			}
			visited.insert(i);
		    }
		    stop_route_map.erase(s); // prune the tree
		}
		if (next.find(target) != next.end()) {
		    return step;
		}
		curr.swap(next);
		next.clear();
		step++;
	    }
	    return -1;
	};

	return bfs(source, target);
    }
};
