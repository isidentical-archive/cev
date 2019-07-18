from __future__ import annotations
import platform
from contextlib import contextmanager
from collections import deque
from dataclasses import dataclass
from typing import Optional, List
import textwrap


@dataclass
class Sign:
    typ: str
    name: str
    args: Optional[Sign] = None

    def __str__(self):
        return f"{self.typ} {self.name}"


@dataclass
class Pragma:
    typ: str
    args: Optional[List[str]] = None
    content: Optional[str] = None


class Code(deque):
    def __str__(self):
        return "\n".join(self)

    def write(self, *args, **kwargs):
        return self.append(*args, **kwargs)

    def head(self, *args, **kwargs):
        return self.appendleft(*args, **kwargs)

    def nl(self, fr):
        if fr == "h":
            self.head("")
        else:
            self.write("")


@contextmanager
def gcode(code_type="source", libs=None, alias=None):
    code = Code()
    try:
        yield code
    finally:
        if code_type == "source":
            libs = libs or []
            code.nl("h")
            for lib in libs:
                if not lib.startswith("_"):
                    code.head(f"#include <{lib}.h>")
                else:
                    code.head(f'#include "{lib[1:]}.h"')
                    code.nl("h")
        elif code_type == "lib":
            alias = alias.upper()
            code.nl("h")
            code.head(f"#define {alias}_H")
            code.head(f"#ifndef {alias}_H")
            code.nl("t")
            code.write("#endif")
            code.nl("t")
        return code


class CGen:
    CGEN_SUPPORTES = {"Linux", "Darwin"}

    def __init__(self, alias):
        if platform.system() not in self.CGEN_SUPPORTES:
            raise OSError(f"LHook doesn't support your platform: {platform.system()}")
        self.alias = alias
        self.source = None
        self.header = None

    def generate(self):
        with open(f"{self.alias.lower()}.c", "w") as source:
            source.write(str(self.source))
        
        with open(f"{self.alias.lower()}.h", "w") as header:
            header.write(str(self.header))

    def gen_header(self, *signs):
        manager = gcode(code_type="lib", alias=self.alias)
        with manager as code:
            for sign in signs:
                code.write(f"{sign}({', '.join(map(str, sign.args))});")

        self.header = code

    def gen_source(self, source, libs=None, pragmas=None):
        manager = gcode(code_type="source", libs=libs, alias=self.alias)
        with manager as code:
            pragmas = pragmas or []
            for pragma in pragmas:
                code.write(f"#pragma {pragma.typ}({', '.join(pragma.args)})")
                if pragma.content:
                    code.write("\n".join(pragma.content))

            code.write(source)

        self.source = code
