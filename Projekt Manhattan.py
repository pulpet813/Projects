import tkinter as tk

# Biblioteka numpy, sluzaca do optymalizowania projektu
import numpy as np

"Biblioteka mpmath, sluzaca do wykonywania precyzyjnych obliczen matematycznych"
import mpmath as mp

"Biblioteka matplotlib, sluzaca do tworzenia wykresow"
import matplotlib.pyplot as plt

"Okreslenie precyzji wykonywania obliczen"
mp.mp.dps = 50

"Zdefiniowane zmienne, zawierajace predkosc swiatla w prozni"
pr_swiatla = mp.mpf(299792458)
c = 1

"Definiowanie klasy, przedstawiajace pojedyncza czastke"


class Czastka:
    # Parametry klasy
    predkosc_ul = None
    predkosc_ms = None
    masa_spoczynkowa = None
    przyspieszenie_ul = None
    przyspieszenie_ms = None
    wektor_predkosci = None
    wektor_przyspieszenia = None
    "Zapisanie parametrow funkcji"

    def __init__(self, pr_x=0.0, pr_y=0.0, pr_z=0.0, przysp_x=0.0, przysp_y=0.0, przysp_z=0.0, mas_spo=0.0, typ=0):
        # parametr "typ" odpowiada za zaznaczenie przez uzytkownika, czy chce podac predkosc oraz przyspieszenie
        # jako ulamek pr. swiatla czy jednak w jednostkach m/s oraz m/s^2. Jezeli typ = 0, to predkosc i przysp sa podawane
        # jako ulamek pr. swiatla.
        if typ == 0:
            z = True
            while z:
                # Definiowanie predkosci jako ulamek pr. swiatla, z dodatkowym warunkiem na wartosc
                self.predkosc_ul = mp.mpf(((pr_x ** 2) + (pr_y ** 2) + (pr_z ** 2)) ** 0.5)
                if self.predkosc_ul >= 1:
                    pr_x = float(input(
                        "Zbyt duza predkosc, podaj wartosc predkosci wzgledem osi x ponownie (mniej niz 1)\n"))
                    if pr_y != 0:
                        pr_y = float(input(
                            "Zbyt duza predkosc, podaj wartosc predkosci wzgledem osi y ponownie (mniej niz 1)\n"))
                    if pr_z != 0:
                        pr_z = float(input(
                            "Zbyt duza predkosc, podaj wartosc predkosci wzgledem osi z ponownie (mniej niz 1)\n"))
                else:
                    z = False
            "Definiowanie reszty parametrow"
            self.predkosc_ms = mp.mpf(self.predkosc_ul * pr_swiatla)
            self.przyspieszenie_ul = mp.mpf(((przysp_x ** 2) + (przysp_y ** 2) + (przysp_z ** 2)) ** 0.5)
            self.przyspieszenie_ms = mp.mpf(self.przyspieszenie_ul * pr_swiatla)
        else:
            z = True
            while z:
                self.predkosc_ms = mp.mpf(((pr_x ** 2) + (pr_y ** 2) + (pr_z ** 2)) ** 0.5)
                if self.predkosc_ms >= pr_swiatla:
                    pr_x = float(input(
                        "Zbyt duza predkosc, podaj wartosc predkosci wzgledem osi x ponownie (mniej niz 299 792 458 "
                        "m/s)\n"))
                    if pr_y != 0:
                        pr_y = float(input(
                            "Zbyt duza predkosc, podaj wartosc predkosci wzgledem osi y ponownie (mniej niz 299 792 "
                            "458 m/s)\n"))
                    if pr_z != 0:
                        pr_z = float(input(
                            "Zbyt duza predkosc, podaj wartosc predkosci wzgledem osi z ponownie (mniej niz 299 792 "
                            "458 m/s)\n"))
                else:
                    z = False
            self.predkosc_ul = mp.mpf(self.predkosc_ms / pr_swiatla)
            self.przyspieszenie_ms = mp.mpf(((przysp_x ** 2) + (przysp_y ** 2) + (przysp_z ** 2)) ** 0.5)
            self.przyspieszenie_ul = mp.mpf(self.przyspieszenie_ms / pr_swiatla)
        self.wektor_predkosci = np.array([mp.mpf(pr_x), mp.mpf(pr_y), mp.mpf(pr_z)])
        self.wektor_przyspieszenia = np.array([mp.mpf(przysp_x), mp.mpf(przysp_y), mp.mpf(przysp_z)])
        self.czynnik_lor = mp.mpf((1 - self.predkosc_ul ** 2) ** (-0.5))
        self.masa_spoczynkowa = mas_spo

    "Funkcja liczaca droge przebyta przez otoczenie, wzgledem czastki poruszajacej sie jednostajnie"
    "lub droge przebyta przez obiekt przyspieszajacy jednostajnie, wzgledem obserwatora. Liczy rowniez w "
    "obu przypadkach droge w sensie newtonowskim, dla porownania"

    def droga(self, t):
        if self.przyspieszenie_ms == 0:
            t_dylatacja = t / self.czynnik_lor
            droga = self.predkosc_ms * t_dylatacja
            droga_new = self.predkosc_ms * t
        else:
            droga = ((np.sqrt(1 + (((self.przyspieszenie_ms * t + self.predkosc_ms * self.czynnik_lor) ** 2)
                                   / pr_swiatla ** 2))) - self.czynnik_lor) * (pr_swiatla ** 2) / self.przyspieszenie_ms
            droga_new = self.predkosc_ms * t + (1 / 2) * self.przyspieszenie_ms * t ** 2
        return droga, droga_new

    "Funkcja liczaca predkosc obiektu przyspieszanego."

    def predkosc_przyspieszanego_obiektu(self, t):
        predkosc = (self.przyspieszenie_ms * t + self.predkosc_ms * self.czynnik_lor) * (
                1 + (((self.przyspieszenie_ms * t + self.predkosc_ms * self.czynnik_lor) ** 2)
                     / pr_swiatla ** 2)) ** (-0.5)
        return predkosc

    "Funkcja liczaca czas, po ktorym predkosc przyspieszanego obiektu jest bardzo bliska pr_swiatla"

    def czas(self):
        t = (((299000000 * pr_swiatla) ** 2 / (pr_swiatla ** 2 - 299000000 ** 2)) ** (
            0.5) - self.predkosc_ms * self.czynnik_lor) / self.przyspieszenie_ms
        return t

    "Funkcja liczaca predkosc jednej czastki, poruszajacej sie ruchem jednostajnym prostoliniowym, wzgledem innej"
    "czastki poruszajacej ruchem jednostajnym prostoliniowym, lecz z innym wektorem predkosci"

    def wzgledna_predkosc(self, czasteczka2):
        pr_2_wzgl_1 = (
            (1 / self.czynnik_lor * (
                    1 - mp.fdot(self.wektor_predkosci, czasteczka2.wektor_predkosci) / pr_swiatla ** 2) *
             (czasteczka2.wektor_predkosci - self.wektor_predkosci + self.wektor_predkosci * (self.czynnik_lor - 1) *
              ((mp.fdot(self.wektor_predkosci, czasteczka2.wektor_predkosci) / self.predkosc_ms ** 2) - 1))))
        szyb_2_wzgle_1 = (pr_2_wzgl_1[0] ** 2 + pr_2_wzgl_1[1] ** 2 + pr_2_wzgl_1[2] ** 2) ** 0.5
        return pr_2_wzgl_1, szyb_2_wzgle_1

    "Funkcja obliczajaca mase relatywistyczna obiektu"

    def masa_relatywistyczna(self, v):
        m_relat = self.masa_spoczynkowa * ((1 - (v / pr_swiatla) ** 2) ** (-0.5))
        return m_relat


