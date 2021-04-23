import time
import copy

ADANCIME_MAX = 4
TIP_ESTIMARE = 1

'''
Jucatorul B -> Blue -> muta al doilea, are de la stanga la dreapta de facut
Jucatorul R -> Red -> muta primul, are de sus in jos  

Pentru joc : pozitia de 0 0 est in coltul stanga sus 

'''
class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_COLOANE = 5
    NR_LINII = 5
    JMIN = None
    JMAX = None
    GOL = '#'

    # intiializez tabla de joc
    def __init__(self, tabla=None, nrLinii = None, nrColoane = None):  # Joc()
        if nrLinii is not None and nrColoane is not None:
            self.NR_COLOANE = nrColoane
            self.NR_LINII = nrLinii

        self.matr = tabla or [Joc.GOL] * self.NR_LINII * self.NR_COLOANE

    #ca sa convertesc de la x y la coordonata liniara
    @classmethod
    def obtine_pozitie(cls, lin, col):
        if lin < 0 or lin >= cls.NR_LINII or col < 0 or col >= cls.NR_COLOANE:
            return None
        return lin * cls.NR_COLOANE + col

    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    def final(self):
        # mai intai fac pentru jucatoru rosu, trebuie sa fie de sus in jos
        dp = [0] * self.NR_LINII * self.NR_COLOANE
        #initializez
        for col in range(self.NR_COLOANE):
            poz = self.obtine_pozitie(0, col)
            #daca e rosu e ok
            if self.matr[poz] == 'R':
                dp[poz] = 1
        #calculez dp-ul
        for lin in range(1, self.NR_LINII):
            for col in range(self.NR_COLOANE - 1):
                poz = self.obtine_pozitie(lin, col)
                if self.matr[poz] == 'R':
                    dp[poz] = max(dp[self.obtine_pozitie(lin - 1, col)], dp[self.obtine_pozitie(lin - 1, col + 1)])

            #asta poate sa fie prelungit doar de la cel de sus
            if self.matr[self.obtine_pozitie(lin, self.NR_COLOANE - 1)] == 'R':
                dp[self.obtine_pozitie(lin, self.NR_COLOANE - 1)] = dp[self.obtine_pozitie(lin - 1, self.NR_COLOANE - 1)]

        #vad daca a castigat rosul
        for col in range(self.NR_COLOANE):
            if dp[self.obtine_pozitie(self.NR_LINII - 1, col)] == 1:
                return 'R'

        #trebuie sa fac in mare aceleasi verificari si pentru albastru
        dp = [0] * self.NR_LINII * self.NR_COLOANE
        for lin in range(self.NR_LINII):
            poz = self.obtine_pozitie(lin, 0)
            #daca e albastru, e ok
            if self.matr[poz] == "B":
                dp[poz] = 1
        #calculez dp- ul
        for col in range(1, self.NR_COLOANE):
            for lin in range(self.NR_LINII - 1):
                if self.matr[self.obtine_pozitie(lin, col)] == 'B':
                    dp[self.obtine_pozitie(lin, col)] = max(dp[self.obtine_pozitie(lin, col - 1)], dp[self.obtine_pozitie(lin + 1, col - 1)])

            if self.matr[self.obtine_pozitie(self.NR_LINII - 1, col)] == 'B':
                dp[self.obtine_pozitie(self.NR_LINII - 1, col)] = dp[self.obtine_pozitie(self.NR_LINII - 1, col - 1)]

        #vad daca a castigat albastrul
        for lin in range(self.NR_LINII):
            if dp[self.obtine_pozitie(lin, self.NR_COLOANE - 1)] == 1:
                return "B"

        #de verificat si remiza
        for lin in range(self.NR_LINII):
            for col in range(self.NR_COLOANE):
                if self.matr[self.obtine_pozitie(lin, col)] == Joc.GOL:
                    return False

        return "remiza"


    def mutari(self, jucator):  # jucator = simbolul jucatorului care muta
        l_mutari = []
        for i in range(len(self.matr)):
            if self.matr[i] == Joc.GOL:
                copie_matr = copy.deepcopy(self.matr)
                copie_matr[i] = jucator
                l_mutari.append(Joc(copie_matr))
        return l_mutari

    #imi returneaza in cate mutari castig in mod optim
    def cate_mutari(self, jucator):
        if jucator == 'B':
            #stanga dreapta
            dp = [float("inf")] * (self.NR_LINII * self.NR_COLOANE + 1)
            #initial, pentru prima coloana
            for lin in range(self.NR_LINII):
                col = 0
                poz = self.obtine_pozitie(lin, col)
                if self.matr[poz] == 'B':
                    dp[poz] = 0
                elif self.matr[poz] == 'R':
                    dp[poz] = float("inf")
                else:
                    dp[poz] = 1
            for col in range(1, self.NR_COLOANE):
                lin = 0
                poz = self.obtine_pozitie(lin, col)
                if self.matr[poz] == 'R':
                    dp[poz] = float('inf')
                else:
                    dp[poz] = min(dp[self.obtine_pozitie(lin, col - 1)], dp[self.obtine_pozitie(lin + 1, col - 1)])
                    if self.matr[poz] != 'B':
                        dp[poz] += 1
                for lin in range(1, self.NR_LINII - 1):
                    poz = self.obtine_pozitie(lin, col)
                    if self.matr[poz] == 'R':
                        dp[poz] = float('inf')
                    else:
                        dp[poz] = min(dp[self.obtine_pozitie(lin - 1, col)], dp[self.obtine_pozitie(lin, col -1)],
                                      dp[self.obtine_pozitie(lin + 1, col)])
                        if self.matr[poz] != 'B':
                            dp[poz] += 1
                lin = self.NR_LINII - 1
                poz = self.obtine_pozitie(lin, col)
                if self.matr[poz] == 'R':
                    dp[poz] = float('inf')
                else:
                    dp[poz] = min(dp[self.obtine_pozitie(lin-1, col)], dp[self.obtine_pozitie(lin, col -1)])
            ans = float('inf')
            for lin in range(self.NR_LINII):
                col = self.NR_COLOANE - 1
                ans = min(ans, dp[self.obtine_pozitie(lin, col)])
            return ans
        #pentru Red
        else:
            dp = [float("inf")] * (self.NR_LINII * self.NR_COLOANE + 1)
            for col in range(self.NR_COLOANE):
                lin = 0
                poz = self.obtine_pozitie(lin, col)
                if self.matr[poz] == 'R':
                    dp[poz] = 0
                elif self.matr[poz] =='B':
                    dp[poz] = float('inf')
                else:
                    dp[poz] = 1
            for lin in range(1, self.NR_LINII):
                for col in range(self.NR_COLOANE - 1):
                    poz = self.obtine_pozitie(lin, col)
                    if self.matr[poz] == 'B':
                        dp[poz] = 'inf'
                    else:
                        dp[poz] = min(dp[self.obtine_pozitie(lin - 1, col)], dp[self.obtine_pozitie(lin, col + 1)])
                        if self.matr[poz] != 'R':
                            dp[poz] += 1
                col = self.NR_COLOANE - 1
                poz = self.obtine_pozitie(lin, col)
                if self.matr[poz] == 'B':
                    dp[poz] = float('inf')
                else:
                    dp[poz] = dp[self.obtine_pozitie(lin -1, col)]
                    if self.poz != 'R':
                        dp[poz] += 1
            ans = float('inf')
            for col in range(self.NR_COLOANE):
                lin = self.NR_LINII - 1
                poz = self.obtine_pozitie(lin, col)
                ans = min(ans, dp[poz])
            return ans



    #calculez pe cate drumuri mai poate castiga un jucator
    def cate_drumuri(self, jucator):
        #trebuie facuta sperata pentru fiecare tip de jucator
        if jucator == 'B':
            #stanga dreapta
            #dinamica care ne ajuta sa obtinem acest numar de drumuri.
            #calculez mai intai dp-ul de pe prima coloana
            dp = [0]  * (self.NR_COLOANE * self.NR_LINII  + 1)
            for lin in range (self.NR_LINII):
                col = 0
                poz = self.obtine_pozitie(lin, col)
                if self.matr[poz] != 'R':
                    dp[poz] = 1
                else:
                    dp[poz] = 0
            #calculez restul de dp-uri
            for col in range (1, self.NR_COLOANE):
                lin = 0
                poz = self.obtine_pozitie(lin, col)
                if self.matr != 'R':
                    dp[poz] = dp[self.obtine_pozitie(lin + 1, col - 1)] + dp[self.obtine_pozitie(lin, col - 1)]
                else:
                    dp[poz] = 0
                for lin in range(1, self.NR_LINII - 1):
                    poz = self.obtine_pozitie(lin, col)
                if self.matr != 'R':
                    dp[poz] = dp[self.obtine_pozitie(lin + 1, col - 1)] + dp[self.obtine_pozitie(lin, col - 1)] + \
                                dp[self.obtine_pozitie(lin - 1, col)]
                else:
                    dp[poz] = 0
            lin = self.NR_LINII - 1
            poz = self.obtine_pozitie(lin, col)

            if self.matr[poz] != 'R':
                dp[poz] = dp[self.obtine_pozitie(lin - 1, col)] + dp[self.obtine_pozitie(lin, col - 1)]
            ans = 0
            #calculez suma posibilitatiilor
            for lin in range(self.NR_LINII):
                ans += dp[self.obtine_pozitie(lin, self.NR_COLOANE - 1)]
            return ans
        #suntem cu rosu
        else:
            dp = [0] * (self.NR_COLOANE * self.NR_LINII + 1)
            #intializam
            for col in range (self.NR_COLOANE):
                lin = 0
                poz = self.obtine_pozitie(lin, col)
                if self.matr[poz] != 'B':
                    dp[poz] = 1
            #calculam pentru toata matricea
            for lin in range(1, self.NR_LINII):
                for col in range(self.NR_COLOANE - 1):
                    poz = self.obtine_pozitie(lin ,col)
                    if self.matr[poz] != 'B':
                        dp[poz] = dp[self.obtine_pozitie(lin, col)] + dp[self.obtine_pozitie(lin ,col + 1)]
                    else:
                        dp[poz] = 0
                col = self.NR_COLOANE - 1
                poz = self.obtine_pozitie(lin, col)

                if self.matr[poz] != 'B':
                    dp[poz] = dp[self.obtine_pozitie(lin - 1, col)]
            #calculam raspunsul
            ans = 0
            for col in range(self.NR_COLOANE):
                lin = self.NR_LINII - 1
                poz = self.obtine_pozitie(lin, col)
                ans += dp[poz]
            return ans

    # primul sau al doilea tip de estimare
    def estimeaza_scor(self, adancime, tip = 1):
        t_final = self.final()
        # if (adancime==0):
        if t_final == self.__class__.JMAX:  # self.__class__ referinta catre clasa instantei
            return (9999 + adancime)
        elif t_final == self.__class__.JMIN:
            return (-9999 - adancime)
        elif t_final == 'remiza':
            return 0
        else:
            if tip == 1:
                #primul tip de estimare
                return (self.cate_drumuri(self.__class__.JMAX) - self.cate_drumuri(self.__class__.JMIN))
            else:
                return (self.cate_mutari(self.__class__.JMIN) - self.cate_mutari(self.__class__.JMAX))


    def sirAfisare(self):
        sir = "  |"
        sir += " ".join([str(i) for i in range(self.NR_COLOANE)]) + "\n"
        sir += "-" * (self.NR_COLOANE + 1) * 2 + "\n"
        for i in range(self.NR_LINII):  # itereaza prin linii
            sir += str(i) + " |" + " ".join(
                [str(x) for x in self.matr[self.NR_COLOANE * i: self.NR_COLOANE * (i + 1)]]) + "\n"
        # [0,1,2,3,4,5,6,7,8]
        return sir

    def __str__(self):
        return self.sirAfisare()

    def __repr__(self):
        return self.sirAfisare()


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    O instanta din clasa stare este un nod din arborele minimax
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
    """

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.estimare = estimare

        # lista de mutari posibile (tot de tip Stare) din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        # e de tip Stare (cel mai bun succesor)
        self.stare_aleasa = None

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)  # lista de informatii din nodurile succesoare
        juc_opus = Joc.jucator_opus(self.j_curent)

        # mai jos calculam lista de noduri-fii (succesori)
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")\n"
        return sir


""" Algoritmul MinMax """


def min_max(stare):
    # daca sunt la o frunza in arborele minimax sau la o stare finala
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime, TIP_ESTIMARE)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariCuEstimare = [min_max(x) for x in
                        stare.mutari_posibile]  # expandez(constr subarb) fiecare nod x din mutari posibile

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)  # def f(x): return x.estimare -----> key=f
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)

    stare.estimare = stare.stare_aleasa.estimare
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime, TIP_ESTIMARE)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        estimare_curenta = float('-inf')  # in aceasta variabila calculam maximul

        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta(alpha, beta, mutare)  # aici construim subarborele pentru stare_noua

            if (estimare_curenta < stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if (alpha < stare_noua.estimare):
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        estimare_curenta = float('inf')
        # completati cu rationament similar pe cazul stare.j_curent==Joc.JMAX
        for mutare in stare.mutari_posibile:
            # calculeaza estimarea
            stare_noua = alpha_beta(alpha, beta, mutare)  # aici construim subarborele pentru stare_noua

            if (estimare_curenta > stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if (beta > stare_noua.estimare):
                beta = stare_noua.estimare
                if alpha >= beta:
                    break

    stare.estimare = stare.stare_aleasa.estimare

    return stare


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()  # metoda final() returneaza "remiza" sau castigatorul ("x" sau "0") sau False daca nu e stare finala
    if (final):
        if (final == "remiza"):
            print("Remiza!")
        else:
            print("A castigat " + final)

        return True

    return False


def main():
    # initializare algoritm
    raspuns_valid = False

    # TO DO 1
    while not raspuns_valid:
        tip_algoritm = input("Algoritmul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")
    # initializare jucatori
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = input("Doriti sa jucati cu R sau cu B? ").upper()
        if (Joc.JMIN in ['R', 'B']):
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie R sau B.")
    Joc.JMAX = 'B' if Joc.JMIN == 'R' else 'R'

    # initializare tabla
    tabla_curenta = Joc();  # apelam constructorul
    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, 'R', ADANCIME_MAX)

    while True:
        if (stare_curenta.j_curent == Joc.JMIN):
            # muta jucatorul utilizator

            print("Acum muta utilizatorul cu simbolul", stare_curenta.j_curent)
            raspuns_valid = False
            while not raspuns_valid:
                try:
                    linie = int(input("linie="))
                    coloana = int(input("coloana="))

                    if (linie in range(Joc.NR_LINII) and coloana in range(Joc.NR_COLOANE)):
                        if stare_curenta.tabla_joc.matr[Joc.obtine_pozitie(linie, coloana)] == Joc.GOL:
                            raspuns_valid = True
                        else:
                            print("Exista deja un simbol in pozitia ceruta.")
                    else:
                        print("Linie sau coloana invalida (trebuie sa fie unul dintre numerele 0,1,2).")

                except ValueError:
                    print("Linia si coloana trebuie sa fie numere intregi")

            # dupa iesirea din while sigur am valide atat linia cat si coloana
            # deci pot plasa simbolul pe "tabla de joc"
            stare_curenta.tabla_joc.matr[linie * Joc.NR_LINII + coloana] = Joc.JMIN

            # afisarea starii jocului in urma mutarii utilizatorului
            print("\nTabla dupa mutarea jucatorului")
            print(str(stare_curenta))
            # TO DO 8a
            # testez daca jocul a ajuns intr-o stare finala
            # si afisez un mesaj corespunzator in caz ca da
            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)

        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator

            print("Acum muta calculatorul cu simbolul", stare_curenta.j_curent)
            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))

            # stare actualizata e starea mea curenta in care am setat stare_aleasa (mutarea urmatoare)
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm==2
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc  # aici se face de fapt mutarea !!!
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
            # TO DO 8b
            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare.  jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)


if __name__ == "__main__":
    main()
# TO DO 9