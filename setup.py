"""setup tools script."""
from setuptools import setup, find_packages

setup(
    name="jfh",

    version="0.1",
    
    package_dir={"": "src"},
    
    packages=find_packages(where="src",),

    python_requires=">=3.8",

    author="Jacob Edwards Wiese",

    author_email="jake9wi@outlook.com",

    entry_points={
        "console_scripts": [
            "jfh = jfh.funcs:main",
        ]
    }

)
