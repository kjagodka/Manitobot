import os.path
import typing

PROD = True  # if ktulu_serwer

if PROD:
    GUILD_ID = 710039683798794270
    PLAYER_ROLE_ID = 710051008608469012
    MANITOU_ROLE_ID = 710050970352222229
    NOTATNIK_MANITOU_CHANNEL_ID = 710048748897828885
    PRZEGRALEM_ROLE_ID = 710050205688660040
    GLOSOWANIA_CHANNEL_ID = 710048541346758729
    ANKIETAWKA_CHANNEL_ID = 710050073181945896
    FRAKCJE_CATEGORY_ID = 710048159681740820
    NIEPUBLICZNE_CATEGORY_ID = 716304427442765824
    TRUP_ROLE_ID = 710051039218368513
    BOT_ID = 692390349053886515
    SPECTATOR_ROLE_ID = 710052408205770772
    TOWN_CHANNEL_ID = 710048183211786301
    MY_ID = 388764073191538688
    VOICE_CHANNEL_ID = 710039683798794274
    DUEL_WINNER_ID = 710051109242404864
    DUEL_LOSER_ID = 710051419117453313
    SEARCHED_ID = 710053492152074363
    HANGED_ID = 710051077718016013
    NEWCOMMER_ID = 720235063144349720
    GUN_ID = 717099650087387158
    FAC2CHANN_ID: typing.Dict[str, int] = {
        "Bandyci": 710048209115807753,
        "Indianie": 710048231924564008,
        "Ufoki": 710048271980167259,
        "Inkwizycja": 710048333762396191
    }
    FAC2EMOJI: typing.Dict[str, int] = {
        "Bandyci": 770345428977582090,
        "Indianie": 770345346983002209,
        "Ufoki": 770345372865265724,
        "Inkwizycja": 770345470677483566
    }
    ADMIN_ROLE_ID = 710040986260209715
    QUALIFIED_MANITOU_ROLE_ID = 879495334093525052
    CONTROL_PANEL_ID = 770344422625378325
    SET_CHANNEL_ID = 890289302230171658
    PING_REMINDER_ID = 779091574801301505
    PING_GAME_ID = 779091611736604693
    PING_BLUE_ID = 779100908872794132
    PING_GREEN_ID = 779101225471049738
    PING_MESSAGE_ID = 779673013330116609
else:
    GUILD_ID = 694111942729662474
    PLAYER_ROLE_ID = 694112133880741888
    MANITOU_ROLE_ID = 694112018596233246
    NOTATNIK_MANITOU_CHANNEL_ID = 694113999691972638
    PRZEGRALEM_ROLE_ID = 694115711152291881
    GLOSOWANIA_CHANNEL_ID = 694112614988513312
    ANKIETAWKA_CHANNEL_ID = 714773492544962643
    FRAKCJE_CATEGORY_ID = 694112717266616372
    NIEPUBLICZNE_CATEGORY_ID = 799603854349041674
    TRUP_ROLE_ID = 694112166105841724
    BOT_ID = 709695265413791829
    SPECTATOR_ROLE_ID = 694112245814263869
    TOWN_CHANNEL_ID = 694112761386500146
    MY_ID = 388764073191538688
    VOICE_CHANNEL_ID = 694111942729662478
    DUEL_WINNER_ID = 701077841848172544
    DUEL_LOSER_ID = 701078158102888538
    SEARCHED_ID = 701076474320650310
    HANGED_ID = 701462743504519308
    NEWCOMMER_ID = 720307369245933649
    GUN_ID = 717105928067088384
    FAC2CHANN_ID = {
        "Bandyci": 694112800221560872,
        "Indianie": 706155488202457229,
        "Ufoki": 706155509069381733,
        "Inkwizycja": 706155539788202107
    }
    FAC2EMOJI = {
        "Bandyci": 770304712011415563,
        "Indianie": 770306713735266336,
        "Ufoki": 770304617895559178,
        "Inkwizycja": 770303863844241410
    }
    ADMIN_ROLE_ID = 694112331537317898
    QUALIFIED_MANITOU_ROLE_ID = 694112331537317898
    CONTROL_PANEL_ID = 770310603691786311
    SET_CHANNEL_ID = 890289714534428773
    PING_REMINDER_ID = 780379731962494997
    PING_GAME_ID = 780379814846267392
    PING_BLUE_ID = None
    PING_GREEN_ID = None
    PING_MESSAGE_ID = None


EMOJI2COMMAND: typing.Dict[str, typing.Tuple[str, str]] = {  # for DayState methods - emoji: (label, method_name)
    '⏪': ('Cofnij', 'undo'),
    '❌': ('Anuluj', 'cancel'),
    '🗳️': ('Głosowanie', 'voting'),
    '🎲': ('Wylosuj', 'random'),
    '🔒': ('Blokuj', 'lock'),
    '⏩': ('Dalej', 'end')
}

REMOVABLE: typing.List[str] = [EMOJI2COMMAND['🔒'][1]]  # state commands to accept in `reaction_remove` event

RULLER = '=' * 48

CONFIG = {
    'DM_Manitou': True
}

LOG_FILE = 'error.log'
FULL_LOG_FILE = 'full.log'

SETS_DB_PATH = os.path.join('data', 'sets.sqlite3')
