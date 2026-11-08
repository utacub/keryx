# Applies the UTAC Keryx 0.6.14 change to the built UTAC_Keryx_v0.6.13_local.html (Marc, 2026-11-08):
# the "Identitat gràfica…" paragraph is removed from the Information window, and Marc's name no longer appears
# anywhere in the app (the "Identitat gràfica aprovada…" sentence is also removed from the licence text, in every language).
# Usage: python3 patch0614.py UTAC_Keryx_v0.6.13_local.html UTAC_Keryx_v0.6.14_local.html
import sys, re
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8',newline='').read()
def rep(a,b,count=1):
    global s
    n=s.count(a); assert n==count,(a[:90],n); s=s.replace(a,b)
s=re.sub(r'(?<!/\* )0\.6\.13(?![:\d])','0.6.14',s)
CA="Identitat gràfica: logotip de Keryx i logotip original d’UTAC, aportats per Marc Coronas. Els logotips són marques de les institucions titulars i no formen part de la llicència de l’app."
ES="Identidad gráfica: logotipo de Keryx y logotipo original de UTAC, aportados por Marc Coronas. Los logotipos son marcas de las instituciones titulares y no forman parte de la licencia de la app."
rep(',el(\'p\',{},tr("'+CA+'","'+ES+'"))','')
# dictionary entries for that paragraph
key='"'+CA+'":"'
for _ in range(4):
    i=s.index(key);j=s.index('",',i+len(key))+2;s=s[:i]+s[j:]
assert CA not in s
# the remaining sentences that name Marc
while 'Coronas' in s:
    i=s.index('Coronas')
    a=s.rindex('. ',0,i)+2
    b=s.index('. ',i)+2
    assert b-a<200,s[a:b]
    s=s[:a]+s[b:]
assert 'Coronas' not in s
open(dst,'w',encoding='utf-8',newline='').write(s)
print('ok',dst)
