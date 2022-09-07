from setuptools import setup

setup(
    name="PySvelte",
    version="1.0.0",
    packages=["pysvelte"],
    license="LICENSE",
    description="A library for visualising and interpreting ML model activations in IPython and Jupyter notebooks",
    long_description=open("README.md").read(),
    install_requires=[
        'einops',
        'numpy',
        'torch',
        'datasets',
        'transformers',
        'tqdm',
        'pandas',
        'typeguard'
    ]
)
