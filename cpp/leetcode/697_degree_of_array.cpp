struct count_t {
    int n;
    int first;
    int last;

    int len() {
	return last - first + 1;
    }
};


class Solution {
public:
    int findShortestSubArray(vector<int>& nums) {
	std::map<int, count_t> m;
	int index = 0;
	for (auto i : nums) {
	    if (m.find(i) == m.end()) {
		m.insert(std::make_pair(i, count_t{1, index, index}));
	    }
	    else {
		auto& c= m[i];
		c.n += 1;
		c.last = index;
	    }
	    index++;
	}

	int max_num = 0;
	for (auto& p : m) {
	    auto& c = p.second;
	    if (c.n >= max_num) {
		max_num = c.n;
	    }
	}

	int min_len = nums.size();
	for (auto& p : m) {
	    auto& c = p.second;
	    if (c.n == max_num) {
		if (c.len() <= min_len) {
		    min_len = c.len();
		}
	    }
	}
	return min_len;
    }
};
