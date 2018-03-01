import setuptools


def get_version():
    """
    Gets version.

    :return: str
    """
    from os.path import dirname, join
    for line in open(join(dirname(__file__), "maze/version.py")):
        if "version" in line:
            return line.split("\"")[1]


setuptools.setup(
    name="maze",
    version=get_version(),
    description="Create and solve mazes in Python.",
    author="Julian Smolka",
    packages=[
        "maze"
    ],
    install_requires=[
        "numpy",
        "Pillow"
    ],
    package_data={
        "maze": [
            "lib/*.dll"
        ]
    }
)
