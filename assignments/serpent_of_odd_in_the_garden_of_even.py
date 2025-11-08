# Übung vom 6.11.2025 von den Habmann Slides

def habmann_odd_even():
    odd_even_check = lambda my_wonderful_number: "gerade" if my_wonderful_number % 2 == 0 else "ungerade"
    zahl = int(input("Nummer: "))
    print(f"Die Zahl ist {odd_even_check(zahl)}.")

if __name__ == "__main__":
    habmann_odd_even()