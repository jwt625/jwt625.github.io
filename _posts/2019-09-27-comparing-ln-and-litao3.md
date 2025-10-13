---
categories:
- Tutorial
date: '2019-09-27'
original_date: '2019-09-27'
tags:
- Piezoelectric
- Simulation
title: Comparing LN and LiTaO3
toc: true
toc_sticky: true
use_math: true
---

( originally written on 2019-09-27, converted on 2025-10-12. )

Numbers are from COMSOL.
# Mechanics
## Elasticity
These are the upper right half matrix of the 6x6 voigt notation matrix
- ordered as E11, E12, E22, E13, \...
LTO:
- {2.32966e+011\Pa\, 4.68904e+010\Pa\, 2.32966e+011\Pa\, 8.02342e+010\Pa\, 8.02342e+010\Pa\, 2.75364e+011\Pa\, -1.10267e+010\Pa\, 1.10267e+010\Pa\, 0\Pa\, 9.38995e+010\Pa\, 0\Pa\, 0\Pa\, 0\Pa\, 0\Pa\, 9.38995e+010\Pa\, 0\Pa\, 0\Pa\, 0\Pa\, 0\Pa\, -1.10267e+010\Pa\, 9.3038e+010\Pa\}
LN:
- {2.02897e+011\Pa\, 5.29177e+010\Pa\, 2.02897e+011\Pa\, 7.49098e+010\Pa\, 7.49098e+010\Pa\, 2.43075e+011\Pa\, 8.99874e+009\Pa\, -8.99874e+009\Pa\, 0\Pa\, 5.99034e+010\Pa\, 0\Pa\, 0\Pa\, 0\Pa\, 0\Pa\, 5.99018e+010\Pa\, 0\Pa\, 0\Pa\, 0\Pa\, 0\Pa\, 8.98526e+009\Pa\, 7.48772e+010\Pa\}
## Density
LTO: 7450
LN: 4700
### Acoustic wave velocity sqrt(M/rho)
LTO: 5592 m/s
LN: 6570 m/s
## Piezoelectric d matrix
LTO:
- {0\C/N\, -7e-012\C/N\, -2e-012\C/N\,
- 0\C/N\, 7e-012\C/N\, -2e-012\C/N\,
- 0\C/N\, 0\C/N\, 8e-012\C/N\,
- 0\C/N\, 2.6e-011\C/N\, 0\C/N\,
- 2.6e-011\C/N\, 0\C/N\, 0\C/N\,
- -1.4e-011\C/N\, 0\C/N\, 0\C/N\}
LN:
- {0\C/N\, -2.1e-011\C/N\, -1e-012\C/N\,
- 0\C/N\, 2.1e-011\C/N\, -1e-012\C/N\,
- 0\C/N\, 0\C/N\, 6e-012\C/N\,
- 0\C/N\, 6.8e-011\C/N\, 0\C/N\,
- 6.8e-011\C/N\, 0\C/N\, 0\C/N\,
- -4.2e-011\C/N\, 0\C/N\, 0\C/N\}
Since the permittivities are similar, LTO is not as piezoelectric.