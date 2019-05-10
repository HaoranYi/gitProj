#include "solution.h"
#include <vector>
#include <iostream>

using namespace std;

int main()
{
    Solution s;
    vector<int> v1{2, 7, 11, 15};

    vector<int> result = s.twoSum(v1, 9);
    for (auto& x : result) 
    {
        std::cout << x << ' ';
    }

    return 0;
}
