# Übung vom 6.11.2025 von den Habmann Slides

def die_listen_uebung():
    die_tatverdaechtigen = ["Opa", "Enkel", "Schwieegermutter"]

    for tatverdaechtiger in die_tatverdaechtigen:
        print(f"Der Tatverdächtige ist: {tatverdaechtiger}")

    print("Und jetzt nochma alle sortiert:")
    for tatverdaechtiger in sorted(die_tatverdaechtigen):
        print(f"Der Tatverdächtige ist: {tatverdaechtiger}")
      
    print("Jetzt drehen wir den Spieß um:") # Also uff der originalen Liste die davor wurde nur für die Iteration vorher in eine andere Sitzordung geprügelt.
    for tatverdaechtiger in reversed(die_tatverdaechtigen):
        print(f"Der Tatverdächtige ist: {tatverdaechtiger}")

if __name__ == "__main__":
    die_listen_uebung()