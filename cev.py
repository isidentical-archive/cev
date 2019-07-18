import codecs
import pkgutil
import importlib
from io import BytesIO
from pathlib import Path
from functools import lru_cache, partial
from tokenize import tokenize, untokenize

TRANSLATIONS = {
    "tr": {
        "eger": "if",
        "ve": "and",
        "degilse": "else",
    }
}

LANG_PATH = Path("languages").absolute()

@lru_cache(1)
def language_toolkit(language):
    """ Disabled because simple is better than complex ¯\_(ツ)_/¯ """

    language_files = pkgutil.iter_modules(path = (str(LANG_PATH),))
    for language_file in language_files:
        if language_file.name == language:
            module_finder = language_file.module_finder
            module_loader = module_finder.find_loader(language)[0]
            namespace = {}
            exec(module_loader.get_code(language), namespace)
            return namespace.get("TRANSLATIONS")
            

def decode(buffer, errors="replace", language = "en"):
    toolkit = TRANSLATIONS[language]
    stream = BytesIO(bytes(buffer)).readline
    
    modified_source_tokens = []
    for token in tokenize(stream):
        if token.string in toolkit:
            token = token._replace(string = toolkit[token.string])
        
        modified_source_tokens.append(token)

    return str(untokenize(modified_source_tokens), "utf-8"), len(buffer)


class CevIncrementalDecoder(codecs.BufferedIncrementalDecoder):
    def _buffer_decode(self, data, errors, final):
        if final:
            return decode(data, errors, language = self._language)
        else:
            return ("", 0)

def translate(language):
    if language in TRANSLATIONS:
        encoding = language.strip(language).strip("-") or "utf8"
        encoding = codecs.lookup(encoding)
        
        CevIncrementalDecoder._language = language
        
        language_codec = codecs.CodecInfo(
            name=language,
            encode=encoding.encode,
            decode=partial(decode, language = language),
            incrementalencoder=encoding.incrementalencoder,
            incrementaldecoder=CevIncrementalDecoder,
            streamreader=encoding.streamreader,
            streamwriter=encoding.streamwriter,
        )
        return language_codec

