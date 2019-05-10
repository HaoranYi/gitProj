#include <vector>
#include <unordered_map>

using namespace std;

class Solution
{
public:
    vector<int> twoSum(vector<int>& nums, int target)
    {
        // use HashMap for O(1) lookup
        std::unordered_map<int, int> record;
        for (int i = 0; (size_t)i != nums.size(); ++i)
        {
            auto found = record.find(nums[i]);
            if (found != record.end())
            {
                return {found->second, i};
            }
            record.emplace(target - nums[i], i);
        }
        return {-1, -1};
    }
};
