
NICK = 'marjutest'
PASSWORD = 'marjupassword'
SERVER = "some.server.org"
PORT = 6667

OWNER_NICK = "nick"
OWNER_PASS = "pass"

GOOGLE_KEY = 'yourGoogleKeyHere'
GOOGLE_CX = 'yourGoogleCxHere'

FML_KEY = 'yourFmlKeyHere'
LASTFM_KEY = 'yourlastfmkey'

marjutest = {
    "name": "#marjutest",
    "folder": "marjutest",
    "logging": True,
    "ai": True,
    "old": True,
    "quoting": True,
    "seen": True
}

mingikanal = {
    "name": "#minukanal",
    "folder": "minukanal",
    "logging": False,
    "ai": True,
    "old": False,
    "quoting": True,
    "seen": False
}

channels = {
    marjutest["name"]: marjutest,
    mingikanal["name"]: mingikanal,
}
