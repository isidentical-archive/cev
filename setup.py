import distutils
import os

from setuptools import setup, Extension
from setuptools.command.install import install

from setuptools import setup, find_packages 


class Installer(install):
    def initialize_options(self):
        super().initialize_options()
        contents = "import sys; exec({!r})\n".format(self.read_pth("cev.pth"))
        self.extra_path = (self.distribution.metadata.name, contents)

    def read_pth(self, path):
        with open(path) as f:
            content = f.read()
        return content

    def finalize_options(self):
        super().finalize_options()

        install_suffix = os.path.relpath(self.install_lib, self.install_libbase)
        if install_suffix == self.extra_path[1]:
            self.install_lib = self.install_libbase

setup(
    name="cev",
    version="0.1",
    description="Cevir",
    author = "btaskaya",
    author_email = "batuhanosmantaskaya@gmail.com",
    url = "https://github.com/isidentical/cev",
    py_modules=["cev"],
    cmdclass={"install": Installer},
)
