from setuptools import setup

setup(
    name="crykak",
    version="0.0.1",
    packages=["crykak"],
    extras_require={
        "test": ["pytest"],
        "lint": [
            "pysen==0.10.1",
            "black==21.10b0",
            "flake8==4.0.1",
            "isort==5.10.1",
            "mypy==0.910",
        ],
    },
)
