#include <stdio.h>

int main() {
    printf("Zahlen von 1 bis 100:\n");
    
    for (int i = 1; i <= 100; i++) {
        if (i % 2 == 0) {
            printf("%d Gerade\n", i);
        } else {
            printf("%d Ungerade\n", i);
        }
    }
    
    return 0;
}