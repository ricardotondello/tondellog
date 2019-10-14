import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tondellog",
    version="0.0.1",
    author="Ricardo Tondello",
    author_email="rkdtondello@gmail.com",
    description="Gera o changelog com base no GitLab",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    entry_points={
          'console_scripts': [
              'tondellog = tondellog.commandline:main'
          ]
      },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)