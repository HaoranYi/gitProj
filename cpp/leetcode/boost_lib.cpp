#include <boost/algorithm/cxx11/one_of.hpp>

using namespace boost::algorithm;

void test()
{
  std::cout << one_of(a.begin(), a.end(); [](int x){ x==4; });
  std::cout << any_of(a.begin(), a.end(); [](int x){ x==4; });
  std::cout << none_of(a.begin(), a.end(); [](int x){ x==4; });
}

/**
 * boost.preprocessor library useful to generate repeated codes
 */
#include <boost/preprocessor/seq/for_each.hpp>
BOOST_PP_SEQ_FOR_EACH(MACRO, _, SEQ)



// reference_wrapper: assignable/copiable, useful to be put in a container
#include <algorithm>
#include <list>
#include <vector>
#include <iostream>
#include <numeric>
#include <random>
#include <functional>

int main()
{
  std::list<int> l(10);
  std::iota(l.begin(), l.end(), -4);

  std::vector<std::reference_wrapper<int>> v(l.begin(), l.end());
  std::shuffle(v.begin(), v.end(), std::mt19937(std::random_device{}()));

  for (auto n : l)
    std::cout << n << ' ';

  for (auto i : v)
    std::cout << i << ' ';

  for (auto& i : l)
    i *= 2;

  for (auto i : v)
    std::cout << i << ' '

}
