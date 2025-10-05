from setuptools import setup

setup(
    name='life',
    author='Joan A. Pinol  (japinol)',
    version='1.0.4',
    license='MIT',
    description='John Conway\'s Game of Life.',
    long_description='John Conway\'s Game of Life.',
    url='https://github.com/japinol7/life',
    packages=['life', 'tests'],
    python_requires='>=3.13',
    install_requires=['pygame-ce'],
    entry_points={
        'console_scripts': [
            'life=life.__main__:main',
            ],
    },
)
