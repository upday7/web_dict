import abc
import re
import unicodedata
from typing import Union, Tuple

import requests
from bs4 import BeautifulSoup, Tag
from property_cached import cached_property
from requests import Response

from .utils import STD_HEADERS


def _norm_str(s: str):
    return re.sub(r"\s+", ' ', unicodedata.normalize("NFKD", s)).strip()


class Parser:
    to_dict_fields = ()

    def __init__(self, markup: Union[BeautifulSoup, str, Tag]):
        self._markup = markup

    @property
    def markup(self) -> Union[BeautifulSoup, str, Tag]:
        return self._markup

    @cached_property
    def bs(self) -> Union[BeautifulSoup, Tag]:
        if isinstance(self.markup, (BeautifulSoup, Tag)):
            return self.markup
        else:
            return BeautifulSoup(markup=self.markup, features='lxml')

    def select(self, p: str, one=True, text=True):
        if one:
            t = self.bs.select_one(p)
            if t and text:
                return _norm_str(t.text)
            return t
        else:
            ts = self.bs.select(p)
            if ts and text:
                return [_norm_str(t.text) for t in ts]
            return ts

    def get_by_cls(self, name: str, cls: str, **attrs) -> Tag:
        return self.bs.find(name, class_=cls, attrs=attrs)

    def to_dict(self):
        _ = {}

        fields = []
        fields.extend(self.to_dict_fields)
        fields.extend([prop.lower().split('val_')[-1] for prop in dir(self) if prop.startswith("val_")])

        for field in set([f.lower() for f in fields]):
            try:
                val = getattr(self, field, getattr(self, f"val_{field}", None))
                if callable(val):
                    val = val()
                if isinstance(val, str):
                    val = unicodedata.normalize("NFKD", val)
                if val not in [None, '']:
                    _[field.split('val_')[-1]] = val
            except AttributeError:
                ...
                # _[field.split('val_')[-1]] = None
        return _

    def provider_to_list(self, provider_cls, block_selector: Union[
        str, Tuple[str, dict]
    ]):
        try:
            if isinstance(block_selector, str):
                blocks = self.select(block_selector, one=False, text=False)
            else:
                blocks = self.bs.find_all(
                    block_selector[0],
                    **block_selector[1]
                )
        except AttributeError:
            return []
        return [provider_cls(d).to_dict() for d in blocks]


class WebParser(Parser):

    def __init__(self, word: str):
        self.word = word
        super(WebParser, self).__init__(markup='')

    @property
    @abc.abstractmethod
    def url(self):
        ...

    @cached_property
    def rsp(self) -> Response:
        rsp = requests.get(self.url, headers=STD_HEADERS)
        rsp.raise_for_status()
        return rsp

    @property
    def json(self) -> dict:
        return self.rsp.json()

    @property
    def markup(self) -> str:
        if not self._markup:
            self._markup = self.rsp.content.decode()
        return self._markup