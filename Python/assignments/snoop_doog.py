class SnoopDoog:
    def __init__(self, name: str):
        self.name = name

    def snoop(self):
        print(f"{self.name} is snooping around...")


if __name__ == "__main__":
    snoop = SnoopDoog("Snoop Dogg")
    dr_dre = SnoopDoog("Dr. Dre")

    snoop.snoop()
    dr_dre.snoop()