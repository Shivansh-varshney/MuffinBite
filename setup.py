from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readMeFile:
    long_description = readMeFile.read()
with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

setup(
    name='muffinbite',
    version='0.1.5',
    author='Shivansh Varshney',
    author_email='shivanshvarshney45@gmail.com',
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'bite=muffinbite.management.cli:run_cli',
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Shivansh-varshney/MuffinBite",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)