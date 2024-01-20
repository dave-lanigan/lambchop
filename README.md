<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
    <img src="static/logo.jpg" alt="Logo" width="250" height="250">

  <h3 align="center">lambchop</h3>

  <p align="center">
    🐑 A sidekick for your AWS Lambda 🐑
  <br/>

   ![](https://img.shields.io/badge/language-python-blue)
   ![version](https://img.shields.io/badge/version-1.2.3-green)
   ![](https://img.shields.io/badge/license-mit-red)
   

  </p>
</div>

## Overview

`lambchop` is an Python package to make AWS Lambda functions asyncronous.


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

## Usage

```
import time
from lambchop import SideKick

def long_running_process(x, y):
    print("Starting process.")
    time.sleep(x + y)
    print("Completed.")

sk = SideKick()
sk.process(long_running_process, x=5, y=3)
```
