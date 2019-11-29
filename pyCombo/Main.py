import numpy as np
# from math import inf as INF

std = {}
debug_verify = False

THRESHOLD = 1e-6

# RAND_MAX2 = RAND_MAX / 2; # seems to be method for 50% chance coin
# from random import choice

autoC1, autoC2 = 2, 1.5
use_fixed_tries = False
best_gain = 1.0

# def rand():
#     return choice([0,1])


def ModGain(Q, correctionVector, community) -> float:

    n = len(community)
    mod_gain = 0.0

    for i in range(n):
        for j in range(n):
            if community[i] == community[j]:
                mod_gain += Q[i][j]
            else:
                mod_gain -= Q[i][j]
    mod_gain *= 0.5

    for i in range(n):
        if community[i]:
            mod_gain += correctionVector[i]
        else:
            mod_gain -= correctionVector[i]

    return mod_gain


def PerformKernighansShift(Q, correctionVector, communitiesOld, communitiesNew):
    '''perform a split improvement
    using a Karnigan-Lin-style iterative shifts series
    '''
    
    n = Q.size()
    gains = np.zeroes(n, np.float64)
    
    for i in range(n):
        for j in range(n):
            if i!=j:
                if communitiesOld[i] == communitiesOld[j]:
                    gains[i] -= Q[i][j]
                else:
                    gains[i] += Q[i][j]
        if communitiesOld[i]:
            gains[i] -= correctionVector[i]
        else:
            gains[i] += correctionVector[i]
        gains[i] *= 2

    gains_got = np.zeroes(n, np.float64)
    gains_indexes = np.zeroes(n, np.int)

    communitiesNew = communitiesOld
    for i in range(n):
        it = max(gains)
        gains_got[i] = it
        gains_indexes[i] = gains_ind = it - gains[0]
        
        
        if i > 0:
            gains_got[i] = gains_got[i] + gains_got[i-1];
        for j in range(n):
            if communitiesNew[gains_ind] == communitiesNew[j]:
                gains[j] += 4* Q[gains_ind][j]
            else:
                gains[j] -= 4 * Q[gains_ind][j]
        communitiesNew[gains_ind] = !communitiesNew[gains_ind]
        gains[gains_ind] = gains[gains_ind] - 2*n

    it = max(gains)
    mod_gain = it
    stepsToGetMaxGain  = it - gains_got[0]+1
    
    if mod_gain > 0:
        communitiesNew = communitiesOld
        for i in range(stepsToGetMaxGain):
            communitiesNew[gains_indexes[i]] = not communitiesNew[gains_indexes[i]]
    else:
        communitiesNew = communitiesOld
        mod_gain = 0

    return mod_gain


def Split(Q, correctionVector, splitCommunity):
    
    mod_gain = 0.0
    sumQ = Q.sum(1)
    n = Q.size()

    for i in range(n):
        Q[i][i] += 2 * correctionVector[i] - sumQ[i] # adjust the submatrix
    if use_fixed_tries:
        tries = 2
    else:
        tries = np.pow(np.abs(np.log(best_gain)), autoC2) / autoC1 + 3;
        tryI = 0
    
    while tryI < tries:
        tryI += 1

        if use_fixed_tries:
            communities0 = np.full(n, (2 - tryI))
        else:
            communities0 = np.random.choice(2, n)

        mod_gain0 = ModGain(Q, correctionVector, communities0);
        mod_gain1 = 1;

        while mod_gain1 > THRESHOLD:
            communitiesNew = np.empty(n);
            mod_gain1 = PerformKernighansShift(Q, correctionVector, communities0, communitiesNew);

            if mod_gain1 > THRESHOLD:
                mod_gain0 += mod_gain1
                communities0 = communitiesNew;
                
                if(debug_verify):
                    mod_gain_verify = ModGain(Q, correctionVector, communities0)
                    
                    delta = np.fabs(mod_gain_verify - mod_gain0)
                    if delta > THRESHOLD:
                        raise Exception(f'Gain delta {delta} is above the treshold {THRESHOLD}')
                        
        if mod_gain < mod_gain0:
            splitCommunity = communities0;
            mod_gain = mod_gain0;

        if mod_gain <= 1e-6:
            tries = int(tries / 2)

    if np.fabs(mod_gain) < THRESHOLD:
        splitCommunity.fill(1)

    return mod_gain


