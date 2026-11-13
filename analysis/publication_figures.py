import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import json, re, shutil, textwrap
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, Patch
from matplotlib.ticker import FuncFormatter, MaxNLocator
from PIL import Image, ImageOps, ImageDraw

PROJECT=Path(__file__).resolve().parents[1]
HOME=PROJECT
FIG=PROJECT/'figures'
WORK=HOME/'work/figure-redesign'
FIG.mkdir(parents=True,exist_ok=True);WORK.mkdir(parents=True,exist_ok=True)
E=PROJECT/'outputs/evidence'
q=pd.read_csv(E/'query_summary.csv')
c=pd.read_csv(E/'crud_summary.csv')
s=pd.read_csv(E/'storage_summary.csv')
r=pd.read_csv(E/'resource_summary.csv')
comp=pd.read_csv(E/'comparisons.csv')
q=q[q.n==10].copy();c=c[c.n==10].copy();r=r[r.n==10].copy()
COL={'mongodb':'#00856A','postgresql':'#285A86'}
MARK={'mongodb':'o','postgresql':'s'}
NAME={'mongodb':'MongoDB','postgresql':'PostgreSQL'}
SF=[.1,.5,1.]
plt.rcParams.update({
 'font.family':'STIXGeneral','font.size':8.2,'axes.labelsize':8,
 'axes.titlesize':8.8,'xtick.labelsize':7.2,'ytick.labelsize':7.2,
 'legend.fontsize':7.5,'axes.linewidth':.6,'lines.linewidth':1.35,
 'lines.markersize':4,'figure.facecolor':'white','axes.facecolor':'white',
 'savefig.facecolor':'white','pdf.fonttype':42,'svg.fonttype':'none',
 'xtick.major.width':.6,'ytick.major.width':.6,
})
records={};qa=[]
def clean(ax):
    ax.spines[['top','right']].set_visible(False)
    ax.spines[['left','bottom']].set_color('#7E8792')
    ax.grid(axis='y',color='#E2E6EA',linewidth=.5)
    ax.set_axisbelow(True)
    ax.tick_params(length=2.5,pad=3)
def axis_sf(ax,label=True):
    ax.set_xticks(SF,['0.1','0.5','1.0'])
    ax.set_xlim(.035,1.065)
    if label:ax.set_xlabel('Scale factor',labelpad=4)
def legends(fig,timeout=False,y=.985):
    handles=[Line2D([],[],color=COL[e],marker=MARK[e],label=NAME[e],lw=1.35,markersize=4) for e in COL]
    if timeout:handles.append(Line2D([],[],color='#777777',marker='^',markerfacecolor='white',ls='none',label='TO: 60 s limit',markersize=4.5))
    fig.legend(handles=handles,loc='upper center',bbox_to_anchor=(.54,y),ncol=2 if not timeout else 3,frameon=False,handlelength=1.5,columnspacing=1.1,handletextpad=.45,fontsize=7.2 if timeout else 7.6)
def save(fig,name,data):
    fig.canvas.draw()
    renderer=fig.canvas.get_renderer();fb=fig.bbox
    errors=[]
    # Check the layout objects that caused the reported clipping/overlap.
    texts=[]
    for ax in fig.axes:
        if not ax.axison: continue
        texts.extend([ax.title,ax.xaxis.label,ax.yaxis.label,*ax.get_xticklabels(),*ax.get_yticklabels()])
    texts.extend(fig.texts)
    for t in texts:
        if not t.get_visible() or not t.get_text():continue
        bb=t.get_window_extent(renderer)
        if bb.x0<fb.x0-2 or bb.y0<fb.y0-2 or bb.x1>fb.x1+2 or bb.y1>fb.y1+2:
            errors.append(t.get_text())
    titles=[ax.title.get_window_extent(renderer) for ax in fig.axes if ax.title.get_text()]
    overlap=any(a.overlaps(b) for i,a in enumerate(titles) for b in titles[i+1:])
    qa.append({'file':name,'outside_text':errors,'overlapping_panel_titles':overlap})
    fig.savefig(FIG/name,dpi=600)
    records[name]=data
    plt.close(fig)
def values(frame,engine,key,filters):
    g=frame[frame.engine==engine]
    for k,v in filters.items():g=g[g[k]==v]
    return [float(g[g.sf==sf].iloc[0][key]) if len(g[g.sf==sf]) else np.nan for sf in SF]
