#include <stdio.h>

#define SIZE 3

void splashScreen() {
    printf("\n");
    printf("  ____  _           _    _                _                                               \n");
    printf(" |  _ \\(_) ___     / \\  | |__   ___ _ __ | |_ ___ _   _  ___ _ __                         \n");
    printf(" | | | | |/ _ \\   / _ \\ | '_ \\ / _ \\ '_ \\| __/ _ \\ | | |/ _ \\ '__|                        \n");
    printf(" | |_| | |  __/  / ___ \\| |_) |  __/ | | | ||  __/ |_| |  __/ |                           \n");
    printf(" |____/|_|\\___|_/_/   \\_\\_.__/ \\___|_| |_|\\__\\___|\\__,_|\\___|_|                           \n");
    printf(" \\ \\ / / _ \\| '_ \\                                                                        \n");
    printf("  \\ V / (_) | | | |                                                                       \n");
    printf("  _\\_/_\\___/|_| |_|    _         ___     __  __            _           _ _ _              \n");
    printf(" |  \\/  (_)_ __  _ __ (_) ___   ( _ )   |  \\/  | __ ___  _(_)_ __ ___ (_) (_) __ _ _ __   \n");
    printf(" | |\\/| | | '_ \\| '_ \\| |/ _ \\  / _ \\/\\ | |\\/| |/ _` \\ \\/ / | '_ ` _ \\| | | |/ _` | '_ \\  \n");
    printf(" | |  | | | | | | | | | |  __/ | (_>  < | |  | | (_| |>  <| | | | | | | | | | (_| | | | | \n");
    printf(" |_|  |_|_|_| |_|_| |_|_|\\___|  \\___/\\/ |_|  |_|\\__,_/_/\\_\\_|_| |_| |_|_|_|_|\\__,_|_| |_| \n");
    printf("\n");
}

int max(const int arr[], int size) {
    if (size <= 0) {
        return 0;
    }

    int maximum = arr[0];
    for (int i = 1; i < size; i++) {
        if (arr[i] > maximum) {
            maximum = arr[i];
        }
    }
    return maximum;
}

int min(const int arr[], int size) {
    if (size <= 0) {
        return 0;
    }
    
    int minimum = arr[0];
    for (int i = 1; i < size; i++) {
        if (arr[i] < minimum) {
            minimum = arr[i];
        }
    }
    return minimum;
}

int square(int number) {
    return number * number;
}

int main() {

    splashScreen();

    int numbers[SIZE];

    printf("Drei heilige Runen....bitte....danke:\n");
    for (int i = 0; i < SIZE; i++) {
        printf("Rune %d: ", i + 1);
        if (scanf("%d", &numbers[i]) != 1) {
            printf("Macht keinen Sinn. Ciao.\n");
            return 1;
        }
    }

    int minimum = min(numbers, SIZE);
    int maximum = max(numbers, SIZE);

    printf("\n--- So hier deine Resultate ---\n");
    printf("Minnie ist: %d\n", minimum);
    printf("Maximillian ist: %d\n", maximum);

    long long sum = 0;
    long long product = 1;

    printf("\n--- Die dumme Summe und (mir fällt kein reimendes Adjektive für Produkt ein) Produkt zwischen [%d, %d] ---\n", minimum, maximum);

    printf("Die Summe und Produkt der Runen von %d bis %d...\n", minimum, maximum);
    for (int i = minimum; i <= maximum; i++) {
        sum += i;
        product *= i;
    }
    
    printf("Die dumme Summe aller Runen zwischen %d und %d ist: %lld\n", minimum, maximum, sum);
    printf("Das Produkt aller Runen zwischen %d und %d ist: %lld\n", minimum, maximum, product);

    printf("\n--- Die quadratisch, praktisch, guten Quadrate der eingegebenen Runen ---\n");
    for (int i = 0; i < SIZE; i++) {
        int sq = square(numbers[i]);
        printf("Das quadratische Quadrat von %d ist: %d\n", numbers[i], sq);
    }

    return 0;
}