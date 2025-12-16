#include <stdio.h>
#include <ctype.h> // Grande Importante: für toupper() – nicht vergessen, sonst klappt A/a nicht case-insensitve und so!


void printSplashScreen() {
    printf("\n");
    printf("                                                                                                   \n");
    printf(" @@@@@@@   @@@@@@   @@@        @@@@@@@  @@@  @@@  @@@        @@@@@@   @@@@@@@   @@@@@@   @@@@@@@   \n");
    printf("@@@@@@@@  @@@@@@@@  @@@       @@@@@@@@  @@@  @@@  @@@       @@@@@@@@  @@@@@@@  @@@@@@@@  @@@@@@@@  \n");
    printf("!@@       @@!  @@@  @@!       !@@       @@!  @@@  @@!       @@!  @@@    @@!    @@!  @@@  @@!  @@@  \n");
    printf("!@!       !@!  @!@  !@!       !@!       !@!  @!@  !@!       !@!  @!@    !@!    !@!  @!@  !@!  @!@  \n");
    printf("!@!       @!@!@!@!  @!!       !@!       @!@  !@!  @!!       @!@!@!@!    @!!    @!@  !@!  @!@!!@!   \n");
    printf("!!!       !!!@!!!!  !!!       !!!       !@!  !!!  !!!       !!!@!!!!    !!!    !@!  !!!  !!@!@!    \n");
    printf(":!!       !!:  !!!  !!:       :!!       !!:  !!!  !!:       !!:  !!!    !!:    !!:  !!!  !!: :!!   \n");
    printf(":!:       :!:  !:!   :!:      :!:       :!:  !:!   :!:      :!:  !:!    :!:    :!:  !:!  :!:  !:!  \n");
    printf(" ::: :::  ::   :::   :: ::::   ::: :::  ::::: ::   :: ::::  ::   :::     ::    ::::: ::  ::   :::  \n");
    printf(" :: :: :   :   : :  : :: : :   :: :: :   : :  :   : :: : :   :   : :     :      : :  :    :   : :  \n");
    printf("\n");
    printf("                      The ancient abacus of forbidden arithmetic stirs...                          \n");
    printf("\n");
    printf("\n");
}

// Puffer leeren, sonst spuckt scanf Reste aus. Quelle: https://stackoverflow.com/questions/7898215/how-can-i-clear-an-input-buffer-in-c
void clear_input_buffer() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

int main() {
    // kp ob float auch gereicht hätte, aber desto mehr desto besser? Bei so nem Mini Taschenrechner?
    double zahl1, zahl2, ergebnis;
    char operation;
    
    printSplashScreen();
    printf("Welcome, mortal, to the Calculator of the Abyss!\n");
    // Schleife Bis der Nutzer was sinvolles eingibt.
    do {
        printf("Feed the first sacrificial number to the hungry void: ");

        if (scanf("%lf", &zahl1) == 1) {
            break; // Sinnvoller Input
        } else {
            printf("The void rejects your offering! Scream a valid number into the abyss!\n");
            clear_input_buffer();
        }
    } while (1);

    // Gleiche wie oben für die zweite Zahl
    do {
        printf("Now, whisper the second cursed numeral to the whispering engine: ");
        if (scanf("%lf", &zahl2) == 1) {
            break;
        } else {
            printf("Your whisper is gibberish to the machine! Utter a number it can taste!\n");
            clear_input_buffer();
        }
    } while (1);

    printf("\nChoose the ritual symbol to bind them (A:summon, S:sever, M:multiply, D:devour):\n");
    printf("summon (add), sever (subtract), multiply(ehm...selbsterklärend) und devour(DIVISION)!\n");
    clear_input_buffer();

    // Übrigens Lernerfolg wenn auch minimal. C hat wohl keine Bollean Werte - hätte ich nicht gedacht.
    int erfolg = 1; 

    do {
        printf("Sophies Choice: ");
        // Nur den ersten Buchstaben lesen
        if (scanf("%c", &operation) != 1) {
            printf("The ritual faltered! The symbol slipped from your mind!\n");
            erfolg = 0;
            continue;
        }

        // Umwandeln in Cap Buchstaben -- case-insense usw
        operation = toupper(operation);
        clear_input_buffer();

        switch (operation) {
            case 'A':
                ergebnis = zahl1 + zahl2;
                printf("HERE WE GO\n");
                break;
            case 'S':
                ergebnis = zahl1 - zahl2;
                break;
            case 'M':
                ergebnis = zahl1 * zahl2;
                break;
            case 'D':
                if (zahl2 == 0) {
                    printf("\nCATASTROPHE! You invoked the devourer with NOTHING! The void hungers infinitely!\n");
                    erfolg = 0;
                } else {
                    ergebnis = zahl1 / zahl2;
                }
                break;
            default:
                printf("\nThat symbol is a heresy! Use only the sanctified ones: A, S, M, or D!\n");
                erfolg = 0;
                continue;
        }
        
        break;
        
    } while (1);

    // Debug prints für mich
    // printf("OUTSIDE THE LOOP\n");
    // printf("erfolg: %d\n", erfolg);
    // printf("operation: %c\n", operation);

    if (erfolg && operation != 'D') {
         printf("\nThe calculation is complete. The unspeakable result is: %.2lf\n", ergebnis);
    } else if (erfolg && operation == 'D' && zahl2 != 0) {
         printf("\nThe calculation is complete. The unspeakable result is: %.2lf\n", ergebnis);
    } 

    return 0;
}