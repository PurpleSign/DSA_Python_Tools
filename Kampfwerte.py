#!/usr/bin/env python
# coding: utf-8

# Kleines Script zur Validierung des Schwierigkeitsgrades von Gegner fuer vorhandene
#     Spieler*Innen Charaktere.
#
# Das Script berechnet auf Basis der Trefferwahrscheinlichkeiten, bestimmt durch 
#     Angriffs- und Verteidigungswert, den durchschnittlichen Schaden, den ein
#     Spieler*Innen Charakter gegen ein Gegner, und ein Gegner gegen einen Charakter
#     anrichtet.


import numpy as np
import uncertainties.unumpy as unp

from uncertainties import ufloat
from uncertainties.unumpy import (nominal_values as noms,
                                  std_devs as stds)



def calChance(pAT, pPA, pAT_Mod, pPA_Mod):
    vAT = (pAT + pAT_Mod)
    if vAT < 0:
        vAT = 0
    elif vAT > 19:
        vAT = 19
    vPA = (pPA + pPA_Mod)
    if vPA < 0:
        vPA = 0
    elif vPA > 19:
        vPA = 19
        
    return (vAT/20)*((20 - vPA)/20)

def rekDamAve(pStage, pPreTP, pTP, pRS, pDamage_Ave, pCount):
    if pStage == 0:
        vDamage_Temp = pPreTP+pTP-pRS
        if vDamage_Temp < 0:
            vDamage_Temp = 0
            
        pDamage_Ave += vDamage_Temp
        pCount += 1
    else:
        for i in range(0, 6):
            pDamage_Ave, pCount = rekDamAve(pStage-1, pPreTP+(i+1), pTP, pRS, pDamage_Ave, pCount)
    
    return (pDamage_Ave, pCount)
def rekDamStd(pStage, pPreTP, pTP, pRS, pDamage_Ave, pDamage_Std):
    if pStage == 0:
        vDamage_Temp = pPreTP+pTP-pRS
        if vDamage_Temp < 0:
            vDamage_Temp = 0
            
        pDamage_Std += (pDamage_Ave - vDamage_Temp)**2
    else:
        for i in range(0, 6):
            pDamage_Std = rekDamStd(pStage-1, pPreTP+(i+1), pTP, pRS, pDamage_Ave, pDamage_Std)
            
    return pDamage_Std
def calDamage(pTP, pRS, pTP_Mod, pRS_Mod):
    vTP = pTP[1] + pTP_Mod
    vRS = pRS + pRS_Mod
    
    vDamage_Ave, vCount = rekDamAve(pTP[0], 0, vTP, vRS, 0, 0)
    vDamage_Ave = vDamage_Ave/vCount
    
    vDamage_Std = rekDamStd(pTP[0], 0, vTP, vRS, vDamage_Ave, 0)
    vDamage_Std = vDamage_Std/vCount
    
    return ufloat(vDamage_Ave, vDamage_Std)

def calValues(pFighter, pEnemie):
    vAttStats = []
    vDefStats = []
    
    for i in range(0, len(pFighter[1])):
        vAttArr = []
        vDefArr = []
        for u in range(0, len(pEnemie[1])):
            vDamStat = calDamage(pFighter[3][i], pEnemie[5], pFighter[6][2], pEnemie[6][4])
            vAttArr += [vDamStat*calChance(pFighter[1][i], pEnemie[2][u], pFighter[6][0], pEnemie[6][1])]
            
            vDamStat = calDamage(pEnemie[3][u], pFighter[5], pEnemie[6][2], pFighter[6][4])
            vDefArr += [vDamStat*calChance(pEnemie[1][u], pFighter[2][i], pEnemie[6][0], pFighter[6][1])]
        vAttStats += [vAttArr]
        vDefStats += [vDefArr]
    
    return (vAttStats, vDefStats)


