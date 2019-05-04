// variant is a type-safe union.

#include <iostream>
#include <variant>  //C++ 17
#include <string>
#include <cassert>

struct AA
{
    int _x;
    AA(int x) : _x(x) {}
};

int main()
{
    std::variant<int, float, AA> v, w;
    v = 12;                      // v contains int
    int i = std::get<int>(v);
    w = std::get<int>(v);
    w = std::get<0>(v);          // same effect as prev line
    w = v;                       // same effect as prev line

    // user type
    v.emplace<AA>(2);
    w = std::get<2>(v);

    try {
        std::get<float>(w);
    }
    catch (const std::bad_variant_access&) {}

    using namespace std::literals;
    std::variant<std::string> x("abc");  // converting constructors work when unambiguous
    x = "def";   // converting assignment work when unambiguous

    std::variant<std::string, void const*> y("abc");
    // casts to void const* when passed a char const *
    assert(std::holds_alternative<void const*>(y));
    y = "xyz"s;
    assert(std::holds_alternative<std::string>(y));

    // TODO std::visit
    // functor: https://www.bfilipek.com/2018/09/visit-variants.html
    // lambda: https://en.cppreference.com/w/cpp/utility/variant/visit


}
