from setuptools import setup

# Setup the python package with dependencies
setup(name='gym_csgo', version='0.0.1', install_requires=[
    'gym', 'mss', 'numpy', 'opencv-python', 'flask', 'pynput', 'pygame'
])
