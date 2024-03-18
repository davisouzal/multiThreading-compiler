# MultiThreading Compiler

This project is a compiler implemented in Python, featuring threading and socket communication. The compiler takes source code written in a simple language and translates it into executable instructions.

## Requirements

Make sure you have the following dependencies installed:

- Python 3.x

## Installation

## Usage

To use the compiler, follow these steps:

1. Clone the repository:

    ```
    git clone https://github.com/davisouzal/multiThreading-compiler.git
    ```

2. Navigate to the project directory:

    ```
    cd multiThreading-compiler/Minipar
    ```

3. Execute the compiler with your source code file:

    ```
    python Minipar.py your_source_code_file.mp
    ```

Replace `your_source_code_file.mp` with the path to your source code file.

## Features

- **Threading**: The compiler supports parallel execution of code blocks using threads.
- **Socket Communication**: It facilitates communication between different parts of the code using sockets.
- **Syntax Highlighting**: The compiler provides basic syntax highlighting for easy code understanding.
- **Tokenization**: The lexer tokenizes the source code, breaking it down into meaningful units for interpretation.
- **Interpretation**: The interpreter processes the tokenized code, executing the instructions and handling any errors encountered.

## Supported Constructs

The compiler supports the following language constructs:

- **Variables**: Declaration and assignment of integer, boolean, and string variables.
- **Arithmetic Operations**: Addition, subtraction, multiplication, and division of integer variables.
- **Logical Operations**: Comparison operators (>, <, >=, <=, ==, !=) for boolean expressions.
- **Control Flow**: IF statements with optional ELSE blocks, and WHILE loops.
- **Input/Output**: Reading input from the user and printing output to the console.
- **Threading**: Parallel execution of code blocks using threads.
- **Socket Communication**: Sending and receiving messages between client and server sockets.

## Example

Here's an example of a simple source code file:

```python
seq {
    int x = 5;
    print(x);
    
    par {
        int y = 10;
        print(y);
    }
}
