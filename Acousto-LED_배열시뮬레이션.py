# -*- coding: utf-8 -*-
import os
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'figures'); os.makedirs(OUT,exist_ok=True)
import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams['font.family']='Noto Sans CJK JP'; plt.rcParams['axes.unicode_minus']=False
INK='#131313'; NAVY='#131313'; AMB='#6e6e6e'; MUT='#b0b0b0'; GRID='#dcdcdc'
c=343.0; d=0.0216
def af(f,th,steer=0.0,pitch=d,N=16):
    n=(np.arange(N)-(N-1)/2)*pitch; k=2*np.pi*f/c
    ph=k*n[None,:]*(np.sin(np.radians(th))[:,None]-np.sin(np.radians(steer)))
    return np.abs(np.sum(np.exp(1j*ph),axis=1))/N
def db(x): return np.clip(20*np.log10(np.maximum(x,1e-12)),-40,None)
th=np.linspace(-90,90,4001)
def bw3(f,L):
    t=np.linspace(-90,90,24001); N=int(round(L/d))
    m=db(af(f,t,0,d,N)); i=np.where(m>=-3)[0]; return t[i[-1]]-t[i[0]]

fig,ax=plt.subplots(2,2,figsize=(11.4,6.28))
def style(a,ttl):
    a.set_xlim(-90,90); a.set_ylim(-40,3); a.set_xticks(np.arange(-90,91,30))
    a.grid(True,color=GRID,lw=.6); a.set_axisbelow(True)
    a.set_title(ttl,fontsize=10.5,color=INK,fontweight='bold',pad=6)
    a.set_xlabel('각도 [deg]',fontsize=8.5); a.set_ylabel('정규화 응답 [dB]',fontsize=8.5)
    a.tick_params(labelsize=7.5)

# (a) 2 kHz 조향
for s,col,ls in [(-30,MUT,'--'),(0,NAVY,'-'),(30,AMB,'-')]:
    ax[0,0].plot(th,db(af(2000,th,s)),color=col,lw=1.6,ls=ls,label=f'조향 {s:+d}°')
style(ax[0,0],'(a) 2 kHz — 지연만 바꿔 주엽을 옮긴다')
ax[0,0].legend(fontsize=7.5,loc='lower center',ncol=3,framealpha=.95,fancybox=False,edgecolor='#c8c8c8')

# (b) 7.9 kHz 조향
for s,col,ls in [(-30,MUT,'--'),(0,NAVY,'-'),(30,AMB,'-')]:
    ax[0,1].plot(th,db(af(7900,th,s)),color=col,lw=1.6,ls=ls)
style(ax[0,1],'(b) 7.9 kHz — 같은 조향, 주엽이 6.4°까지 좁아진다')

# (c) 피치 비교 @ 7.9 kHz, +30°
ax[1,0].plot(th,db(af(7900,th,30,d,16)),color=NAVY,lw=1.8,label='본 제안  d = 21.6 mm (16ch), d/λ = 0.50')
ax[1,0].plot(th,db(af(7900,th,30,0.115,3)),color='#6e6e6e',lw=1.5,label='소수 actuator  d = 115 mm (3ch), d/λ = 2.65')
ax[1,0].axvline(30,color=AMB,lw=1,ls=':')
style(ax[1,0],'(c) 왜 λ/2 인가 — 같은 +30° 조향, 다른 피치')
ax[1,0].legend(fontsize=7,loc='lower center',framealpha=.95,fancybox=False,edgecolor='#c8c8c8')

# (d) 빔폭 vs 주파수
fr=np.linspace(500,8000,260)
bh=np.array([bw3(f,0.3456) for f in fr]); bv=np.array([bw3(f,0.1944) for f in fr])
a=ax[1,1]
a.plot(fr/1000,bh,color=NAVY,lw=2,label='수평 (개구 345.6 mm)')
a.plot(fr/1000,bv,color=AMB,lw=2,label='수직 (개구 194.4 mm)')
a.axvspan(0.5,0.99,color='#e8e8e8',alpha=.5)
a.axvline(7.9,color=MUT,lw=1,ls=':')
for f in [1000,2000,7900]:
    v=bw3(f,0.3456); a.plot([f/1000],[v],'o',color=NAVY,ms=4.5)
    a.annotate(f'{f/1000:g}k  {v:.0f}°',(f/1000,v),textcoords='offset points',
               xytext=(7,7),fontsize=7.5,color=NAVY)
a.set_xlim(0.5,9.3); a.set_ylim(0,150); a.grid(True,color=GRID,lw=.6); a.set_axisbelow(True)
a.set_xlabel('주파수 [kHz]',fontsize=8.5); a.set_ylabel('3 dB 빔폭 [deg]',fontsize=8.5)
a.tick_params(labelsize=7.5); a.legend(fontsize=7.5,loc='upper right',framealpha=.95,fancybox=False,edgecolor='#c8c8c8')
a.set_title('(d) 개구가 정하는 지향성 한계',fontsize=10.5,color=INK,fontweight='bold',pad=6)
a.text(0.76,26,'빔포밍 하한 미만',fontsize=6.8,color='#6e6e6e',ha='left',va='center',rotation=90)
a.text(7.75,138,'λ/2 상한',fontsize=6.8,color=MUT,ha='right',va='top')

fig.tight_layout(pad=1.1,rect=[0,0,1,0.935])
fig.text(0.006,0.985,'도식 5. 16채널 선형 배열 시뮬레이션 — 조향 성능과 개구가 정하는 한계',fontsize=13,fontweight='bold',color=INK,va='top')
fig.text(0.006,0.951,'배열 계수 |AF(θ)|를 직접 계산한 결과다. 실측이 아니라 설계 수치의 자체 검증이다',fontsize=9,color='#454545',va='top')
fig.savefig(f'{OUT}/도식5_배열시뮬레이션.png',dpi=200,bbox_inches='tight',facecolor='white')
from PIL import Image
im=Image.open(f'{OUT}/도식5_배열시뮬레이션.png'); print(im.size, im.size[0]/im.size[1])
for f in [1000,2000,4000,7900]:
    print(f, round(bw3(f,0.3456),1), round(bw3(f,0.1944),1))
