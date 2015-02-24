from setuptools import setup

setup(
    name='pySUMO',
    version='0.0.0a1',
    description='A graphical IDE for Ontologies written in SUO-Kif',
    long_description='A graphical IDE for Ontologies written in SUO-Kif',
    url='',
    author='',
    author_email='',
    license='',
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'License :: ',
                 'Programming Language :: Python :: 3.4',
                ],
    keywords='SUMO Ontologies SUO-Kif',
    package_dir={'':'src'},
    packages=['pysumo', 'pysumo.logger', 'pySUMOQt', 'pySUMOQt.Designer', 'pySUMOQt.Widget'],
    install_requires=['pyside'],
    data_files=[('data', ['data/Merge.kif', 'data/MILO.kif']),
                ('data/wordnet', [''.join(['data/wordnet/sdata.', x]) for x in
                                  ['adj', 'adv', 'noun', 'verb']]),],
    entry_points={'gui_scripts': ['pySUMOQt = pySUMOQt.MainWindow:main']},
)

