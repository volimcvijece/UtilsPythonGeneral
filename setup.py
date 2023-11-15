from setuptools import setup

setup(
    name='UtilsPythonGeneral',
    version='0.0.2',
    description='Utility functions for Python, Pandas DF and Excel exporting through pandas',
    url='git@github.com:volimcvijece/UtilsPythonGeneral.git',
    author='Tonko Caric',
    author_email='caric.tonko@gmail.com',
    license='unlicense',
    packages=['utilspythongeneral'],
    # Needed for dependencies
    install_requires=['pandas', 'datetime', 'pathlib'], #no nr - any version. specify - "numpy>=1.13.3"
    zip_safe=False
)