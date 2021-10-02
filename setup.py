from setuptools import setup, find_packages

# Read long description from README
with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

# Setup the python package with dependencies
setup(
    # Package name and version and contained packages
    name='gym_csgo', version='0.0.1', packages=find_packages(),
    # Package metadata
    description="Counter-Strike: Global Offensive environment for OpenAI Gym "
                "on Linux",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iksnagreb/gym-csgo",
    author="Christoph Berganski",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux"
    ],
    # Package requirements
    install_requires=[
        'gym', 'mss', 'numpy', 'opencv-python', 'flask', 'pynput', 'pygame'
    ],
    # Add non-code files to package
    include_package_data=True,
)
