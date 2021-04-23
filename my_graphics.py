import time
import copy
import pygame
import sys

ADANCIME_MAX = 2

class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_COLOANE = 8
    NR_LINII = 11
    JMIN = None
    JMAX = None
    GOL = '#'

    # intiializez tabla de joc
    def __init__(self, tabla=None, nrLinii = None, nrColoane = None):  # Joc()
        if nrLinii is not None and nrColoane is not None:
            self.NR_COLOANE = nrColoane
            self.NR_LINII = nrLinii

        self.matr = tabla or [Joc.GOL] * self.NR_LINII * self.NR_COLOANE


    @classmethod
    def initializeaza(cls, display, dim_celula=100):
        NR_LINII = cls.NR_LINII
        NR_COLOANE = cls.NR_COLOANE
        cls.display = display
        cls.dim_celula = dim_celula
        cls.celuleGrid = []  # este lista cu patratelele din grid
        for linie in range(NR_LINII):
            for coloana in range(NR_COLOANE):
                patr = pygame.Rect(coloana * (dim_celula + 1) + linie * (dim_celula + 1) / 2,
                                   linie * (dim_celula + 1), dim_celula, dim_celula)
                cls.celuleGrid.append(patr)

    def deseneaza_grid(self, coloana_marcaj=None, linie_marcaj=None):  # tabla de exemplu este ["#","x","#","0",......]

        for ind in range(self.__class__.NR_COLOANE * self.__class__.NR_LINII):
            linie = ind // self.__class__.NR_COLOANE  # // inseamna div
            coloana = ind % self.__class__.NR_COLOANE

            culoare = (255, 255, 255) # alb, e necolorat

            if self.matr[ind] == 'R':
                culoare = (255, 0, 0)
            elif self.matr[ind] == 'B':
                culoare = (0, 0, 255)

            if linie == linie_marcaj and coloana == coloana_marcaj:
                if culoare == (255, 255, 255):
                    culoare = (255, 255, 0)
                else:
                    culoare = (0, 255, 255)

            pygame.draw.rect(self.__class__.display, culoare, self.__class__.celuleGrid[ind])

        pygame.display.update()


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

    # linie deschisa inseamna linie pe care jucatorul mai poate forma o configuratie castigatoare
    # practic e o linie fara simboluri ale jucatorului opus
    def linie_deschisa(self, lista, jucator):
        jo = self.jucator_opus(jucator)
        # verific daca pe linia data nu am simbolul jucatorului opus
        if not jo in lista:
            # return lista.count(jucator)
            return 1
        return 0

    def linii_deschise(self, jucator):
        return self.linie_deschisa(self.matr[0:3], jucator) + self.linie_deschisa(self.matr[3:6],
                                                                                  jucator) + self.linie_deschisa(
            self.matr[6:9], jucator) + self.linie_deschisa(self.matr[0:9:3], jucator) + self.linie_deschisa(
            self.matr[1:9:3], jucator) + self.linie_deschisa(self.matr[2:9:3], jucator) + self.linie_deschisa(
            self.matr[0:9:4], jucator) + self.linie_deschisa(self.matr[2:7:2], jucator)

    # TO DO 7
    def estimeaza_scor(self, adancime):
        t_final = self.final()
        # if (adancime==0):
        if t_final == self.__class__.JMAX:  # self.__class__ referinta catre clasa instantei
            return (99 + adancime)
        elif t_final == self.__class__.JMIN:
            return (-99 - adancime)
        elif t_final == 'remiza':
            return 0
        else:
            return (self.linii_deschise(self.__class__.JMAX) - self.linii_deschise(self.__class__.JMIN))

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




