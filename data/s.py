class Solution:
    def cherryPickup(self, grid: List[List[int]]) -> int
        self.grid = grid
        self.r1 = [0,0,0]
        self.r2 = [0,len(grid[0])-1,0]
        pass
    def _get_max(self,i,j):
        values = []
        pos = []
        if ( j - 1)>-1:
            values.append(grid[i+1][j-1])
            pos.append(j-1)
        values.append(grid[i+1][j])
        pos.append(j)
        if j+1 <len(grid[0]):
            values.append(grid[i+1][j])
            pos.append(j+1)
        return sorted(values), sorted(pos,key=values)
    def update(self,i,j1,j2):
        v1 , pos1 = self.max(i,j1)
        v2 , pos2 = self.max(i,j2)
        self.r1[0] =i
        self.r2[0] =i
        if mod(j1-j2) >1: 
            self.r1[1] = pos1[-1]
            self.r2[1] = pos2[-1]
            self.r1[1] +=v1[-1]
            self.r2[1] +=v2[-1]
        else:
            self.r1[1] = pos1[-1]
            self.r2[1] = pos2[-1]
            self.r1[1] +=v1[-2]
            self.r2[1] +=v2[-2]






        
        