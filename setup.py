import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stock-trading-backend", # Replace with your own username
    version="0.0.1",
    author="Igor Ryzhkov",
    author_email="igor.o.ryzhkov@gmail.com",
    description="Back-end for stock trading with reinforcement learning.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iryzhkov/stock-trading-backend",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
