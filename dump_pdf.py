from tika import parser
import string

# string.ascii_letters

raw = parser.from_file("./assets/mind.pdf")

data: "list[str]"
data = [x + "\n" for x in list(filter(lambda x: len(x) > 3, raw["content"].split("\n")))]

# for idx, line in enumerate(data):
#     line = line.strip()
#     if line.isupper() and len(line.split()) == 1:
#         data[idx] = "\n"
    

with open("./dump/books_content_dataset.txt", "a", encoding='utf-8') as f:
    f.writelines(data)
    f.write(f"{'='*100}\n")
