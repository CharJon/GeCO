from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    readme_text = f.read()


setup(
    name="GeCO",
    version="1.0.3",
    description="Generators for Combinatorial Optimization",
    long_description=readme_text,
    long_description_content_type="text/markdown",
    url="https://github.com/CharJon/GeCO",
    license="MIT License",
    packages=find_packages(exclude=("tests", "docs", "data", "notebooks", "examples")),
    install_requires=["pyscipopt", "networkx", "numpy"]
)
