import os, json, fontforge, subprocess, platform
from collections import defaultdict

pydir = os.path.abspath(os.path.dirname(__file__))

def ckfile(f):
	f=f.strip()
	if not os.path.isfile(f):
		if os.path.isfile(f.strip('"')):
			return f.strip('"')
		elif os.path.isfile(f.strip("'")):
			return f.strip("'")
	return f

inf=str()
outf=str()
print('====IPAmj明朝体传承化方案====\n')
while not os.path.isfile(inf):
	inf=input('请输入字体文件路径（或拖入文件）：\n')
	inf=ckfile(inf)
	if not os.path.isfile(inf):
		print('文件不存在，请重新选择！\n')
while not outf.strip():
	outf=input('请输入输出文件：\n')

style=str()
while style not in ('1', '2', '3'):
	style=input('请选择字形变体参考对象：\n\t1.新细明体\n\t2.传承旧字综合\n\t3.康熙字典\n')

tv=dict()
with open('uvs-get-MARK-0'+style+'.txt', 'r', encoding='utf-8') as f:
	for line in f.readlines():
		if line.startswith('#'):
			continue
		line=line.strip()
		if line.endswith('X'):
			a=line.split(' ')
			tv[ord(a[0])]=int(a[3].strip('X').strip(), 16)

print('正在载入字体...')
font = fontforge.open(inf)
if font.is_cid:
	font.cidFlatten()
font.reencode("unicodefull")
ltb=list()
for gls in font.glyphs():
	#if True or gls.unicode<0:
	if gls.altuni!=None:
		for alt in gls.altuni:
			if alt[1]>0:
				if alt[0] in tv and tv[alt[0]]==alt[1]:
					ltb.append((gls.glyphname, alt[0]))
print('正在移动代码点...')
for t1 in ltb:
	g=font[font.findEncodingSlot(t1[1])]
	if t1[0]==g.glyphname:
		continue
	if g.unicode==t1[1]:
		g.unicode=-1
	elif g.altuni!=None:
		l1=list()
		for aa in g.altuni:
			if aa[0] == t1[1] and aa[1] == 0:
				continue
			l1.append(aa)
		if len(l1) > 0:
			g.altuni = tuple(l1)
		else:
			g.altuni = None
	if font[t1[0]].unicode == -1:
		font[t1[0]].unicode = t1[1]
	else:
		l2 = list()
		if font[t1[0]].altuni != None:
			for a2 in font[t1[0]].altuni:
				l2.append(a2)
		l2.append((t1[1], 0, 0))
		font[t1[0]].altuni = tuple(l2)
sfntnames=list(font.sfnt_names)
for jn in sfntnames:
	if jn[0]=='Japanese':
		for lan in ['Chinese (Taiwan)', 'Chinese (PRC)', 'Chinese (Hong Kong)', 'Chinese (Macau)']:
			n1=list(jn)
			n1[0]=lan
			sfntnames.append(tuple(n1))
sfntnames2=list()
for nt in sfntnames:
	nn=list(nt)
	nn[2]=nn[2].replace('IPAmjMincho', 'IPAmjMincho-0'+style).replace('IPAmj明朝', 'IPAmj明朝-0'+style)
	nt=tuple(nn)
	sfntnames2.append(nt)
font.sfnt_names=tuple(sfntnames2)
del tv
print('正在生成字体...')
font.generate(outf)
print('完成!')

