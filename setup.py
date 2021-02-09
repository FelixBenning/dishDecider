from setuptools import setup

setup(
    name='dishDecider',
    version='0.0.1',
    py_modules=[ 'dishDecider' ],
    install_requires=[
        "PyYAML>=5.3.1",
        "numpy>=1.20.0"
    ],
    entry_points='''
        [console_scripts]
        select-dish=dishDecider:print_select_dish
    ''',
)