def getOutValues(pFighterStrings, pEnemieStrings, pAttStats, pDefStats):
    vOutputString = 'Kampfstats fuer ' + pFighterStrings[0] + ' gegen ' + pEnemieStrings[0] + ':'
    
    for u in range(0, len(pAttStats[0])):
        vOutLine = '\n' + pEnemieStrings[0] + ' ' + pEnemieStrings[u+1] + ':\t\t'
        
        for i in range(0, len(pAttStats)):
            vAT = ufloat(np.round(noms(pAttStats[i][u]), 1), np.round(stds(pAttStats[i][u]), 1))
            vPA = ufloat(np.round(noms(pDefStats[i][u]), 1), np.round(stds(pDefStats[i][u]), 1))
            
            vOutLine += 'AT {}, PA {};\t'.format(vAT, vPA)
        
        vOutputString += vOutLine
        
    return vOutputString
def getOutFighter(pFighterStrings):
    vOutputString = pFighterStrings[0] + ' kaempf mit'
    for i in range(1, len(pFighterStrings)):
        vOutputString += ' ' + pFighterStrings[i] + ','
    vOutputString += '\n'
    
    return vOutputString



vFighters = []
 # Spieler-Werte
vStrings_0 = ['Erejin', 'Schwert Nachtwind', 'Anderthalbhaender Nachtwind']
vAT_0 = np.array([18, 11])          # Nachtwind Schwert, Anderhalb
vPA_0 = np.array([13, 16])
vTP_0 = np.array([(1, 4), (1, 4)])
vLeP_0 = 31
vRS_0 = 3
vMods_0 = np.array([0, 0, 0, 0, 0])
vFighter_0 = [vStrings_0, vAT_0, vPA_0, vTP_0, vLeP_0, vRS_0, vMods_0]
vFighters += [vFighter_0]

vStrings = ['Al Achim', 'Rabenschnabel']
vAT = np.array([15])          # Rabenschnabel
vPA = np.array([11])
vTP = np.array([(1, 4)])
vLeP = 30
vRS = 1
vMods = np.array([0, 0, 0, 0, 0])
vFighter_1 = [vStrings, vAT, vPA, vTP, vLeP, vRS, vMods]
vFighters += [vFighter_1]

vStrings = ['Arkadius', 'Stab', 'Schwert']
vAT = np.array([12, 12])
vPA = np.array([8, 9])
vTP = np.array([(1, 1), (1, 4)])
vLeP = 30
vRS = 0
vMods = np.array([0, 0, 0, 0, 0])
vFighter_2 = [vStrings, vAT, vPA, vTP, vLeP, vRS, vMods]
#vFighters += [vFighter_2]

vStrings = ['Ehrwan', 'Anderhalb', 'Hieb']
vAT = np.array([14, 12])
vPA = np.array([14, 13])
vTP = np.array([(1, 5), (1, 4)])
vLeP = 31
vRS = 2
vMods = np.array([-4, -4, 0, -23, 0])
vFighter_3 = [vStrings, vAT, vPA, vTP, vLeP, vRS, vMods]
#vFighters += [vFighter_3]

vStrings = ['Shalomie', 'Bogen', 'Dolch']
vAT = np.array([15, 10])
vPA = np.array([6, 7])
vTP = np.array([(1, 4), (1, 1)])
vLeP = 30
vRS = 0
vMods = np.array([0, 0, 0, 0, 0])
vFighter_4 = [vStrings, vAT, vPA, vTP, vLeP, vRS, vMods]
#vFighters += [vFighter_4]


 # Gegner-Werte
