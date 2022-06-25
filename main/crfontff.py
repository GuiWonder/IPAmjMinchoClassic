import os, json, fontforge, subprocess, platform

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
print('正在合并多编码汉字...')
tbmulcod=(('併','倂'), ('醖','醞'), ('輼','轀'), ('嬷','嬤'), ('煴','熅'), ('緼','縕'), ('縆','緪'), ('酝','醞'), ('脱','脫'), ('腽','膃'), ('蒀','蒕'), ('芈','羋'), ('蕰','薀'), ('蜕','蛻'), ('藴','蘊'), ('删','刪'), ('别','別'), ('刹','剎'), ('内','內'), ('册','冊'), ('呐','吶'), ('弑','弒'), ('兑','兌'), ('兖','兗'), ('姗','姍'), ('媪','媼'), ('秃','禿'), ('税','稅'), ('栅','柵'), ('涚','涗'), ('滚','滾'), ('温','溫'), ('捝','挩'), ('悦','悅'), ('榅','榲'), ('愠','慍'), ('敚','敓'), ('氲','氳'), ('揾','搵'), ('棁','梲'), ('俞','兪'), ('值','値'), ('偷','偸'), ('即','卽'), ('告','吿'), ('唧','喞'), ('喻','喩'), ('塈','墍'), ('填','塡'), ('妍','姸'), ('媮','婾'), ('尚','尙'), ('屏','屛'), ('帡','帲'), ('惪','悳'), ('慎','愼'), ('既','旣'), ('暨','曁'), ('概','槪'), ('榆','楡'), ('槙','槇'), ('清','淸'), ('溉','漑'), ('真','眞'), ('研','硏'), ('箳','簈'), ('胼','腁'), ('迸','逬'), ('郎','郞'), ('青','靑'), ('鷏','鷆'), ('俱','倶'), ('查','査'), ('瓶','甁'), ('訮','詽'), ('豜','豣'), ('熙','煕'), ('教','敎'), ('軿','輧'), ('鄉', '鄕'))
for chd in tbmulcod:
	ord(chd[0])
	if ord(chd[1]) not in font:
		continue
	glyt = font[font.findEncodingSlot(ord(chd[1]))]
	if ord(chd[0]) in font:
		glyn = font[font.findEncodingSlot(ord(chd[0]))]
		if glyt.glyphname == glyn.glyphname:
			continue
		if glyn.unicode == ord(chd[0]):
			glyn.unicode = -1
		elif glyn.altuni != None:
			l1 = list()
			for aa in glyn.altuni:
				if aa[0] != ord(chd[0]):
					l1.append(aa)
			if len(l1) > 0:
				glyn.altuni = tuple(l1)
			else:
				glyn.altuni = None
	#print('处理 '+chd[0]+'-'+chd[1])
	l2=list()
	if glyt.altuni != None:
		for a2 in glyt.altuni:
			l2.append(a2)
	l2.append((ord(chd[0]), 0, 0))
	glyt.altuni = tuple(l2)

print('正在设置字体名称...')
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

