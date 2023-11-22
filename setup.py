from setuptools import setup, find_packages

setup(
    name="my_package",  
    version="0.1.0",  
    author="Manoj Kumar Singade",  
    author_email="msingade@mail.yu.edu",  
    description="A package for extracting and analyzing web data",  
    long_description=open(
        "README.md"
  ).read(),  # Long description read of the the readme file
    long_description_content_type="text/markdown",
    url="",  
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "pandas>=1.2.0",
        "beautifulsoup4>=4.9.3",
        
   
    ],
