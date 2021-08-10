import setuptools


setuptools.setup(
    name='stockkit',
    version='0.0.1.rc1',
    packages=setuptools.find_packages(where="src"),
    package_dir={'': 'stockkit/src'},
    url='http://example.com',
    license='MIT License',
    author='ravi',
    author_email='ultra.stockkit@gmail.com',
    description='Stock decision API',
    python_requires=">=3.6"
)