"Komendy odpowiadajace za samo okno programu"
okno = tk.Tk()
okno.geometry('2100x580')
okno.title('Projekt Manhattan')
nazwa = tk.Label(okno, text="Projekt Manhattan")

"tk.LabelFrame(nazwa) tworzy ramkę przypisaną do okna"
"Trzy ramki, pierwsza dla predkosci bez przyspieszenia, druga dla predkosci z przyspieszeniem, trzecia dla wzglednej"
"predkosci"
ramka1 = tk.LabelFrame(okno)

ramka2 = tk.LabelFrame(okno)

ramka3 = tk.LabelFrame(okno)

"Funkcje sluzace do zamiany okienek"

"Funkcja place(x,y) służy do umiejcowienia elementu (ramki, przycisku, etykiety) do okienka/ramki "
" atrybut place_forget() sprawia, ze dany element staje się niewidoczny"


def zmien1():
    ramka2.place_forget()
    ramka3.place_forget()
    ramka1.place(x=0, y=50, width=1500, height=400)


def zmien2():
    ramka1.place_forget()
    ramka3.place_forget()
    ramka2.place(x=0, y=50, width=1500, height=400)


def zmien3():
    ramka1.place_forget()
    ramka2.place_forget()
    ramka3.place(x=0, y=50, width=1500, height=400)


"przyciski odpowiadajace za zmiane okienka. atrubyt place(x,y) umieszcza element w punkcie (x,y), gdzie punkt (0,0)"
"znajduje sie w lewym gornym rogu okna/ramki"
strona1 = tk.Button(okno, text="Ruch jednej czastki bez przyspieszenia", command=zmien1)
strona1.place(x=0, y=0)

strona2 = tk.Button(okno, text="ruch jednej czastki z przyspieszeniem", command=zmien2)
strona2.place(x=500, y=0)

strona3 = tk.Button(okno, text="Ruch wzgledny dwoch czastek", command=zmien3)
strona3.place(x=1000, y=0)

"pola do wpisywania znakow jak i opisy do tych pol. tk.Entry sluzy do stworzenia 'okienka' do wpisywania danych."
"Insert zaś umieszcza dany tekst w okienku tekstowym"
tk.Label(ramka1, text='podaj skladowa x predkosci').grid(row=0, column=0, padx=2, pady=2)
wspx = tk.Entry(ramka1, width=50)
wspx.grid(row=0, column=1)
wspx.insert(0, '0')

tk.Label(ramka1, text='podaj skladowa y predkosci').grid(row=1, column=0, padx=2, pady=2)
wspy = tk.Entry(ramka1, width=50)
wspy.grid(row=1, column=1)
wspy.insert(0, '0')

