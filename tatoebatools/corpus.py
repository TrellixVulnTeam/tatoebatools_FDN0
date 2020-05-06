import csv
import logging
from datetime import datetime

from .config import SENTENCES_DIR
from .utils import lazy_property
from .version import Versions


class Corpus:
    """The Tatoeba file containing the detailed sentences in a given language.
    """

    _dir = SENTENCES_DIR

    def __init__(self, language_code):

        # the language code of the sentences (ISO-639 code most of the time)
        self._lg = language_code

    def __iter__(self):

        try:
            with open(self.path) as f:
                fieldnames = [
                    "sentence_id",
                    "lang",
                    "text",
                    "username",
                    "date_added",
                    "date_last_modified",
                ]
                rows = csv.DictReader(f, delimiter="\t", fieldnames=fieldnames)
                for row in rows:
                    yield Sentence(**row)
        except OSError:
            logging.exception(f"an error occurred while reading {self.path}")

    @property
    def filename(self):
        """Get the name of the file of this corpus.
        """
        return f"{self._lg}_sentences_detailed.tsv"

    @property
    def path(self):
        """Get the path of the corpus' datafile.
        """
        return Corpus._dir.joinpath(self.filename)

    @lazy_property
    def version(self):
        """Get the version of the downloaded data of this corpus.
        """
        return Versions().get(self.filename)


class Sentence:
    """A sentence from the Tatoeba corpus.
    """

    def __init__(
        self, sentence_id, lang, text, username, date_added, date_last_modified
    ):

        self._id = sentence_id
        self._lg = lang
        self._txt = text
        self._usr = username
        self._dtad = date_added
        self._dtlm = date_last_modified

    @property
    def id(self):
        """Get the id of the sentence.
        """
        return int(self._id)

    @property
    def lang(self):
        """Get the language of the sentence.
        """
        return self._lg

    @property
    def text(self):
        """Get the text of the sentence.
        """
        return self._txt

    @property
    def username(self):
        """Get the name of the author of the sentence.
        """
        return self._usr

    @property
    def date_added(self):
        """Get the date of the addition of the sentence.
        """
        try:
            dt = datetime.strptime(self._dtad, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            dt = None
        finally:
            return dt

    @property
    def date_last_modified(self):
        """Get the date of the last modification of the sentence.
        """
        try:
            dt = datetime.strptime(self._dtlm, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            dt = None
        finally:
            return dt
