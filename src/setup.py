from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        'cpp_utils',
        ['cpp_utils.cpp'],
        include_dirs=[pybind11.get_include()],
        language='c++'
    ),
]

setup(
    name='cpp_utils',
    ext_modules=ext_modules,
)