#include <fstream>
#include <iostream>
#include <sstream>
#include <map>
#include <numeric>

int main() {

    class RGB {
        std::map<std::string, int> colors;

        public:
        RGB() {
            colors["red"] = 0;
            colors["green"] = 0;
            colors["blue"] = 0;
        }

        int operator [](const std::string& color) {
            return colors[color];
        }
        
        void update_color(const std::string& color, int n) {
            if (colors[color] < n)
                colors[color] = n;
        }

        int power() const {
            return std::accumulate(colors.cbegin(), colors.cend(), 1,
                [](int prod, auto a) { return prod * a.second; });
        }
    };

    std::ifstream ifile("input.txt");
    std::string line;
    int sum_id{0};
    int sum_power{0};
    while (std::getline(ifile, line)) {
        std::istringstream iss{line};
        std::string word;
        int game;
        iss >> word >> game >> word;   // "Game" >> number >> ":"
        RGB rgb;
        
        int n;
        while (iss >> n >> word) {
            // remove ,; after color name when present
            auto pos = word.find_first_of(",;");
            if (pos != std::string::npos) 
                word.erase(pos);
            rgb.update_color(word, n);
        }

        if (rgb["red"] <= 12 && rgb["green"] <= 13 && rgb["blue"] <= 14)
            sum_id += game;

        sum_power += rgb.power();
    }

    std::cout << "Part 1: " << sum_id << "\nPart 2: " << sum_power;
}