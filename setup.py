import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gefragt_gejagt",
    version="0.0.2",
    author="Simeon Keske, Der mit dem Zopf",
    author_email="simeon@noemis.me, der@mit-dem-zopf.cf",
    description="The studio software for the quizgame 'Gefragt Gejagt'",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nkreer/gefragt-gejagt-studio",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Operating System :: OS Independent",
        "Natural Language :: German",
        "Topic :: Games/Entertainment",
    ],
    install_requires=['eel'],
    python_requires='>=3.6',
)