tk.Label(ramka1, text='podaj skladowa z predkosci').grid(row=2, column=0, padx=2, pady=2)
wspz = tk.Entry(ramka1, width=50)
wspz.grid(row=2, column=1)
wspz.insert(0, '0')

tk.Label(ramka1, text='podaj czas t').grid(row=3, column=0, padx=2, pady=2)
wspt = tk.Entry(ramka1, width=50)
wspt.grid(row=3, column=1)
wspt.insert(0, '0')

tk.Label(ramka1, text='podaj mase').grid(row=4, column=0, padx=2, pady=2)
masa = tk.Entry(ramka1, width=50)
masa.grid(row=4, column=1)
masa.insert(0, '0')

"Funkcja wypisujaca odpowiednie wartosci, po wcisnieciu przycisku. Dla odpowiedniej wartosci wywoluje funkcje dla"
"podanych argumentow i typu danych (m/s czy ul. predkosci swiatla)"


def pisz(wartosc):
    # obsluga wyjatkow. Jezeli wpisana wartosc nie jest liczba, zwraca ValueError, wpisuje
    # w okienku odpowiednie znaki oraz konczy dzialanie programu
    # gdy jest liczba, lecz nie mieszczaca sie w odpowiednim przedziale, zwraca w okienku odpowiednie znaki i konczy
    # dzialanie programu
    try:
        float(wspx.get())
    except ValueError:
        wspx.delete(0, tk.END)
        wspx.insert(0, "to musi byc liczba")
        return
    else:
        if ((float(wspx.get()) >= 1 or float(wspx.get()) < 0) and wartosc == 2) or (
                (float(wspx.get()) >= 299792458 or float(wspx.get()) < 0) and wartosc == 1):
            if wartosc == 2:
                wspx.delete(0, tk.END)
                wspx.insert(0, 'Wartosc musi byc nieujemna i mniejsza niz 1')
            if wartosc == 1:
                wspx.delete(0, tk.END)
                wspx.insert(0, 'Wartosc musi byc nieujemna i mniejsza niz 299792458')
            return

    try:
        float(wspy.get())
    except ValueError:
        wspy.delete(0, tk.END)
        wspy.insert(0, "to musi byc liczba")
        return
    else:
        if ((float(wspy.get()) >= 1 or float(wspy.get()) < 0) and wartosc == 2) or (
                (float(wspy.get()) >= 299792458 or float(wspy.get()) < 0) and wartosc == 1):
            if wartosc == 2:
                wspy.delete(0, tk.END)
                wspy.insert(0, 'Wartosc musi byc nieujemna i mniejsza niz 1')
            if wartosc == 1:
                wspy.delete(0, tk.END)
                wspy.insert(0, 'Wartosc musi byc nieujemna i mniejsza niz 299792458')
            return
    try:
        float(wspz.get())
    except ValueError:
        wspz.delete(0, tk.END)
        wspz.insert(0, "to musi byc liczba")
        return
    else:
        if ((float(wspz.get()) >= 1 or float(wspz.get()) < 0) and wartosc == 2) or (
                (float(wspz.get()) >= 299792458 or float(wspz.get()) < 0) and wartosc == 1):
            if wartosc == 2:
                wspz.delete(0, tk.END)
                wspz.insert(0, 'Wartosc musi byc nieujemna i mniejsza niz 1')
            if wartosc == 1:
                wspz.delete(0, tk.END)
                wspz.insert(0, 'Wartosc musi byc nieujemna i mniejsza niz 299792458')
            return
    try:
        float(wspt.get())
    except ValueError:
        wspt.delete(0, tk.END)
        wspt.insert(0, "to musi byc liczba")
        return
    else:
        if float(wspt.get()) <= 0:
            wspt.delete(0, tk.END)
            wspt.insert(0, "to musi byc liczba dodatnia")
            return

    try:
        float(masa.get())
    except ValueError:
        masa.delete(0, tk.END)
        masa.insert(0, "to musi byc liczba")
        return
    else:
        if float(masa.get()) < 0:
            masa.delete(0, tk.END)
            masa.insert(0, "to musi byc liczba dodatnia")
            return
    '''w zaleznosci od typu danych (m/s czy ulamek predkosci swiatla) program tworzy inne obiekty klasy Czastka.
    Tworzone sa odpowiednie etykiety, ktore mowia o wynikach obliczen'''
    global czasteczka1
    if wartosc == 1:
        czasteczka1 = Czastka(float(wspx.get()), float(wspy.get()), float(wspz.get()), mas_spo=float(masa.get()), typ=1)
    elif wartosc == 2:
        czasteczka1 = Czastka(float(wspx.get()), float(wspy.get()), float(wspz.get()), mas_spo=float(masa.get()), typ=0)
    rel, new = czasteczka1.droga(float(wspt.get()))
    momo1 = tk.Label(ramka1, text='Droga w sensie newtonowskim: ' + str(new), width=150)
    momo1.place(x=300, y=130)
    momo2 = tk.Label(ramka1, text='Droga w sensie relatywistycznym: ' + str(rel), width=150)
    momo2.place(x=300, y=150)
    momo3 = tk.Label(ramka1, width=150)
    "obsluga wyjatkow sluzaca do okreslenia, czy zachodzi dzielenie przez 0"
    try:
        (new - rel) * 100 / new
    except ZeroDivisionError:
        momo3.config(text='zerowa predkosc, brak wzglednej drogi')
    else:
        momo3.config(text='Droga w sensie relatywistycznym jest mniejsza od drogi w sensie newtonowsim o: ' + str(
            (new - rel) * 100 / new) + '%')
    momo3.place(x=300, y=170)