class Buton:
    def __init__(self, display=None, left=0, top=0, w=0, h=0, culoareFundal=(53, 80, 115),
                 culoareFundalSel=(89, 134, 194), text="", font="arial", fontDimensiune=16, culoareText=(255, 255, 255),
                 valoare=""):
        self.display = display
        self.culoareFundal = culoareFundal
        self.culoareFundalSel = culoareFundalSel
        self.text = text
        self.font = font
        self.w = w
        self.h = h
        self.selectat = False
        self.fontDimensiune = fontDimensiune
        self.culoareText = culoareText
        # creez obiectul font
        fontObj = pygame.font.SysFont(self.font, self.fontDimensiune)
        self.textRandat = fontObj.render(self.text, True, self.culoareText)
        self.dreptunghi = pygame.Rect(left, top, w, h)
        # aici centram textul
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)
        self.valoare = valoare

    def selecteaza(self, sel):
        self.selectat = sel
        self.deseneaza()

    def selecteazaDupacoord(self, coord):
        if self.dreptunghi.collidepoint(coord):
            self.selecteaza(True)
            return True
        return False

    def updateDreptunghi(self):
        self.dreptunghi.left = self.left
        self.dreptunghi.top = self.top
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)

    def deseneaza(self):
        culoareF = self.culoareFundalSel if self.selectat else self.culoareFundal
        pygame.draw.rect(self.display, culoareF, self.dreptunghi)
        self.display.blit(self.textRandat, self.dreptunghiText)


class GrupButoane:
    def __init__(self, listaButoane=[], indiceSelectat=0, spatiuButoane=10, left=0, top=0):
        self.listaButoane = listaButoane
        self.indiceSelectat = indiceSelectat
        self.listaButoane[self.indiceSelectat].selectat = True
        self.top = top
        self.left = left
        leftCurent = self.left
        for b in self.listaButoane:
            b.top = self.top
            b.left = leftCurent
            b.updateDreptunghi()
            leftCurent += (spatiuButoane + b.w)

    def selecteazaDupacoord(self, coord):
        for ib, b in enumerate(self.listaButoane):
            if b.selecteazaDupacoord(coord):
                self.listaButoane[self.indiceSelectat].selecteaza(False)
                self.indiceSelectat = ib
                break
        else:
            return False
        for i in range(len(self.listaButoane)):
            if i != self.indiceSelectat:
                self.listaButoane[i].selecteaza(False)
        self.listaButoane[self.indiceSelectat].selecteaza(True)
        return True

    def deseneaza(self):
        # atentie, nu face wrap
        for b in self.listaButoane:
            b.deseneaza()

    def getValoare(self):
        return self.listaButoane[self.indiceSelectat].valoare


############# ecran initial ########################
def deseneaza_alegeri(display, tabla_curenta):
    btn_alg = GrupButoane(
        top=30,
        left=30,
        listaButoane=[
            Buton(display=display, w=80, h=30, text="minimax", valoare="minimax"),
            Buton(display=display, w=80, h=30, text="alphabeta", valoare="alphabeta")
        ],
        indiceSelectat=1)
    btn_juc = GrupButoane(
        top=80,
        left=30,
        listaButoane=[
            Buton(display=display, w=35, h=30, text="Red", valoare="R"),
            Buton(display=display, w=35, h=30, text="Blue", valoare="B")
        ],
        indiceSelectat=0)

    btn_tip_joc = GrupButoane(
        top = 130,
        left = 30,
        listaButoane=[
            Buton(display=display, w=45, h=30, text="PvP", valoare="PvP"),
            Buton(display=display, w=45, h=30, text="PvAI", valoare="PvAI"),
            Buton(display=display, w=45, h=30, text="AIvAI", valoare="AIvAI")
        ],
        indiceSelectat= 1)

    btn_dificultate = GrupButoane(
        top = 180,
        left = 30,
        listaButoane=[
            Buton(display=display, w=45, h=30, text="Usor", valoare = "3"),
            Buton(display=display, w=45, h=30, text="Mediu", valoare= "4"),
            Buton(display=display, w=45, h=30, text="Greu", valoare= "5" )
        ],
        indiceSelectat= 0)

    ok = Buton(display=display, top=250, left=30, w=40, h=30, text="ok", culoareFundal=(155, 0, 55))
    btn_alg.deseneaza()
    btn_juc.deseneaza()
    btn_dificultate.deseneaza()
    btn_tip_joc.deseneaza()
    ok.deseneaza()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not btn_alg.selecteazaDupacoord(pos):
                    if not btn_juc.selecteazaDupacoord(pos):
                        if not btn_tip_joc.selecteazaDupacoord(pos):
                            if not btn_dificultate.selecteazaDupacoord(pos):
                                if ok.selecteazaDupacoord(pos):
                                    display.fill((0, 0, 0))  # stergere ecran
                                    tabla_curenta.deseneaza_grid()
                                    return btn_juc.getValoare(), btn_alg.getValoare(), btn_tip_joc.getValoare(), btn_dificultate.getValoare()
        pygame.display.update()



