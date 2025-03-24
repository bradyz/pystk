# Python SuperTuxKart

This is a heavily modified version of the free [SuperTuxKart](https://github.com/supertuxkart/stk-code) racing game for sensorimotor control experiments.

Many parts that make SuperTuxKart fun and entertaining to play were removed, and replaced with a highly efficient and customizable python interface to the game.
The python interface supports the full rendering engine and all assets of the original game, but no longer contains any sound playback, networking, or user interface.

See [https://pystk.readthedocs.io](https://pystk.readthedocs.io) for a full documentation.

If you find a bug in this version of supertuxkart please do not report it to the original project, this project significantly diverged from the original intention of the video game.

## Hardware Requirements
To run SuperTuxKart, make sure that your computer's specifications are equal or higher than the following specifications:

* A graphics card capable of 3D rendering - NVIDIA GeForce 8 series and newer (GeForce 8100 or newer), AMD/ATI Radeon HD 4000 series and newer, Intel HD Graphics 3000 and newer. OpenGL >= 3.3
* You should have a CPU that's running at 1 GHz or faster. 
* You'll need at least 512 MB of free VRAM (video memory).
* Minimum disk space: 800 MB 

## License
The software is released under the GNU General Public License (GPL) which can be found in the file [`COPYING`](/COPYING) in the same directory as this file. Information about the licenses for the artwork is contained in `data/licenses`.

## Notes

### Development

Supports
- **OS:** Linux, MacOS, ~~Windows~~
- **Python:** 3.6, 3.7, 3.8, 3.9, 3.10, 3.11

Tested so far
- Linux 3.6, 3.11

This script creates a temporary conda env + builds the wheel.

TODO: have some automated testing for correctness

```bash
PYTHON_VERSION=3.11

source make_wheel.sh $PYTHON_VERSION
```

### Release

Relevant files:
- `.github/workflows/wheels.yml`
- `CMakeLists.txt`

Workflow:
```bash
TAGNAME=v0.5

git commit -m "new release yay"

# check what tags have been used already
# git tag

git tag $TAGNAME

# this only pushes the commit
git push origin master

# REQUIRED: for CI to start building
git push origin $TAGNAME
```

Then check out the TAGS tab in the github repo to see the build and pray there's no failures


