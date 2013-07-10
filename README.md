marju2
======

Marju 2.0

+++Seadistamine+++
- /conf/ kausta tekitada konfifail. Näidis 'configsample.py' on olemas. Muuhulgas on vaja lisada Google ja FML API'de koodid.
- Määrata marjubot.py's kasutatav konfifail, nt 'import conf.configsample as config'
- Tekitada vastavalt konfitud kanalitele kaustad. Nt teha folder /minukanal/. Seal hoitakse tsitaadifaile, logi jms.

+++Muu+++
- Võiks jooksutada Python 2.6 või 2.7 peal. Sobib ka 3.x, kuid mingis kohas see feilis mäletamistmööda.
- Exceptioni korral logitakse stacktrace enne sulgumist faili exceptions.log
- Debugimiseks seada failis irclib.py lipu DEBUG väärtuseks 1

+++TODO list+++
- Varemlingitud URL'ide detectimine
- Youtube videode otsing
- Päringud eraldi threadi, juhuks kui on timeout vms
- Logimine viia eraldi muust loogikast
- REFACTORDADA TÄIEGA
- ????