def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if (final):
        if (final == "remiza"):
            print("Remiza!")
        else:
            print("A castigat " + final)

        return True

    return False


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Savu Ioan Daniel Hex")
    # dimensiunea ferestrei in pixeli
    w = 50
    ecran = pygame.display.set_mode(size=((int(0.5 * Joc.NR_LINII)  + 1 + Joc.NR_COLOANE ) * (w + 1) - 1,
                                          (int(Joc.NR_COLOANE * 0.5) + 1 + Joc.NR_LINII) * (w + 1) - 1))

    Joc.initializeaza(ecran, dim_celula=w)
    tabla_curenta = Joc()
    Joc.JMIN, tip_algoritm = deseneaza_alegeri(ecran, tabla_curenta)
    print(Joc.JMIN, tip_algoritm)

    Joc.JMAX = 'R' if Joc.JMIN == 'B' else 'B'

    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, 'R', ADANCIME_MAX)

    while True:
        if (stare_curenta.j_curent == Joc.JMIN):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # iesim din program
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:

                    pos = pygame.mouse.get_pos()  # coordonatele cursorului
                    for np in range(len(Joc.celuleGrid)):
                        if Joc.celuleGrid[np].collidepoint(pos):
                            stare_curenta.tabla_joc.deseneaza_grid(coloana_marcaj=np % Joc.NR_COLOANE, linie_marcaj = np // Joc.NR_COLOANE)
                            break

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    pos = pygame.mouse.get_pos()  # coordonatele cursorului la momentul clickului

                    for np in range(len(Joc.celuleGrid)):

                        if Joc.celuleGrid[np].collidepoint(pos):
                            linie = np // Joc.NR_COLOANE
                            coloana = np % Joc.NR_COLOANE
                            ###############################

                            if stare_curenta.tabla_joc.matr[np]== Joc.GOL:
                                stare_curenta.tabla_joc.matr[np] = Joc.JMIN
                                niv = 0

                                # afisarea starii jocului in urma mutarii utilizatorului
                                print("\nTabla dupa mutarea jucatorului")
                                print(str(stare_curenta))

                                stare_curenta.tabla_joc.deseneaza_grid(coloana_marcaj=coloana, linie_marcaj=linie)
                                # testez daca jocul a ajuns intr-o stare finala
                                # si afisez un mesaj corespunzator in caz ca da
                                if (afis_daca_final(stare_curenta)):
                                    break

                                # S-a realizat o mutare. Schimb jucatorul cu cel opus
                                stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # iesim din program
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:

                    pos = pygame.mouse.get_pos()  # coordonatele cursorului
                    for np in range(len(Joc.celuleGrid)):
                        if Joc.celuleGrid[np].collidepoint(pos):
                            stare_curenta.tabla_joc.deseneaza_grid(coloana_marcaj=np % Joc.NR_COLOANE,
                                                                   linie_marcaj=np // Joc.NR_COLOANE)
                            break

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    pos = pygame.mouse.get_pos()  # coordonatele cursorului la momentul clickului

                    for np in range(len(Joc.celuleGrid)):

                        if Joc.celuleGrid[np].collidepoint(pos):
                            linie = np // Joc.NR_COLOANE
                            coloana = np % Joc.NR_COLOANE
                            ###############################

                            if stare_curenta.tabla_joc.matr[np] == Joc.GOL:
                                stare_curenta.tabla_joc.matr[np] = Joc.JMAX
                                niv = 0

                                # afisarea starii jocului in urma mutarii utilizatorului
                                print("\nTabla dupa mutarea jucatorului")
                                print(str(stare_curenta))

                                stare_curenta.tabla_joc.deseneaza_grid(coloana_marcaj=coloana, linie_marcaj=linie)
                                # testez daca jocul a ajuns intr-o stare finala
                                # si afisez un mesaj corespunzator in caz ca da
                                if (afis_daca_final(stare_curenta)):
                                    break

                                # S-a realizat o mutare. Schimb jucatorul cu cel opus
                                stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
