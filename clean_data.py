min_token = 32
max_token = 64

def split_content(tokens, max_token, f):
    if len(tokens) < min_token: return
    if len(tokens) > max_token:
        return split_content(" ".join(tokens.split()[:len(tokens.split())//2]), max_token, f) \
            or split_content(" ".join(tokens.split()[len(tokens.split())//2:]), max_token, f)
    return f.write("".join(tokens) + "|\n")


batch = []
with open("./dump/books_content_dataset.txt", "r", encoding="utf-8") as dump, \
     open("./dump/dataset.txt", "a", encoding="utf-8") as dataset:

    for line in dump:
        if line.isupper():
            split_content(" ".join(batch), max_token, dataset)
            batch = []
            continue
        batch.append(line.strip().lower())


            

