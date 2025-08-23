import setuptools
from setuptools import setup 

setup(
    name='sphericalpolygon',
    version='1.2.3',
    description='A package to handle the spherical polygon',
    author='Chunxiao Li',
    author_email='lcx366@126.com',
    url='https://github.com/lcx366/SphericalPolygon',
    license='MIT',
    long_description_content_type='text/markdown',
    long_description=open('README.md', 'rb').read().decode('utf-8'),
    keywords = ['spherical polygon','polygon area','polygon inertia tensor'],
    python_requires = '>=3.11',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'License :: OSI Approved :: MIT License',
        ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'scipy',
        'numpy'
        ],
    )