'''tk.Button sluzy do stworzenia przycisku o okreslonej wartosci, szerokosci oraz funkcji.' 
command = lambda: pisz(l.get()) znaczy, ze po wcisnieciu przycisku uruchamia sie funkcja 'pisz'
wraz z argumentem l.get() czyli wartosci zmiennej tk.IntVar, istotnej dla obiektow typu"
radiobutton'''
button1 = tk.Button(ramka1, text='wyswietl wartosci', width=20, command=lambda: pisz(l.get()))
button1.grid(row=7, column=0)

"tworzenie zmiennej tk.IntVar oraz ustawienie jej wartosci na 1"
l = tk.IntVar()
l.set(1)
'''stworzenie obiektu typu RadioButton, ktory zwiazany jest ze zmienna l. Uruchomienie tego obiektu sprawia, ze
zmienna l przyjmuje wartosc rowna zmiennej value w danym obiekcie'''
radio11 = tk.Radiobutton(ramka1, text='metry na sekunde', variable=l, value=1)
radio11.grid(row=0, column=3, padx=2, pady=2)

radio22 = tk.Radiobutton(ramka1, text='ulamek predkosci swiatla', variable=l, value=2)
radio22.grid(row=1, column=3, padx=2, pady=2)
tk.Label(ramka2, text='podaj skladowa x predkosci').grid(row=0, column=0, padx=2, pady=2)
wspx2 = tk.Entry(ramka2, width=50)
wspx2.grid(row=0, column=1)
wspx2.insert(0, '0')

tk.Label(ramka2, text='podaj skladowa y predkosci').grid(row=1, column=0, padx=2, pady=2)
wspy2 = tk.Entry(ramka2, width=50)
wspy2.grid(row=1, column=1)
wspy2.insert(0, '0')

tk.Label(ramka2, text='podaj skladowa z predkosci').grid(row=2, column=0, padx=2, pady=2)
wspz2 = tk.Entry(ramka2, width=50)
wspz2.grid(row=2, column=1)
wspz2.insert(0, '0')

tk.Label(ramka2, text='podaj przyspieszenie w tym kierunku').grid(row=3, column=0, padx=2, pady=2)
wspxp = tk.Entry(ramka2, width=50)
wspxp.grid(row=3, column=1)
wspxp.insert(0, '0')

tk.Label(ramka2, text='podaj czas t').grid(row=6, column=0, padx=2, pady=2)
wspt2 = tk.Entry(ramka2, width=50)
wspt2.grid(row=6, column=1)
wspt2.insert(0, '0')

tk.Label(ramka2, text='podaj mase m').grid(row=7, column=0, padx=2, pady=2)
masa2 = tk.Entry(ramka2, width=50)
masa2.grid(row=7, column=1)
masa2.insert(0, '0')

"funkcja dzialajaca jak funkcja 'pisz'"


