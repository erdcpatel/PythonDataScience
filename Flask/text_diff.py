def compare_files(file1, file2):
    chunk_size = 1024 * 1024  # 1 MB

    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        while True:
            chunk1 = f1.read(chunk_size)
            chunk2 = f2.read(chunk_size)
            if chunk1 != chunk2:
                line_number = 1
                for line1, line2 in zip(chunk1.splitlines(), chunk2.splitlines()):
                    if line1 != line2:
                        print(f"Line {line_number}: {line1} != {line2}")
                        print(f"Difference: {line1.split() != line2.split()}")
                        line_number += 1
                        if line_number > 5:
                            break
                break

compare_files("file1.txt", "file2.txt")
