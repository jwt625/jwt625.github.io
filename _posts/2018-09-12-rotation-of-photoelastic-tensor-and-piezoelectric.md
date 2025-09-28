---
categories:
- Tutorial
date: '2025-09-27'
original_date: '2018-09-12'
tags:
- Lithium Niobate
- Materials
- Piezoelectric
- Simulation
- Reference
title: Rotation of photoelastic and piezoelectric tensor
toc: true
toc_sticky: True
use_math: true
header:
  cover: /assets/images/imported/rotation-of-photoelastic-tensor-and-piezoelectric-20180912/image7.png
  overlay_image: /assets/images/imported/rotation-of-photoelastic-tensor-and-piezoelectric-20180912/image7.png
  show_overlay_excerpt: false
  overlay_filter: 0.5
---

( originally written on 2018-09-12, converted on 2025-09-27. )


# Reproduce Jasper's results:
P. 97 of Jasper Chan's thesis:

![Image 14](/assets/images/imported/rotation-of-photoelastic-tensor-and-piezoelectric-20180912/image14.png)

## Carry out the equation (C.2) using Mathematica online (<https://sandbox.open.wolframcloud.com>):
You could run your code but can't save the notebook/results.
## Code used:
You should be able to reproduce all the results if you copy-paste the following code
- pmat=\{\{p11,p12,p12,0,0,0},{p12,p11,p12,0,0,0},{p12,p12,p11,0,0,0},{0,0,0,p44,0,0},{0,0,0,0,p44,0},{0,0,0,0,0,p44\}\};
- pmat//MatrixForm
- (* generate the 3 by 3 by 3 by 3 PE tensor *)
- pt1={0,0,0};
- pt2={pt1,pt1,pt1};
- pt3={pt2,pt2,pt2};
- ptensor={pt3,pt3,pt3};
- ptensor//MatrixForm
- For\ii=1,ii\<=3,ii++,
- For[jj=1,jj\<=3,jj++,
- For[kk=1,kk\<=3,kk++,
- For[ll=1,ll\<=3,ll++,
- If[ii==jj,ij=ii,ij=9-ii-jj\;
- If\kk==ll,kl=kk,kl=9-kk-ll\;
- ptensor\[ii,jj,kk,ll\]=pmat\[ij,kl\];
- ]]]]
- ptensor//MatrixForm
- rotmz=RotationMatrix\\\[Theta\,{0,0,1}];
- rotmz//MatrixForm
- (* checking MMA's TensorProduct, as expected *)
- tmpmat=TensorProduct\\{\{a11,a12},{a21,a22\}\},\{\{b11,b12},{b21,b22\}\}\;
- tmpmat//MatrixForm
- tmpmat\[1,2,2,1\]
- (* check TensorContract *)
- TensorContract\tmpmat,{1,2}\//MatrixForm
- TensorContract\tmpmat,{2,3}\//MatrixForm
- (* carry out rotation *)
- ptensorR1=Simplify\TensorContract[TensorProduct[rotmz,ptensor\,{2,6}]];
- ptensorR2=Simplify\TensorContract[TensorProduct[rotmz,ptensorR1\,{2,6}]];
- ptensorR3=Simplify\TensorContract[TensorProduct[rotmz,ptensorR2\,{2,6}]];
- ptensorR4=Simplify\TensorContract[TensorProduct[rotmz,ptensorR3\,{2,6}]];
- (* convert back to Voigt notation *)
- pmr1={0,0,0,0,0,0};
- pmatrot={pmr1,pmr1,pmr1,pmr1,pmr1,pmr1};
- pmatrot//MatrixForm
- iiarray={1,2,3,2,3,1};
- jjarray={1,2,3,3,1,2};
- For\ij=1,ij\<=6,ij++,
- For[kl=1,kl\<=6,kl++,
- ii=iiarray[[ij\];jj=jjarray\[ij\];kk=iiarray\[kl\];ll=jjarray\[kl\];
- pmatrot\[ij,kl\]=ptensorR4\[ii,jj,kk,ll\]
- ]]
- pmatrot//MatrixForm
## Results:

![Image 7](/assets/images/imported/rotation-of-photoelastic-tensor-and-piezoelectric-20180912/image7.png)

![Image 3](/assets/images/imported/rotation-of-photoelastic-tensor-and-piezoelectric-20180912/image3.png)

Agree with Jasper's results except a minus sign for theta, i.e., he actually means rotating the crystal and calculating the rotated PE tensor in the global coordinates.
# Now is the time for LN
The code above is now formulated as functions:
pmat2ptensor: convert from Voigt notation to rank 4 (3x3x3x3) tensor
ptensor2pmat: rank 4 tensor to Voigt notation matrix
rotptensor\ptensor, rotm\: take a 3x3x3x3 tensor and rotate by a 3x3 rotm matrix.
- pmat2ptensor=(
- pmat=#1;
- pt1={0,0,0};
- pt2={pt1,pt1,pt1};
- pt3={pt2,pt2,pt2};
- ptensor={pt3,pt3,pt3};
- For\ii=1,ii\<=3,ii++,
- For[jj=1,jj\<=3,jj++,
- For[kk=1,kk\<=3,kk++,
- For[ll=1,ll\<=3,ll++,
- If[ii==jj,ij=ii,ij=9-ii-jj\;
- If\kk==ll,kl=kk,kl=9-kk-ll\;
- ptensor\[ii,jj,kk,ll\]=pmat\[ij,kl\];
- ]]]];
- ptensor
- )&;
- ptensor2pmat=(
- ptensor=#1;
- pmr1={0,0,0,0,0,0};
- pmatrot={pmr1,pmr1,pmr1,pmr1,pmr1,pmr1};
- iiarray={1,2,3,2,3,1};
- jjarray={1,2,3,3,1,2};
- For\ij=1,ij\<=6,ij++,
- For[kl=1,kl\<=6,kl++,
- ii=iiarray[[ij\];jj=jjarray\[ij\];kk=iiarray\[kl\];ll=jjarray\[kl\];
- pmatrot\[ij,kl\]=ptensor\[ii,jj,kk,ll\]
- ]];
- pmatrot)&;
- rotptensor=(ptensor=#1;rotm=#2;
- ptensorR1=Simplify\TensorContract[TensorProduct[rotm,ptensor\,{2,6}]];
- ptensorR2=Simplify\TensorContract[TensorProduct[rotm,ptensorR1\,{2,6}]];
- ptensorR3=Simplify\TensorContract[TensorProduct[rotm,ptensorR2\,{2,6}]];
- ptensorR4=Simplify\TensorContract[TensorProduct[rotm,ptensorR3\,{2,6}]];
- ptensorR4
- )&;
## Notes on rotated coordinate in COMSOL:
- first of all, the Euler angles are ZXZ convention, supported in Mathematica but not in MATLAB (I have to manually make up the matrix in MATLAB)
- In COMSOL, the Euler rotation rotates the coordinates, hence the same matrix rotates quantities in rotated coordinates to the global coordinates.
- What I used to do: To get rid of rotating the PE tensor, I work in the rotated(local/material) coordinates for PE expression calculation and I use the strain in the local coordinates which COMSOL offers me. The rotation I need is to rotate the EM fields in the global coordinates to the local coordinates, by the inverse of the Euler matrix.
- Now I'm trying to work in global coordinates hence I need to rotate the PE tensor, which I know in the local coordinates, to the global coordinates, hence it's the Euler matrix, no inversion.
## Rotation matrix for LNY + in-plane rotation theta:
- rotLNYinPlane=RotationMatrix\\\[Theta\,{0,0,1}].EulerMatrix\{-\\[Pi\/2,-\\\Pi\/2,\\\Pi\},{3,1,3}];
- rotLNYinPlane//MatrixForm

![Image 5](/assets/images/imported/rotation-of-photoelastic-tensor-and-piezoelectric-20180912/image5.png)

Checked that vector expressed in rotated/material coordinate system got correctly expressed in the global coordinate system.
## Rotated PE matrix in global coordinate:
OH MY GOD:

![Image 6](/assets/images/imported/rotation-of-photoelastic-tensor-and-piezoelectric-20180912/image6.png)

Now I want to convert this to matlab expression automatically for numeric evaluation. I don't want to type it.
Yes I have it now:
- (* convert mma vector to matlab row vector*)
- mma2matlab=(
- mmaexpr=#1;
- inputstr=ToString\mmaexpr/.{\\[Theta\-\>theta},InputForm];
- matlabstr=StringReplace\inputstr,{\"Sin\"-\>\"sin\",\"Cos\"-\>\"cos\",\"[\"-\>\"(\",\"\\"-\>\")\",\"{\"-\>\"\\",\"}\"-\>\"\\"}])&;
- (*convert mma matrix to matlab matrix*)
- mma2matlabFullMat=(
- mmaMat=#1;
- dim=Dimensions\mmaMat\;
- nRow=dim\[1\];
- matlabstr=\"\\";
- For[ii=1,ii\<nRow,ii++,
- matlabstr=matlabstr\<\>mma2matlab[mmaMat[[ii,;;\]]\<\>\";\";];
- matlabstr=matlabstr\<\>mma2matlab\mmaMat[[nRow,;;\]]\<\>\"]\"
- )&;
## Final results:
- mma2matlabFullMat\pmatLNRotLNYinPlane\ =
- \[p33*cos(theta)\^4+(p13+p31)*cos(theta)\^2*sin(theta)\^2+p11*sin(theta)\^4+p44*sin(2*theta)\^2,p31*cos(theta)\^4+(p11+p33-4*p44)*cos(theta)\^2*sin(theta)\^2+
- p13*sin(theta)\^4,p31*cos(theta)\^2+p12*sin(theta)\^2,-2*p41*cos(theta)\^2*sin(theta)+p14*sin(theta)\^3,(p14+2*p41)*cos(theta)*sin(theta)\^2,cos(theta)*sin(theta)*((-p31+
- p33)*cos(theta)\^2-2*p44*cos(2*theta)+(-p11+p13)*sin(theta)\^2)\;\p13*cos(theta)\^4+(p11+p33)*cos(theta)\^2*sin(theta)\^2+p31*sin(theta)\^4-p44*sin(2*theta)\^2,
- p11*cos(theta)\^4+(p13+p31)*cos(theta)\^2*sin(theta)\^2+p33*sin(theta)\^4+p44*sin(2*theta)\^2,p12*cos(theta)\^2+p31*sin(theta)\^2,(p14+2*p41)*cos(theta)\^2*sin(theta),
- p14*cos(theta)\^3-2*p41*cos(theta)*sin(theta)\^2,cos(theta)*sin(theta)*((-p11+p13)*cos(theta)\^2+2*p44*cos(2*theta)+(-p31+p33)*sin(theta)\^2)\;\p13*cos(theta)\^2+
- p12*sin(theta)\^2,p12*cos(theta)\^2+p13*sin(theta)\^2,p11,-(p14*sin(theta)),-(p14*cos(theta)),(-p12+p13)*cos(theta)*sin(theta)\;\-2*p14*cos(theta)\^2*sin(theta)+
- p41*sin(theta)\^3,(2*p14+p41)*cos(theta)\^2*sin(theta),-(p41*sin(theta)),((p11-p12)*cos(theta)\^2)/2+p44*sin(theta)\^2,((-p11+p12+2*p44)*cos(theta)*sin(theta))/2,
- cos(theta)*(p14*cos(2*theta)-p41*sin(theta)\^2)\;(2*p14+p41)*cos(theta)*sin(theta)\^2,p41*cos(theta)\^3-2*p14*cos(theta)*sin(theta)\^2,-(p41*cos(theta)),((-p11+p12+
- 2*p44)*cos(theta)*sin(theta))/2,p44*cos(theta)\^2+((p11-p12)*sin(theta)\^2)/2,-((p41*cos(theta)\^2+p14*cos(2*theta))*sin(theta))\;(-p13+p33-2*p44)*cos(theta)\^3*sin(theta)+
- (-p11+p31+2*p44)*cos(theta)*sin(theta)\^3,-((p11+p13-p31-p33+(p11-p13-p31+p33-4*p44)*cos(2*theta))*sin(2*theta))/4,(-p12+p31)*cos(theta)*sin(theta),
- p41*cos(theta)\^3-(p14+p41)*cos(theta)*sin(theta)\^2,-((p14+(p14+2*p41)*cos(2*theta))*sin(theta))/2,-(p44*cos(2*theta)*sin(theta)\^2)+cos(theta)\^2*(p44*cos(2*theta)+(p11-
- p13-p31+p33)*sin(theta)\^2)\]
## Rotated PE components:
PE components:

![Image 10](/assets/images/imported/rotation-of-photoelastic-tensor-and-piezoelectric-20180912/image10.png)

![Image 16](/assets/images/imported/rotation-of-photoelastic-tensor-and-piezoelectric-20180912/image16.png)

![Image 19](/assets/images/imported/rotation-of-photoelastic-tensor-and-piezoelectric-20180912/image19.png)

![Image 8](/assets/images/imported/rotation-of-photoelastic-tensor-and-piezoelectric-20180912/image8.png)

## In-plane rotation on LNX
rotLNX=EulerMatrix\{\\[Pi\/2,-\\\Pi\/2,-\\\Pi\/2},{3,1,3}];
rotLNXinPlane=RotationMatrix\\\[Theta\,{0,0,1}].rotLNX;
Corresponded ZXZ Euler angles:
- \theta-pi/2, pi/2, pi/2\
- theta is the x axis in the following plots
20181105, this is wrong!

![Image 15](/assets/images/imported/rotation-of-photoelastic-tensor-and-piezoelectric-20180912/image15.png)

Updated 20181106:

![Image 2](/assets/images/imported/rotation-of-photoelastic-tensor-and-piezoelectric-20180912/image2.png)

## At 45(wrong) 135 deg in-plane rotation:
\% from A. S. Andrushchak et. al, JOURNAL OF APPLIED PHYSICS 106, 073510 (2009).

![Image 13](/assets/images/imported/rotation-of-photoelastic-tensor-and-piezoelectric-20180912/image13.png)

For GaAs (from R.W.Dixon, Photoelastic Properties of Selected Materials..., 1967):

![Image 18](/assets/images/imported/rotation-of-photoelastic-tensor-and-piezoelectric-20180912/image18.png)

PE tensor of Si (from Jasper's thesis)

![Image 9](/assets/images/imported/rotation-of-photoelastic-tensor-and-piezoelectric-20180912/image9.png)

p11 = -0.021;   p12 = 0.06;     p13 = 0.172;    p14 = -0.052;
p31 = 0.141;    p33 = 0.118;    p41 = -0.109;   p44 = 0.121;
on LNX:
- p22' = (p11+p33+p13+p31+4*p44-2*p14-2*p41)/4 = 0.304
on LNY:
- p22' = (p11+p33+p13+p31+4*p44)/4 = 0.223
## Rotation of piezoelectric tensor, 180920
Functions:
- dmat2dtensor=(
- dmat=#1;
- dt1={0,0,0};
- dt2={dt1,dt1,dt1};
- dtensor={dt2,dt2,dt2};
- For\ii=1,ii\<=3,ii++,
- For[kk=1,kk\<=3,kk++,
- For[ll=1,ll\<=3,ll++,
- If[kk==ll,kl=kk;coef=1;,kl=9-kk-ll;coef=2;\;
- dtensor\[ii,kk,ll\]=dmat\[ii,kl\]/coef;
- ]]];
- dtensor
- )&;
- dtensor2dmat=(
- dtensor=#1;
- dmr1={0,0,0,0,0,0};
- dmat={dmr1,dmr1,dmr1};
- iiarray={1,2,3,2,3,1};
- jjarray={1,2,3,3,1,2};
- coefs={1,1,1,2,2,2};
- For\ii=1,ii\<=3,ii++,
- For[kl=1,kl\<=6,kl++,
- kk=iiarray[[kl\];ll=jjarray\[kl\];coef=coefs\[kl\];
- dmat\[ii,kl\]=dtensor\[ii,kk,ll\]*coef;
- ]];
- dmat)&;
- rotdtensor=(dtensor=#1;rotm=#2;
- dtensorR1=Simplify\TensorContract[TensorProduct[rotm,dtensor\,{2,5}]];
- dtensorR2=Simplify\TensorContract[TensorProduct[rotm,dtensorR1\,{2,5}]];
- dtensorR3=Simplify\TensorContract[TensorProduct[rotm,dtensorR2\,{2,5}]];
- dtensorR3
- )&;
Results for LNY in-plane rotation:

![Image 11](/assets/images/imported/rotation-of-photoelastic-tensor-and-piezoelectric-20180912/image11.png)

Bender effect is from d_ij where j \<= 3, i != j.
in-plane bending: d12 or d12
### Notes added on 20191111, WTJ
- theta = 0 here is Z parallel to x
- see <https://www.wolframcloud.com/obj/b93a29a1-2329-4c70-a0d4-e8f30a1213fb>
Using the nanobender paper convention (theta = 0 is X parallel to x):

![Image 17](/assets/images/imported/rotation-of-photoelastic-tensor-and-piezoelectric-20180912/image17.png)

Agree with FMM's simulation qualitatively:

![Image 12](/assets/images/imported/rotation-of-photoelastic-tensor-and-piezoelectric-20180912/image12.png)

Also checked the matlab code (getRotated_d_tensor_LNY.m)
- path: /user_data/wtjiang/COMSOL/LN/20191112_rotated_piezo

![Image 1](/assets/images/imported/rotation-of-photoelastic-tensor-and-piezoelectric-20180912/image1.png)

Results of LNX in-plane rotation

![Image 4](/assets/images/imported/rotation-of-photoelastic-tensor-and-piezoelectric-20180912/image4.png)

## 20190402, d16 components
d16 connects xy shear to x field

![Image 20](/assets/images/imported/rotation-of-photoelastic-tensor-and-piezoelectric-20180912/image20.png)

# 20200515, rotation of elasticity matrix