from distutils.core import setup

setup(
    name = 'nodeweightedbudget',
    packages = ['nodeweightedbudget'],
    version = '0.0.1',
    license = 'MIT',
    description = 'This package maximizes the total prize with a budget constraint for an undirected node-weighted rooted graph very loosely following Bateni 2018 algorithm from DOI:10.1137/15M102695X',
    url = 'https://github.com/ipgmvq/nodeweightedbudget',
    download_url = 'https://github.com/ipgmvq/nodeweightedbudget/archive/refs/tags/v0.0.1.tar.gz',
    keywords = ['nodeweightedbudget', 'graph', 'undirected', 'budget', 'nodeweighted'],
    classifiers = [],
    install_requires = ['numpy']
)