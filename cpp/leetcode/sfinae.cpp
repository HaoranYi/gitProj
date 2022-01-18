#include <type_traits>
#include <vector>
#include <iostream>

/**
 * there are three ways to use enable_if
 * 1. enable_if for template parameter (reduce one template
 *    parameter, sink-hole with N parameter, 1 default to void,
 *    enable_if specialization with N-1 parameters)
 * 2. enable_if for return type
 * 3. enable_if for function paramter (usually as default value)
 */

template<int n, typename T=std::integral_constant<int, n>>
//template<int n>
struct foo {
  void print()
  {
    std::cout << "foo\n";
  }
};

template<>
struct foo<1> {
  void print()
  {
    std::cout << "foo1\n";
  }
};

template<>
struct foo<2> {
  void print()
  {
    std::cout << "foo2\n";
  }
};

void test_foo()
{
  foo<1> f1;
  foo<2> f2;
  foo<3> f3;

  f1.print();
  f2.print();
  f3.print();
}


///////////////////////////
template<typename T, typename V=void>
struct bar
{
  void print() {
    std::cout << "bar_false\n";
  }
};

template<typename T>
struct bar<T, std::enable_if_t<T::value>>
{
  void print()
  {
    std::cout << "bar_true\n";
  }
};

void test_bar()
{
  bar<std::integral_constant<bool, true>> bar1;
  bar<std::integral_constant<bool, false>> bar2;
  bar1.print();
  bar2.print();
}

////////////////////////////
template<typename T, typename = void>
struct is_container : std::false_type {};

template<typename T>
struct is_container<T, std::void_t<decltype(std::declval<T>().begin()), decltype(std::declval<T>().end())>> : std::true_type {};

void test_is_container()
{
  std::cout << is_container<int>::value << "\n";
  std::cout << is_container<std::vector<int>>::value << "\n";
}

///////////////////////////
template<bool b>
void test_conditional_t()
{
  using T=std::conditional_t<b, char, float>;
  T a;

  std::cout << sizeof(a) << "\n";
}

///////////////////////////
int main()
{
  test_foo();
  test_bar();
  test_is_container();
  test_conditional_t<true>();
  test_conditional_t<false>();
}
