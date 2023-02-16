from setuptools import (
    find_packages,
    setup,
)

with open('README.md', encoding='utf-8') as readme:
    long_description = readme.read()


setup(
    name='lord-of-the-clips',
    version='0.1.10',
    license='MIT',
    description=(
        '🎥✂️🔗 Video downloader, trimmer, and merger using the terminal.'
        ' Supports YouTube, Facebook, Reddit, Twitter, TikTok, Instagram, LinkedIn, 9GAG, etc.'
        ' Downloads/trims at multiple points. Merges multiple clips.'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ranel Padon',
    author_email='ranel.padon@gmail.com',
    url='https://github.com/ranelpadon/lord-of-the-clips',
    python_requires='>=3.7',
    packages=find_packages(),
    include_package_data=True,
    install_requires=open('requirements.txt').read().splitlines(),
    entry_points={
        'console_scripts': [
            'lotc = lotc.main:cli',
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
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
    platforms=['Windows', 'macOS', 'Linux'],
)