def curves(ax,frame,key,filters,log=False):
    clean(ax);axis_sf(ax)
    for engine in COL:
        ys=values(frame,engine,key,filters)
        ax.plot(SF,ys,color=COL[engine],marker=MARK[engine],label=NAME[engine])
    if log:
        ax.set_yscale('log')
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{v:g}' if v<1000 else f'{v/1000:g}k'))
    elif len(frame):
        ax.set_ylim(bottom=0)
        ax.yaxis.set_major_locator(MaxNLocator(nbins=4))
def queryplot(ax,query,mode,log=False,censor=False):
    curves(ax,q,'median_ms',{'query':query,'mode':mode},log)
    if censor:
        for engine in COL:
            ys=values(q,engine,'median_ms',{'query':query,'mode':mode})
            for sf,y in zip(SF,ys):
                if not np.isfinite(y):
                    # The supplied core comparison table identifies these as timeouts.
                    row=comp[(comp.sf==sf)&(comp['mode']==mode)&(comp['query']==query)]
                    assert len(row)==1
                    n=row.iloc[0]['mongo_n' if engine=='mongodb' else 'postgres_n']
                    assert n<10
                    shift=-.012 if engine=='mongodb' else .012
                    ax.plot(sf+shift,60000,marker='^',mfc='white',mec=COL[engine],ms=5,ls='none')
                    ax.annotate('TO',(sf+shift,60000),xytext=(0,6),textcoords='offset points',ha='center',fontsize=6.5,color=COL[engine])
        ax.axhline(60000,color='#A4ACB4',ls=(0,(3,3)),lw=.65)
        ax.set_ylim(.35 if query=='q1' else 50,120000)
    ax.set_ylabel('Latency (ms, log)' if log else 'Latency (ms)',labelpad=5)
def short(v):
    return f'{v/1000:g}k' if abs(v)>=1000 else f'{v:g}'

# 1. Architecture: individually wrapped text kept entirely within each box.
fig=plt.figure(figsize=(3.5,4.25))
ax=fig.add_axes([.035,.025,.93,.95]);ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off')
layers=[
 ('Data generation and export','8 TPC-H-derived entities\nCSV sizes and SHA-256 hashes'),
 ('Database loading and validation','Local PostgreSQL and MongoDB\nMatching row and document counts'),
 ('Workloads and indexes','Q1-Q5; 50-record CRUD batches\nBaseline and optional indexes'),
 ('Measurement and plans','3 warm-ups; 10 measured runs\n60 s server-side query limit'),
 ('Statistical analysis','Output checks and measured medians\nMann-Whitney U; Holm adjustment')]
for i,(title,body) in enumerate(layers):
    y=.83-i*.195
    ax.add_patch(FancyBboxPatch((.035,y),.93,.155,boxstyle='square,pad=.008',fc='white',ec='black',lw=.8))
    ax.text(.075,y+.116,title,fontsize=9,weight='bold',ha='left',va='center',color='black')
    ax.text(.075,y+.055,body,fontsize=7.8,ha='left',va='center',linespacing=1.35,color='black')
    if i<4:ax.annotate('',xy=(.5,y-.034),xytext=(.5,y-.009),arrowprops={'arrowstyle':'-|>','color':'black','lw':.8})
save(fig,'fig1_system_architecture.png',{'layers':layers})