def pisz2(wartosc, typ):
    global czasteczka10
    try:
        float(wspx2.get())
    except ValueError:
        wspx2.delete(0, tk.END)
        wspx2.insert(0, "to musi byc liczba")
        return
    else:
        if ((float(wspx2.get()) >= 1 or float(wspx2.get()) < 0) and typ == 2) or (
                (float(wspx2.get()) >= 299792458 or float(wspx2.get()) < 0) and typ == 1):
            if typ == 2:
                wspx2.delete(0, tk.END)
                wspx2.insert(0, 'Wartosc musi byc nieujemna i mniejsza niz 1')
            if typ == 1:
                wspx2.delete(0, tk.END)
                wspx2.insert(0, 'Wartosc musi byc nieujemna i mniejsza niz 299792458')
            return
    try:
        float(wspy2.get())
    except ValueError:
        wspy2.delete(0, tk.END)
        wspy2.insert(0, "to musi byc liczba")
        return
    else:
        if ((float(wspy2.get()) >= 1 or float(wspy2.get()) < 0) and typ == 2) or (
                (float(wspy2.get()) >= 299792458 or float(wspy2.get()) < 0) and typ == 1):
            if typ == 2:
                wspy2.delete(0, tk.END)
                wspy2.insert(0, 'Wartosc musi byc nieujemna i mniejsza niz 1')
            if typ == 1:
                wspy2.delete(0, tk.END)
                wspy2.insert(0, 'Wartosc musi byc nieujemna i mniejsza niz 299792458')
            return
    try:
        float(wspz2.get())
    except ValueError:
        wspz2.delete(0, tk.END)
        wspz2.insert(0, "to musi byc liczba")
        return
    else:
        if ((float(wspz2.get()) >= 1 or float(wspz2.get()) < 0) and typ == 2) or (
                (float(wspz2.get()) >= 299792458 or float(wspz2.get()) < 0) and typ == 1):
            if typ == 2:
                wspz2.delete(0, tk.END)
                wspz2.insert(0, 'Wartosc musi byc nieujemna i mniejsza niz 1')
            if typ == 1:
                wspz2.delete(0, tk.END)
                wspz2.insert(0, 'Wartosc musi byc nieujemna i mniejsza niz 299792458')
            return
    try:
        float(wspxp.get())
    except ValueError:
        wspxp.delete(0, tk.END)
        wspxp.insert(0, "to musi byc liczba")
        return
    else:
        if float(wspxp.get()) <= 0 and wartosc == 1:
            wspxp.delete(0, tk.END)
            wspxp.insert(0, "to musi byc liczba dodatnia")
            return
    try:
        float(wspt2.get())
    except ValueError:
        wspt2.delete(0, tk.END)
        wspt2.insert(0, "to musi byc liczba")
        return
    else:
        if float(wspt2.get()) <= 0:
            wspt2.delete(0, tk.END)
            wspt2.insert(0, "to musi byc liczba dodatnia")
            return

    try:
        float(masa2.get())
    except ValueError:
        masa2.delete(0, tk.END)
        masa2.insert(0, "to musi byc liczba")
        return
    else:
        if float(masa2.get()) < 0:
            masa2.delete(0, tk.END)
            masa2.insert(0, "to musi byc liczba dodatnia")
            return

    try:
        float(wspxp2.get())
    except ValueError:
        wspxp2.delete(0, tk.END)
        wspxp2.insert(0, "to musi byc liczba")
        return
    else:
        if float(wspxp2.get()) < 0:
            wspxp2.delete(0, tk.END)
            wspxp2.insert(0, "to musi byc liczba nieujemna")
            return
    try:
        float(wspyp2.get())
    except ValueError:
        wspyp2.delete(0, tk.END)
        wspyp2.insert(0, "to musi byc liczba")
        return
    else:
        if float(wspyp2.get()) < 0:
            wspyp2.delete(0, tk.END)
            wspyp2.insert(0, "to musi byc liczba nieujemna")
            return

    try:
        float(wspzp2.get())
    except ValueError:
        wspzp2.delete(0, tk.END)
        wspzp2.insert(0, "to musi byc liczba")
        return
    else:
        if float(wspzp2.get()) < 0:
            wspzp2.delete(0, tk.END)
            wspzp2.insert(0, "to musi byc liczba nieujemna")
            return
    if typ == 1:
        if wartosc == 1:
            czasteczka10 = Czastka(float(wspx2.get()), float(wspy2.get()), float(wspz2.get()), float(wspxp.get()),
                                   mas_spo=float(masa2.get()), typ=1)
        elif wartosc == 2:
            czasteczka10 = Czastka(przysp_x=float(wspxp2.get()), przysp_y=float(wspyp2.get()),
                                   przysp_z=float(wspzp2.get()),
                                   mas_spo=float(masa2.get()),
                                   typ=1)
    elif typ == 2:
        if wartosc == 1:
            czasteczka10 = Czastka(float(wspx2.get()), float(wspy2.get()), float(wspz2.get()), float(wspxp.get()),
                                   mas_spo=float(masa2.get()), typ=0)
        elif wartosc == 2:
            czasteczka10 = Czastka(przysp_x=float(wspxp2.get()), przysp_y=float(wspyp2.get()),
                                   przysp_z=float(wspzp2.get()),
                                   mas_spo=float(masa2.get()),
                                   typ=0)

    rel, new = czasteczka10.droga(float(wspt2.get()))
    momo1 = tk.Label(ramka2, text='Droga w sensie newtonowskim: ' + str(new), width=150)
    momo1.place(x=300, y=200)

    momo2 = tk.Label(ramka2, text='Droga w sensie relatywistycznym: ' + str(rel), width=150)
    momo2.place(x=300, y=220)

    momo3 = tk.Label(ramka2, width=150)

    try:
        (new - rel) * 100 / new
    except ZeroDivisionError:
        momo3.config(text='Zerowa droga, brak wzglednej drogi')
    else:
        momo3.config(text='Droga w sensie relatywistycznym jest mniejsza od drogi w sensie newtonowsim o: ' + str(
            (new - rel) * 100 / new) + '%')
    momo3.place(x=300, y=240)

    momo4 = tk.Label(ramka2, text='masa relatywistyczna: ' + str(
        czasteczka10.masa_relatywistyczna(
            czasteczka10.predkosc_przyspieszanego_obiektu(float(wspt2.get())))), width=150)
    momo4.place(x=300, y=260)
    "wlacza odpowiednie przycisku, aby mozna bylo ich uzywac"
    button_wykres1.config(state='normal')
    button_wykres2.config(state='normal')
    button_wykres3.config(state='normal')
    button_wykres4.config(state='normal')


button2 = tk.Button(ramka2, text='wyswietl wartosci', width=20, command=lambda: pisz2(r.get(), l2.get()))
button2.grid(row=8, column=0)

"funkcje, ktore sluza do tworzenia wykresow"


def wykres_new_rel():
    x = np.linspace(0, float(wspt2.get()), 1000)
    y = czasteczka10.droga(x)[0]
    w = czasteczka10.droga(x)[1]
    plt.plot(x, y, color='g', label='droga rel.')
    plt.plot(x, w, color='r', label='droga new.')
    plt.legend(('droga rel.', 'droga new'), loc='upper center', shadow=True)
    plt.xlabel('czas')
    plt.ylabel('droga')
    plt.show()


