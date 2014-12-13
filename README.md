marju2
======

Marju 2.0

+++Seadistamine+++
- /conf/ kausta tekitada konfifail. Näidis 'configsample.py' on olemas. Muuhulgas on vaja lisada Google ja FML API'de koodid.
- Määrata marjubot.py's kasutatav konfifail, nt 'import conf.configsample as config'
- Tekitada vastavalt konfitud kanalitele kaustad alamkausta 'channels'. Seal hoitakse tsitaadifaile, logi jms.

+++Muu+++
- Võiks jooksutada Python 2.6 v'i 2.7 peal. Sobib ka 3.x, kuid mingis kohas see feilis maletamistmööda.
- Exceptioni korral logitakse stacktrace enne sulgumist faili exceptions.log

+++TODO list+++
- !nom kasule otsinguvõimalus
- !seen käsk eraldi pluginasse
- Youtube videode otsing
- tõlkefunktsioon
- REFACTORDADA TÄIEGA
- ????
