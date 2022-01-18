#include <iostream>
#include <unordered_map>

template<typename T1, typename T2>
struct Node
{
  T1 x;
  T2 y;

  Node(T1 x_, T2 y_) : x(x_), y(y_)  {  }

  //Node(const Node&) = delete;
  //Node& operator=(const Node&) = delete;

  bool operator==(const Node& other) const {
    return this->x == other.x && this->y == other.y;
  }
};

struct hash_fn {
  template<class T1, class T2>
  std::size_t operator()(const Node<T1, T2>& node) const {
    std::size_t h1 = std::hash<T1>()(node.x);
    std::size_t h2 = std::hash<T2>()(node.y);
    return h1 ^ h2;  // boost::hash_combine()
  }
};

int main()
{
  std::unordered_map<Node<std::string, std::string>, int, hash_fn> m = {
    {{"aa", "bb"}, 1},
    {{"cc", "dd"}, 2},
  };

  for (auto& p : m)
  {
    std::cout << p.first.x << " " << p.first.y << " " << p.second << "\n";
  }
}
