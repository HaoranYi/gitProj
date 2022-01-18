// reverse the list
// an optimization will be reverse the original list

std::vector<int> next_greater_node(Node * head)
{
  std::vector<int> a;
  auto curr = head;
  while (curr) {
    a.push_back(curr->val);
    curr = curr->next;
  }

  int n = a.size();
  std::vector<int> ret(n);
  ret[n-1] = 0;
  curr_max = a[n-1];
  for (int i = n-2; i >=0; i--)
  {
    if (a[i] > curr_max) {
      ret[i] = 0;
      curr_max = a[i];
    }
    else {
      ret[i] = curr_max;
    }
  }
  return ret;
}