# 2. Data model: all eight entities and exact PostgreSQL primary keys.
fig=plt.figure(figsize=(3.5,4.3));ax=fig.add_axes([.025,.015,.95,.97]);ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off')
ax.add_patch(FancyBboxPatch((.025,.445),.95,.53,boxstyle='square,pad=.009',fc='white',ec='black',lw=.8))
ax.text(.07,.938,'PostgreSQL: normalized tables',fontsize=9.3,weight='bold',color='black',va='center')
ax.text(.07,.897,'Declared primary keys',fontsize=7.5,color='black')
keys=['region       r_regionkey','nation       n_nationkey','supplier     s_suppkey','customer     c_custkey','part         p_partkey','partsupp     (ps_partkey, ps_suppkey)','orders       o_orderkey','lineitem     (l_orderkey, l_linenumber)']
for i,label in enumerate(keys):ax.text(.07,.852-i*.045,label,fontsize=7.05,fontfamily='DejaVu Sans Mono',va='center')
ax.text(.07,.476,'Foreign keys enforce the declared relationships.',fontsize=7.4,color='black')
ax.add_patch(FancyBboxPatch((.025,.04),.95,.34,boxstyle='square,pad=.009',fc='white',ec='black',lw=.8))
ax.text(.07,.342,'MongoDB: separate BSON collections',fontsize=9.2,weight='bold',color='black')
collections=['region','nation','supplier','customer','part','partsupp','orders','lineitem']
for i,name in enumerate(collections):ax.text(.09+(i%2)*.46,.285-(i//2)*.043,name,fontsize=8,fontfamily='DejaVu Sans Mono')
ax.text(.07,.075,'Mandatory _id; business-key links at query time.',fontsize=7.3,color='black')
save(fig,'fig2_data_model_comparison.png',{'postgres_keys':keys,'mongo_collections':collections})

# 3. CRUD, indexed: one legend, compact panels, shared units.
fig,axs=plt.subplots(2,2,figsize=(3.5,3.5));fig.subplots_adjust(left=.17,right=.97,bottom=.14,top=.84,wspace=.45,hspace=.62)
for ax,op,title in zip(axs.flat,['create','read','update','delete'],['(a) Insert','(b) Read','(c) Update','(d) Delete']):
    curves(ax,c,'median_ms',{'operation':op,'mode':'indexed'})
    ax.set_title(title,loc='left',pad=6)
    ax.set_xlabel('')
fig.supxlabel('Scale factor',y=.025,fontsize=8.5);fig.supylabel('Median batch latency (ms)',x=.02,fontsize=8.5)
legends(fig)
save(fig,'fig3_crud_latency.png',c[c['mode']=='indexed'].to_dict('records'))

# 4. Insert throughput, indexed.
fig,ax=plt.subplots(figsize=(3.5,2.6));fig.subplots_adjust(left=.19,right=.97,bottom=.21,top=.82)
curves(ax,c,'median_ops_s',{'operation':'create','mode':'indexed'})
ax.set_ylabel('Throughput (records/s)',labelpad=6)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:short(v)))
legends(fig)
save(fig,'fig4_insert_throughput.png',c[(c['mode']=='indexed')&(c.operation=='create')].to_dict('records'))

# 5. Q1: show baseline on log scale so both engines remain visible.
fig,axs=plt.subplots(2,1,figsize=(3.5,3.9));fig.subplots_adjust(left=.2,right=.97,bottom=.12,top=.87,hspace=.64)
for ax,mode,title in zip(axs,['none','indexed'],['(a) Baseline: no optional indexes','(b) Optional indexes enabled']):
    queryplot(ax,'q1',mode,log=(mode=='none'))
    ax.set_title(title,loc='left',pad=6)
axs[0].set_xlabel('');legends(fig)
save(fig,'fig5_q1_lookup_latency.png',q[q['query']=='q1'].to_dict('records'))

# 6. Q2 and Q3: explicit zero-result qualification.
assert (q[q['query'].isin(['q2','q3'])].rows==0).all()
fig,axs=plt.subplots(2,1,figsize=(3.5,3.9));fig.subplots_adjust(left=.2,right=.97,bottom=.15,top=.87,hspace=.6)
for ax,query,title in zip(axs,['q2','q3'],['(a) Q2: range predicate','(b) Q3: multiple predicates']):
    queryplot(ax,query,'indexed')
    ax.set_title(title,loc='left',pad=6)
axs[0].set_xlabel('');legends(fig)
fig.text(.53,.015,'Indexed; fixed predicates returned zero rows.',ha='center',fontsize=7,color='#596575')
save(fig,'fig6_range_multi_latency.png',q[(q['mode']=='indexed')&q['query'].isin(['q2','q3'])].to_dict('records'))

# 7. Core volume scaling: timeouts shown at their limit, never as zero.
fig,axs=plt.subplots(3,1,figsize=(3.5,5.15));fig.subplots_adjust(left=.21,right=.96,bottom=.09,top=.9,hspace=.66)
for ax,query,title in zip(axs,['q1','q4','q5'],['(a) Q1: equality lookup','(b) Q4: two-way join','(c) Q5: join and aggregation']):
    queryplot(ax,query,'indexed',log=(query=='q5'),censor=(query=='q5'))
    ax.set_title(title,loc='left',pad=6)
    if query!='q5':ax.set_xlabel('')
legends(fig,timeout=True)
save(fig,'fig7_latency_vs_volume.png',comp[(comp['mode']=='indexed')&comp['query'].isin(['q1','q4','q5'])].to_dict('records'))

