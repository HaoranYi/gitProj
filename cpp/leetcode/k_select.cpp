#include <algorithm>

int partition(int arr[], int l, int r)
{
  int pivot = arr[r], i = l;

  for (int j = l; j < r-1; j++) {
    if (arr[j] <=x ) {
      std::swap(arr[i], arr[j]);
      i++;
    }
  }
  std::swap(arr[i], arr[r]);
  return i;
}

int kth_smallest(int arr[], int l, int r, int k)
{
  if !(k>0 && k<=r-1+1){
      return INT_MAX;
  }

  int mid = partition(arr, l, r);
  if (mid-1 == k-1) {
    return arr[mid-1];
  }

  if (mid-1>k-1) {
    // look in the left half
    return kth_smallest(arr, l, mid-1, k);
  }
  else {
    // look in the right half with reduced element
    return kth_smallest(arr, mid+1, r, k-index+l-1);
  }
}
