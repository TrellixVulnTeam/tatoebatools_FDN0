import csv
import logging

from .config import DATA_DIR
from .utils import lazy_property
from .version import Version


class Links:
    """The links between the Tatoeba sentences of a pair of languages.  
    """

    _dir = DATA_DIR.joinpath("links")

    def __init__(self, source_language, target_language):

        self._src_lg = source_language
        self._tgt_lg = target_language

    def __iter__(self):

        try:
            with open(self.path) as f:
                fieldnames = [
                    "sentence_id",
                    "translation_id",
                ]
                rows = csv.DictReader(f, delimiter="\t", fieldnames=fieldnames)
                for row in rows:
                    yield Link(**row)
        except OSError:
            logging.exception(f"an error occurred while reading {self.path}")

    @property
    def source_language(self):
        """Get the source language of these links.
        """
        return self._src_lg

    @property
    def target_language(self):
        """Get the target language of these links.
        """
        return self._tgt_lg

    @property
    def path(self):
        """Get the path where the links are saved for this language pair.
        """
        return Links._dir.joinpath(self.filename)

    @property
    def filename(self):
        """Get the name of the file where the links for this language
        pair are saved.
        """
        return f"{self._src_lg}-{self._tgt_lg}_links.csv"

    @lazy_property
    def sentence_ids(self):
        """Get the source ids of the links.
        """
        return {lk.sentence_id for lk in self}

    @lazy_property
    def translation_ids(self):
        """Get the target ids of the links.
        """
        return {lk.translation_id for lk in self}

    @lazy_property
    def version(self):
        """Get the version of the downloaded data of these links.
        """
        return Version()[self.filename]


class Link:
    """A link between a Tatoeba's sentence and its translation.
    """

    def __init__(self, sentence_id, translation_id):

        self._src_id = sentence_id
        self._tgt_id = translation_id

    @property
    def sentence_id(self):
        """The id of the source sentence.
        """
        return int(self._src_id)

    @property
    def translation_id(self):
        """The id of the target sentence.
        """
        return int(self._tgt_id)
