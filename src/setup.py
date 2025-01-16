import sys
from setuptools import setup, Extension
import pybind11

extra_compile_args = []
if sys.platform == "darwin":  # macOS
    extra_compile_args += ["-stdlib=libc++", "-O2"]
elif sys.platform == "win32":  # Windows
    extra_compile_args += ["/O2"]  # 注意 Windows 使用不同的编译器标志格式
else:  # Linux 和其他 Unix 系统
    extra_compile_args += ["-O2"]

ext_modules = [
    Extension(
        'cpp_utils',
        ['cpp_utils.cpp'],
        include_dirs=[pybind11.get_include()],
        language='c++',
        extra_compile_args=extra_compile_args,
    ),
]

setup(
    name='cpp_utils',
    ext_modules=ext_modules,
)