#!/usr/bin/env python3
"""Independent arithmetic checks of the main worked examples; no source value is trusted."""
import json, math, statistics
from pathlib import Path
root=Path(__file__).resolve().parent.parent
upgrade=json.loads((root/'pedagogy-upgrade-2026.json').read_text(encoding='utf8'))
def close(a,b,tol=5e-6):
    assert abs(a-b)<=tol,(a,b)
def regression(x,y):
    n=len(x); mx=sum(x)/n;my=sum(y)/n
    vx=sum((v-mx)**2 for v in x)/n
    vy=sum((v-my)**2 for v in y)/n
    cov=sum((a-mx)*(b-my) for a,b in zip(x,y))/n
    slope=cov/vx;intercept=my-slope*mx
    return slope,intercept,cov/math.sqrt(vx*vy)
# Chapter 1: complete distribution, unequal-width classes.
n=[4,12,32,32,60,35,25,5,5]
edges=[10,14,18,26,30,35,40,45,50,55]
assert sum(n)==210 and sum(n[:5])==140 and sum(n[5:])==70
assert [v/(edges[i+1]-edges[i]) for i,v in enumerate(n)]==[1,3,4,8,12,7,5,1,1]
# Chapter 2: grouped median, quartiles, and approximate mean.
close(30+5*(105-80)/60,32.0833333333)
close(26+4*(52.5-48)/32,26.5625)
close(35+5*(157.5-140)/35,37.5)
mid=[(a+b)/2 for a,b in zip(edges,edges[1:])]
close(sum(v*c for v,c in zip(n,mid)),6665)
close(sum(v*c*c for v,c in zip(n,mid)),227036.5)
# Chapter 3: population/sample variance and MAD.
x=[5,6,6,7,7,8,8,9,9,10,11,20]
close(sum(x),106);close(sum(v*v for v in x),1106)
mean=sum(x)/len(x)
close(sum(abs(v-mean) for v in x)/12,2.4722222222)
close(sum((v-mean)**2 for v in x)/12,14.1388888889)
close(sum((v-mean)**2 for v in x)/11,15.4242424242)
# Chapter 4: two-stage regressions and extrapolated sales.
t=[1,2,3,4,5,6];a=[4,5,7,8,10,11];y=[10,12,15,18,22,24]
a1,b1,r1=regression(t,a);a2,b2,r2=regression(a,y)
close(a1,1.45714285714);close(b1,2.4)
close(a2,2.01333333333);close(b2,1.73333333333)
close(a2*(a1*8+b1)+b2,30.035047619)
# Chapter 5: nine MA4, eight CMA4, trend, seasonal factors, 2022 forecast.
y=[40,52,48,68,44,58,53,76,50,65,60,84]
ma=[sum(y[i:i+4])/4 for i in range(9)]
cma=[(ma[i]+ma[i+1])/2 for i in range(8)]
close(sum(cma),462.375)
close(sum((i+3)*v for i,v in enumerate(cma)),3073.5)
slope,intercept,_=regression(list(range(3,11)),cma)
close(slope,1.620535714285714)
close(intercept,47.26339285714286)
ratios=[v/(slope*(i+1)+intercept) for i,v in enumerate(y)]
season=[sum(ratios[j::4])/3 for j in range(4)]
normalized=[4*v/sum(season) for v in season]
close(sum(normalized),4)
forecasts=[(slope*t+intercept)*normalized[(t-1)%4] for t in range(13,17)]
for a,b in zip(forecasts,[55.0316399695,71.4624455684,65.3927452618,92.1738602707]):close(a,b)
# Chapter 5 previous forecasting/validation: unrounded coefficients.
prev=[(6.343*t+86.939)*s for t,s in zip(range(13,17),[.789,.903,1.052,1.255])]
for a,b in zip(prev,[133.655022,158.694123,191.552368,236.475885]):close(a,b)
errors=[v-f for v,f in zip([136,162,188,245],prev)]
close(sum(abs(e) for e in errors)/4,4.43183475)
close(math.sqrt(sum(e*e for e in errors)/4),5.0425087)
# Chapter 6: four-product Fisher factor reversal.
p0=[53,41,75,25];q0=[20,28,35,30];p1=[62,52,82,38];q1=[25,34,38,33]
A=sum(p*q for p,q in zip(p0,q0));B=sum(p*q for p,q in zip(p1,q0))
C=sum(p*q for p,q in zip(p0,q1));D=sum(p*q for p,q in zip(p1,q1))
assert (A,B,C,D)==(5583,6706,6394,7688)
fp=math.sqrt(100*B/A*100*D/C);fq=math.sqrt(100*C/A*100*D/B)
close(fp*fq/100,100*D/A)
# Chapter 7: independent mock exam, regression and seasonal forecasts.
t=[1,2,3,4,5,6];x=[5,6,8,9,11,13];y=[12,15,18,20,24,29]
a1,b1,_=regression(t,x);a2,b2,_=regression(x,y)
close(a2*(a1*8+b1)+b2,34.331372549)
q=[72,88,80,110,78,96,88,121]
T=[2.8*t+78 for t in range(1,13)]
rat=[v/T[i] for i,v in enumerate(q)]
season=[(rat[j]+rat[j+4])/2 for j in range(4)]
norm=[4*v/sum(season) for v in season]
pred=[T[i]*norm[(i)%4] for i in range(8,12)]
for a,b in zip(pred,[88.9482436272,108.5090956186,98.5555461055,134.8782293694]):close(a,b)
# Assert that both language versions actually print the validated values.
for lang in ('fr','en'):
    assert '30.035048' in upgrade['4'][lang]['solutionAdd']['E5']
    assert '55.0316' in upgrade['5'][lang]['solutionAdd']['E5']
    assert '137.703744' in upgrade['6'][lang]['solutionAdd']['E4']
    assert '34.331373' in upgrade['7'][lang]['solutionReplace']['CB']
    assert '134.8782' in upgrade['7'][lang]['solutionReplace']['CB']
print('PASS: independent arithmetic checks, two-stage regressions, time-series, grouped statistics and Fisher indices in FR/EN')
