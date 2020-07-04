#!/usr/bin/env python
# coding: utf-8

# Kleines Script um zu berechnen, wie viele Beschwoerungen ein Charakter in
#     eienr gegeben Spielzeit in Tagen beschworen bekommt.
#
# Dabei berücksichtigt das Script die Regenration des Charakters und fuehrt die
#     entsprechenden Beschwoerungsproben durch, und gibt deren Erfolg, oder
#     Misserfolg aus.


import numpy as np
import matplotlib as plt
from random import randint as throw


def fProofAttribute(pValue):
    if pValue < throw(1, 20):
        return False
    else:
        return True
def fgetCastValue(pCast):
    vRet = []
    if pCast == 'Manifesto':
        vRet = (zManifesto, zKl, zIn, zCh)
    elif pCast == 'Dschinruf':
        vRet = (zDschinruf, zMu, zKl, zCh)
    else:
        print('Error: Wrong Castname!')
        
    return vRet
    
def fProofMeditationSuccess():
    vRet, vRit = True, zRitualkenntnis
    vThrow0, vThrow1, vThrow2 = throw(1, 20), throw(1, 20), throw(1, 20)
    vHoleThrow = np.array([vThrow0, vThrow1, vThrow2])
    
    if vThrow0 > zIn:
        vRit = vRit - (vThrow0 - zIn)
    if vThrow1 > zCh:
        vRit = vRit - (vThrow1 - zCh)
    if vThrow2 > zKo:
        vRit = vRit - (vThrow2 - zKo)
        
    if len(vHoleThrow[vHoleThrow == 20]) == 2:
        vRet = False
        print('Kritischer Misserfolg bei einer Ritualkenntnis-Probe!')
    elif len(vHoleThrow[vHoleThrow == 1]) == 2:
        print('Kritischer Erfolg bei einer Ritualkenntnis-Probe!')
    elif vRit < 0:
        vRet = False
        
    return vRet

def fProccedCast(pCast, pMod):
    vCastValue, vAttValue0, vAttValue1, vAttValue2 = fgetCastValue(pCast)
    vRet = vCastValue - pMod
    vThrow0, vThrow1, vThrow2 = throw(1, 20), throw(1, 20), throw(1, 20)
    vHoleThrow = np.array([vThrow0, vThrow1, vThrow2])
    
    if vRet < 0:
        vMali = -vRet
    else:
        vMali = 0
    
    if vThrow0 > vAttValue0 - vMali:
        vRet = vRet - (vThrow0 - vAttValue0 + vMali)
    if vThrow1 > vAttValue1 - vMali:
        vRet = vRet - (vThrow1 - vAttValue1 + vMali)
    if vThrow2 > vAttValue2 - vMali:
        vRet = vRet - (vThrow2 - vAttValue2 + vMali)
        
    if vRet >= vCastValue - pMod:
        vRet = 0
        
    if len(vHoleThrow[vHoleThrow == 20]) == 2:
        if vRet > 0:
            vRet = -15
        print('Kritischer Misserfolg bei einer {}-Probe!'.format(pCast))
    elif len(vHoleThrow[vHoleThrow == 1]) == 2:
        if vRet < 0:
            vRet += 15
        print('Kritischer Erfolg bei einer {}-Probe!'.format(pCast))
        
    if vRet > vCastValue:
        vRet = vCastValue
        
    return vRet
def fProofControl(pMod):
    if throw(1, 20) < (zKontroll - pMod):
        return True
    else:
        return False


def fProccedRegeneration(pCurLeP, pCurAsP):
    vCurLeP, vCurAsP = pCurLeP, pCurAsP
    vAddLeP, vAddAsP = throw(1, 6), 11
    
    if fProofMeditationSuccess() == True:
        vAddAsP += 3
        vAddLeP += -(3 + throw(0, 2))
    else:
        vAddLeP += -(3 + throw(0, 2))/2
        
    if fProofAttribute(zKo):
        vAddLeP += 1
    if fProofAttribute(zIn):
        vAddAsP += 1
        
    if vCurLeP + vAddLeP < zMaxLeP:
        vCurLeP += vAddLeP
    elif vCurLeP < zMaxLeP:
        vCurLeP = zMaxLeP
            
    if vCurAsP + vAddAsP < zMaxAsP:
        vCurAsP += vAddAsP
    elif vCurAsP < zMaxAsP:
        vCurAsP = zMaxAsP
        
    return vCurLeP, vCurAsP        
    
def fProccedInvocation(pCurAsP):
    vAsP = 0
    
    vZfP = 0
    while (vZfP < 24) and ((vAsP + 30 + 2) <= pCurAsP):
        vTemp = fProccedCast('Manifesto', -4)
        
        if vTemp >= 0:
            vZfP += vTemp
            vAsP += 2
        else:
            vAsP += 1
    
    vZfP = fProccedCast('Dschinruf', 2)
    if (vZfP < 0) and ((vAsP + 30) > pCurAsP):
        if (vZfP < 0):
            vAsP += 15
        else:
            vAsP = pCurAsP
        print('Dschinruf fehlgeschlagen, ...')
    else:
        vAsP += 29
        vZfP += 30
        
        vTemp = False
        while (vTemp == False) and (vZfP >= 7):
            vTemp = fProofControl(-1)
            vZfP = vZfP - 7
            if vTemp == False:
                print('Beherrschungsprobe zur Bindung fehlgeschlagen, ...')
            if (vTemp == True) and (vZfP < 7):
                print('Erzdschinbeschworen; {} eAsP übrig.'.format(vZfP))
        
        if vZfP >= 7:
            vTemp = fProofControl(-1)
            if vTemp == False:
                print('Beherrschungsprobe zum Kampf fehlgeschlagen, ...')
            else:
                #vTemp = np.trunc(vZfP/7)
                #vZfP += -(7*vTemp)
                #print('Erzdschinbeschworen für {} Gegner; {} eAsP übrig.'.format(vTemp, vZfP))
            
                print('Erzdschinbeschworen; {} eAsP übrig.'.format(vZfP))
            
    return vAsP


def fProccedDays(pDays, pCurLeP, pCurAsP):
    vCurLeP, vCurAsP = pCurLeP, pCurAsP
    
    for i in range(0, pDays):
        vCurLeP, vCurAsP = fProccedRegeneration(vCurLeP, vCurAsP)
        
        if vCurAsP >= 38:
            vCurAsP = fProccedInvocation(vCurAsP)
    
    return vCurLeP, vCurAsP


zMu, zKl, zIn, zCh = 14, 14, 15, 14
zFf, zGe, zKo, zKk = 12, 11, 9, 12
zMaxLeP, zMaxAsP = 25, 43
zRitualkenntnis, zManifesto, zDschinruf, zKontroll = 12, 15, 17, 14


fProccedDays(8, 25, 23)