def grouped(ax,mode):
    clean(ax);x=np.arange(3)
    for i,engine in enumerate(COL):
        for j,query in enumerate(['q1','q4','q5']):
            row=comp[(comp.sf==1)&(comp['mode']==mode)&(comp['query']==query)].iloc[0]
            y=row['mongo_median_ms' if engine=='mongodb' else 'postgres_median_ms']
            n=row['mongo_n' if engine=='mongodb' else 'postgres_n']
            xx=x[j]+(i-.5)*.23
            if n==10 and np.isfinite(y):
                ax.bar(xx,y,width=.22,color=COL[engine],zorder=3)
            else:
                ax.plot(xx,60000,'^',mfc='white',mec=COL[engine],ms=5,zorder=5)
                ax.annotate('TO',(xx,60000),xytext=(0,6),textcoords='offset points',ha='center',fontsize=6.1,color=COL[engine])
    ax.set_yscale('log');ax.set_ylim(.4,150000);ax.set_xlim(-.48,2.48)
    ax.set_xticks(x,['Q1','Q4','Q5'])
    ax.set_yticks([1,10,100,1000,10000,60000],['1','10','100','1k','10k','60k'])
    ax.axhline(60000,color='#A4ACB4',ls=(0,(3,3)),lw=.6)
    ax.set_ylabel('Latency (ms, log)',labelpad=6)

# 8. Complexity: log scaling preserves small Q1 bars; TO explicitly encoded.
fig,ax=plt.subplots(figsize=(3.5,2.9));fig.subplots_adjust(left=.2,right=.97,bottom=.14,top=.82)
grouped(ax,'indexed');legends(fig,timeout=True)
save(fig,'fig8_complexity_breakdown.png',comp[(comp.sf==1)&(comp['mode']=='indexed')].to_dict('records'))

# 9. Join and aggregation scaling.
fig,axs=plt.subplots(2,1,figsize=(3.5,3.9));fig.subplots_adjust(left=.21,right=.96,bottom=.12,top=.87,hspace=.65)
for ax,query,title in zip(axs,['q4','q5'],['(a) Q4: two-way join','(b) Q5: join and aggregation']):
    queryplot(ax,query,'indexed',log=(query=='q5'),censor=(query=='q5'))
    ax.set_title(title,loc='left',pad=6)
axs[0].set_xlabel('');legends(fig,timeout=True)
save(fig,'fig9_join_aggregation_deepdive.png',comp[(comp['mode']=='indexed')&comp['query'].isin(['q4','q5'])].to_dict('records'))

# 10. Index impact: identical log axes and explicit timeout markers.
fig,axs=plt.subplots(2,1,figsize=(3.5,4));fig.subplots_adjust(left=.21,right=.96,bottom=.1,top=.87,hspace=.64)
for ax,mode,title in zip(axs,['none','indexed'],['(a) Baseline, SF 1.0','(b) Indexed, SF 1.0']):
    grouped(ax,mode);ax.set_title(title,loc='left',pad=6)
legends(fig,timeout=True)
save(fig,'fig10_index_impact.png',comp[(comp.sf==1)&comp['query'].isin(['q1','q4','q5'])].to_dict('records'))

# 11. Storage: concise panel titles and a single external legend.
ss=s.copy();ss['mib']=ss.total_bytes/2**20
fig,axs=plt.subplots(2,1,figsize=(3.5,3.8));fig.subplots_adjust(left=.22,right=.97,bottom=.12,top=.87,hspace=.64)
for ax,mode,title in zip(axs,['none','indexed'],['(a) Baseline','(b) Indexed']):
    curves(ax,ss,'mib',{'mode':mode});ax.set_title(title,loc='left',pad=6)
    ax.set_ylim(0,1700);ax.set_yticks([0,500,1000,1500]);ax.set_ylabel('Storage (MiB)',labelpad=6)
axs[0].set_xlabel('');legends(fig)
save(fig,'fig11_storage_analysis.png',s.to_dict('records'))

# 12. Q5 resource measurements: NM labelled without fabricating zeroes.
fig,axs=plt.subplots(2,1,figsize=(3.5,3.9));fig.subplots_adjust(left=.21,right=.96,bottom=.15,top=.87,hspace=.66)
rr=r[r['query']=='q5'].copy();rr['rss_mib']=rr.avg_rss_bytes/2**20
for ax,key,title,ylab in zip(axs,['avg_cpu','rss_mib'],['(a) Mean sampled CPU','(b) Mean summed process RSS'],['CPU (% of host)','RSS (MiB)']):
    curves(ax,rr,key,{'mode':'indexed'});ax.set_title(title,loc='left',pad=6);ax.set_ylabel(ylab,labelpad=6)
    if key=='avg_cpu':ax.set_ylim(0,8);ax.set_yticks([0,2,4,6,8])
    else:ax.set_ylim(0,1200);ax.set_yticks([0,400,800,1200])
    for sf in [.5,1.]:
        ax.text(sf,.08,'NM',transform=ax.get_xaxis_transform(),ha='center',color=COL['mongodb'],fontsize=7.2)
