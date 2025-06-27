from abc import ABC, abstractmethod
from datetime import datetime ,timedelta

# Absztrakt Járat osztály
class Jarat(ABC):
    def __init__(self, jaratszam: str, celallomas: str, jegyar: float):
        self.jaratszam = jaratszam
        self.celallomas = celallomas
        self.jegyar = jegyar
        self.elerheto = True 

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
        
    def jegyet_foglal(self, utas_nev: str, jarat_index: int, datum_str: str):
     try:
         jarat = self.jaratok[jarat_index - 1]
         if not jarat.elerheto:
            print("❌ Ez a járat nem elérhető foglalásra.")
            return

         datum = datetime.strptime(datum_str, "%Y-%m-%d")
         if datum < datetime.today():
            print("❌ Nem foglalható múltbeli dátumra.")
            return

         foglalas = JegyFoglalas(utas_nev, jarat, datum_str)
         self.foglalasok.append(foglalas)
         print(f"\n✅ Foglalás sikeres! Ár: {jarat.jegyar} Ft")

     except IndexError:
        print("❌ Hibás járatindex!")
     except ValueError as ve:
        print(f"❌ Hibás dátum: {ve}")

    def foglalas_lemondas(self, utas_nev: str, jaratszam: str):
     for f in self.foglalasok:
        if f.utas_nev == utas_nev and f.jarat.jaratszam == jaratszam:
            self.foglalasok.remove(f)
            print(f"❎ Foglalás törölve: {utas_nev} - {jaratszam}")
            return
    print("❌ Nincs ilyen foglalás!")

    def listaz_foglalasokat(self):
        if not self.foglalasok:
            print("ℹ️ Nincs aktív foglalás.")
        for f in self.foglalasok:
            print(f.foglalas_info())


# Jegyfoglalás osztály
class JegyFoglalas:
    def __init__(self, utas_nev: str, jarat: Jarat, datum_str: str):
        self.utas_nev = utas_nev
        self.jarat = jarat
        try:
            self.datum = datetime.strptime(datum_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Hibás dátumformátum! (várható: ÉÉÉÉ-HH-NN)")

    def foglalas_info(self):
        datum_str = self.datum.strftime("%Y-%m-%d")
        return (f"Foglalás: {self.utas_nev} számára a(z) {self.jarat.jarat_tipus()} "
                f"járatra ({self.jarat.jaratszam}) - {self.jarat.celallomas}, "
                f"Dátum: {datum_str}, Ár: {self.jarat.jegyar} Ft")

def menu():
    print("\n=== Légitársaság Jegyfoglaló Rendszer ===")
    print("1. Járatok listázása")
    print("2. Jegy foglalása")
    print("3. Foglalás lemondása")
    print("4. Foglalások listázása")
    print("0. Kilépés")


if __name__ == "__main__":

    # Légitársaság létrehozása
    airline = LegiTarsasag("Ryanair")

    # Járatok hozzáadása
    j1 = BelfoldiJarat("HUN101", "Debrecen", 8000)
    j2 = NemzetkoziJarat("INT202", "Berlin", 35000)
    j3 = NemzetkoziJarat("INT303", "London", 42000)

    airline.jarat_hozzaad(j1)
    airline.jarat_hozzaad(j2)
    airline.jarat_hozzaad(j3)

    # Dátum generálás (jövőbeli napok)
    today = datetime.today()
    d1 = (today + timedelta(days=3)).strftime("%Y-%m-%d")
    d2 = (today + timedelta(days=5)).strftime("%Y-%m-%d")
    d3 = (today + timedelta(days=7)).strftime("%Y-%m-%d")

    # Foglalások hozzáadása
    airline.foglalasok.append(JegyFoglalas("Kovács Anna", j1, d1))
    airline.foglalasok.append(JegyFoglalas("Szabó Béla", j1, d2))
    airline.foglalasok.append(JegyFoglalas("Nagy Eszter", j2, d1))
    airline.foglalasok.append(JegyFoglalas("Tóth Gábor", j2, d2))
    airline.foglalasok.append(JegyFoglalas("Farkas Dóra", j3, d1))
    airline.foglalasok.append(JegyFoglalas("Kiss Péter", j3, d3))

    print("📦 Előre betöltött adatok: 1 légitársaság, 3 járat, 6 foglalás.")

    print("📦 Előre betöltött adatok: 1 légitársaság, 3 járat, 6 foglalás.")
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
                datum = input("Utazás dátuma (ÉÉÉÉ-HH-NN): ")
                airline.jegyet_foglal(nev, index,datum)
            except ValueError:
                print("❌ Érvénytelen bemenet.")

        elif valasztas == "3":
            nev = input("Add meg a nevet a lemondáshoz: ")
            jaratszam = input("Add meg a járatszámot: ")
            airline.foglalas_lemondas(nev,jaratszam)

        elif valasztas == "4":
            airline.listaz_foglalasokat()

        elif valasztas == "0":
            print("👋 Kilépés...")
            break

        else:
            print("❌ Érvénytelen opció.")
