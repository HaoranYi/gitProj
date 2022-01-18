#include <iostream>
#include <cmath>

double newton_sqrt(double n)
{
  double x0 = 1;
  double err = 1;
  double x1;

  while (err > 1e-9){
    x1 = 0.5*(n/x0 + x0);
    err = std::abs(x1 - x0);
    x0 = x1;
  }
  return x1;
}

int main()
{
  double n = 42;
  std::cout << std::sqrt(n) << "\n";
  std::cout << newton_sqrt(n) << "\n";
}
