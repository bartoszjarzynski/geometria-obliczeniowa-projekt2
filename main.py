import matplotlib.pyplot as plt  # do tworzenia wykresów
from random import randint  # do tworzenia i sortowania danych
from math import atan2  # for computing polar angle


# Tworzy wykres punktowy, dane wejściowe to lista współrzędnych (x,y).
# Drugie dane wejściowe 'otoczka_wypukla' to kolejna lista współrzędnych (x,y) składająca się z punktów w 'koordynaty' zewnętrzne, jeśli nie jest pusta, elementy tej listy zostaną użyte do narysowania granicy zewnętrznej.
def wykres_punktowy(koordynaty, otoczka_wypukla=None):
    xs, ys = zip(*koordynaty)  # rozdziel do listy współrzędnych
    plt.scatter(xs, ys)  # wykresl punkty

    if otoczka_wypukla != None:
        # Wykreśl wypukłą granicę otoczki, dodatkowa iteracja na końcu, aby linia ograniczająca zawinęła się wokół
        for i in range(1, len(otoczka_wypukla) + 1):
            if i == len(otoczka_wypukla):
                i = 0  # zawiń
            c0 = otoczka_wypukla[i - 1]
            c1 = otoczka_wypukla[i]
            plt.plot((c0[0], c1[0]), (c0[1], c1[1]), 'r')
    plt.show()


# Zwraca kąt biegunowy (radiany) od p0 do p1.
# Jeśli p1 jest puste, domyślnie zastępuje je globalną zmienną 'min_kat_bieg', ustawioną w funkcji 'alg_grahama'.
def kat_biegunowy(p0, p1=None):
    if p1 == None:
        p1 = min_kat_bieg
    y_zakres = p0[1] - p1[1]
    x_zakres = p0[0] - p1[0]
    return atan2(y_zakres, x_zakres)


# Zwraca odległość euklidesową od p0 do p1, pierwiastek kwadratowy nie jest stosowany ze względu na szybkość.
# Jeśli p1 jest puste, domyślnie zastępuje je globalną zmienną 'min_kat_bieg', ustawioną w funkcji 'alg_grahama'.
def odleglosc(p0, p1=None):
    if p1 is None:
        p1 = min_kat_bieg
    y_zakres = p0[1] - p1[1]
    x_zakres = p0[0] - p1[0]
    return y_zakres ** 2 + x_zakres ** 2


# Zwraca wyznacznik macierzy 3x3
# 	[p1(x) p1(y) 1]
#	[p2(x) p2(y) 1]
# 	[p3(x) p3(y) 1]
# Jeśli >0, to przeciwnie do ruchu wskazówek zegara
# Jeśli <0, to zgodnie z ruchem wskazówek zegara
# Jeśli =0 to współliniowe
def sprawdz_wyznacznik(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])


# Sortuje w porządku rosnącym kąta biegunowego od punktu „min_kat_bieg”.
# Zakłada się, że zmienna 'kotwica' jest globalna, ustawiana wewnątrz 'alg_grahama'.
# W przypadku dowolnych wartości o równych kątach biegunowych stosuje się drugie sortowanie, aby zapewnić rosnącą odległość od punktu „min_kat_bieg”.
def szybkie_sortowanie(a):
    if len(a) <= 1:
        return a
    mniejsza, rowna, wieksza = [], [], []
    piv_ang = kat_biegunowy(a[randint(0, len(a) - 1)])  # wybierz losowy punkt
    for pt in a:
        pt_ang = kat_biegunowy(pt)  # obliczyć bieżący kąt punktu
        if pt_ang < piv_ang:
            mniejsza.append(pt)
        elif pt_ang == piv_ang:
            rowna.append(pt)
        else:
            wieksza.append(pt)
    return szybkie_sortowanie(mniejsza) + sorted(rowna, key=odleglosc) + szybkie_sortowanie(wieksza)


