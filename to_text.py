from PyPDF2 import PdfFileReader as pdf

with open("dict.pdf", "rb") as f:
    reader = pdf(f)

    start = 24
    end = 270
    text = ""
    for i in range(start, end):
        page = reader.getPage(i)
        text += page.extractText()

pos = ["art", "conj", "prep", "v", "pron", "adj", "adv", "nm",
        "nf", "num", "interj", "nc", "nmf", "nm/f"]

register = {"o": "oral",
            "f": "fiction",
            "nf": "non-fiction",
            "w": "web"}

def exceptions(l):
    keywords = ["1954 –", "25 grados", "–", "1996 –",
            "26,000", "12, 1492", "12 de",
            "«nunca»", "“never”", "300,000",
            "46%", "«Cuerpo Perfecto»", "30 a los 60",
            "+ b² =", "19th century", "1813 – Hegel",
            "4,000 francs", "18th century", "30 representatives",
            "“We don’t", "7 usd", "36.000 kilómetros",
            "2-kilometer", "$60.", "100 o más",
            "20 a 35 años", "15 mil estudiantes", "7 años de"]
    ex = [l.startswith(k) for k in keywords]
    if any(ex):
        return True
    else:
        return False

def genres(l):
    genre = ["12. Professions (profesión 1513-F) Top words # 1–5000",
            "7012-M cricket",
            "10. Natural features and plants  Top 60 words",
            "13. Creating nouns",
            "15. Nouns—differences across genres",
            "1418 impossible",
            "18. Nationalities and place adjectives",
            "19. Adjectives with ser/estar",
            "20. Adjectives of emotion (sentir + ADJ)  Top 65 Words",
            "21. Adjectives—differences across genres",
            "4311 fearful",
            "22. Verbs of movement (go from A to B)  Top 40 words # 1–8000",
            "24. Use of the “reflexive marker” se",
            "25. Preterit/imperfect  Top 50 words # 1–8000",
            "27. Verbs—differences across genres",
            "28. Adverbs—differences across genres",
            "29. New words since the 1800s  Top 50 words # 1–8000"
            ]
    ex = [l == g for g in genre]
    if any(ex):
        return True
    else:
        return False

with open("frequency.txt", "w") as f:
    lines = text.split("\n")
    lines = [l.strip() for l in lines]
    inside = False
    example = "" 
    for l in lines:
        if not l[0].isdigit() and not inside:
            continue
        else:
            if genres(l):
                inside = False
                continue
            if l.split()[0][-1] in ["M", "F"]:
                # genre-based vocab list
                continue
            # definition
            print("Reading line {}".format(l))
            if l[0].isdigit() and not exceptions(l):
                inside = True
                tokens = l.split()
                if l[1] == ".":
                    # genre-based vocab list
                    continue
                if not tokens[1][0].isalpha():
                    freq_book = tokens[0] # non-fiction, fiction, spoken
                    freq_web = tokens[2]
                    if len(tokens) == 4:
                        genre = tokens[3]
                    inside = False
                    print(example)
                    if " - " in example:
                        src, trg = example.split(" - ")
                    else:
                        src, trg = example.split(" – ")
                    f.write("{}\n".format(src))
                    f.write("{}\n".format(trg))
                    # these scraped lines below are not reliable
                    # f.write("Book frequency: {}\n".format(freq_book))
                    # f.write("Web frequency : {}\n".format(freq_web))
                else:
                    index = int(tokens[0])
                    cursor = 1
                    word = []
                    for i in range(1, len(tokens)):
                        if tokens[i][-1] == ",":
                            w = tokens[i][:-1]
                            word.append(w)
                        else:
                            w = tokens[i]
                            word.append(w)
                            cursor += i
                            break
                    pos = tokens[cursor]
                    sem = " ".join(tokens[cursor+1:])
                    f.write("{}\n".format(index))
                    f.write("{}\n".format(word))
                    f.write("{}\n".format(pos))
                    f.write("{}\n".format(sem))
            elif l.startswith("•"):
                if l == "•and youth":
                    # typo
                    example += l.strip("•")
                else:
                    example = l.strip("•")
            elif l[0].isalpha() or exceptions(l):
                example += (" " + l)

                # print("Unknown line: {}".format(l))