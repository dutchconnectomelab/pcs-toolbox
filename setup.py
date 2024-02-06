from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="connect_toolbox",
    version="0.1.0",
    python_requires=">=3.7",
    author="Dutch Connectome Lab",
    author_email="i.libedinsky@vu.nl",
    description="An open-source toolbox for connectome-based prediction and analysis.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="",
    license="MIT",
    packages=["connect_toolbox"],
    install_requires=[
        "numpy >= 1.15.4",
        "pandas >= 1.0.0",
    ],
    extras_require={
        "test": [
            "pytest==7.4.*",
            "pytest-cov>=4.0,<4.2",
            "pytest-xdist==3.4.*",
            "pytest-mock>=3.11,<3.13",
            "snapshottest==0.6.*",
        ],
        "lint": [
            "black==23.12.1",
            "flake8==6.0.*",
            "isort==5.13.*",
            "pytype==2024.1.24",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
