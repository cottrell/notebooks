#include <algorithm>
#include <iostream>
#include <string>
using namespace std;

int main()
{
    string str;
    cout << "Please enter a  word: "; //ask for input
    cin >> str;
    sort(str.begin(), str.end());
    do {
        cout << str << '\n';
    } while (next_permutation(str.begin(), str.end()));
}
