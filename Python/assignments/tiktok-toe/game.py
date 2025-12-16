import numpy as np
from collections import Counter
import random

# Hab ich von https://patorjk.com/ die generieren diese ASCII Art Zeug
def splash_screen():
    print("\n" * 2)
    print(
r"""
          d8, d8b                        d8b                                  
   d8P   `8P  ?88          d8P           ?88              d8P                 
d888888P       88b      d888888P          88b          d888888P               
  ?88'    88b  888  d88'  ?88'   d8888b   888  d88'      ?88'   d8888b  d8888b
  88P     88P  888bd8P'   88P   d8P' ?88  888bd8P'       88P   d8P' ?88d8b_,dP
  88b    d88  d88888b     88b   88b  d88 d88888b         88b   88b  d8888b   
  `?8b  d88' d88' `?88b,  `?8b  `?8888P'd88' `?88b,      `?8b  `?8888P'`?888P'
""".strip()
)
    print("\nWillkommen zu TikTok Toe!\nSpieler 1 ist 'O' und Spieler 2 (Maschine) ist 'X'\n")

class SpielBrett:
    def __init__(self):
        self.spielbrett = np.zeros((3, 3), dtype=int)
        self.spiel_durch = False
    
    @property
    def gewinner_tuples(self):
        gewinner = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        return gewinner
    
    @property
    def nicer_view_des_bretts(self):
        map = {0: " ", 1: "O", 2: "X"}

        print("Aktuelles Spielbrett:")
        print(f"-"*7)
        for zeile in self.spielbrett:
            zeilen_liste = []
            for feld in zeile:
                zeilen_liste.append(map[feld])
            print(f"|{'|'.join(zeilen_liste)}|")
            print(f"-"*7)
        
    def symbol_setzen(self, zeile: int, spalte: int, spieler: int):
        #guard_clausing
        if self.spielbrett[zeile, spalte] != 0:
            print(f"Feld ist schon belegt mit einem {self.spielbrett[zeile, spalte]}!")
            return
        
        self.spielbrett[zeile, spalte] = spieler

        if self.schon_gewonnen(self.spielbrett) != 0:
            self.spiel_durch = True
            print(f"Spieler {spieler} hat gewonnen")

        return
    
    def update_brett(self, new_brett: np.array):
        self.spielbrett = new_brett

        if self.schon_gewonnen(self.spielbrett) != 0:
            self.spiel_durch = True
            print(f"Spieler {self.schon_gewonnen(self.spielbrett)} hat gewonnen")

    def schon_gewonnen(self, brett: np.array) -> int:
        
        brett_ravel = brett.ravel()

        #unique_values = np.unique(brett_ravel)


        for winning_tuple in self.gewinner_tuples:
            if (brett_ravel[winning_tuple[0]] == brett_ravel[winning_tuple[1]] == brett_ravel[winning_tuple[2]] != 0):
                return brett_ravel[winning_tuple[0]]

        return 0

class Machine:
    def __init__(self, spielbrett):
        self.aktuelles_brett = spielbrett.spielbrett
        self.gewinner_zuege = spielbrett.gewinner_tuples

    def bestes_feld(self):

        gewinner = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        
        raveled_brett = self.aktuelles_brett.ravel()

        default_return = np.random.choice(np.where(raveled_brett == 0)[0])

        actual_winning_tuples = []
        for winning_tuple in gewinner:
            if (raveled_brett[winning_tuple[0]] == raveled_brett[winning_tuple[1]] == raveled_brett[winning_tuple[2]]) and raveled_brett[winning_tuple[0]] == 0:
                actual_winning_tuples.extend(winning_tuple)

        häufigkeiten = Counter(actual_winning_tuples)

        if not häufigkeiten:
            return default_return
        
        max_häufigkeit = max(häufigkeiten.values())
        positionen = [k for k, v in häufigkeiten.items() if v == max_häufigkeit]
        return np.random.choice(positionen)

    def setzen(self):

        raveld_brett = self.aktuelles_brett.ravel()
        feld = self.bestes_feld()
        raveld_brett[feld] = 2
        brett = raveld_brett.reshape(3,3)
        self.aktuelles_brett = brett
        return feld


