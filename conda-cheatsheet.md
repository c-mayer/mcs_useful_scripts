                               CONDA 4.6 CHEAT SHEET
                                  Take a conda test drive at bit.ly/tryconda     For full documentation of any command,
                                                                                 add --help to the command.
                                  Windows, macOS, Linux:
                                  Same commands for all platforms.               EXAMPLE: conda create --help


Getting Started

Verify Conda is installed, check version number                   conda info

Update Conda to the current version                               conda update -n base conda

Update all packages to the latest version of
Anaconda. Will install stable and compatible                      conda update anaconda
versions, not necessarily the very latest.


Working with Environments

Create a new environment named ENVNAME with                       conda create --name ENVNAME python=3.6
specific version of Python and packages installed.                "PKG1>7.6" PKG2

Activate a named Conda environment                                conda activate ENVNAME

Activate a Conda environment at a particular location on disk     conda activate /path/to/environment-dir

Deactivate current environment                                    conda deactivate

List all packages and versions in the active environment          conda list

List all packages and versions in a named environment             conda list --name ENVNAME

List all revisions made within the active environment             conda list --revisions

List all revisions made in a specified environment                conda list --name ENVNAME --revisions

Restore an environment to a previous revision                     conda install --name ENVNAME --revision
                                                                  REV_NUMBER

Delete an entire environment                                      conda remove --name ENVNAME --all

TIP: Anaconda Navigator is a desktop graphical user interface to manage packages and environments with
Conda. With Navigator you do not need to use a terminal to run Conda commands, Jupyter Notebooks,
JupyterLab, Spyder, and other tools. Navigator is installed with Anaconda, and may be added with Miniconda.

Sharing Environments

Make an exact copy of an environment                              conda create --clone ENVNAME --name NEWENV

Export an environment to a YAML file that can be
                                                                  conda env export --name ENVNAME > envname.yml
read on Windows, macOS, and Linux

Create an environment from YAML file                              conda env create --file envname.yml

Create an environment from the file named
                                                                  conda env create
environment.yml in the current directory

Export an environment with exact package
                                                                  conda list --explicit > pkgs.txt
versions for one OS

Create an environment based on
                                                                  conda create --name NEWENV --file pkgs.txt
exact package versions




                                                                                                        Continued on back →
Using Packages and Channels

Search for a package in currently configured channels         conda search PKGNAME=3.1 "PKGNAME
with version range >=3.1.0, <3.2"                             [version='>=3.1.0,<3.2']"

Find a package on all channels using the Anaconda
                                                              anaconda search FUZZYNAME
Client

Install package from a specific channel                       conda install conda-forge::PKGNAME

Install a package by exact version number (3.1.4)             conda install PKGNAME==3.1.4
Install one of the listed versions (OR)                       conda install "PKGNAME[version='3.1.2|3.1.4']"

Install following several constraints (AND)                   conda install "PKGNAME>2.5,<3.2"

Add a channel to your Conda configuration                     conda config --add channels CHANNELNAME




Additional Useful Hints

Detailed information about package versions                   conda search PKGNAME --info

Remove unused cached files including unused packages          conda clean --all

Remove a package from an environment                          conda uninstall PKGNAME --name ENVNAME

Update all packages within an environment                     conda update --all --name ENVNAME

Run most commands without requiring
                                                              conda install --yes PKG1 PKG2
a user prompt. Useful for scripts.

Examine Conda configuration and configuration services        conda config --show
                                                              conda config --show-sources




More Resources

Free Community Support                              http://bit.lyconda_list

Online Documentation                                https://conda.io

Paid Support Options                                anaconda.com/support

Anaconda On-Site Training Courses                   anaconda.com/training

Anaconda Consulting Services                        anaconda.com/consulting




Follow us on Twitter @anacondainc and join the #AnacondaCrew!
Connect with data scientists and developers and contribute to the open source movement at anaconda.com/community



About Anaconda

With over 11 million users, Anaconda is the world’s most popular Python data science platform and the foundation of
modern machine learning and AI. Anaconda Enterprise simplifies and automates collaboration and deployment of
machine learning and AI at speed and scale, unleashing the full potential of your organization.




                                                      anaconda.com · info@anaconda.com · 512-776-1066 · v1.2019
