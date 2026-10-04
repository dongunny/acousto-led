# -*- coding: utf-8 -*-
import os
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'figures'); os.makedirs(OUT,exist_ok=True)
import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams['font.family']='Noto Sans CJK JP'; plt.rcParams['axes.unicode_minus']=False
INK='#131313'; NAVY='#131313'; AMB='#6e6e6e'; RED='#9a9a9a'; MUT='#b0b0b0'; GRID='#dcdcdc'; LB='#b0b0b0'

# ── 도식6 : BOM 구조
fig,ax=plt.subplots(1,2,figsize=(11.4,3.86),gridspec_kw={'width_ratios':[1.35,1]})
items=[('기구·PCB·PMIC·조립\n(추정)',100),('ITO 전극 2층',7),('PVDF-TrFE 압전 재료',10),
       ('ToF 트래킹 모듈',8),('제어 FPGA',25),('144채널 HV 구동단\n(단가 대용값)',314),('Micro-LED 패널 15.6" 4K',2745)]
lab=[i[0] for i in items]; val=[i[1] for i in items]
col=['#bdbdbd','#bdbdbd','#7a7a7a','#bdbdbd','#bdbdbd','#7a7a7a','#131313']
b=ax[0].barh(range(len(val)),val,color=col,height=.62)
ax[0].set_yticks(range(len(val))); ax[0].set_yticklabels(lab,fontsize=8)
ax[0].set_xscale('log'); ax[0].set_xlim(3,26000)
for i,v in enumerate(val):
    ax[0].text(v*1.15,i,f'${v:,}  ({v/3209*100:.1f}%)',va='center',fontsize=8,color=INK)
ax[0].set_xlabel('패널당 원가 [USD, 로그 눈금]',fontsize=8.5)
ax[0].tick_params(labelsize=8); ax[0].grid(True,axis='x',color=GRID,lw=.6); ax[0].set_axisbelow(True)
ax[0].set_title('(a) 패널당 BOM 실단가 — 합계 약 $3,209',fontsize=10.5,color=INK,fontweight='bold',pad=6)

names=['Micro-LED 구성\n(최종 목표 제품)','기존 패널 + 압전 레이어\n(1단계 사업화)']
panel=[2745,35]; audio=[464,464]
x=np.arange(2)
ax[1].bar(x,panel,color='#c4c4c4',width=.5,label='패널',edgecolor='#7a7a7a',linewidth=.6)
ax[1].bar(x,audio,bottom=panel,color='#131313',width=.5,label='음향 레이어 + 제어')
for i,(p_,a_) in enumerate(zip(panel,audio)):
    ax[1].text(i,p_+a_+120,f'${p_+a_:,}',ha='center',fontsize=10,fontweight='bold',color=INK)
ax[1].set_xticks(x); ax[1].set_xticklabels(names,fontsize=8.5)
ax[1].set_ylim(0,3800); ax[1].set_ylabel('패널당 BOM [USD]',fontsize=8.5)
ax[1].tick_params(labelsize=8); ax[1].grid(True,axis='y',color=GRID,lw=.6); ax[1].set_axisbelow(True)
ax[1].legend(fontsize=8,loc='upper right',framealpha=.95,fancybox=False,edgecolor='#c8c8c8')
ax[1].set_title('(b) 원가의 85.5%는 패널이 만든다',fontsize=10.5,color=INK,fontweight='bold',pad=6)
fig.tight_layout(pad=1.0,rect=[0,0,1,0.895])
fig.text(0.008,0.975,'도식 6. 패널당 예비 BOM 구조 — 유통 실단가 기준',fontsize=13,fontweight='bold',color=INK,va='top')
fig.text(0.008,0.917,'원가의 대부분은 Micro-LED 패널이 만든다. 음향 레이어를 얹는 1단계 구성이 성립하는 이유다',fontsize=9,color='#454545',va='top')
fig.savefig(f'{OUT}/도식6_BOM구조.png',dpi=200,bbox_inches='tight',facecolor='white')

# ── 도식7 : 단위 경제
fig2,ax2=plt.subplots(1,2,figsize=(11.4,3.86))
fx=np.linspace(1e6,20e6,300); asp,bomv=1200,499
cm=asp-bomv-asp*0.10
ax2[0].plot(fx/1e6,fx/cm/1000,color=NAVY,lw=2.2)
for f in [2e6,5e6,10e6]:
    ax2[0].plot([f/1e6],[f/cm/1000],'o',color=AMB,ms=6)
    ax2[0].annotate(f'{f/1e6:.0f}M USD → {f/cm:,.0f}대',(f/1e6,f/cm/1000),
                    textcoords='offset points',xytext=(9,-3),fontsize=8,color=INK)
ax2[0].set_xlabel('연간 고정비 [USD M]',fontsize=8.5); ax2[0].set_ylabel('손익분기 물량 [천 대]',fontsize=8.5)
ax2[0].grid(True,color=GRID,lw=.6); ax2[0].set_axisbelow(True); ax2[0].tick_params(labelsize=8)
ax2[0].set_title('(a) 손익분기 물량  (ASP 1,200 · BOM 499 USD · 판관비 10%)',fontsize=10,color=INK,fontweight='bold',pad=6)
ax2[0].text(11.5,3.2,f'단위 공헌이익 {cm:.0f} USD',fontsize=8.5,color=NAVY,fontweight='bold')

gm=np.linspace(.30,.60,200)
for bv,c_,lb_ in [(499,NAVY,'1단계 BOM 499 USD'),(3209,RED,'Micro-LED BOM 3,209 USD')]:
    ax2[1].plot(gm*100,bv/(1-gm),color=c_,lw=2.2,label=lb_)
ax2[1].axhline(1200,color=AMB,lw=1.3,ls='--')
ax2[1].text(31,1310,'1단계 목표 ASP 1,200 USD',fontsize=8,color=AMB)
ax2[1].set_yscale('log'); ax2[1].set_ylim(600,12000)
ax2[1].set_xlabel('BOM 대비 차액률 [%]',fontsize=8.5); ax2[1].set_ylabel('필요 ASP [USD, 로그]',fontsize=8.5)
ax2[1].grid(True,color=GRID,lw=.6); ax2[1].set_axisbelow(True); ax2[1].tick_params(labelsize=8)
ax2[1].legend(fontsize=8,loc='upper left',framealpha=.95,fancybox=False,edgecolor='#c8c8c8')
ax2[1].set_title('(b) BOM이 정하는 가격 하한',fontsize=10,color=INK,fontweight='bold',pad=6)
fig2.tight_layout(pad=1.0,rect=[0,0,1,0.895])
fig2.text(0.008,0.975,'도식 7. 단위 경제 — 손익분기 물량과 BOM이 정하는 가격 하한',fontsize=13,fontweight='bold',color=INK,va='top')
fig2.text(0.008,0.917,'ASP 1,200 USD는 1단계 BOM 499 USD 위에서만 성립한다. Micro-LED BOM으로는 같은 가격이 나오지 않는다',fontsize=9,color='#454545',va='top')
fig2.savefig(f'{OUT}/도식7_단위경제.png',dpi=200,bbox_inches='tight',facecolor='white')

from PIL import Image
for p in ['도식6_BOM구조','도식7_단위경제']:
    im=Image.open(f'{OUT}/{p}.png'); print(p, im.size, round(im.size[0]/im.size[1],4))
