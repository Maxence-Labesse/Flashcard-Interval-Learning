from setuptools import setup
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='Flashcard-Interval-Learning',
    version='1.0.0',
    description="Software for interval learning with Flash cards",
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/Maxence-Labesse/Flashcard-Interval-Learning',
    author='Maxence LABESSE',
    author_email="maxence.labesse@yahoo.fr",
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["flashcards.utils"]
)
