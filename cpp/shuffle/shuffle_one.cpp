#include <algorithm>
#include <iostream>
#include <string>
using namespace std;

int main()
{
    string str;
    cout << "Please enter a  word: "; //ask for input
    cin >> str;
    random_shuffle(str.begin(), str.end());
    cout << str << '\n';
}
