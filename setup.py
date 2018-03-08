from setuptools import setup

setup(
    name='csdownloader',
    version='0.0.1',
    description='A tool for extracting data via API provided by Clearspending.ru',
    url='https://github.com/ansakoy/cs_downloader',
    author='Anna Sakoyan',
    author_email='ansakoy@gmail.com',
    install_requires=['openpyxl', 'python-telegram-bot', 'requests'],
    packages=['downloader'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Natural Language :: Russian',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Database :: Front-Ends'
    ]
)
