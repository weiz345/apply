for i in range(1, 6):
    filename = f"resume_{i}.txt"
    with open(filename, 'w') as f:
        f.write(f"This is {filename}\n")
    print(f"Created: {filename}")
