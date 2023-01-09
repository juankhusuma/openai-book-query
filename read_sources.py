import os
from pypdf import PdfReader

def dump(include: "list[str]" = None) -> '[str]':
    for root, _, files in os.walk("sources"):
        for file in files:
            if include and file not in include:
                continue
            path = os.path.join(root, file)
            with open(os.path.join("ai_generated/dumps", file), "w", encoding="utf-8") as g:
                pass
            with open(os.path.join("ai_generated/dumps", file), "a", encoding="utf-8") as f:
                reader = PdfReader(path)
                for idx, page in enumerate(reader.pages):
                    if idx == 0:
                        continue
                    content = page.extract_text().lower()
                    if "............." in content:
                        continue
                    f.write(content)
                pass

if __name__ == '__main__':
    dump()