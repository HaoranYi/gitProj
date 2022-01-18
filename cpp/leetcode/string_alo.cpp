#include <sstream>

// extracted formated input >>( T& )

void examples()
{
  int n;
  std::cin >> n;

  std::cin >> std::hex >> n;

  char c;
  istream.get(c); // get(char&)

  std::in.getline(title, 256, deli);

  std::getline(istream& is, string& str, char delim);
}

void split()
{
  while (getline(ss, item, delim))
    v.emplace_back(ss);

  p = str.find(del);
  auto token = s.sub(0, p);
}

// strtok pattern: internall remember the last token and modify the orignal string by setting the delimiter to null.
void split2()
{
  p = strtok(str, ',');
  while (p)
  {
    printf("%s ", p);
    p = strtok(nullptr, ',');
  }
}

void split()
{
  boost::tokenizer<boost::char_seperator<char>> tokenizer;
  boost::char_separator<char> sep{" ", "+"};
  tokenizer tok{s, sep};
  for (auto& t : tok)
    std::cout << t << '\n';
}

string join()
{
  std::ostringstream o;
  for (auto x : parts)
    o << x << ",";
  s = o.str();
  s.pop_back();
  return s;
}

#include <boost/algorithm/string/join.hpp>

boolt::algorithm::join(vec, ",")
boolt::algorithm::split(ss, ",")


// c++ algorithm
std::max_element(first, last);
std::min_element(first, last);
std::sort(first, last)
