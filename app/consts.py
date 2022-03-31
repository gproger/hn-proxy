
# ==============
# General config
# ==============

#: Default port proxy port number
PORT = 8232
#: Default patched word length
WORD_LEN = 6
#: Default word appended to patched word
WORD_APP = "™"
#: Default target proxyfied url
TARGET_URL = "https://news.ycombinator.com"
#: Default source proxy ipv4 addr
SOURCE_IPV4 = '0.0.0.0'
#: Default patcher for html based on BeatifulSoup or regex
REG_PATCHER = False


# =============================
# BeatifulSoup Patcher defaults
# =============================

#: Patcher skipped tags
BS_SKIP_TAGS = {'code', 'script', 'meta', 'style'}
