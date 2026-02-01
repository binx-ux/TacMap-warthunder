from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tacmap",
    version="1.0.0",
    author="binxix",
    author_email="antmanitis7@gmail.com",
    description="Read-only tactical map overlay for War Thunder - displays game data on secondary monitor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/binx-ux/tacmap",  # Update this
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows",
        "Environment :: Win32 (MS Windows)",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pygame>=2.5.0",
    ],
    entry_points={
        "console_scripts": [
            "tacmap=tacmap.main:main",
            "tacmap-scanner=tacmap.scanner:main",
        ],
    },
    include_package_data=True,
    package_data={
        "tacmap": ["config/*.json"],
    },
    keywords="warthunder tactical map overlay memory scanner game",
    project_urls={
        "Bug Reports": "https://github.com/binx-ux/tacmap/issues",
        "Source": "https://github.com/binx-ux/tacmap",
        "Documentation": "https://github.com/binx-ux/tacmap#readme",
    },
)
