from setuptools import setup, find_packages

setup(
    name='rooter',
    description="Python Package",
    version='1.0.0',
    author='MG',
    author_email='m.gedaliah57@gmail.com',
    url='https://github.com/mg-project0/rooter',
    python_requires=">=3.10",
    packages=find_packages(exclude=['test']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Idependant"
    ]
)