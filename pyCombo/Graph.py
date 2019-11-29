"""
CalcModMtrix
SetCommunities
Modularity
CommunityIndices
GetCorrectionVector
GetModularitySubmatrix
DeleteCommunityIfEmpty
CommunityNumber
PerformSplit
Size
"""
import numpy as np
import networkx as nx


class Graph:
    m = 1
    m_size = 0
    m_totalWeight = 0.0
    m_isOriented = False
    m_communityNumber = 0

    def __init__(graph:nx.Graph):
        

    def FillMatrix(self, src, dst, weight):
        m = min(src.min(), dst.min())
        m = m if m <= 0 else 1

        if self.m_isOriented:
            self.m_totalWeight *= 2

        self.m_size = 1 + max(src.max(), dst.max()) - m
        self.m_matrix = np.zeroes((self.m_size, self.m_size))

        for i in range(len(src)):
            self.m_matrix[src[i] - m][dst[i] - m] += weight[i]
            if self.m_isOriented:
                self.m_matrix[dst[i] - m][src[i] - m] += weight[i]

    def FillModMatrix(self, src, dst, weight):
        m = min(src.min(), dst.min())
        m = m if m <= 0 else 1
        
        if self.m_size == 0:
        self.m_size = 1 + max(src.max(), dst.max()) - m

        if self.m_isOriented:
            self.m_totalWeight *= 2

        self.m_modMatrix = np.zeroes((self.m_size, self.m_size))
        
        sumQ1 = np.zeroes(m_size)
        sumQ2 = np.zeroes(m_size)

        for i in range(len(src)):
            n_weight = (weight[i] / self.m_totalWeight)
            
            self.m_modMatrix[src[i]-m][dst[i]-m] += n_weight

            sumQ1[src[i]-m] += n_weight
            sumQ2[dst[i]-m] += n_weight

            if not self.m_isOriented:
                sumQ1[dst[i]-m] += n_weight
                sumQ2[src[i]-m] += n_weight
        
        for i in range(self.m_size):
            for j in range(self.m_size):
                self.m_modMatrix[i][j] -= sumQ1[i]*sumQ2[j]
        
        for i in range(self.m_size):   # FIX: I think here is a meaningfull double loop
            for j in range(self.m_size):
                self.m_modMatrix[i][j] = self.m_modMatrix[j][i] = (self.m_modMatrix[i][j] + self.m_modMatrix[j][i]) / 2;

    def EdgeWeight(self, i, j):
        return self.m_matrix[i,j]
    
    def CalcModMtrix(self):

        if not hasattr(self, 'm_modMatrix'):
            return
        
        self.m_modMatrix = self.m_matrix / self.m_totalWeight

        sumQ1 = self.m_modMatrix.sum(0)
        sumQ2 = self.m_modMatrix.sum(1)

        for i in range(self.m_size):
            for j in range(self.m_size):
                self.m_modMatrix[i][j] -= sumQ1[i]*sumQ[j]
        for i in range(self.m_size):  # FIX: I think here is a meaningfull double loop
            for j in range(self.m_size):
                self.m_modMatrix[i][j] = self.m_modMatrix[j][i] = (self.m_modMatrix[i][j] + self.m_modMatrix[j][i]) / 2
    
    def print(self):
        print(f'Matrix:\n\n{self.m_matrix}\n\nModularity matrix:\n\n{self.m_modMatrix}\n\n')
    
    def SetCommunities(self, new_communities, number:int=-1)->None:
        if self.m_size != len(new_communities):
            raise Exception(f'wrong length of communities vector: {len(communities)}, expected {self.m_size}')

        self.m_communities = new_communities
        if number == -1:
            self.m_communityNumber = self.m_communities.max() + 1
        else:
            self.m_communityNumber = number
    
    # def PrintCommunity(filename:str):
    #     with open(filename, 'w') as f:

    def Modularity(self) -> float:
        mod = 0
        for i in range(len(self.m_modMatrix)):
            for j in range(len(self.m_modMatrix)):
                if self.m_communities[i] == m_communities[j]:
                    mod += self.m_modMatrix[i][j]
        return mod

    def PerformSplit(self, origin, dest, split_communities):
        if dest > self.m_communityNumber:
            dest = self.m_communityNumber
        if dest == self.m_communityNumber:
            self.m_communityNumber += 1  # NOT SURE IF

        for i in range(self.m_size):
            if self.m_communities[i] == origin and split_communities[i]:
                self.m_communities[i] = dest

    def IsCommunityEmpty(self, comm:int)->bool:
        return (self.m_communities != comm).all()
    
    def DeleteCommunityIfEmpty(self, comm:int)->bool:
        if self.IsCommunityEmpty(comm):
            
            mask = self.m_communities > comm
            self.m_communities[mask] -= 1
            self.m_communityNumber = self.m_communities.unique()
            return True
        
        return False

    def CommunityIndices(self, comm:int):
        
        res = np.arange(len(self.m_communities))
        return res[self.m_communities == com]

    def GetModularitySubmatrix(self, indices):
        l = len(indices)
        res = np.empty((l, l))

        for i in range(l):
            for j in range(l):
                res[i][k] = self.m_modMatrix[indices[i]][indices[j]]

        return res

    def GetCorrectioNVector(self, origCommInd, destCommInd):
        l = len(origCommInd)
        res = np.zeroes(l)
        
        for i in range(l):
            for j in range(l):
                res[i] += self.m_modMatrix[destCommInd[j]][origCommInd[i]]

        return res

        






