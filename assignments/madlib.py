# Übung vom 7.11.2025 basierend auf diesem Video von Kylie Ying....url is die https://www.youtube.com/watch?v=8ext9G7xspg&t=5s

def mad_lib_uebung(n: int = 3) -> None:

    adjektive = [input(f"Adjektiv {i+1}: ") for i in range(n)]
    substantive = [input(f"Substantiv {i+1}: ") for i in range(n)]
    verben = [input(f"Verb {i+1}: ") for i in range(n)]

    # Too be fair, die Sätze hier sind KI generiert. Nur so aus Transparenzgründen und so weiter, ne...

    # Ach so und wenn ich jetzt hier ernst entwickeln würde wäre das hier eine Stelle, wo ic ein TODO setzen würde-
    # Der Grund: Naja oben ist die n-Anzahl der Wörter variabel, aber die Sätze sind fest kodiert.
    # Alsooooooo FIXME wa?
    
    sätze = [
        f"An einem {adjektive[0]} Tag beschloss das {substantive[0]}, zu {verben[0]}.",
        f"Später erschien ein {adjektive[1]} {substantive[1]}, das laut begann zu {verben[1]}.",
        f"Am Abend blieb nur ein {adjektive[2]} {substantive[2]} zurück, das müde aufhörte zu {verben[2]}."
    ]

    print(" ".join(sätze))

if __name__ == "__main__":
    mad_lib_uebung()