vEnemies = []
#   Korobar
vStrings = ['Korobar\t\t', 'Stab\t', 'direkt\t']
vAT = np.array([12, 0])          # Stab          
vPA = np.array([16, 0])
vTP = np.array([(1, 2), (0, 0)])
vLeP = 37
vRS = 2
vMods = np.array([0, 0, 0, 0, 0])
vEnemies += [[vStrings, vAT, vPA, vTP, vLeP, vRS, vMods]]
#   Alwine
vStrings = ['Alwine\t\t', 'Morgenstern', 'Armbrust', 'direkt\t']
vAT = np.array([13, 18, 0])
vPA = np.array([15, 0, 0])
vTP = np.array([(1, 5), (1, 6), (0, 0)])
vLeP = 20
vRS = 2
vMods = np.array([0, 0, 0, 0, 0])
#vEnemies += [[vStrings, vAT, vPA, vTP, vLeP, vRS, vMods]]
#   Beresch
vStrings = ['Beresch\t\t', 'Lindwurmschläger', 'Armbrust', 'direkt\t']
vAT = np.array([14, 15, 0])
vPA = np.array([11, 0, 0])
vTP = np.array([(1, 6), (1, 4), (0, 0)])
vLeP = 42
vRS = 5
vMods = np.array([0, 0, 0, 0, 0])
#vEnemies += [[vStrings, vAT, vPA, vTP, vLeP, vRS, vMods]]
#   Geschmine
vStrings = ['Geschmine\t', 'Zweihänder', 'direkt\t']
vAT = np.array([13, 0])                     # Zweihänder        
vPA = np.array([11, 0])
vTP = np.array([(2, 3), (0, 0)])
vLeP = 17
vRS = 2
vMods = np.array([0, 0, 0, 0, 0])
vEnemies += [[vStrings, vAT, vPA, vTP, vLeP, vRS, vMods]]
#   Alrik
vStrings = ['Alrik\t\t', 'Schwert', 'direkt\t']
vAT = np.array([16, 0])
vPA = np.array([12, 0])
vTP = np.array([(1, 5), (0, 0)])
vLeP = 35
vRS = 4
vMods = np.array([0, 0, 0, 0, 0])
vEnemies += [[vStrings, vAT, vPA, vTP, vLeP, vRS, vMods]]
#   Perainidan
vStrings = ['Perainidan\t', 'Rapier', 'Armbrust', 'direkt\t']
vAT = np.array([14, 19, 0])
vPA = np.array([13, 0, 0])
vTP = np.array([(1, 3), (1, 6), (0, 0)])
vLeP = 31
vRS = 3
vMods = np.array([0, 0, 0, 0, 0])
vEnemies += [[vStrings, vAT, vPA, vTP, vLeP, vRS, vMods]]

 #   Terkol
vStrings = ['Terkol\t\t', 'Schwert', 'direkt\t']
vAT = np.array([15, 0])          # Schwert
vPA = np.array([13, 0])
vTP = np.array([(1, 5), (0 , 0)])
vLeP = 35
vRS = 4
vMods = np.array([0, 0, 0, 0, 0])
#vEnemies += [[vStrings, vAT, vPA, vTP, vLeP, vRS, vMods]]

 #   Sordul
vStrings = ['Sordul\t\t', 'Krallen', 'Biss\t', 'direkt\t']
vAT = np.array([12, 16, 0])          # Krallen
vPA = np.array([8, 9, 0])
vTP = np.array([(2, 2), (1, 8), (0, 0)])
vLeP = 40
vRS = 3
vMods = np.array([0, 0, 0, 0, 0])
#vEnemies += [[vStrings, vAT, vPA, vTP, vLeP, vRS, vMods]]

 #   Leichname
vStrings = ['Leichname\t', 'Säbel\t', 'direkt\t']
vAT = np.array([10, 0])          # Säbel
vPA = np.array([5, 0])
vTP = np.array([(1, 4), (0, 0)])
vLeP = 20
vRS = 3
vMods = np.array([0, 0, 0, 0, 0])
vEnemies += [[vStrings, vAT, vPA, vTP, vLeP, vRS, vMods]]
 #   Skelette
