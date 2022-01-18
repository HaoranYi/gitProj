#include<iostream>
#include<map>

// temlate paramter pack
template<typename... Ts>
struct tuple{};

// function paramter pack
template<typename...Ts>
void f(Ts... args){}


// function parameter pack
template<typename... Ts>
//void foo(Ts&... args) {
void foo(Ts... args) {

  f(args...);  // pattern pack
  f(++args...);
}


int main()
{
  int sell_qty = 8;
  int buy_qty = 2;
  double sell_price = 100;
  double buy_price = 90;

  int avg_qty_in_packet = 9;
  int first_sell_qty = 8;
  double sell_mom = -10*first_sell_qty/avg_qty_in_packet;

  double fair_price = ((sell_price * buy_qty) + (buy_price * sell_qty))/(buy_qty + sell_qty);
  std::cout << fair_price << std::endl;
  std::cout << sell_mom << std::endl;

  foo(1,2,3);

  std::map<int, int> m{{1,2}};
  for (auto x :m)
    std::cout << x.first << " " << x.second << "\n";
}

// emplace(iter, args)
// emplace_back(args)
