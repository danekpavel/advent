#include <fstream>
#include <iostream>
#include <vector>
#include <map>
#include <algorithm>

struct PN {
    size_t start;
    size_t end;
    int num;

    PN(size_t start, size_t end, int num) : start(start), end(end), num(num) {}
};

const std::string DIGITS{"0123456789"};
const std::string NONSYMB = "." + DIGITS;

int main() {
    
    std::ifstream ifile{"input.txt"};
    std::vector<std::string> lines;
    std::string line;
    std::multimap<size_t, PN> part_numbers;
    size_t line_i{0};
    size_t tmp;

    // locate all numbers
    while (std::getline(ifile, line)) {
        if (line_i == 0)  // store first line's length
            tmp = line.length();
        lines.push_back(line);

        size_t j{0};
        size_t start;
        while ((start = line.find_first_of(DIGITS, j)) != std::string::npos) {
            size_t end = line.find_first_not_of(DIGITS, start);
            if (end == std::string::npos)
                end = line.length();
            part_numbers.emplace(std::piecewise_construct, 
                std::forward_as_tuple(line_i),
                std::forward_as_tuple(start, end, 
                std::stoi(line.substr(start, end - start))));
            j = end;
        }
        ++line_i;
    }

    const size_t M{line_i};
    const size_t N{tmp};

    // remove non-part numbers
    for (auto it = part_numbers.begin(); it != part_numbers.end(); ) {
        line_i = it->first;
        size_t i_from = line_i == 0 ? 0 : line_i - 1;
        for (size_t i = i_from; i < std::min(M, line_i + 2); ++i) {
            size_t j_from = it->second.start == 0 ? 0 : it->second.start - 1;
            for (size_t j = j_from; j < std::min(N, it->second.end + 1); ++j) {
                // continue with next number when a symbol is found
                if (NONSYMB.find(lines[i][j]) == std::string::npos) {
                    ++it;
                    goto no_erase;
                }
            }
        }
        // only if no symbol was found
        it = part_numbers.erase(it);

        no_erase: ;
    }

    int total{0};
    for (const auto& pn : part_numbers) {
        total += pn.second.num;
    }

    std::cout << "Part 1: " << total << "\n";

    total = 0;
    for (size_t i = 0; i < M; ++i) 
        for (size_t j = 0; j < N; ++j) 
            if (lines[i][j] == '*') {
                std::vector<int> pn_adj;  // adjacent part numbers
                size_t i_from = i==0 ? 0 : i - 1;
                size_t j_from = j==0 ? 0 : j - 1;
                // across adjacent lines (searching for values >= M doesn't matter)
                for (size_t ii = i_from; ii < i + 2; ++ii) {
                    auto range = part_numbers.equal_range(ii);
                    // across all part numbers on the line
                    for (auto it = range.first; it != range.second; ++it) {
                        auto& pn = it->second;
                        if ((pn.start >= j_from && pn.start <= j + 1) ||
                            (pn.end > j_from && pn.end <= j + 2) ||                           
                            (pn.start < j && pn.end > j))
                            pn_adj.push_back(pn.num);
                    }
                }
                if (pn_adj.size() == 2)
                    total += pn_adj[0] * pn_adj[1];
            }

    std::cout << "Part 2: " << total << "\n";
}