class Solution {
public:
    int romanToInt(string s) {

	std::map<std::string, int> M = {
	    {"I", 1},
	    {"V", 5},
	    {"X", 10},
	    {"L", 50},
	    {"C", 100},
	    {"D", 500},
	    {"M", 1000},
	    {"IV", 4},
	    {"IX", 9},
	    {"XL", 40},
	    {"XC", 90},
	    {"CD", 400},
	    {"CM", 900}
	};

	int ret = 0;
	int index = 0;
	while (index < s.size()) {
	    auto s2 = s.substr(index, 2);
	    if (M.find(s2) != M.end()) {
		ret += M[s2];
		index += 2;
	    }
	    else {
		auto s1 = s.substr(index, 1);
		if (M.find(s1) != M.end()) {
		    ret += M[s1];
		    index++;
		}
		else {
		    throw std::runtime_error("invalid rome number" + s1);
		}
	    }
	}
	return ret;
    }
};