# FULL DISCLOSURE Hier hab ich einfach auf CoPilot accept geklickt.
if __name__ == "__main__":
    splash_screen()
    spielbrett = SpielBrett()

    while not spielbrett.spiel_durch:
        zeile = int(input("Zeile (0-2): "))
        spalte = int(input("Spalte (0-2): "))
        spielbrett.symbol_setzen(zeile, spalte, 1)
        print(spielbrett.nicer_view_des_bretts)

        if spielbrett.spiel_durch:
            break

        maschine = Machine(spielbrett)
        feld = maschine.setzen()
        zeile_maschine, spalte_maschine = divmod(feld, 3)
        print(f"Maschine setzt auf Feld: ({zeile_maschine}, {spalte_maschine})")
        spielbrett.update_brett(maschine.aktuelles_brett)
        print(spielbrett.nicer_view_des_bretts)


    # maschine = Machine(spielbrett)

    # spielbrett.symbol_setzen(0, 0, 1)
    # spielbrett.symbol_setzen(0, 1, 1)
    # print(spielbrett.spielbrett)
    # bestes_feld = maschine.bestes_feld()
    # print(f"Maschine wählt Feld: {bestes_feld}")
# if __name__ == "__main__":
#     spielbrett = SpielBrett()
#     maschine = Machine(spielbrett)

#     spielbrett.symbol_setzen(0, 0, 1)
#     spielbrett.symbol_setzen(0, 1, 1)
#     print(spielbrett.spielbrett)
#     bestes_feld = maschine.bestes_feld()
#     print(f"Maschine wählt Feld: {bestes_feld}")


# def schon_gewonnen_test(brett: np.array) -> int:
    
#     brett_ravel = brett.ravel()

#     #unique_values = np.unique(brett_ravel)
#     gewinner = [
#         (0, 1, 2), (3, 4, 5), (6, 7, 8),
#         (0, 3, 6), (1, 4, 7), (2, 5, 8),
#         (0, 4, 8), (2, 4, 6)
#     ]

#     default_return = np.random.choice(np.where(test2 == 0)[0])

#     actual_winning_tuples = []
#     for winning_tuple in gewinner:
#         if (brett_ravel[winning_tuple[0]] == brett_ravel[winning_tuple[1]] == brett_ravel[winning_tuple[2]]) and brett_ravel[winning_tuple[0]] == 0:
#             actual_winning_tuples.extend(winning_tuple)

#     # häufigkeiten = Counter(actual_winning_tuples)

#     # if not häufigkeiten:
#     #     return default_return
    
#     # max_häufigkeit = max(häufigkeiten.values())
#     # position = [k for k, v in häufigkeiten.items() if v == max_häufigkeit]
#     return actual_winning_tuples

    
# test = np.random.randint(0, 3, size=(3, 3))
# print(test)

# #x/y coordinates of zeros
# print(np.where(test == 0))
# test_ravel =test.ravel()
# print(type(test_ravel))
# print(test_ravel)
# test_ravel[4] = 19
# print(test_ravel)
# unique = np.unique(test_ravel)
# print(unique)

test2 = np.array(([1, 1, 0],
                 [0, 0, 0],
                [0, 2, 0]))

print(test2[0])
# print("HERE")
# print(test2)
# tuples = schon_gewonnen_test(test2)
# print(tuples)
# häufigkeiten = Counter(tuples)

# max_häufigkeit = max(häufigkeiten.values())
# position = [k for k, v in häufigkeiten.items() if v == max_häufigkeit]
# print("Positionen mit höchster Häufigkeit:", position)
# print(tuples)
# test2 = test2.ravel()
# print(np.where(test2 == 0))
# print(np.random.choice(np.where(test2 == 0)[0]))
# print(test2)

# test_list = [1, 4, 5, 2, 7]

# print(random.choice(test_list))
