from setuptools import setup, find_packages

setup(
    name="market_sim",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'matplotlib',
        'networkx',
        'pandas',
        'numpy'
    ],
    author="Torbellino Tech SL",
    author_email="juan.diez@torbellino.tech",
    description="Market simulation engine with blockchain consensus",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://www.torbellino.tech/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        'console_scripts': [
            'run-consensus=simulation.scenarios.consensus_scenario:main'
        ]
    }
)