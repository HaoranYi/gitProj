/**
 * Find the intersection between two lists.
 * Traverse the list and store the pointers in a set or hash_table.
 * Traverse the other list and find the first element that in the hash_table.
 * Complexity O(M+N).
 * Easy question.
 * $> g++ find_list_intersect.cpp  // to compile
 * $> a.exe                        // to run
 */
#include <iostream>
#include <set>
#include <vector>

int main()
{
    int a, b, c, d;

    std::set<int*> s;
    s.insert(&a);
    s.insert(&b);
    s.insert(&c);
    s.insert(&d);

    std::vector<int*> v {&a, &b, &c, &d};

    for (auto x: v) {
        if (s.find(x) != s.end())
        {
            std::cout << x << " Found." << '\n';
        }
        else
        {
            std::cout << x << " Not found." << '\n';
        }
    }
}
