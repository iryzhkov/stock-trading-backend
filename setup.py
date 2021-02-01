import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stock-trading-backend",
    version="0.0.1",
    author="Igor Ryzhkov",
    author_email="igor.o.ryzhkov@gmail.com",
    description="Back-end for stock trading with reinforcement learning.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iryzhkov/stock-trading-backend",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires='>=3.7',
)
