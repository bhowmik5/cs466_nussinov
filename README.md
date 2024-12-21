# CS 466 Nussinov's Project

## Nussinov RNA Folding Project
This project implements a solution for RNA secondary structure prediction using the Nussinov algorithm. The core script, nussinovs_code.py performs RNA structure folding and outputs the predicted structure in dot-bracket notation, while the other scripts facilitate testing and managing input/output.

## Contents

  1. [Installation](#install)
     * [Using pip](#compilation)
          * [Dependencies](#pre-requisites)
  2. [Usage instructions](#usage)

<a name="install"></a>

## Installation

### Using pip

<a name="pre-requisites"></a>
#### Pre-requisites
+ python3 (>=3.6)
+ [numpy](https://numpy.org/doc/)
+ [pandas](https://pandas.pydata.org/pandas-docs/stable/index.html)

<a name="install"></a>
  1. Clone the repository
      ```bash
            $ git clone https://github.com/bhowmik5/cs466_nussinov
        ```
  2. Navigate to the project directory in your terminal.
  3. Run the program with
      ```bash
            python3 nussinov.py
        ```
## Usage instructions
When executing nussinov.py, you will be prompted to enter a RNA sequence. Upon entering the RNA sequence, the program will output a list of possible structures for that given sequence.

## Authors
Anuprova Bhowmik <br />
Diptatanu Das <br />
Zheng Wei <br />
