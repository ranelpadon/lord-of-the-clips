import io
from setuptools import (
    find_packages,
    setup,
)


def dependencies(file):
    with open(file) as f:
        return f.read().splitlines()


with io.open('README.md', encoding='utf-8') as readme_file:
    long_description = readme_file.read()


setup(
    name='Lord of the Clips',
    version='0.1.0',
    license='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
    ],
    python_requires='>=3.7',
    description='Video downloader, trimmer, and merger using the terminal. Supports YouTube, Facebook, Reddit, Twitter, etc. Trims at multiple points and merges multiple clips.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ranel Padon',
    author_email='ranel.padon@gmail.com',
    url='https://github.com/ranelpadon/lord-of-the-clips',
    keywords=[
        'video',
        'downloader',
        'trimmer',
        'snipper',
        'cutter',
        'merger',
        'splicer',
        'cli',
        'terminal',
        'youtube',
        'facebook',
        'reddit',
        'twitter',
        'multiple',
        'click',
        'rich',
        'movie',
        'snip',
        'clip',
        'subclip',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=dependencies('requirements.txt'),
    entry_points={
        'console_scripts': [
            'lotc = main:cli',
        ],
    },
)