axs[0].set_xlabel('');legends(fig)
fig.text(.54,.014,'Q5, indexed. NM: no completed measurement.',ha='center',fontsize=7,color='#596575')
save(fig,'fig12_resource_utilization.png',rr.to_dict('records'))

# 13. Integer counters; zero baseline retained rather than 0.94-1.06 autozoom.
fig,axs=plt.subplots(2,1,figsize=(3.5,3.5));fig.subplots_adjust(left=.21,right=.97,bottom=.13,top=.93,hspace=.68)
diag=[('MongoDB: documents examined',[1,1,1],COL['mongodb'],'Documents',2),('PostgreSQL: shared-buffer hits',[3,0,0],COL['postgresql'],'Buffer hits',4)]
for ax,(title,ys,color,ylab,maxy) in zip(axs,diag):
    clean(ax);axis_sf(ax);ax.bar(SF,ys,width=.115,color=color,zorder=3);ax.set_ylim(0,maxy)
    ax.set_yticks(range(maxy+1));ax.set_ylabel(ylab,labelpad=6);ax.set_title(title,loc='left',pad=6)
    for sf,y in zip(SF,ys):ax.annotate(str(y),(sf,y),xytext=(0,4),textcoords='offset points',ha='center',fontsize=7.2,color=color)
axs[0].set_xlabel('')
save(fig,'fig13_execution_plan_diagnostics.png',{'mode':'indexed','query':'q1','sf':SF,'mongo_docs':[1,1,1],'pg_shared_hits':[3,0,0]})

# 14. Radar with the exact stated efficiency formula.
v=comp[(comp.sf==.1)&(comp['mode']=='indexed')&comp['query'].isin(['q1','q4','q5'])].set_index('query').loc[['q1','q4','q5']]
assert v.p_value.notna().all()
angles=np.array([0,2*np.pi/3,4*np.pi/3])
fig=plt.figure(figsize=(3.5,3.55));ax=fig.add_axes([.20,.22,.60,.58],projection='polar')
ax.set_theta_offset(np.pi/2);ax.set_theta_direction(-1)
for engine in COL:
    col='mongo_median_ms' if engine=='mongodb' else 'postgres_median_ms'
    ys=(v[['mongo_median_ms','postgres_median_ms']].min(axis=1)/v[col]).to_numpy()
    ax.plot(np.r_[angles,angles[0]],np.r_[ys,ys[0]],color=COL[engine],marker=MARK[engine],markersize=3.5,lw=1.35)
    ax.fill(np.r_[angles,angles[0]],np.r_[ys,ys[0]],color=COL[engine],alpha=.065)
ax.set_ylim(0,1.04);ax.set_yticks([.25,.5,.75,1],['0.25','0.50','0.75','1.00'],fontsize=6.4,color='#66717F')
ax.set_rlabel_position(15);ax.set_xticks(angles,['Q1\nLookup','Q4\nJoin','Q5\nAggregation'],fontsize=8)
ax.tick_params(axis='x',pad=8);ax.spines['polar'].set_color('#B5BEC8');ax.spines['polar'].set_linewidth(.6)
ax.grid(color='#DCE2E8',linewidth=.55)
fig.text(.5,.97,'Indexed-query efficiency, SF 0.1',ha='center',va='top',fontsize=9)
legends(fig,y=.105)
save(fig,'fig14_engine_capability_radar.png',v.reset_index().to_dict('records'))

# Contact sheet is an intermediate QA artifact, not a manuscript figure.
names=sorted(records,key=lambda n:int(re.match(r'fig(\d+)',n)[1]))
thumbs=[]
for name in names:
    im=Image.open(FIG/name).convert('RGB')
    thumb=ImageOps.contain(im,(420,550))
    canvas=Image.new('RGB',(450,590),'#E9EEF3')
    canvas.paste(thumb,((450-thumb.width)//2,25))
    ImageDraw.Draw(canvas).text((12,566),name,fill='#263645')
    thumbs.append(canvas)
sheet=Image.new('RGB',(450*4,590*4),'#E9EEF3')
for i,im in enumerate(thumbs):sheet.paste(im,((i%4)*450,(i//4)*590))
sheet.save(WORK/'contact-sheet.png')
(WORK/'plotted-data.json').write_text(json.dumps(records,indent=2,default=str),encoding='utf-8')
(WORK/'layout-check.json').write_text(json.dumps(qa,indent=2),encoding='utf-8')
issues=[a for a in qa if a['outside_text'] or a['overlapping_panel_titles']]
print('Recreated',len(records),'figures at 600 dpi.')
print('Layout findings:',json.dumps(issues))