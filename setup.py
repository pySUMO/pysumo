from setuptools import setup

setup(
    name='pySUMO',
    version='1.1',
    description='A graphical IDE for Ontologies written in SUO-Kif',
    long_description='A graphical IDE for Ontologies written in SUO-Kif',
    url='',
    author='',
    author_email='',
    license='BSD',
    classifiers=['Development Status :: 2 - Pre-Alpha',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Programming Language :: Python :: 3.4',
                ],
    keywords='SUMO Ontologies SUO-Kif',
    package_dir={'':'src'},
    packages=['pysumo', 'pysumo.logger', 'pySUMOQt', 'pySUMOQt.Designer', 'pySUMOQt.Widget'],
    package_data={'pysumo':['data/*.kif', 'data/wordnet/sdata.*']},
    install_requires=['pyside', 'pygraphviz>=1.3rc2','sphinxcontrib-plantuml'],
    entry_points={'gui_scripts': ['pySUMOQt = pySUMOQt.MainWindow:main']},
)

