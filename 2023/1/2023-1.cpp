#include <iostream>
#include <fstream>
#include <vector>
// #include <algorithm>

const std::string NUMBERS{"0123456789"};
const std::vector<std::string> NUMBERS_CHAR{"one", "two", "three", "four",
    "five", "six", "seven", "eight", "nine"};

// Sums the first and last digits found in a string
int sum_outer(const std::string& line) {

    auto first = line.find_first_of(NUMBERS);
    if (first == std::string::npos) 
        return 0;

    std::string both(1, line[first]); 
    auto last = line.find_last_of(NUMBERS);
    both += line[last];
    return std::stoi(both);
}

int main() {

    std::ifstream ifile("input.txt"); 
    std::string line;
    long total1{0};
    long total2{0};

    while (ifile >> line) {
        total1 += sum_outer(line);

        // find first/last spelled digit
        size_t first_i, last_i;
        size_t first_pos{0}, last_pos{0};
        bool found{false};
        for (size_t i = 0; i < NUMBERS_CHAR.size(); ++i) {
            // first digit word
            auto pos = line.find(NUMBERS_CHAR[i]);
            if (pos != std::string::npos && (!found || pos < first_pos)) {
                found = true;
                first_i = i;
                first_pos = pos;
            }
            // last digit word
            pos = line.rfind(NUMBERS_CHAR[i]);
            if (pos != std::string::npos && pos > last_pos) {
                last_i = i;
                last_pos = pos;
            }
        }
        // insert digits
        if (found) {
            line.insert(first_pos, std::to_string(first_i + 1));
            //  + 1 because of the insertion at first_pos
            line.insert(last_pos + NUMBERS_CHAR[last_i].size() + 1, 
                std::to_string(last_i + 1));
        }

        total2 += sum_outer(line);
    }

    std::cout << "Part 1: " << total1 << "\n" <<
        "Part 2: " << total2 << "\n";
}