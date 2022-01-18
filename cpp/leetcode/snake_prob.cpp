#include <bits/stdc++.h>

using namespace std;

string ltrim(const string &);
string rtrim(const string &);
vector<string> split(const string &);

/*
 * Complete the 'quickestWayUp' function below.
 *
 * The function is expected to return an INTEGER.
 * The function accepts following parameters:
 *  1. 2D_INTEGER_ARRAY ladders
 *  2. 2D_INTEGER_ARRAY snakes
 */

int quickestWayUp_dp_bad(vector<vector<int>> ladders, vector<vector<int>> snakes) {
    int dp[101] = {0};
    dp[1] = 0;
    int MAX= 2147483647;

    auto is_snake = [&snakes](int i) {
	for (auto& p : snakes) {
	    if (p[1] == i) {
		return true;
	    }
	}
	return false;
    };

    auto is_ladder_end = [&ladders](int i) {
	for (auto& p : ladders) {
	    if (p[1] == i) {
		return p[0];
	    }
	}
	return -1;
    };

    auto is_ladder_start = [&ladders](int i) {
	for (auto& p : ladders) {
	    if (p[0] == i) {
		return true;
	    }
	}
	return false;
    };

    for (int i = 2; i < 101; i++)
    {
	if (is_snake(i)) {
	    dp[i] = MAX;
	    continue;
	}

	int ladder_start = is_ladder_end(i);
	if (ladder_start > 0) {
	    dp[i] = dp[ladder_start];
	    continue;
	}

	std::vector<int> vv;
	for (int j = 1; j < 7; j++)
	{
	    if (i - j >= 1) {
		vv.push_back(dp[i-j]);
	    }
	}
	auto mm = *std::min_element(vv.begin(), vv.end());
	dp[i] = (mm == MAX) ? MAX : mm + 1;
    }
    return dp[100] == MAX ? -1 : dp[100];
}

// BFS
int quickestWayUp(vector<vector<int>> ladders, vector<vector<int>> snakes) {
    std::set<int> visited;
    std::vector<int> curr_bag, next_bag;

    auto get_snake = [&snakes](int i) {
	for (auto& p : snakes) {
	    if (p[0] == i) {
		return p[1];
	    }
	}
	return -1;
    };

    auto get_ladder = [&ladders](int i) {
	for (auto& p : ladders) {
	    if (p[0] == i) {
		return p[1];
	    }
	}
	return -1;
    };

    auto add = [&visited, &next_bag](int i)
    {
	if (visited.find(i) == visited.end())
	{
	    visited.insert(i);
	    next_bag.push_back(i);
	}
    };

    int target = 100;
    int dist = 0;
    visited.insert(1);
    curr_bag.push_back(1);

    while (true)
    {
	dist++;
	next_bag.clear();
	for (auto x : curr_bag) {
	    for (int j = 1; j < 7; j++)
	    {
		if (x+j > 100) {
		    continue;
		}

	       auto snake = get_snake(x + j);
	       auto ladder = get_ladder(x + j);

	       if (snake > 0) {
		   add(snake);
	       }
	       else if (ladder > 0) {
		   add(ladder);
	       }
	       else {
		   add(x+j);
	       }
	    }
	}
	if (std::find(next_bag.begin(), next_bag.end(), target) != next_bag.end()) {
	    break;
	}

	if (dist > 100) {
	    break;
	}
	curr_bag.swap(next_bag);
    }
    return (dist > 100) ? -1 : dist;
}

int main()
{
    ofstream fout(getenv("OUTPUT_PATH"));

    string t_temp;
    getline(cin, t_temp);

    int t = stoi(ltrim(rtrim(t_temp)));

    for (int t_itr = 0; t_itr < t; t_itr++) {
	string n_temp;
	getline(cin, n_temp);

	int n = stoi(ltrim(rtrim(n_temp)));

	vector<vector<int>> ladders(n);

	for (int i = 0; i < n; i++) {
	    ladders[i].resize(2);

	    string ladders_row_temp_temp;
	    getline(cin, ladders_row_temp_temp);

	    vector<string> ladders_row_temp = split(rtrim(ladders_row_temp_temp));

	    for (int j = 0; j < 2; j++) {
		int ladders_row_item = stoi(ladders_row_temp[j]);

		ladders[i][j] = ladders_row_item;
	    }
	}

	string m_temp;
	getline(cin, m_temp);

	int m = stoi(ltrim(rtrim(m_temp)));

	vector<vector<int>> snakes(m);

	for (int i = 0; i < m; i++) {
	    snakes[i].resize(2);

	    string snakes_row_temp_temp;
	    getline(cin, snakes_row_temp_temp);

	    vector<string> snakes_row_temp = split(rtrim(snakes_row_temp_temp));

	    for (int j = 0; j < 2; j++) {
		int snakes_row_item = stoi(snakes_row_temp[j]);

		snakes[i][j] = snakes_row_item;
	    }
	}

	int result = quickestWayUp(ladders, snakes);

	fout << result << "\n";
    }

    fout.close();

    return 0;
}

string ltrim(const string &str) {
    string s(str);

    s.erase(
	s.begin(),
	find_if(s.begin(), s.end(), not1(ptr_fun<int, int>(isspace)))
    );

    return s;
}

string rtrim(const string &str) {
    string s(str);

    s.erase(
	find_if(s.rbegin(), s.rend(), not1(ptr_fun<int, int>(isspace))).base(),
	s.end()
    );

    return s;
}

vector<string> split(const string &str) {
    vector<string> tokens;

    string::size_type start = 0;
    string::size_type end = 0;

    while ((end = str.find(" ", start)) != string::npos) {
	tokens.push_back(str.substr(start, end - start));

	start = end + 1;
    }

    tokens.push_back(str.substr(start));

    return tokens;
}