# Zwraca wierzchołki stanowiące granice otoczki wypukłej zawierające wszystkie punkty w zbiorze wejściowym.
# Wejście 'punkty' jest listą współrzędnych (x,y).
# Jeśli 'pokaz_postep' jest ustawione na True, postęp w konstruowaniu otoczki będzie wykreślany w każdej iteracji.
def alg_grahama(punkty, pokaz_postep):
    global min_kat_bieg

    # Znajdź punkt (x,y) o najniższej wartości y wraz z jego indeksem na liście 'punkty'. Jeśli jest wiele punktów o tej samej wartości y, wybierz ten z najmniejszym x.
    min_wartosc = None
    for i, (x, y) in enumerate(punkty):
        if min_wartosc is None or y < punkty[min_wartosc][1]:
            min_wartosc = i
        if y == punkty[min_wartosc][1] and x < punkty[min_wartosc][0]:
            min_wartosc = i

    # Ustaw zmienną globalną 'min_kat_bieg', używaną przez funkcje 'kat_biegunowy' i 'odleglosc'
    min_kat_bieg = punkty[min_wartosc]

    # Posortuj punkty według kąta biegunowego, a następnie usuń min_kat_bieg z posortowanej listy
    posortowane_pkt = szybkie_sortowanie(punkty)
    del posortowane_pkt[posortowane_pkt.index(min_kat_bieg)]

    # min_kat_bieg i punkt o najmniejszym kącie biegunowym zawsze będzie na otoczka
    otoczka = [min_kat_bieg, posortowane_pkt[0]]
    for s in posortowane_pkt[1:]:
        if pokaz_postep:
            wykres_punktowy(punkty, otoczka)
        while sprawdz_wyznacznik(otoczka[-2], otoczka[-1], s) <= 0:
            del otoczka[-1]
            if len(otoczka) <= 2:
                break
        otoczka.append(s)
    if len(otoczka) == 2:
        if otoczka[0][0] == otoczka[1][0] and otoczka[0][1] == otoczka[1][1]:
            otoczka.pop()
    return otoczka


# Zwraca listę koordynatów (x,y) tworzonych losowo z zakresu wpisanego min i max
def stworz_pkty(ilosc=4, min=-50, max=50):
    return [[randint(min, max), randint(min, max)] for _ in range(ilosc)]


# Sprawdzanie czy wpisana wartość jest liczbą
def sprawdz_wartosc(i, o):
    while True:
        a = input("Podaj " + str(i) + " współrzędną " + str(o) + "-ową: ")
        try:
            return int(a)
        except ValueError:
            try:
                return float(a)
            except ValueError:
                print("Wpisana wartość nie jest liczbą! Spróbuj ponownie..")


# Odpytuje użytkownika o wybrane bądź losowe współrzędne
def wspolrzedne():
    global pkt
    odpowiedz = input("Chcesz wpisać własne współrzędne? (Wpisz tak/nie) ")
    if odpowiedz == ("tak") or odpowiedz == ("Tak"):
        for i in range(1, 5):
            x = None
            y = None
            x = sprawdz_wartosc(i, "X")
            y = sprawdz_wartosc(i, "Y")
            pkt.append([x, y])
    elif odpowiedz == ("nie") or odpowiedz == ("Nie"):
        pkt = stworz_pkty()
    else:
        print("Nie zrozumiałem")
        wspolrzedne()


pkt = []
wspolrzedne()
print("Współrzędne:", pkt)
wykres_punktowy(pkt)
otoczka = alg_grahama(pkt, True)
wykres_punktowy(pkt, otoczka)
print("Współrzędne otoczki wypukłej:", otoczka)
prefix = "Otoczka wypukła jest "
if len(otoczka) == 1:
    print(prefix+"punktem")
if len(otoczka) == 2:
    print(prefix+"odcinkiem")
if len(otoczka) == 3:
    print(prefix+"trójkątem")
if len(otoczka) == 4:
    print(prefix+"czworokątem")
print("Koniec programu")
quit()