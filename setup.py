from setuptools import setup

setup(
    name="pc-info",
    version="2.3.7",
    description="Cross-platform hardware profiler & safe shareable HTML dashboard generator.",
    author="Raj Madheshiya",
    py_modules=["pc_info", "health"],
    packages=["collectors", "renderers"],
    install_requires=[
        "psutil>=5.9.0",
        "jinja2>=3.1.0",
    ],
    entry_points={
        "console_scripts": [
            "pc-info=pc_info:main",
        ],
    },
    include_package_data=True,
    package_data={
        "renderers": ["template.html"],
    },
)