def wykres_new_as():
    x = np.linspace(0, float(wspt2.get()), 1000)
    y = czasteczka10.droga(x)[0]
    z = pr_swiatla * x - pr_swiatla ** 2 / czasteczka10.przyspieszenie_ms
    plt.plot(x, y, color='g', label='droga rel.')
    plt.plot(x, z, color='r', label='droga new.')
    plt.legend(('droga rel.', 'asymptota'), loc='upper center', shadow=True)
    plt.xlabel('czas')
    plt.ylabel('droga')
    plt.show()


def wykres_trzy():
    x = np.linspace(0, float(wspt2.get()), 1000)
    y = czasteczka10.droga(x)[0]
    w = czasteczka10.droga(x)[1]
    z = pr_swiatla * x - pr_swiatla ** 2 / czasteczka10.przyspieszenie_ms
    plt.plot(x, y, color='g', label='droga rel.')
    plt.plot(x, z, color='r', label='droga new.')
    plt.plot(x, w, color='b', label='droga new.')
    plt.legend(('droga rel.', 'asymptota', 'droga new.'), loc='upper center', shadow=True)
    plt.xlabel('czas')
    plt.ylabel('droga')
    plt.show()


def wykres_masa_pred():
    x = np.linspace(0, float(wspt2.get()), 1000)
    n = czasteczka10.predkosc_przyspieszanego_obiektu(x)
    m = czasteczka10.masa_relatywistyczna(n)
    plt.plot(n, m, color='g', label='masa od predkosci')
    plt.legend('masa od predkosci',
               loc='upper center', shadow=True)
    plt.xlabel('predkosc')
    plt.ylabel('masa')
    plt.show()


"przyciski dla wykresow"
button_wykres1 = tk.Button(ramka2, text="narysuj wykresy drogi relatywistycznej i newtonowskiej",
                           command=wykres_new_rel)
button_wykres1.grid(row=9, column=0)
button_wykres1.config(state='disabled')

button_wykres2 = tk.Button(ramka2, text="narysuj wykresy drogi relatywistycznej i asymptoty",
                           command=wykres_new_as)
button_wykres2.grid(row=10, column=0)
button_wykres2.config(state='disabled')

button_wykres3 = tk.Button(ramka2, text="narysuj wszystkie 3 wykresy",
                           command=wykres_trzy)
button_wykres3.grid(row=11, column=0)
button_wykres3.config(state='disabled')

button_wykres4 = tk.Button(ramka2, text="narysuj wykres masy od predkosci",
                           command=wykres_masa_pred)
button_wykres4.grid(row=12, column=0)
button_wykres4.config(state='disabled')

tk.Label(ramka2, text='podaj skladowa x przyspieszenia').grid(row=0, column=3, padx=2, pady=2)
wspxp2 = tk.Entry(ramka2)
wspxp2.grid(row=0, column=4)
wspxp2.insert(0, '0')

tk.Label(ramka2, text='podaj skladowa y przyspieszenia').grid(row=1, column=3, padx=2, pady=2)
wspyp2 = tk.Entry(ramka2)
wspyp2.grid(row=1, column=4)
wspyp2.insert(0, '0')

tk.Label(ramka2, text='podaj skladowa z przyspieszenia').grid(row=2, column=3, padx=2, pady=2)
wspzp2 = tk.Entry(ramka2)
wspzp2.grid(row=2, column=4)
wspzp2.insert(0, '0')
"wylaczenie odpowiednich pol do wpisywania wartosci"
wspx2.config(state='disabled')
wspy2.config(state='disabled')
wspz2.config(state='disabled')
wspxp.config(state='disabled')
wspt2.config(state='disabled')
wspxp.config(state='disabled')
wspxp2.config(state='disabled')
wspyp2.config(state='disabled')
wspzp2.config(state='disabled')
masa2.config(state='disabled')

"funkcja, ktora wlacza odpowiednie pola do wpisywania, zostawiajac wylaczone te zbedne"


def zerowa_niezerowa(wartosc):
    if wartosc == 1:
        wspx2.config(state='normal')
        wspy2.config(state='normal')
        wspz2.config(state='normal')
        wspxp.config(state='normal')
        wspt2.config(state='normal')
        masa2.config(state='normal')
        wspxp2.config(state='disabled')
        wspyp2.config(state='disabled')
        wspzp2.config(state='disabled')

    elif wartosc == 2:
        wspx2.config(state='disabled')
        wspy2.config(state='disabled')
        wspz2.config(state='disabled')
        wspxp.config(state='disabled')
        wspt2.config(state='normal')
        masa2.config(state='normal')
        wspxp2.config(state='normal')
        wspyp2.config(state='normal')
        wspzp2.config(state='normal')


r = tk.IntVar(0)
r.set(0)

l2 = tk.IntVar()
l2.set(1)

radio1 = tk.Radiobutton(ramka2, text='niezerowa predkosc poczatkowa', variable=r, value=1,
                        command=lambda: zerowa_niezerowa(r.get()))
radio1.grid(row=0, column=2, padx=2, pady=2)

radio2 = tk.Radiobutton(ramka2, text='zerowa predkosc poczatkowa', variable=r, value=2,
                        command=lambda: zerowa_niezerowa(r.get()))
radio2.grid(row=1, column=2, padx=2, pady=2)

