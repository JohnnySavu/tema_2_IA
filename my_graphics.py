import time
import copy
import pygame
import sys

ADANCIME_MAX = 2
TIP_ESTIMARE = 1
noduri_generate = 0

class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_COLOANE = 3
    NR_LINII = 3
    JMIN = None
    JMAX = None
    GOL = '#'

    # intiializez tabla de joc
    def __init__(self, tabla=None, nrLinii = None, nrColoane = None):  # Joc()
        if nrLinii is not None and nrColoane is not None:
            self.NR_COLOANE = nrColoane
            self.NR_LINII = nrLinii
        self.drum_castigator = []

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

    def deseneaza_final(self):

        for ind in range(self.__class__.NR_COLOANE * self.__class__.NR_LINII):
            linie = ind // self.__class__.NR_COLOANE  # // inseamna div
            coloana = ind % self.__class__.NR_COLOANE

            culoare = (255, 255, 255) # alb, e necolorat

            if self.matr[ind] == 'R':
                culoare = (255, 0, 0)
            elif self.matr[ind] == 'B':
                culoare = (0, 0, 255)

            if ind in self.drum_castigator:
                culoare = (117, 14, 161)

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
            #vad drumul castigator
            if dp[self.obtine_pozitie(self.NR_LINII - 1, col)] == 1:
                self.drum_castigator.append(self.obtine_pozitie(self.NR_LINII - 1, col))
                pozx = self.NR_LINII - 1
                pozy = col
                while pozx > 0:
                    if self.obtine_pozitie(pozx - 1, pozy) and dp[self.obtine_pozitie(pozx - 1, pozy)] == 1:
                        self.drum_castigator.append(self.obtine_pozitie(pozx - 1, pozy))
                        pozx -= 1
                    elif self.obtine_pozitie(pozx - 1, pozy + 1) and dp[self.obtine_pozitie(pozx - 1, pozy + 1)] == 1:
                        self.drum_castigator.append(self.obtine_pozitie(pozx - 1, pozy + 1))
                        pozx -= 1
                return 'R'

        #trebuie sa fac in mare aceleasi verificari si pentru albastru
        #trebuie sa fie de la stanga la dreapta
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
                    if max(dp[self.obtine_pozitie(lin, col - 1)], dp[self.obtine_pozitie(lin + 1, col - 1)]) > 0:
                        dp[self.obtine_pozitie(lin, col)] = max(dp[self.obtine_pozitie(lin, col - 1)], dp[self.obtine_pozitie(lin + 1, col - 1)]) + 1

            if self.matr[self.obtine_pozitie(self.NR_LINII - 1, col)] == 'B' and dp[self.obtine_pozitie(self.NR_LINII - 1, col - 1)] != 0:
                dp[self.obtine_pozitie(self.NR_LINII - 1, col)] = dp[self.obtine_pozitie(self.NR_LINII - 1, col - 1)] + 1

        #vad daca a castigat albastrul
        for lin in range(self.NR_LINII):
            if dp[self.obtine_pozitie(lin, self.NR_COLOANE - 1)] > 0:
                pozx = lin
                pozy = self.NR_COLOANE - 1
                self.drum_castigator.append(self.obtine_pozitie(pozx, pozy))
                while pozy > 0:
                    if self.obtine_pozitie(pozx - 1, pozy) and dp[self.obtine_pozitie(pozx - 1, pozy)] + 1 == dp[self.obtine_pozitie(pozx, pozy)]:
                        self.drum_castigator.append(self.obtine_pozitie(pozx - 1, pozy))
                        pozx -= 1
                    elif self.obtine_pozitie(pozx + 1, pozy - 1) and dp[self.obtine_pozitie(pozx + 1, pozy - 1)] + 1 == dp[self.obtine_pozitie(pozx, pozy)]:
                        self.drum_castigator.append(self.obtine_pozitie(pozx + 1, pozy - 1))
                        pozx += 1
                        pozy -= 1
                    elif self.obtine_pozitie(pozx, pozy - 1) and dp[self.obtine_pozitie(pozx, pozy - 1)] + 1 == dp[self.obtine_pozitie(pozx, pozy)]:
                        self.drum_castigator.append(self.obtine_pozitie(pozx, pozy - 1))
                        pozy -= 1
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



    def estimeaza_scor(self, adancime):
        global TIP_ESTIMARE
        t_final = self.final()
        # if (adancime==0):
        if t_final == self.__class__.JMAX:  # self.__class__ referinta catre clasa instantei
            return (9999 + adancime)
        elif t_final == self.__class__.JMIN:
            return (-9999 - adancime)
        elif t_final == 'remiza':
            return 0
        else:
            if TIP_ESTIMARE == 1:
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

    btn_estimare = GrupButoane(
        top=250,
        left=30,
        listaButoane=[
            Buton(display=display, w=65, h=30, text="estim_1", valoare="1"),
            Buton(display=display, w=65, h=30, text="estim_2", valoare="2")
        ],
        indiceSelectat=0)


    ok = Buton(display=display, top=330, left=30, w=40, h=30, text="ok", culoareFundal=(155, 0, 55))
    btn_alg.deseneaza()
    btn_juc.deseneaza()
    btn_estimare.deseneaza()
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
                                if not btn_estimare.selecteazaDupacoord(pos):
                                    if ok.selecteazaDupacoord(pos):
                                        display.fill((0, 0, 0))  # stergere ecran
                                        tabla_curenta.deseneaza_grid()
                                        return btn_juc.getValoare(), btn_alg.getValoare(), btn_tip_joc.getValoare(), btn_dificultate.getValoare(), btn_estimare.getValoare()
        pygame.display.update()


