<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
    <img src="https://github.com/dave-lanigan/lambchop/assets/29602997/9c0826c8-b6b0-4ad7-84f4-85ff4b1e7c74" alt="Logo" width="250" height="250">

  <h3 align="center">lambchop</h3>

  <p align="center">
    A sidekick that makes your AWS Lambda async
  <br/>

   ![](https://img.shields.io/badge/language-python-blue)
   ![version](https://img.shields.io/badge/version-1.2.3-green)
   ![](https://img.shields.io/badge/license-MIT-red)
   
  </p>
</div>

## Overview

`lambchop` is an Python package that gives regular AWS Lambda asyncronous functionality by allow them to run background processes. This works by utilizing AWS Lambda [extensions](https://docs.aws.amazon.com/lambda/latest/dg/lambda-extensions.html) which runs in a different process that the main lambda function code.


## Installation
pypi:

```
pip install lambchop
```

github:

```
pip install git+ssh://git@github.com/dave-lanigan/lambchop.git
```
```
pip install git+https://git@github.com/dave-lanigan/lambchop.git
```

> 📝 Sudo privileges may be required since the lambda extensions is placed in the `/opt/extensions/` directory.

## Usage

```
import anyio
import time
from lambchop import SideKick

def long_running_process(x, y):
    print("Starting process.")
    time.sleep(x + y)
    print("Completed.")


def main():
    sk = SideKick()
    sk.process(long_running_process, x=5, y=3)
    print("Done sending.")

if __name__ == "__main__":
    main()
```
