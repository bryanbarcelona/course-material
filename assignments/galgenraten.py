import random
from worter_die_worte_sind import worte
from splash_screen import print_title_screen


# Man könnte noch implementieren: Visualisierung des Galgens (ich glaub Kylie macht das auch zumindest ist da was in ihrem Github)...öhm 
# vielleicht dynamische Versuchszahl basierend auf der Wortlänge...joa mehr fällt mir grad nicht ein
# Nachtrag: Ziemlich dumm....hangman hat ja per definition nur eine gestztet anzahl an Versuchen...duhhhhh....


def wort_aussuchen(worte_liste, mindest_laenge=5):
    passende_worte = [wort for wort in worte_liste if len(wort) >= mindest_laenge]
    return random.choice(passende_worte)

def find_all_char_positions(main_string, char):
    return [i for i, c in enumerate(main_string) if c == char]

anzahl_der_buchstaben = input("Wie viele Zeichen sollte das zu erratende Wort haben mein lieber Herr...oder Frau...oder ehhhmm...joa? ")

das_wort = wort_aussuchen(worte, mindest_laenge=int(anzahl_der_buchstaben))

def galgenraten(wort: str, versuche: int = 6) -> None:

    # Debug print krams
    #print(wort)
    if versuche < len(wort):
        versuche = len(wort)
    print(f"Willkommen in der Hölle! Ich bin der Dämon Jens Detlef Erikson dein worst nightmare. Du hast {versuche} Versuche.")
    print(f"Das Wort hat {len(wort)} Runen.")

    platzhalter_string = "_ " * len(wort)
    print(platzhalter_string)

    versuchstracking = 0
    while versuchstracking < versuche:
        geratenes_wort = input("Bitte gib eine heilige Rune ein oder das vollständige Wort ein: ").lower()

        if geratenes_wort == str(wort):
            print("Wowi das hast du voll fein gemacht.")
            break
        if len(geratenes_wort) == 1 and geratenes_wort.isalpha():
            if geratenes_wort in wort:
                versuchstracking += 1
                print(f"This man is a genius! Der Buchstabe '{geratenes_wort}' ist im Wort enthalten. Du hast noch {versuche - versuchstracking} Versuche übrig.")
                positionen = find_all_char_positions(wort, geratenes_wort)
                for pos in positionen:
                    platzhalter_string = platzhalter_string[:pos * 2] + geratenes_wort + platzhalter_string[pos * 2 + 1:]
                print(platzhalter_string)
                if "_" not in platzhalter_string:
                    print("Wowi das hast du voll fein gemacht.")
                    break
                

            else:
                versuchstracking += 1
                print(f"Nope!!11!1!!! Der Buchstabe '{geratenes_wort}' ist nicht im Wort. Du hast noch {versuche - versuchstracking} Versuche übrig.")
                continue
        elif len(geratenes_wort) == len(wort) and geratenes_wort.isalpha():
            if geratenes_wort == wort:
                print("Wowi das hast du voll fein gemacht.")
                break
            else:
                versuchstracking += 1
                print(f"Meeeep! Das Wort ist nicht '{geratenes_wort}'. Du hast noch {versuche - versuchstracking} Versuche übrig.")
        else:
            print("Bitte gib einen einzelnen Buchstaben oder das vollständige Wort ein.")

    if "_" in platzhalter_string:
        print(f"Muuahahahahaaha. Deine Seele ist mein. Das Wort war '{wort}'. Lol.")
    
    else:
        print("This player is a genius! What you are seeing may seem like magic but it is pure algorithmic brilliance. Like and subscribe for more. Oder was auch immer diese KI-generierten YouTube-Shorts am Ende immer sagen...")



        # if geratenes_wort in wort:
        #     print(f"Richtig! Der Buchstabe '{geratenes_wort}' ist im Wort enthalten.")
        # else:
        #     versuchstracking += 1
        #     print(f"Falsch! Der Buchstabe '{geratenes_wort}' ist nicht im Wort. Du hast noch {versuche - versuchstracking} Versuche übrig.")

galgenraten(das_wort)