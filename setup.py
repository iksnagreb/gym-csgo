from setuptools import setup, find_packages

# Read long description from README
with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

# Setup the python package with dependencies
setup(
    # Package name and version and contained packages
    name='gym-csgo', version='0.0.3', packages=find_packages(),
    # Package metadata
    description="Counter-Strike: Global Offensive environment for OpenAI Gym "
                "on Linux",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iksnagreb/gym-csgo",
    author="Christoph Berganski",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
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
