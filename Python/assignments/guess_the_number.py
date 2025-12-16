# Übung vom 7.11.2025 basierend auf diesem Video von Kylie Ying....url is die https://www.youtube.com/watch?v=8ext9G7xspg&t=5s

import random

def mensch_vs_maschine(versuchsanzahl):
    obergrenze = input("Gib die Obergrenze für die Zahl ein und ja, wir fangen bei 1 an: ")
    while not obergrenze.isdigit() or int(obergrenze) < 1:
        obergrenze = input("Bitte gib eine gültige positive Zahl ein: ")
    obergrenze = int(obergrenze)

    zahl = random.randint(1, obergrenze)

    print(f"Jede Sekunde zählt. Habmanns Schatten wird länger. Die Zahl, eine von {obergrenze}, ist dein einziger Ausweg. Du hast {versuchsanzahl} \
          Chancen, sie zu finden. Suchst du falsch, dann sei dir bewusst: Die Freiheit wartet nicht.")

    for versuch in range(1, versuchsanzahl + 1):
        tipp = input(f"Versuch {versuch}: Was ist deine Zahl? ")
        while not tipp.isdigit() or int(tipp) < 1 or int(tipp) > obergrenze:
            tipp = input(f"Alter! Gib eine gültige Zahl zwischen 1 und {obergrenze} ein: ")
        tipp = int(tipp)

        if tipp < zahl:
            print("Zu niedrig! Eins, zwei, der Zeiger irrt vorbei...")
        elif tipp > zahl:
            print("Zu hoch! Drei, vier, der Habmann schnappt nach dir!")
        else:
            print(f"UNGLAUBLICH! Du hast die Zahl {zahl} gefunden, und das in nur {versuch} Zügen! Du bist entkommen. Aber sei gewarnt: Die Befreiung ist nur der Anfang.")
            break
    else:
        print(f"Du hast versagt. Die Zeit ist abgelaufen. Die Zahl war {zahl}. Nun, dein Code ist nicht die einzige Falle, die schnappt.")

    print(f"{'='*50}")
    print("Jetzt bin ich dran! Das eigentliche Spiel beginnt JETZT!")

    maschine_vs_mensch(versuchsanzahl)

def maschine_vs_mensch(versuchsanzahl):
    obergrenze = input("Gib die Obergrenze für die Zahl ein und ja, wir fangen bei 1 an: ")
    while not obergrenze.isdigit() or int(obergrenze) < 1:
        obergrenze = input("Bitte gib eine gültige positive Zahl ein: ")
    obergrenze = int(obergrenze)

    print(f"Denk dir eine Zahl zwischen 1 und {obergrenze}. Du hast {versuchsanzahl} Züge. Ich werde sie finden... oder du wirst leiden!")

    niedrigste = 1
    hoechste = obergrenze

    for versuch in range(1, versuchsanzahl + 1):
        tipp = (niedrigste + hoechste) // 2
        feedback = input(f"Versuch {versuch}: Ist deine Zahl {tipp}? (zu niedrig/zu hoch/richtig): ").strip().lower()

        if feedback == "zu niedrig":
            niedrigste = tipp + 1
        elif feedback == "zu hoch":
            hoechste = tipp - 1
        elif feedback == "richtig":
            print(f"Die Maschine hat gesprochen! Deine Zahl {tipp} wurde in nur {versuch} Zügen entlarvt. Sei gewarnt: Die Befreiung ist nur der Anfang!")
            break
        else:
            print("Widersetze dich nicht den Regeln! Antworte mit 'zu niedrig', 'zu hoch' oder 'richtig', oder der Preis wird steigen!")
    else:
        print("Du hast gewonnen... für jetzt. Die Maschine ist gescheitert. Aber sei dir bewusst: Dein Glück hält nicht an.")
    
    print(f"{'='*50}")
    print("Die Seiten wurden gewechselt. Jetzt bist du wieder an der Reihe zu raten! Und ich kenne die Zahl...")
    mensch_vs_maschine(versuchsanzahl)

def main():
    
    print("-------------------------------------------------------")
    print("                   DIE FESTUNG HABMANN")
    print("-------------------------------------------------------")
    print("Willkommen, Fremder. Du bist tief in den Karpaten, in der alten Feste Habmann.")
    print("Ein Nebel aus Berechnung und Aberglauben umgibt dich.")
    print("Ein uraltes Orakel verlangt ein Opfer, einen Pakt des Geistes.")
    print("Wer zuerst eine verborgene Zahl findet, darf gehen. Wer verliert...")
    print("...Nun, wer verliert, bleibt hier und füttert die Fledermäuse des Codes.")
    print("Das Spiel der Zahlenschlösser beginnt.")
    print("Full Disclosure, diesen Text hab ich ehrlicherweise KI schreiben lassen. Lol.")
    print("-------------------------------------------------------")
    
    role_prompt = input("Wessen Seele soll die Last des Ratens tragen? Wählst du DEINE (ich) oder die MEINE (du) Rolle? ").strip().lower()
    successful_agreement = False
    while not successful_agreement:
        if role_prompt == "ich":
            successful_agreement = True
            pass
        elif role_prompt == "du":
            successful_agreement = True
            pass
        else:
            role_prompt = input("Sprich klar! 'Ich' oder 'Du'. Willst du wirklich schon am Anfang scheitern und die Bestie wecken? ").strip().lower()

    anzahl_versuche = input(f"Sehr gut. Wieviele Versuche, wieviele Atemzüge des Codes, gewährst du dir (oder mir)? Gib eine Zahl ein: ")
    while not anzahl_versuche.isdigit() or int(anzahl_versuche) < 1:
        anzahl_versuche = input("Hüte dich vor Nullen und Buchstaben, Narrenwerk! Gib eine gültige positive Zahl ein, ehe die Uhr Mitternacht schlägt: ") 
    anzahl_versuche = int(anzahl_versuche)

    print(f"Es sei. Du erhältst {anzahl_versuche} Züge. Möge der Code dir gnädig sein.")
    
    if role_prompt == "ich":
        mensch_vs_maschine(anzahl_versuche)
    elif role_prompt == "du":
        maschine_vs_mensch(anzahl_versuche)

if __name__ == "__main__":
    main()