radio3 = tk.Radiobutton(ramka2, text='metry na sekunde', variable=l2, value=1)
radio3.grid(row=3, column=2, padx=2, pady=2)

radio4 = tk.Radiobutton(ramka2, text='ulamek predkosci swiatla', variable=l2, value=2)
radio4.grid(row=4, column=2, padx=2, pady=2)

tk.Label(ramka3, text='podaj skladowa x predkosci czastki pierwszej').grid(row=0, column=0, padx=2, pady=2)
vx1 = tk.Entry(ramka3)
vx1.grid(row=0, column=1)
vx1.insert(0, '0')

tk.Label(ramka3, text='podaj skladowa y predkosci czastki pierwszej').grid(row=1, column=0, padx=2, pady=2)
vy1 = tk.Entry(ramka3)
vy1.grid(row=1, column=1)
vy1.insert(0, '0')

tk.Label(ramka3, text='podaj skladowa z predkosci czastki pierwszej').grid(row=2, column=0, padx=2, pady=2)
vz1 = tk.Entry(ramka3)
vz1.grid(row=2, column=1)
vz1.insert(0, '0')

tk.Label(ramka3, text='podaj mase czastki pierwszej').grid(row=3, column=0, padx=2, pady=2)
masacz1 = tk.Entry(ramka3)
masacz1.grid(row=3, column=1)
masacz1.insert(0, '0')

tk.Label(ramka3, text='podaj skladowa x predkosci czastki drugiej').grid(row=0, column=2, padx=5, pady=2)
vx2 = tk.Entry(ramka3)
vx2.grid(row=0, column=4)
vx2.insert(0, '0')

tk.Label(ramka3, text='podaj skladowa y predkosci czastki drugiej').grid(row=1, column=2, padx=5, pady=2)
vy2 = tk.Entry(ramka3)
vy2.grid(row=1, column=4)
vy2.insert(0, '0')

tk.Label(ramka3, text='podaj skladowa z predkosci czastki drugiej').grid(row=2, column=2, padx=5, pady=2)
vz2 = tk.Entry(ramka3)
vz2.grid(row=2, column=4)
vz2.insert(0, '0')

tk.Label(ramka3, text='podaj mase czastki drugiej').grid(row=3, column=2, padx=2, pady=2)
masacz2 = tk.Entry(ramka3)
masacz2.grid(row=3, column=4)
masacz2.insert(0, '0')

"funkcja dzialajaca podobnie jak 'pisz' oraz 'pisz2"


