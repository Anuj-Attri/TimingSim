# Define the sequence of numbers
numbers = [64] * 28 + [32] * 16 + [16] * 16 + [8] * 16 + [4] * 16 + [2] * 16 + [1] * 7

# Write the numbers to a file
with open('vlr.txt', 'w') as file:
    for number in numbers:
        file.write(f"{number}\n")

print("File generated successfully.")