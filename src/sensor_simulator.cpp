#include <iostream>
#include <cstdlib>
#include <ctime>

int main() {
    std::srand(std::time(nullptr));

    double wind_speed = 10 + (std::rand() % 10);     // 10–20
    double temperature = 30 + (std::rand() % 10);    // 30–40
    double vibration = (std::rand() % 100) / 100.0;  // 0.0–1.0

    std::cout << "{"
              << "\"wind_speed\": " << wind_speed << ", "
              << "\"temperature\": " << temperature << ", "
              << "\"vibration\": " << vibration
              << "}" << std::endl;

    return 0;
}