def reCalc(G, moves, split_communities, origin, dest):
    moves[origin][dest] = 0

    if origin != dest:
        origCommInd = G.CommunityIndices(origin)
        if not origCommInd.empty():
            correctionVector = G.GetCorrectionVector(origCommInd, G.CommunityIndices(dest));
            splitComunity = origCommInd.size()
            Q = G.GetModularitySubmatrix(origCommInd)
            moves[origin][dest] = Split(Q, correctionVector, splitComunity)
            for i in range(splitCommunity.size()):
                splits_communities[dest][origCommInd[i]] = splitComunity[i]

def BestGain(moves):
    '''computes the best gain from moves matrix'''
    bestGain = max(-1, np.amax(moves))
    origin, dest = np.unravel_index(np.argmax(moves, axis=None), moves.shape)
    
    return bestGain, origin, dest


def DeleteEmptyCommunities(G, moves, splits_communities, origin:int):

    if G.DeleteCommunityIfEmpty(origin):

        commNumber = G.CommunityNumber()
        
        for i in range(origin, commNumber):
            moves[i] = moves[i+1]
        
        moves[commNumber].assign(commNumber+2, 0);
        for i in range(moves.size()):
            for j in range(origin, commNumber):
                moves[i][j] = moves[i][j+1];
            moves[i][commNumber+1] = 0;

        for i in range(origin, commNumber+1):
            splits_communities[i] = splits_communities[i+1]

def RunCombo(G, max_comunities):
    G.CalcModMtrix();
    G.SetCommunities(np.zeros_like(G.Size()))

    currentMod = G.Modularity()
    print(f"Initial modularity: {currentMod:%6f}\n")
   
    moves = np.zeroes((2, 2))
    splits_communities = np.zeroes((2, G.size()))
    
    # vector< vector<double> > moves(2, vector<double>(2, 0)) # results of splitting communities 
    # vectors of boolean meaning that corresponding vertex should be moved to dest
    
    
    for origin in range(G.CommunityNumber()):
        for dest in range(G.CommunityNumber() + (G.CommunityNumber() < max_comunities)):
            reCalc(G, moves, splits_communities, origin, dest)

    best_gain, origin, dest = BestGain(moves);

    while best_gain > THRESHOLD:
        comunityAdded = (dest >= G.CommunityNumber())
        G.PerformSplit(origin, dest, splits_communities[dest]);
    
        if(debug_verify):
            oldMod = currentMod
            currentMod = G.Modularity();
            delta = np.fabs(currentMod - oldMod - best_gain)
            if  delta > THRESHOLD:
                raise Exception(f'Delta {delta} is above the treshold: {TRESHOLD}')

        if comunityAdded and (dest < (max_comunities - 1)):
            if dest >= moves.size() - 1:
                
                # add one more column and row
                moves = np.append((moves, np.zeroes(len(moves))), axis=1)
                moves = np.append((moves, np.zeroes(len(moves)+1)), axis=0)

                splits_communities = np.concatenate((splits_communities, np.zeros(G.Size())), axis=0)

            for i in range(dest):
                moves[i][dest+1] = moves[i][dest];
                splits_communities[dest+1] = splits_communities[dest];


        for i in range((G.CommunityNumber() + (G.CommunityNumber() < max_comunities))):
            reCalc(G, moves, splits_communities, origin, i);
            reCalc(G, moves, splits_communities, dest, i);
            
            if i != dest and i < G.CommunityNumber():
                reCalc(G, moves, splits_communities, i, origin)
            if i != origin and i < G.CommunityNumber():
                reCalc(G, moves, splits_communities, i, dest)

        DeleteEmptyCommunities(G, moves, splits_communities, origin) # remove origin community if empty
        best_gain, origin, dest = BestGain(moves);

