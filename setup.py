from setuptools import setup

setup(
    name='UtilsPandasGeneral',
    version='0.0.1',
    description='Utility functions for Pandas DF and Excel exporting through pandas (private repo',
    url='git@github.com:volimcvijece/UtilsPandasGeneral.git',
    author='Tonko Caric',
    author_email='caric.tonko@gmail.com',
    license='unlicense',
    packages=['utilspandasgeneral'],
    # Needed for dependencies
    install_requires=['pandas', 'datetime', 'pathlib'], #no nr - any version. specify - "numpy>=1.13.3"
    zip_safe=False
)