vStrings = ['Skelette\t\t', 'Schwert', 'direkt\t']
vAT = np.array([10, 0])          # Schwert
vPA = np.array([8, 0])
vTP = np.array([(1, 4), (0, 0)])
vLeP = 15
vRS = 2
vMods = np.array([0, 0, 0, 0, 0])
#vEnemies += [[vStrings, vAT, vPA, vTP, vLeP, vRS, vMods]]
 #   Skelett mit RS
vStrings = ['Skelett mit RS', 'Zweihänder', 'direkt\t']
vAT = np.array([13, 0])          # Zweihänder
vPA = np.array([10, 0])
vTP = np.array([(2, 2), (0, 0)])
vLeP = 15
vRS = 8
vMods = np.array([0, 0, 0, 0, 0])
#vEnemies += [[vStrings, vAT, vPA, vTP, vLeP, vRS, vMods]]

 #   Goblins
vStrings = ['Goblins\t\t', 'Knüppel', 'direkt\t']
vAT = np.array([7, 0])          # Knüppel
vPA = np.array([6, 0])
vTP = np.array([(1, 2), (0, 0)])
vLeP = 12
vRS = 1
vMods = np.array([0, 0, 0, 0, 0])
#vEnemies += [[vStrings, vAT, vPA, vTP, vLeP, vRS, vMods]]
 #   Goblinskaempfer
vStrings = ['Goblinkaempfer\t', 'Saebel\t', 'direkt\t']
vAT = np.array([11, 0])          # Säbel
vPA = np.array([10, 0])
vTP = np.array([(1, 3), (0, 0)])
vLeP = 16
vRS = 2
vMods = np.array([0, 0, 0, 0, 0])
#vEnemies += [[vStrings, vAT, vPA, vTP, vLeP, vRS, vMods]]
 #   Jamuutar
vStrings = ['Jamuutar\t\t', 'Knochenkeule', 'direkt\t']
vAT = np.array([8, 0])          # Knochenkeule
vPA = np.array([7, 0])
vTP = np.array([(1, 3), (0, 0)])
vLeP = 12
vRS = 1
vMods = np.array([0, 0, 0, 0, 0])
#vEnemies += [[vStrings, vAT, vPA, vTP, vLeP, vRS, vMods]]


 #   Heshthot
vStrings = ['Heshthot\t', 'Peitsche', 'Schwert', 'direkt\t']
vAT = np.array([14, 13, 0])
vPA = np.array([9, 9, 0])
vTP = np.array([(1, 0), (1, 4), (0, 0)])
vLeP = 20
vRS = 2
vMods = np.array([0, 0, 0, 0, 0])
#vEnemies += [[vStrings, vAT, vPA, vTP, vLeP, vRS, vMods]]

 #   Sharbazz
vStrings = ['Sharbazz', 'Säbel\t', 'Tritt\t', 'direkt\t']
vAT = np.array([16, 12, 0])
vPA = np.array([14, 14, 0])
vTP = np.array([(2, 6), (1, 3), (0, 0)])
vLeP = 70
vRS = 4
vMods = np.array([0, 0, 0, 0, 0])
#vEnemies += [[vStrings, vAT, vPA, vTP, vLeP, vRS, vMods]]

 #   Zant
vStrings = ['Zant\t\t', 'Pranke', 'Biss\t', 'Schwanz', 'direkt\t']
vAT = np.array([15, 12, 12, 0])
vPA = np.array([8, 8, 8, 0])
vTP = np.array([(1, 4), (2, 2), (1, 2), (0, 0)])
vLeP = 30
vRS = 3
vMods = np.array([0, 0, 0, 0, 0])
#vEnemies += [[vStrings, vAT, vPA, vTP, vLeP, vRS, vMods]]


for u in range(0, len(vFighters)):
    print(getOutFighter(vFighters[u][0]))
    for i in range(0, len(vEnemies)):
        vAtt, vDef = calValues(vFighters[u], vEnemies[i])
        print(getOutValues(vFighters[u][0], vEnemies[i][0], vAtt, vDef))
    print('\n\n')

