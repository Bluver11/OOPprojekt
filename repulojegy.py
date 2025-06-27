from abc import ABC, abstractmethod

# Absztrakt Járat osztály
class Jarat(ABC):
    def __init__(self, jaratszam: str, celallomas: str, jegyar: float):
        self.jaratszam = jaratszam
        self.celallomas = celallomas
        self.jegyar = jegyar

    @abstractmethod
    def jarat_tipus(self):
        pass


# Belföldi Járat
class BelfoldiJarat(Jarat):
    def __init__(self, jaratszam: str, celallomas: str, jegyar: float):
        super().__init__(jaratszam, celallomas, jegyar)

    def jarat_tipus(self):
        return "Belföldi"


# Nemzetközi Járat
class NemzetkoziJarat(Jarat):
    def __init__(self, jaratszam: str, celallomas: str, jegyar: float):
        super().__init__(jaratszam, celallomas, jegyar)

    def jarat_tipus(self):
        return "Nemzetközi"


# Légitársaság osztály
class LegiTarsasag:
    def __init__(self, nev: str):
        self.nev = nev
        self.jaratok = []

    def jarat_hozzaad(self, jarat: Jarat):
        self.jaratok.append(jarat)

    def listaz_jaratokat(self):
        for jarat in self.jaratok:
            print(f"{jarat.jaratszam} - {jarat.celallomas} ({jarat.jarat_tipus()}), Ár: {jarat.jegyar} Ft")
        
    def jegyet_foglal(self, utas_nev: str, jarat_index: int):
        try:
            jarat = self.jaratok[jarat_index - 1]
            foglalas = JegyFoglalas(utas_nev, jarat)
            self.foglalasok.append(foglalas)
            print(f"\n✅ Foglalás sikeres! Ár: {jarat.jegyar} Ft")
        except IndexError:
            print("❌ Hibás járatindex!")

    def foglalas_lemondas(self, utas_nev: str):
        for f in self.foglalasok:
            if f.utas_nev == utas_nev:
                self.foglalasok.remove(f)
                print(f"❎ Foglalás törölve: {utas_nev}")
                return
        print("❌ Nincs ilyen nevű foglalás!")

    def listaz_foglalasokat(self):
        if not self.foglalasok:
            print("ℹ️ Nincs aktív foglalás.")
        for f in self.foglalasok:
            print(f.foglalas_info())


# Jegyfoglalás osztály
class JegyFoglalas:
    def __init__(self, utas_nev: str, jarat: Jarat):
        self.utas_nev = utas_nev
        self.jarat = jarat

    def foglalas_info(self):
        return (f"Foglalás: {self.utas_nev} számára a(z) {self.jarat.jarat_tipus()} "
                f"járatra ({self.jarat.jaratszam}) - {self.jarat.celallomas}, Ár: {self.jarat.jegyar} Ft")

def menu():
    print("\n=== Légitársaság Jegyfoglaló Rendszer ===")
    print("1. Járatok listázása")
    print("2. Jegy foglalása")
    print("3. Foglalás lemondása")
    print("4. Foglalások listázása")
    print("0. Kilépés")


if __name__ == "__main__":
    airline = LegiTarsasag("Ryanair")

    # Teszt járatok
    airline.jarat_hozzaad(BelfoldiJarat("HU101", "Debrecen", 8000))
    airline.jarat_hozzaad(NemzetkoziJarat("INT202", "Berlin", 30000))

    while True:
        menu()
        valasztas = input("Választás: ")

        if valasztas == "1":
            airline.listaz_jaratokat()

        elif valasztas == "2":
            airline.listaz_jaratokat()
            try:
                index = int(input("Melyik járatra szeretne foglalni? (sorszám): "))
                nev = input("Utas neve: ")
                airline.jegyet_foglal(nev, index)
            except ValueError:
                print("❌ Érvénytelen bemenet.")

        elif valasztas == "3":
            nev = input("Add meg a nevet a lemondáshoz: ")
            airline.foglalas_lemondas(nev)

        elif valasztas == "4":
            airline.listaz_foglalasokat()

        elif valasztas == "0":
            print("👋 Kilépés...")
            break

        else:
            print("❌ Érvénytelen opció.")
