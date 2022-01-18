#include <iostream>
#include <vector>
#include <algorithm>

int num_element(vector<int> A)
{
  auto it = std::find(A.begin(), A.end(), (int)('_'));
  return it - A.begin();
}

// inplace merge - start from the end
void merge(vector<int>& A, vector<int>& B)
{
  int i, j, output;

  i = num_element(A)-1;
  j = B.size()-1;
  output = A.size()-1;

  while (i>=0 && j>=0) {
    if (A[i] > B[i]) {
      A[output] = A[i];
      i--;
      output--;
    }
    else {
      A[output] = B[i];
      j--;
      output--;
    }
  }

  while (j >= 0)
    A[output--] = B[j--];
}

// use heap
int find_k_largest(vector<int>& A, int k)
{
  vector<int> heap;
  for (int i = 0; i < k; i++) {
    heap.push_back(A[i]);
  }
  std::make_heap(heap.begin(), heap.end(), std::greater<int>{});  // minheap

  for (int i = k; i < A.size(); i++) {
    if (A[i] > heap[0]) {
      heap.push_back(A[i]);
      std::push_heap(heap.begin(), heap.end(), std::greater<int>());
      std::pop_heap(heap.begin(), heap.end(), std::greater<int>());
      heap.pop_back();
    }
  }

  return heap[0];
}