def min_max(stare):
    global noduri_generate
    noduri_generate += 1
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutari_scor = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
        stare.stare_aleasa = max(mutari_scor, key=lambda x: x.scor)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu scorul minim
        stare.stare_aleasa = min(mutari_scor, key=lambda x: x.scor)
    stare.scor = stare.stare_aleasa.scor
    return stare


def alpha_beta(alpha, beta, stare):
    global noduri_generate
    noduri_generate += 1

    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        scor_curent = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza scorul
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (scor_curent < stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor
            if (alpha < stare_noua.scor):
                alpha = stare_noua.scor
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        scor_curent = float('inf')

        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare)

            if (scor_curent > stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if (beta > stare_noua.scor):
                beta = stare_noua.scor
                if alpha >= beta:
                    break
    stare.scor = stare.stare_aleasa.scor

    return stare




def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if (final):
        if (final == "remiza"):
            print("Remiza!")
        else:
            print("A castigat " + final)

        return True

    return False



def afiseaza_statistici(timp_joc = None, timpi_jucatori = None, noduri_generate = None):
    #afisam statisticile + tabla in configuratia finala
    if timp_joc:
        print("Timpul total de joc: ", timp_joc)

    #to do in continuare

    while True:
        exit_button.deseneaza()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # iesim din program
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                # daca s-a terminat jocul, afisam tabla finala fara a mai face modificari
                stare_curenta.tabla_joc.deseneaza_final()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # vedem daca s a dat click pe o celula
                pos = pygame.mouse.get_pos()  # coordonatele cursorului la momentul clickului
                if exit_button.selecteazaDupacoord(pos):
                    print("exiting")
                    pygame.quit()
                    sys.exit()



def pvp():
    #timpul de inceput al jocului
    timp_joc = time.time()

    timpi_jucatori = dict()
    #pentru a evalua la final timpii de joc
    timpi_jucatori[Joc.JMIN] = []
    timpi_jucatori[Joc.JMAX] = []

    timpi_jucatori[stare_curenta.j_curent].append(time.time())

    while True:
        #afisam butonul de exit
        exit_button.deseneaza()
        if (stare_curenta.j_curent == Joc.JMIN):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # iesim din program
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    #daca s-a terminat jocul, afisam tabla finala fara a mai face modificari
                    pos = pygame.mouse.get_pos()  # coordonatele cursorului

                    for np in range(len(Joc.celuleGrid)):
                        #vedem daca s-a dat hover pe o celula de joc
                        if Joc.celuleGrid[np].collidepoint(pos):
                            stare_curenta.tabla_joc.deseneaza_grid(coloana_marcaj=np % Joc.NR_COLOANE, linie_marcaj = np // Joc.NR_COLOANE)
                            break

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #vedem daca s a dat click pe o celula
                    pos = pygame.mouse.get_pos()  # coordonatele cursorului la momentul clickului
                    if exit_button.selecteazaDupacoord(pos):
                        print("exiting")
                        pygame.quit()
                        sys.exit()

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
                                    #pygame.quit()
                                    stare_curenta.tabla_joc.deseneaza_final()
                                    hasWon = True
                                    timp_joc = time.time() -  timp_joc
                                    afiseaza_statistici(timp_joc = timp_joc, timpi_jucatori = timpi_jucatori)
                                    break
                                timpi_jucatori[stare_curenta.j_curent][-1] = time.time() - timpi_jucatori[stare_curenta.j_curent][-1]
                                print("Timpul de gandire pentru jucatorul 1 este:", timpi_jucatori[stare_curenta.j_curent][-1])
                                # S-a realizat o mutare. Schimb jucatorul cu cel opus
                                stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)

                                timpi_jucatori[stare_curenta.j_curent].append(time.time())
        else:
            for event in pygame.event.get():
                exit_button.deseneaza()
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

                    #desenam si butonul de exit game

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    pos = pygame.mouse.get_pos()  # coordonatele cursorului la momentul clickului
                    if exit_button.selecteazaDupacoord(pos):
                        print("exiting")
                        pygame.quit()
                        sys.exit()

                    for np in range(len(Joc.celuleGrid)):

                        if Joc.celuleGrid[np].collidepoint(pos):
                            linie = np // Joc.NR_COLOANE
                            coloana = np % Joc.NR_COLOANE
                            ###############################

                            if stare_curenta.tabla_joc.matr[np]== Joc.GOL:
                                stare_curenta.tabla_joc.matr[np] = Joc.JMAX
                                niv = 0

                                # afisarea starii jocului in urma mutarii utilizatorului
                                print("\nTabla dupa mutarea jucatorului")
                                print(str(stare_curenta))

                                stare_curenta.tabla_joc.deseneaza_grid(coloana_marcaj=coloana, linie_marcaj=linie)
                                # testez daca jocul a ajuns intr-o stare finala
                                # si afisez un mesaj corespunzator in caz ca da
                                if (afis_daca_final(stare_curenta)):
                                    stare_curenta.tabla_joc.deseneaza_final()
                                    print(stare_curenta.tabla_joc.drum_castigator)
                                    timp_joc = time.time() -  timp_joc
                                    afiseaza_statistici(timp_joc = timp_joc, timpi_jucatori = timpi_jucatori)
                                    break

                                timpi_jucatori[stare_curenta.j_curent][-1] = time.time() - \
                                                                             timpi_jucatori[stare_curenta.j_curent][-1]
                                print("Timpul de gandire pentru jucatorul 2 este:",
                                      timpi_jucatori[stare_curenta.j_curent][-1])
                                # S-a realizat o mutare. Schimb jucatorul cu cel opus
                                stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)

                                timpi_jucatori[stare_curenta.j_curent].append(time.time())




