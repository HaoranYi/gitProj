// Given a list of class schedule (start, end), compute the mininum number of
// rooms needed for those classes.

#include <iostream>
#include <vector>

struct Schedule
{
    int start;
    int end;
};

bool is_overlap(Schedule& x, Schedule& y)
{
    if (x.start <= y.start && y.start <= x.end)
    {
        return true;
    }
    if (y.start <= x.start && x.start <= y.end)
    {
        return true;
    }
    return false;
}

int main()
{
    std::vector<Schedule> v { {30, 75}, {0, 50}, {60, 150} };

    std::vector<std::vector<int>> dp;
    for (int i = 0; i < v.size(); ++i) 
    {
        std::vector<int> r(v.size());
        dp.push_back(r);
    }

    for (int i = 0; i < v.size(); ++i)
        dp[i][i] = 1;

    for (int i = 0; i < v.size(); ++i)
    {
        for (int j = i+1; j < v.size(); ++j)
        {
            if (is_overlap(v[i], v[j]))
            {
                dp[i][j] =1;
                dp[j][i] =1;
            }
        }
    }

    int max = 0;
    for (int i = 0; i < v.size(); ++i)
    {
        int count = 0;
        for (int j = 0; j < v.size(); ++j)
        {
            count += dp[i][j];
        }

        if (count > max)
        {
            max = count;
        }
    }
    std::cout << max << '\n';
}
