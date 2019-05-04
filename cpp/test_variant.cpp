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

}

// std::visit
// functor: https://www.bfilipek.com/2018/09/visit-variants.html
// lambda: https://en.cppreference.com/w/cpp/utility/variant/visit
//   https://www.bfilipek.com/2018/06/variant.html#overload
//   create an overload struct, that inherits from all lambda operator()
struct Fluid { };
struct LightItem { };
struct HeavyItem { };
struct FragileItem { };

struct VisitPackage
{
    void operator()(Fluid& ) { cout << "fluid\n"; }
    void operator()(LightItem& ) { cout << "light item\n"; }
    void operator()(HeavyItem& ) { cout << "heavy item\n"; }
    void operator()(FragileItem& ) { cout << "fragile\n"; }
};

void test_variant_visit_functor()
{
    std::variant<Fluid, LightItem, HeavyItem, FragileItem> package { 
        FragileItem() };
    std::visit(VisitPackage(), package);
}

// helper struct overload that inherits from all lambda's operator()
template<class... Ts> struct overload : Ts... { using Ts::operator()...; };
template<class... Ts> overload(Ts...) -> overload<Ts...>;

void test_vairant_visit_lambda()
{
    std::variant<Fluid, LightItem, HeavyItem, FragileItem> package;

    std::visit(overload{
        [](Fluid& ) { cout << "fluid\n"; },
        [](LightItem& ) { cout << "light item\n"; },
        [](HeavyItem& ) { cout << "heavy item\n"; },
        [](FragileItem& ) { cout << "fragile\n"; }
    }, package);
}

// visit mutliple variant. must provide implementation for all type
// combinations.
void test_variant_visit_many()
{

    std::variant<LightItem, HeavyItem> basicPackA;
    std::variant<LightItem, HeavyItem> basicPackB;

    std::visit(overload{
            [](LightItem&, LightItem& ) { cout << "2 light items\n"; },
            [](LightItem&, HeavyItem& ) { cout << "light & heavy items\n"; },
            [](HeavyItem&, LightItem& ) { cout << "heavy & light items\n"; },
            [](HeavyItem&, HeavyItem& ) { cout << "2 heavy items\n"; },
            }, basicPackA, basicPackB);
}
