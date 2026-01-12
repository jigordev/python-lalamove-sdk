from enum import Enum


class Market(str, Enum):
    BR = "BR"
    HK = "HK"
    ID = "ID"
    MY = "MY"
    MX = "MX"
    PH = "PH"
    SG = "SG"
    TW = "TW"
    TH = "TH"
    VN = "VN"


class Language(str, Enum):
    EN_BR = "en_BR"
    PT_BR = "pt_BR"
    EN_HK = "en_HK"
    ZH_HK = "zh_HK"
    EN_ID = "en_ID"
    ID_ID = "id_ID"
    EN_MY = "en_MY"
    MS_MY = "ms_MY"
    EN_MX = "en_MX"
    ES_MX = "es_MX"
    EN_PH = "en_PH"
    EN_SH = "en_SG"
    ZH_TW = "zh_TW"
    EN_TH = "en_TH"
    TH_TH = "th_TH"
    EN_VN = "en_VN"
    VN_VN = "vn_VN"
