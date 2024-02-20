
class Diffusion:
    """Diffusion Simulator"""

    def __init__(self, rows=10, cols=10, bcset=[1, 1, 1, 1], bcr=None, bcl=None, bct=None, bcb=None):
        # variable attributes
        self.space = []
        self.rows = rows
        self.cols = cols
        self.bc_settings = bcset
        self.left_bc = rows*[0.0] if bcl==None else [float(x) for x in bcl]
        self.right_bc = rows*[0.0] if bcr==None else [float(x) for x in bcr]
        self.top_bc = cols*[0.0] if bct==None else [float(x) for x in bct]
        self.bottom_bc = cols*[0.0] if bcb==None else [float(x) for x in bcb]
        
        # creating self.space
        for i in range(rows):
            self.space.append([0.0]*cols)

    def set_cell(self, row_rng, col_rng, state):
        for i in range(row_rng[0], row_rng[1]+1):
            for j in range(col_rng[0], col_rng[1]+1):
                self.space[i][j] = float(state)

    def next_step(self, t_steps):
        # copy of boundary conditions
        left = [i for i in self.left_bc]
        right = [i for i in self.right_bc]
        top = [i for i in self.top_bc]
        bottom = [i for i in self.bottom_bc]
        
        for t in range(t_steps):
            temp_space = [a[:] for a in self.space]
            
            # calculate neumann bc (when settings==2)
            if 2 in self.bc_settings:
                if self.bc_settings[0]==2:
                    for n in range(self.rows):
                        left[n] = temp_space[n][1] - self.left_bc[n]*2
                if self.bc_settings[1]==2:
                    for n in range(self.rows):
                        right[n] = temp_space[n][-2] + self.right_bc[n]*2
                if self.bc_settings[2]==2:
                    for n in range(self.cols):
                        top[n] = temp_space[1][n] - self.top_bc[n]*2
                if self.bc_settings[3]==2:
                    for n in range(self.cols):
                        bottom[n] = temp_space[-2][n] - self.bottom_bc[n]*2
                
            # place boundary conditions into temp_space
            for n, i in enumerate(temp_space):
                i.insert(0, left[n])
                i.append(right[n])
            temp_space.insert(0, [0] + top + [0])
            temp_space.append([0] + bottom + [0])

            # updating values in self.space
            for i in range(1,self.rows+1):
                for j in range(1, self.cols+1):
                    ux = (temp_space[i][j+1] - 2*temp_space[i][j] + temp_space[i][j-1])
                    uy = (temp_space[i+1][j] - 2*temp_space[i][j] + temp_space[i-1][j])
                    du = 0.0001*(ux+uy)
                    self.space[i-1][j-1] += du

def main():
    t = time()
    space1 = Diffusion(11,15,[2, 2, 1, 1], 11*[0], 11*[0], 15*[1], 15*[1]) 
    space1.set_cell([4,6],[5,9],1)
    space1.set_cell([0,2],[0,2],1)
    space1.next_step(10000)
    space1.print_space()
    print(space1.left_bc)
    print(space1.top_bc)
    dt = time()-t
    print(dt)
  
if __name__ == "__main__":
    main()
