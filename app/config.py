class ProxyConfig:
    """Configuration for Hacker News proxy"""
    #: local HTTP proxy listen port
    port : int
    #: word length to patch
    word_len : int
    #: str what need to add to matched word
    word_app: str
    #: target url to proxify
    target_url: str
    #: source ipv4 addr for incoming connections
    source_ipv4: str
    #: use BeatifulSoup patcher or regex
    regex_patcher: bool