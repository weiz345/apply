import glob
import os

def combine_python_files():
    py_files = glob.glob('*.py')
    combined_content = ''

    for filename in py_files:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        combined_content += f"### File: {filename}\n\n{content}\n\n"

    return combined_content

if __name__ == "__main__":
    output = combine_python_files()
    print(output)
