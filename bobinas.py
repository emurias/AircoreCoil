#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Enrique Murias Fernández
# Python 2.7
# CALCULADORA BOBINAS DE NÚCLEO DE AIRE

import math
import matplotlib

#Se definen las características del conductor

Res=float(8.282*(10**(-5))) 	#resistencia por unidad de longitud (Ω/cm)
d= float(1.62814) 		#unidades en mm
s= float(0.5)     		#separacion entre espiras en mm
p= (d+s)          		#paso en mm
n= float(10.0)        		#numero de espiras
l= (p*n)/10	        	#longitud bobina en cm
r= float(1.0)         		#radio bobina en cm  
eps0= float(8.8541878176) 	#permitividad magnetica vacio (pF/m) 
epsri= float(1.0)     		#permitividad relativa en el interior del solenoide
epsrx= float(1.0)     		#permitividad relativa fuera del solenoide
D= 2*r/100			#diametro bobina en m
f= float(30*(10**(6)))		#frecuencia de cálculo (Hz)

#ACLARACIONES
#En las bobinas de nucleo de aire las permitividades relativas son iguales 1

#Calculo del factor de Nagaoka

k= 1/(1+(float(0.9)*r/l)-((2*10**(-12))*((r/l)**2)))

#Factor de correccion espiras espaciadas
from math import log10
from math import pi
from math import cos
from math import atan
from math import sqrt

A= 2.3*log10(1.73*(d/p))
B= 0.336*(1-(2.5/n)+(3.8/n**2))
fcorr= (1-((l*(A+B))/(pi*r*n*k)))

#Inductancia

L= k*4*(((r**2)*(pi**2)*(n**2))/l)*10**(-3)*fcorr

#Angulo de paso
psi= atan((p/10)/(2*pi*r))

#Factor de correccion de David W. Knight, (kc)

kc= 0.717439*(D/(l/100))+0.933048*((D/(l/100))**(3/2))+0.106*((D/(l/100))**2)

#Self-capacitance

Cl=(((4*eps0*r)/pi)*(l/100)*(1+((kc*(1+epsri/epsrx))/2)))/(cos(psi)**2)

#Self-resonant frequency (SRF)

SRF=(1/(2*pi*sqrt(L*(10**(-6))*Cl*(10**(-12)))))/(10**(6))

#Resistencia serie equivalente ESR

R=0.672*(d/10)*r*n*Res*sqrt(f)

ESR= R/(1+(((2*pi*f)**2)*(R**2)*((Cl*10**(-12))**2))-(2*((2*pi*f)**2)*(L*10**(-6))*(Cl*10**(-12)))+((((2*pi*f)**2)*(L*10**(-6))*(Cl*10**(-12)))**2))

#Factor de calidad Q

Q=((2*pi*f)*(L*10**(-6)))/ESR

#Impedancia Z
Z=sqrt((ESR**2)+(((2*pi*f*(L*10**(-6)))-(1/(2*pi*f*(Cl*10**(-12)))))**2))

#Salida

print """
      ___      _ _             _            _       _             
 Air / __\ore (_) |   ___ __ _| | ___ _   _| | __ _| |_ ___  _ __ 
    / /  / _ \| | |  / __/ _` | |/ __| | | | |/ _` | __/ _ \| '__|
   / /__| (_) | | | | (_| (_| | | (__| |_| | | (_| | || (_) | |   
   \____/\___/|_|_|  \___\__,_|_|\___|\__,_|_|\__,_|\__\___/|_| 
    by Enrique Murias Fernández                                 v0.1

"""


print"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

print"""
      |<----l---->|                    _ L _         ESR
        __  __  __     ___      ------| |_| |_|----/\/\/\-------
       /  \/  \/  \     |          |                       |
   ___/  / \ / \ __\___ |D         |__________| |__________|
        /  //  //  /    |                     | |
        \_/ \_/ \_/    _|_                     Cl

"""
print"""~~~~~~~~~~~~~~~~~~~~~~~~~~DATOS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
print "\033[1;48mDiámetro del conductor (d):\033[1;m", "%23s" % d, "%5s" % "mm"
print "\033[1;48mSeparación entre espiras (s):\033[1;m", "%17s" % s, "%9s" % "mm"
print "\033[1;48mDiámetro bobina (D):\033[1;m", "%26s" % (2*r), "%9s" % "cm"
print "\033[1;48mNumero de espiras (N):\033[1;m", "%25s" % n, "%9s" % "rev"
print "\033[1;48mFrecuencia de cálculo (f):\033[1;m", "%27s" % f, "%2s" % "Hz"
print ""
print"""~~~~~~~~~~~~~~~~~~~~~~~~RESULTADOS~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
print "\033[1;31mInductancia (L):\033[1;m", "%40s" % L, "%3s" % "uH"
print "\033[1;31mCapacidad propia (Cl):\033[1;m", "%35s" % Cl, "%2s" % "pF"
print "\033[1;31mFrecuencia de autorresonancia (SRF):\033[1;m", "%20s" % SRF, "%4s" % "MHz"
print "\033[1;31mResistencia serie equivalente (ESR):\033[1;m", "%21s" % ESR, "%2s" % "Ω"
print "\033[1;31mFactor de calidad (Q):\033[1;m", "%34s" % Q
print "\033[1;31mImpedancia a freq. de cálculo (Z):\033[1;m", "%22s" % Z, "%3s" % "Ω"
print "\033[1;31mLongitud bobina (l):\033[1;m", "%36s" % l, "%3s" % "cm"

print"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


#En esta parte se sacan las graficas en funcion de la frecuencia de muestreo

import matplotlib.pyplot as plt 	#impota librerias
from numpy import *

x= linspace(178,181,10000000) 	#establece el rango del eje X y el numero de puntos
y= sqrt((((0.672*(d/10)*r*n*Res*sqrt((x*10**(6))))/(1+(((2*pi*(x*10**(6)))**2)*(R**2)*((Cl*10**(-12))**2))-(2*((2*pi*(x*10**(6)))**2)*(L*10**(-6))*(Cl*10**(-12)))+((((2*pi*(x*10**(6)))**2)*(L*10**(-6))*(Cl*10**(-12)))**2)))**2)+(((2*pi*(x*10**(6))*(L*10**(-6)))-(1/(2*pi*(x*10**(6))*(Cl*10**(-12)))))**2)) #funcion de la inductancia respecto a frecuencia 
plt.ylim((1*(10**3)),(1*(10**8)))	#limites del eje y
plt.xlim(178,181)			#limites del eje x
plt.semilogy()				#escala del eje y como logaritmica
plt.grid(True)				#pinta rejilla de fondo
plt.plot(x,y)				#grafica la funcion
plt.ylabel(u'Impedancia (ohm)')		#nombre eje y
plt.xlabel(u'Frecuencia (MHz)')		#nombre eje x
plt.show()				#muestra la gráfica
