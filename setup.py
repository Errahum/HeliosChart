from setuptools import setup, find_packages

setup(
    name='helioschart',
    version='1.0.0',
    author='Errahum',
    description='A project for fine-tuning OpenAI models using HeliosTuner.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Errahum/helioschart',
    packages=find_packages(),
    install_requires=[
        'PyQt5',
        'matplotlib',
        'pandas'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'helioschart=helioschart:helioschart',
        ],
    },
    include_package_data=True,
    license='MIT',
)