from random import sample
from Selector import SelectNumber
from copy import deepcopy

def buat_koordinat_garis(size_sel: int)->list[list[tuple]]:

    titik = []
    for y in range(1, 9): #buat bikin garis horizontal
        temp=[]
        temp.append((0, y * size_sel))
        temp.append((900, y * size_sel))
        titik.append(temp)

    for x in range(1, 10): #buat bikin garis vertikal
        temp = []
        temp.append((x * size_sel, 0))
        temp.append((x * size_sel, 900))
        titik.append(temp)
    '''print(titik)'''
    return titik

sizesubgrid = 3
sizegrid = sizesubgrid*sizesubgrid

def generate_pola(baris:int,kolom:int)->int:
    return (sizesubgrid*(baris%sizesubgrid)+baris // sizesubgrid+kolom) % sizegrid

def shuffle(samp: range)->list:
    return sample(samp, len(samp))

def buat_subgrid(sub_grid: int)-> list[list]:
    basis_b=range(sub_grid)
    baris = [g * sub_grid + b for g in shuffle(basis_b) for b in shuffle(basis_b)]
    kolom = [g * sub_grid + k for g in shuffle(basis_b) for k in shuffle(basis_b)]
    nomer = shuffle(range(1, sub_grid * sub_grid +1))
    return [[nomer[generate_pola(b,k)]for k in kolom] for b in baris]

def hapus_nomor(buat_subgrid: list[list])->None:
    banyak_sel_tot=sizegrid*sizegrid
    kosongan = banyak_sel_tot * 3//7
    for i in sample(range(banyak_sel_tot), kosongan):
        buat_subgrid[i//sizegrid][i%sizegrid]=0



class grid:
    def __init__(self, pygame, font):
        self.size_sel=100
        self.num_x_offset = 35
        self.num_y_offset = 12
        self.koordinat_garis = buat_koordinat_garis(self.size_sel)
        self.buat_subgrid = buat_subgrid(sizesubgrid)
        self.game_font = font
        self.__ref_grid = deepcopy(self.buat_subgrid)
        self.win = False
        hapus_nomor(self.buat_subgrid)
        self.sel_isian=self.isian()

        '''print(self.sel_isian)'''
        '''print(self.__ref_grid)'''

        self.Selector = SelectNumber(pygame, self.game_font)

    def restart(self)->None:
        self.buat_subgrid=buat_subgrid(sizesubgrid)
        self.__ref_grid = deepcopy(self.buat_subgrid)
        hapus_nomor(self.buat_subgrid)
        self.sel_isian = self.isian()
        self.win= False

    def isian(self) -> list[tuple]:
        sel_isian = []
        for y in range(len(self.buat_subgrid)):
            for x in range(len(self.buat_subgrid[y])):
                if self.get_cell(x, y) != 0:
                    sel_isian.append((y, x))
        return sel_isian

    def __gambar_garis(self, pg, surface)-> None:
        for index, line in enumerate(self.koordinat_garis):
            if index==2 or index==5 or index==10 or index==13 or index==16:
                pg.draw.line(surface, (235, 237, 171), line[0],line[1])
            else:
                pg.draw.line(surface, (80, 80, 80), line[0], line[1])

    def is_sel_isian(self, x:int, y:int)->bool:
        for sel in self.sel_isian:
            if x == sel[1] and y == sel[0]:
                return True

        return False

    def cek_grid(self):
        for y in range(len(self.buat_subgrid)):
            for x in range(len(self.buat_subgrid[y])):
                if self.buat_subgrid[y][x] != self.__ref_grid[y][x]:
                     return False
        return True

    def get_mouse_click(self, x:int, y:int)-> None:
        if x<=900:
            grid_x, grid_y = x//100, y//100
            '''print(grid_x,grid_y)'''
            if not self.is_sel_isian(grid_x, grid_y):
                self.set_cell(grid_x, grid_y, self.Selector.selected_number)
        self.Selector.klik_tombol(x, y)
        if self.cek_grid():
            '''print("you win")'''
            self.win=True

    def __munculkan_angka(self,surface)->None:
        for y in range(len(self.buat_subgrid)):
            for x in range(len(self.buat_subgrid[y])):
                if self.get_cell(x, y)!=0:
                    if(y, x) in self.sel_isian:
                        text_surface = self.game_font.render(str(self.get_cell(x, y)), False, (227, 230, 161))
                    else:
                        text_surface = self.game_font.render(str(self.get_cell(x, y)), False, (9, 232, 35))

                    if self.get_cell(x, y)!=self.__ref_grid[x][y]:
                        text_surface = self.game_font.render(str(self.get_cell(x, y)), False, (179, 0, 0))

                    surface.blit(text_surface, (x*self.size_sel + self.num_x_offset, y*self.size_sel+self.num_y_offset))

    def draw_all(self, pg, surface):
        self.__gambar_garis(pg, surface)
        self.__munculkan_angka(surface)
        self.Selector.gambar_tombol(pg, surface)

    def get_cell(self, x:int, y:int)->int:
        return self.buat_subgrid[x][y]

    def set_cell(self, x:int, y:int, nilai:int)->None:
        self.buat_subgrid[x][y]=nilai

    '''def show(self):
        for sel in self.buat_subgrid:
            print(sel)'''

'''if __name__=='__main__':
    grid=grid()
    grid.show()'''