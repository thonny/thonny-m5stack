from setuptools import setup
import os.path

setupdir = os.path.dirname(__file__)

requirements = []
for line in open(os.path.join(setupdir, 'requirements.txt'), encoding="UTF-8"):
    if line.strip() and not line.startswith('#'):
        requirements.append(line)

setup(
      name="thonny-m5stack",
      version="0.1b1",
      description="M5Stack MicroPython support for Thonny IDE",
      long_description="""Plug-in for Thonny IDE which M5Stack MicroPython backends. 
      
More info: 

* https://github.com/thonny/thonny-m5stack
* https://github.com/thonny/thonny/wiki/MicroPython
* https://thonny.org
""",
      url="https://github.com/thonny/thonny-m5stack",
      author="Aivar Annamaa",
	  author_email="aivar.annamaa@gmail.com",
      license="MIT",
      classifiers=[
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "License :: Freeware",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Education",
        "Topic :: Software Development",
        "Topic :: Software Development :: Embedded Systems",
      ],
      keywords="IDE education programming M5Stack ESP32 MicroPython Thonny",
      platforms=["Windows", "macOS", "Linux"],
      python_requires=">=3.5",
      include_package_data=True,
	  package_data={'thonnycontrib.m5stack': ['api_stubs/*']},
      install_requires=requirements,
      packages=["thonnycontrib.m5stack"],
)
