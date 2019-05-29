// Given a sorted sequence, binary search to find the element
// std::lower_bound return the first element that is no less than search element
// std::upper_bound return the first element that is greater than search element
// std::equal_range equivalent to [lower_bound, uppper_bound]
// std::partition return the first element of the second group (a step in quick sort)
#include <algorithm>
#include <iostream>
#include <vector>
#include <iterator>
#include <string>
#include <stdio.h>

int main()
{
    std::vector<int> data = {1, 1, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 6};
    auto ll = std::lower_bound(data.begin(), data.end(), 4);
    auto uu = std::upper_bound(data.begin(), data.end(), 4);
    std::copy(ll, uu, std::ostream_iterator<int>(std::cout, " "));
    std::cout << '\n';

    auto pp = std::equal_range(data.begin(), data.end(), 4);
    std::copy(ll, uu, std::ostream_iterator<int>(std::cout, " "));
    std::cout << '\n';

    auto mm = std::partition(data.begin(), data.end(), [](int x) { return x < 4; });
    std::copy(data.begin(), mm, std::ostream_iterator<int>(std::cout, " "));
    std::cout << '\n';
    std::copy(mm, data.end(), std::ostream_iterator<int>(std::cout, " "));
    std::cout << '\n';


    std::cin.ignore();
    /** getchar() don't skip white space. cin skip white space.
     * when using getchar(), you need extra getchar() to eat '\n'.
     */
    //char ch;
    //ch = getchar();
    //ch = getchar();
    //ch = getchar();
}
