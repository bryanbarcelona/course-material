#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <numeric>
#include <map>
#include <stdexcept>
#include <iomanip>
#include <string>
#include <windows.h>

// Spash Screen mit Farben etc mit Hilfe von KI gemacht, also aufgepasst
// Hätte hier auch using namespace std; benutzen können, war aber schon fast am Ende...in tiere.cpp hab ichs benutzt

// Windows color codes
#define COLOR_RESET  7   // Default
#define COLOR_RED    12  // Bright Red
#define COLOR_GREEN  10  // Bright Green
#define COLOR_BLUE   9   // Bright Blue
#define COLOR_CYAN   11  // Bright Cyan
#define COLOR_YELLOW 14  // Bright Yellow

void setColor(int color) {
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), color);
}

void printSplashScreen() {
    // Clear screen
    system("cls");
    
    // Print colored ASCII art
    setColor(COLOR_GREEN);
       
    std::cout << 
            "     _______.___________.    ___   .___________. __       _______.___________. __   __  ___                   \n"
        "    /       |           |   /   \\  |           ||  |     /       |           ||  | |  |/  /                   \n"
        "   |   (----`---|  |----`  /  ^  \\ `---|  |----`|  |    |   (----`---|  |----`|  | |  '  /                    \n";
    setColor(COLOR_CYAN);
    std::cout <<
        "    \\   \\       |  |      /  /_\\  \\    |  |     |  |     \\   \\       |  |     |  | |    <                     \n"
        ".----)   |      |  |     /  _____  \\   |  |     |  | .----)   |      |  |     |  | |  .  \\                    \n"
        "|_______/       |__|    /__/     \\__\\  |__|     |__| |_______/       |__|     |__| |__|\\__\\                   \n";
    setColor(COLOR_YELLOW);
    std::cout <<
        "                                                                                                              \n"
        " __  ___ .______       __  .___  ___.      _______. __  ___ .______          ___      .___  ___.      _______.\n"
        "|  |/  / |   _  \\     |  | |   \\/   |     /       ||  |/  / |   _  \\        /   \\     |   \\/   |     /       |\n"
        "|  '  /  |  |_)  |    |  | |  \\  /  |    |   (----`|  '  /  |  |_)  |      /  ^  \\    |  \\  /  |    |   (----`\n";
    setColor(COLOR_BLUE);
    std::cout <<
        "|    <   |      /     |  | |  |\\/|  |     \\   \\    |    <   |      /      /  /_\\  \\   |  |\\/|  |     \\   \\    \n"
        "|  .  \\  |  |\\  \\----.|  | |  |  |  | .----)   |   |  .  \\  |  |\\  \\----./  _____  \\  |  |  |  | .----)   |   \n"
        "|__|\\__\\ | _| `._____||__| |__|  |__| |_______/    |__|\\__\\ | _| `._____/__/     \\__\\ |__|  |__| |_______/    \n\n\n";
    // Reset to default color
    setColor(COLOR_RESET);
}

double findMedian(std::vector<int> numbers) {
    if (numbers.empty()) {
        throw std::invalid_argument("Auf leeren Magen lässt sich schlecht ein Median berechnen, wa?");
    }

    std::sort(numbers.begin(), numbers.end());

    size_t n = numbers.size();
    size_t middle = n / 2;

    if (n % 2 != 0) {
        return static_cast<double>(numbers[middle]);
    } else {
        return (static_cast<double>(numbers[middle - 1]) + numbers[middle]) / 2.0;
    }
}

double calculateMean(const std::vector<int> &numbers) {
    if (numbers.empty()) {
        throw std::invalid_argument("Auf leeren Magen lässt sich schlecht ein Durchschnitt berechnen, wa?");
    }

    long long sum = std::accumulate(numbers.begin(), numbers.end(), 0LL); // Quelle https://codeforces.com/blog/entry/91004

    return static_cast<double>(sum) / numbers.size();
}

int findMode(const std::vector<int> &numbers) {
    if (numbers.empty()) {
        throw std::invalid_argument("Auf leeren Magen lässt sich schlecht ein Modus berechnen, wa?");
    }

    std::map<int, int> counts;
    for (int num : numbers) {
        counts[num]++;
    }

    int mode = numbers[0];
    int maxCount = 0;

    for (const auto& pair : counts) {
        if (pair.second > maxCount) {
            maxCount = pair.second;
            mode = pair.first;
        }
    }

    return mode;
}

double calculateStandardDeviation(const std::vector<int> &numbers) {
    if (numbers.size() < 1) {
        throw std::invalid_argument("Freundchen, Standardabweichung braucht mindestens eine Zahl.");
    }

    double mean = calculateMean(numbers);

    double squaredDifferencesSum = 0.0;
    for (int num : numbers) {
        double difference = static_cast<double>(num) - mean;
        squaredDifferencesSum += difference * difference;
    }

    double variance = squaredDifferencesSum / numbers.size();

    return std::sqrt(variance);
}

int main() {

    printSplashScreen();

    std::vector<int> numbers;
    int input;
    
    std::cout << "--- Statistik Rumgespiele mit Zahlen ---" << std::endl;
    std::cout << "Eine Zahlen pro Zeile please. Zum stoppen was anderes als ne Zahl eingeben:" << std::endl;

    while (std::cin >> input) {
        numbers.push_back(input);
    }
    
    std::cin.clear();
    
    if (numbers.empty()) {
        std::cout << "Ja mindestens eine Zahl brauchen wir Freundchen." << std::endl;
        return 0;
    }

    std::cout << "\n--- Ok, hier die schnieke Analyse ---" << std::endl;
    std::cout << "Dit warn' deine Ziffern, wa?: ";
    for (size_t i = 0; i < numbers.size(); ++i) {
        std::cout << numbers[i] << (i < numbers.size() - 1 ? ", " : "");
    }
    std::cout << std::endl;

    std::cout << std::fixed << std::setprecision(2);

    try {
        double median = findMedian(numbers);
        std::cout << "Median: " << median << std::endl;

        double mean = calculateMean(numbers);
        std::cout << "Durchschnitt: " << mean << std::endl;

        int mode = findMode(numbers);
        std::cout << "Modus: " << mode << std::endl;

        double stdDev = calculateStandardDeviation(numbers);
        std::cout << "Standardabweichung (Grundgesamtheit): " << stdDev << std::endl;
        
    } catch (const std::invalid_argument& e) {
        std::cerr << "Fehler (macht jeder): " << e.what() << std::endl;
        return 1;
    }

    return 0;
}