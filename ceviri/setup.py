from setuptools import setup, Extension

hookify = Extension(
    name = 'ceviri',
    sources = ['ceviri.c', 'lpyhook.c'],
)
    
setup(
    name = 'ceviri',
    version = '0.1',
    author = 'BTaskaya',
    author_email = 'batuhanosmantaskaya@gmail.com',
    url = "https://github.com/isidentical/cev",
    description = "Helper package to cev",
    ext_modules = [hookify]
)
