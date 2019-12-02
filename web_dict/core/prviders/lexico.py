import re

from .base_provider import BaseProvider
from ..parser import Parser


class _ExampleProvider(Parser):

    def val_sent(self):
        sent = self.select("em", one=False)[0]
        if not sent:
            sent = self.bs.contents
        return re.search("‘?(?P<c>.+)’?", sent).group("c") if sent else None

    def val_trans(self):
        try:
            return self.select("em", one=False)[1]
        except IndexError:
            return None


class _ExpEntryProvider(Parser):

    @property
    def val_indicators(self):
        return self.select("span.indicators")

    @property
    def val_trans(self):
        trans = self.select("div.tr")
        return re.search("‘?(?P<c>.+)’?", trans).group("c") if trans else None

    @property
    def val_exp(self):
        exp = self.select("div.exg.em")
        if not exp:
            exp = self.select(".ind")
        return re.search("‘?(?P<c>.+)’?", exp).group("c") if exp else None

    @property
    def val_examples(self):
        _ = self.provider_to_list(_ExampleProvider, 'div.examples > div.exg > ul > li.ex')
        _.insert(0, _ExampleProvider(self.select(".ex", one=True, text=False)).to_dict())
        if not _:
            return _
        return [_ExampleProvider(self.select(".exg > .ex", one=True, text=False)).to_dict(), ]


class _GrambProvider(Parser):

    @property
    def val_pos(self):
        return self.select('span.pos')

    @property
    def val_exps(self):
        return self.provider_to_list(_ExpEntryProvider, 'ul.semb > li')


class _PrimaryHeaderProvider(Parser):

    def val_head_word(self):
        sup = self.select("span.hw > sup")
        return self.select("span.hw").replace(sup if sup else '', "")

    def val_trans(self):
        return self.select('span.head-translation')


class Lexico(BaseProvider):

    @property
    def url(self):
        _ = 'definition'
        if self.seg in ('es-en',): _ = 'traducir'
        if self.seg in ('en-es',): _ = 'translate'
        if self.seg in ('es',): _ = 'definicion'
        return f"https://www.lexico.com/{self.seg}/{_}/{self.word}"

    def __init__(self, word: str, seg='es-en'):
        super(Lexico, self).__init__(word, seg)
        self.seg = seg

    @property
    def head_word(self):
        return _PrimaryHeaderProvider(self.select(".primary_homograph", text=False)).to_dict()

    @property
    def val_audio(self):
        return self.select("a.headwordAudio.rsbtn_play", text=False).audio['src']

    @property
    def val_defs(self):
        return self.provider_to_list(_GrambProvider, 'section.gramb')