from setuptools import setup, find_packages


setup(
    name='stockkit',
    version='0.0.1.rc1',
    packages=find_packages('src'),
    package_dir={"": "src"},
    url='http://example.com',
    license='MIT License',
    author='ravi',
    author_email='ultra.stockkit@gmail.com',
    description='Stock decision API',
    python_requires=">=3.6",
    install_requires=['pandas>=1.2.4',
                      'yfinance==0.1.63',
                      'configparser>=5.0.2'
                      ],
    # For setting dev/test env, run:  pip install stockkit[dev]
    extras_require={'dev': ['matplotlib>=3.4.2'
                            ],
                    },
    package_data={"stockkit": ["config/*.ini"]
                  },
    keywords='stockkit'
)
