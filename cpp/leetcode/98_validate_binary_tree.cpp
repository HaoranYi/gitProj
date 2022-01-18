#include <iostream>
#include <vector>


// inorder traversal shuld result in sorted order
// cur_val should be greater than prev.
bool validate_binary_tree(Node* node, int& prev)
{
  if (!node)
    return true;

  bool left = validate_binary_tree(node->left, prev);
  if (!left)
    return false;

  if (node->val < prev)
    return false;

  prev = node->val;
  return validate_binary_tree(node->right, prev);
}

bool validate(Node* root)
{
  // assume node->val > 0
  return validate(root, 0);
}