def pisz3(typ):
    global czasteczka20, czasteczka30
    try:
        float(vx1.get())
    except ValueError:
        vx1.delete(0, tk.END)
        vx1.insert(0, "to musi byc liczba")
        return
    else:
        if ((float(vx1.get()) >= 1 or float(vx1.get()) < 0) and typ == 2) or (
                (float(vx1.get()) >= 299792458 or float(vx1.get()) < 0) and typ == 1):
            if typ == 2:
                vx1.delete(0, tk.END)
                vx1.insert(0, 'Wartosc musi byc nieujemna i mniejsza niz 1')
            if typ == 1:
                vx1.delete(0, tk.END)
                vx1.insert(0, 'Wartosc musi byc nieujemna i mniejsza niz 299792458')
            return

    try:
        float(vy1.get())
    except ValueError:
        vy1.delete(0, tk.END)
        vy1.insert(0, "to musi byc liczba")
        return
    else:
        if ((float(vy1.get()) >= 1 or float(vy1.get()) < 0) and typ == 2) or (
                (float(vy1.get()) >= 299792458 or float(vy1.get()) < 0) and typ == 1):
            if typ == 2:
                vy1.delete(0, tk.END)
                vy1.insert(0, 'Wartosc musi byc nieujemna i mniejsza niz 1')
            if typ == 1:
                vy1.delete(0, tk.END)
                vy1.insert(0, 'Wartosc musi byc nieujemna i mniejsza niz 299792458')
            return

    try:
        float(vz1.get())
    except ValueError:
        vz1.delete(0, tk.END)
        vz1.insert(0, "to musi byc liczba")
        return
    else:
        if ((float(vz1.get()) >= 1 or float(vz1.get()) < 0) and typ == 2) or (
                (float(vz1.get()) >= 299792458 or float(vz1.get()) < 0) and typ == 1):
            if typ == 2:
                vz1.delete(0, tk.END)
                vz1.insert(0, 'Wartosc musi byc nieujemna i mniejsza niz 1')
            if typ == 1:
                vz1.delete(0, tk.END)
                vz1.insert(0, 'Wartosc musi byc nieujemna i mniejsza niz 299792458')
            return

    try:
        float(vx2.get())
    except ValueError:
        vx2.delete(0, tk.END)
        vx2.insert(0, "to musi byc liczba")
        return
    else:
        if ((float(vx2.get()) >= 1 or float(vx2.get()) < 0) and typ == 2) or (
                (float(vx2.get()) >= 299792458 or float(vx2.get()) < 0) and typ == 1):
            if typ == 2:
                vx2.delete(0, tk.END)
                vx2.insert(0, 'Wartosc musi byc nieujemna i mniejsza niz 1')
            if typ == 1:
                vx2.delete(0, tk.END)
                vx2.insert(0, 'Wartosc musi byc nieujemna i mniejsza niz 299792458')
            return

    try:
        float(vy2.get())
    except ValueError:
        vy2.delete(0, tk.END)
        vy2.insert(0, "to musi byc liczba")
        return
    else:
        if ((float(vy2.get()) >= 1 or float(vy2.get()) < 0) and typ == 2) or (
                (float(vy2.get()) >= 299792458 or float(vy2.get()) < 0) and typ == 1):
            if typ == 2:
                vy2.delete(0, tk.END)
                vy2.insert(0, 'Wartosc musi byc nieujemna i mniejsza niz 1')
            if typ == 1:
                vy2.delete(0, tk.END)
                vy2.insert(0, 'Wartosc musi byc nieujemna i mniejsza niz 299792458')
            return

    try:
        float(vz2.get())
    except ValueError:
        vz2.delete(0, tk.END)
        vz2.insert(0, "to musi byc liczba")
        return
    else:
        if ((float(vz2.get()) >= 1 or float(vz2.get()) < 0) and typ == 2) or (
                (float(vz2.get()) >= 299792458 or float(vz2.get()) < 0) and typ == 1):
            if typ == 2:
                vz2.delete(0, tk.END)
                vz2.insert(0, 'Wartosc musi byc nieujemna i mniejsza niz 1')
            if typ == 1:
                vz2.delete(0, tk.END)
                vz2.insert(0, 'Wartosc musi byc nieujemna i mniejsza niz 299792458')
            return

    try:
        float(masacz1.get())
    except ValueError:
        masacz1.delete(0, tk.END)
        masacz1.insert(0, "to musi byc liczba")
        return
    else:
        if float(masa2.get()) < 0:
            masacz1.delete(0, tk.END)
            masacz1.insert(0, "to musi byc liczba dodatnia")
            return

    try:
        float(masacz2.get())
    except ValueError:
        masacz2.delete(0, tk.END)
        masacz2.insert(0, "to musi byc liczba")
        return
    else:
        if float(masacz2.get()) < 0:
            masacz2.delete(0, tk.END)
            masacz2.insert(0, "to musi byc liczba dodatnia")
            return
    if typ == 1:
        czasteczka20 = Czastka(typ=1, pr_x=float(vx1.get()), pr_y=float(vy1.get()), pr_z=float(vz1.get()),
                               mas_spo=float(masacz1.get()))
        czasteczka30 = Czastka(typ=1, pr_x=float(vx2.get()), pr_y=float(vy2.get()), pr_z=float(vz2.get()),
                               mas_spo=float(masacz2.get()))
    elif typ == 2:
        czasteczka20 = Czastka(typ=0, pr_x=float(vx1.get()), pr_y=float(vy1.get()), pr_z=float(vz1.get()),
                               mas_spo=float(masacz1.get()))
        czasteczka30 = Czastka(typ=0, pr_x=float(vx2.get()), pr_y=float(vy2.get()), pr_z=float(vz2.get()),
                               mas_spo=float(masacz2.get()))
    momo1 = tk.Label(ramka3, width=200)
    try:
        wzgl_predkosc, wzgl_szybkosc = czasteczka20.wzgledna_predkosc(czasteczka30)
        czasteczka30.wzgledna_predkosc(czasteczka20)
    except ZeroDivisionError:
        momo1.config(text='zerowa predkosc ktorejs czastki (dzielenie przez 0)')
        momo1.place(x=100, y=200)
        return
    momo1.config(text='predkosc czastki 2 wzgledem czastki 1 wynosi: [' + str(wzgl_predkosc[0]) + ', ' + str(
        wzgl_predkosc[1]) + ', ' + str(wzgl_predkosc[2]) + ']')
    momo1.place(x=100, y=200)
    momo2 = tk.Label(ramka3, text='szybkosc czastki 2 wzgledem czastki 1 wynosi: ' + str(wzgl_szybkosc))
    momo2.place(x=300, y=220)

    momo3 = tk.Label(ramka3, text="masa czastki 1 wzgledem czastki 2 wynosi: " + str(
        czasteczka20.masa_relatywistyczna(czasteczka30.wzgledna_predkosc(czasteczka20)[1])))
    momo3.place(x=300, y=240)
    momo4 = tk.Label(ramka3, text="masa czastki 2 wzgledem czastki 1 wynosi: " + str(czasteczka30.masa_relatywistyczna(
        czasteczka20.wzgledna_predkosc(czasteczka30)[1])))
    momo4.place(x=300, y=260)


l3 = tk.IntVar()
l3.set(1)

button_pre_wzgl = tk.Button(ramka3, text='wyswietl wartosci', width=20, command=lambda: pisz3(l2.get()))
button_pre_wzgl.grid(row=4, column=0)

radio31 = tk.Radiobutton(ramka3, text='metry na sekunde', variable=l3, value=1)
radio31.grid(row=0, column=5, padx=2, pady=2)

radio32 = tk.Radiobutton(ramka3, text='ulamek predkosci swiatla', variable=l3, value=2)
radio32.grid(row=1, column=5, padx=2, pady=2)
"okno.mainloop() sluzy do tego, aby okno bylo uruchomione do momentu, gdy zostanie wylaczone przez uzytkownika"
okno.mainloop()
