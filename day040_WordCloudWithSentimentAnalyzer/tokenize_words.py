# tokenize_words.py

### === Imports ===
from __future__ import annotations
import re
from collections import Counter
from typing import Iterable, Literal, Sequence, Set, Dict, List
import pandas as pd
import flet as ft

AnalyzerName = Literal["Janome", "Sudachi"]

_URL_RE = re.compile(r"https?://\S+|www\.\S+")
_MENTION_RE = re.compile(r"@[A-Za-z0-9_]+")
# 記号・数字など（最低限）：必要なら拡張
_SYMBOL_NUM_RE = re.compile(r"[0-9０-９!-/:-@［\]\\^_`｛｜｝~・、。,:;\"'“”‘’()（）［］{}<>《》【】…—-]+")

DEFAULT_POS_KEEP = {"名詞", "形容詞", "動詞", "副詞"}

class JapaneseTokenizer:
    def __init__(self, analyzer: AnalyzerName = "Sudachi", sudachi_mode: Literal["A", "B", "C"]="C"):
        self.analyzer = analyzer
        self.sudachi_mode = sudachi_mode
        self._janome_t = None
        self._sudachi_tok = None
        self._sudachi_mode_obj = None

        if analyzer == "Janome":
            try:
                from janome.tokenizer import Tokenizer as JanomeTokenizer
                self._janome_t = JanomeTokenizer()
            except ImportError as e:
                raise RuntimeError("Janome is not installed.")

        elif analyzer == "Sudachi":
            try:
                from sudachipy import dictionary, tokenizer as sudachi_tokenizer
                self._sudachi_tok = dictionary.Dictionary().create()
                mode_map ={
                    "A": sudachi_tokenizer.Tokenizer.SplitMode.A,
                    "B": sudachi_tokenizer.Tokenizer.SplitMode.B,
                    "C": sudachi_tokenizer.Tokenizer.SplitMode.C,
                }
                self._sudachi_mode_obj = mode_map[self.sudachi_mode]
            except ImportError as e:
                raise RuntimeError("SudachiPy is not installed.")
        else:
            raise ValueError(f"Unknown analyzer: {analyzer}")

    @staticmethod
    def _normalize(text: str) -> str:
        # 1) URL・メンション除去 2) 記号・数字類簡易除去 3) 英字は小文字化
        text = _URL_RE.sub(" ", text)
        text = _MENTION_RE.sub(" ", text)
        text = _SYMBOL_NUM_RE.sub(" ", text)
        return text.lower()

    def tokenize_one(
            self,
            text: str,
            pos_keep: Set[str] = DEFAULT_POS_KEEP,
            stopwords: Set[str] = frozenset(),
            use_base_form: bool = True,
            min_len: int = 2,
    ) -> List[str]:
        text = self._normalize(text)
        tokens: List[str] = []

        if self.analyzer == "Janome":
            # Janome
            for t in self._janome_t.tokenize(text):
                pos = t.part_of_speech.split(",")[0]
                if pos not in pos_keep:
                    continue
                # 基本形（動詞と形容詞に有効）。未知語は*が返ることも。
                token = (t.base_form if use_base_form and t.base_form != "*" else t.surface).strip()
                if len(token) < min_len or token in stopwords:
                    continue
                tokens.append(token)

        else:
            # SudachiPy
            for m in self._sudachi_tok.tokenize(text, self._sudachi_mode_obj):
                pos = m.part_of_speech()[0]
                if pos not in pos_keep:
                    continue
                lemma = m.dictionary_form() if use_base_form else m.surface()
                token = lemma.strip().lower()
                if len(token) < min_len or token in stopwords:
                    continue
                tokens.append(token)

        return tokens

    def tokenize_many(
            self,
            texts: Iterable[str],
            pos_keep: Set[str] = DEFAULT_POS_KEEP,
            stopwords: Set[str] = frozenset(),
            use_base_form: bool = True,
            min_len: int = 2
    ) -> Counter:
        cnt: Counter = Counter()
        for s in texts:
            if not s:
                continue
            cnt.update(self.tokenize_one(
                s, pos_keep=pos_keep, stopwords=stopwords,
                use_base_form=use_base_form, min_len=min_len
            ))
        return cnt