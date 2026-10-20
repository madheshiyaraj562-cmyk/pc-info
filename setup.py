from setuptools import setup, find_packages

setup(
    name="pc-info",
    version="1.0.0",
    description="Cross-platform hardware profiler & safe shareable HTML dashboard generator.",
    author="pc-info team",
    py_modules=["pc_info", "health"],
    packages=["collectors", "renderers"],
    install_requires=[
        "psutil>=5.9.0",
        "jinja2>=3.1.0"
    ],
    entry_points={
        "console_scripts": [
            "pc-info=pc_info:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["template.html"]
    }
)