def pvai():
    global tip_algoritm
    global noduri_generate
    #timpul de inceput al jocului
    timp_joc = time.time()

    lista_noduri_generate = dict()
    lista_noduri_generate[Joc.JMAX] = []

    timpi_jucatori = dict()
    #pentru a evalua la final timpii de joc
    timpi_jucatori[Joc.JMIN] = []
    timpi_jucatori[Joc.JMAX] = []

    timpi_jucatori[stare_curenta.j_curent].append(time.time())

    while True:
        #afisam butonul de exit
        exit_button.deseneaza()
        if (stare_curenta.j_curent == Joc.JMIN):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # iesim din program
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    #daca s-a terminat jocul, afisam tabla finala fara a mai face modificari
                    pos = pygame.mouse.get_pos()  # coordonatele cursorului

                    for np in range(len(Joc.celuleGrid)):
                        #vedem daca s-a dat hover pe o celula de joc
                        if Joc.celuleGrid[np].collidepoint(pos):
                            stare_curenta.tabla_joc.deseneaza_grid(coloana_marcaj=np % Joc.NR_COLOANE, linie_marcaj = np // Joc.NR_COLOANE)
                            break

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #vedem daca s a dat click pe o celula
                    pos = pygame.mouse.get_pos()  # coordonatele cursorului la momentul clickului
                    if exit_button.selecteazaDupacoord(pos):
                        print("exiting")
                        pygame.quit()
                        sys.exit()

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
                                    #pygame.quit()
                                    stare_curenta.tabla_joc.deseneaza_final()
                                    hasWon = True
                                    timp_joc = time.time() -  timp_joc
                                    afiseaza_statistici(timp_joc = timp_joc, timpi_jucatori = timpi_jucatori, noduri_generate=lista_noduri_generate)
                                    break
                                timpi_jucatori[stare_curenta.j_curent][-1] = time.time() - timpi_jucatori[stare_curenta.j_curent][-1]
                                print("Timpul de gandire pentru jucatorul 1 este:", timpi_jucatori[stare_curenta.j_curent][-1])
                                # S-a realizat o mutare. Schimb jucatorul cu cel opus
                                stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)

                                timpi_jucatori[stare_curenta.j_curent].append(time.time())
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator

            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            noduri_generate = 0
            if tip_algoritm == 'minimax':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm=="alphabeta"
                stare_actualizata = alpha_beta(-1000, 1000, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc

            print("Tabla dupa mutarea calculatorului\n" + str(stare_curenta))

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            timpi_jucatori[stare_curenta.j_curent][-1] = t_dupa - t_inainte

            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

            lista_noduri_generate[Joc.JMAX].append(noduri_generate)
            print("NODURI GENERATE: ", noduri_generate)
            stare_curenta.tabla_joc.deseneaza_grid()
            if (afis_daca_final(stare_curenta)):
                afiseaza_statistici(timp_joc=timp_joc, timpi_jucatori=timpi_jucatori, noduri_generate=lista_noduri_generate)
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
            timpi_jucatori[stare_curenta.j_curent].append(time.time())


def aivai():
    global tip_algoritm
    global noduri_generate
    # timpul de inceput al jocului
    timp_joc = time.time()

    lista_noduri_generate = dict()
    lista_noduri_generate[Joc.JMAX] = []
    lista_noduri_generate[Joc.JMIN] = []

    timpi_jucatori = dict()
    # pentru a evalua la final timpii de joc
    timpi_jucatori[Joc.JMIN] = []
    timpi_jucatori[Joc.JMAX] = []

    timpi_jucatori[stare_curenta.j_curent].append(time.time())

    while True:
        # afisam butonul de exit
        exit_button.deseneaza()
        if (stare_curenta.j_curent == Joc.JMIN):
            # Mutare calculator

            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            noduri_generate = 0
            if tip_algoritm == 'minimax':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm=="alphabeta"
                stare_actualizata = alpha_beta(-1000, 1000, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc

            print("Tabla dupa mutarea calculatorului 1\n" + str(stare_curenta))

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            timpi_jucatori[stare_curenta.j_curent][-1] = t_dupa - t_inainte

            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

            lista_noduri_generate[stare_curenta.j_curent].append(noduri_generate)
            print("NODURI GENERATE: ", noduri_generate)
            stare_curenta.tabla_joc.deseneaza_grid()
            if (afis_daca_final(stare_curenta)):
                afiseaza_statistici(timp_joc=timp_joc, timpi_jucatori=timpi_jucatori,
                                    noduri_generate=lista_noduri_generate)
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
            timpi_jucatori[stare_curenta.j_curent].append(time.time())
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator

            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            noduri_generate = 0
            if tip_algoritm == 'minimax':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm=="alphabeta"
                stare_actualizata = alpha_beta(-1000, 1000, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc

            print("Tabla dupa mutarea calculatorului\n" + str(stare_curenta))

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            timpi_jucatori[stare_curenta.j_curent][-1] = t_dupa - t_inainte

            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

            lista_noduri_generate[Joc.JMAX].append(noduri_generate)
            print("NODURI GENERATE: ", noduri_generate)
            stare_curenta.tabla_joc.deseneaza_grid()
            if (afis_daca_final(stare_curenta)):
                afiseaza_statistici(timp_joc=timp_joc, timpi_jucatori=timpi_jucatori,
                                    noduri_generate=lista_noduri_generate)
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
            timpi_jucatori[stare_curenta.j_curent].append(time.time())


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Savu Ioan Daniel Hex")
    # dimensiunea ferestrei in pixeli
    w = 50
    nrLinii = max(5, Joc.NR_LINII)
    nrColoane = max(5, Joc.NR_COLOANE)
    ecran = pygame.display.set_mode(size=((int(0.5 * nrLinii)  + 1 + nrColoane ) * (w + 1) - 1,
                                          (int(nrColoane * 0.5) + 1 + nrLinii) * (w + 1) - 1))
    poz_exit_button =  int((int(Joc.NR_COLOANE * 0.5) + 1 + Joc.NR_LINII) * (w + 1) - 1) - 50
    exit_button = Buton(display=ecran, top=poz_exit_button, left=30, w=40, h=30, text="exit", culoareFundal=(155, 0, 55))
    Joc.initializeaza(ecran, dim_celula=w)
    tabla_curenta = Joc()



    Joc.JMIN, tip_algoritm, tip_joc, dificultate, tip_estimare = deseneaza_alegeri(ecran, tabla_curenta)
    TIP_ESTIMARE = int(tip_estimare)

    print(Joc.JMIN, tip_algoritm)

    Joc.JMAX = 'R' if Joc.JMIN == 'B' else 'B'

    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala
    ADANCIME_MAX = int(dificultate) - 1
    print("ADANCIME MAXIMA:", ADANCIME_MAX)
    stare_curenta = Stare(tabla_curenta, 'R', ADANCIME_MAX)
    print(tip_joc)

    if tip_joc == 'PvP':
        pvp()
    elif tip_joc == 'PvAI':
        pvai()
    else:
        aivai()

