// 2022/1/23 google screen question 2

#include <iostream>
#include <iterator>
#include <algorithm>
#include <vector>
#include <exception>

// question 1
bool is_power_of_two(std::uint32_t n)
{
  return 0 == (n & (n-1));
}

// question 2
void print_post_order(std::vector<int>& preorder, std::vector<int>& inorder)
{
  if (preorder.size() != inorder.size()) {
    throw std::runtime_error("invalid tree");
  }

  if (preorder.empty()) {
    return;
  }

  if (preorder.size() == 1) {
    std::cout << preorder[0] << " ";
    return;
  }

  std::vector<int> preorder_left, preorder_right;
  std::vector<int> inorder_left, inorder_right;

  auto curr = preorder[0];
  auto it = std::find(inorder.begin(), inorder.end(), curr);

  std::copy(inorder.begin(), it, std::back_inserter(inorder_left));
  std::copy(it+1, inorder.end(), std::back_inserter(inorder_right));
  int s = inorder_left.size();

  std::copy(preorder.begin() + 1, preorder.begin() + 1 + s, std::back_inserter(preorder_left));
  std::copy(preorder.begin() + 1 + s, preorder.end(), std::back_inserter(preorder_right));
  print_post_order(preorder_left, inorder_left);
  print_post_order(preorder_right, inorder_right);
  std:: cout << curr << " ";
}

int main()
{
  for (int i=0; i < 64; i++) {
    if (is_power_of_two(i)){
      std::cout << i << std::endl;
    }
  }

  std::vector<int> preorder = {1, 2, 3};
  std::vector<int> inorder = {2, 1, 3};

  print_post_order(preorder, inorder);
}
