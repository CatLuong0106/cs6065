import pathlib
import socket
from collections import Counter
 
def main():
    nwords1, nwords2 = 0, 0
    if_words = []

    # List name of all the text file at location: /home/data
    cwd = pathlib.Path("/home/data")
    files = list(cwd.glob('*.txt'))

    # Read the two text files and count total number of words in each text files
    # List the top 3 words with maximum number of counts in IF.txt. Include the word counts for the top 3 words.

    for file in files: 
        if file.name == "IF.txt": 
            with open(file,'r', encoding="utf-8") as f:
                data = f.read()
                lines = data.split()
                for line in lines:
                    words = line.split()
                    if_words.extend(words)
                    nwords1 += len(words)
        elif file.name == "Limerick-1.txt": 
            with open(file,'r', encoding="utf-8") as f: 
                data = f.read()
                lines = data.split()
                for line in lines: 
                    nwords2 += len(line.split())

    # Find the IP address of your machine

    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

    # Write all the output to a text file at location: /home/output/result.txt (inside your container).
    pathlib.Path("/home/output").mkdir(parents=True, exist_ok=True)
    out_path = pathlib.Path("/home/output/result.txt")

    with open(out_path, 'w', encoding='utf-8') as f: 
        f.write(f"The text files at the data location is: {[str(file.name) for file in files]}\n")
        f.write(f"The number of words for IF.txt is {nwords1}\n")
        f.write(f"The number of words for Limerick-1.txt is {nwords2}\n")
        f.write(f"The total number of words for both text files is {nwords1 + nwords2}\n")
        f.write(f"The top 3 words with maximum number of counts in IF.txt is: {Counter(if_words).most_common()[0:3]}\n")
        f.write(f"Your Computer Name is: {hostname}\n")
        f.write(f"Your Computer IP Address is: {IPAddr}")

    # Print it all to the terminal
    with open(out_path, 'r', encoding='utf-8') as f: 
        lines = f.readlines()
        for line in lines:
            print(line)

if __name__ == "__main__":
    main()



