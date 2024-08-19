from tabula import read_pdf
from sys import argv, exit


def parse_elektron_manual(path, page) -> str:
    """
    Parses a PDF for tables and creates a JSON from the data.
    It returns the filename of the newly created JSON file.
    """
    df = read_pdf(path,
                  pages=page,
                  lattice=True
                  )

    # Assumes full path, and device name is before "_User_Manual_"
    name = path.split("/")[-1]
    name = name.split("_User")[0] + ".json"
    print(name)

    with open(name, "w") as f:
        # manually create a json-array of each entry
        f.write("[")
        for data in df:
            data.drop(data.index[0])

            js = data.iloc[1:].to_json(orient="split")
            f.write(js + ",")
        pos = f.tell()
        # remove trailing comma
        f.seek(pos-1)
        f.write("]")

    return name


if __name__ == "__main__":
    if argv[1] == "-h" or argv[1] == "--help":
        print("""
  Usage: takes two arguments\n\t
    path: absolute path to an elektron manual as PDF
    pages: string of pages, ex: 108-115 or 111,120-125
        """)
        exit(0)

    path = "/Users/viktorsandstrom/Documents/PDF/elektron_manuals/Digitakt_II_User_Manual_OS1.02_240627.pdf"
    pages = "all"
    if argv[1] is not None:
        path = argv[1]

    if argv[2] is not None:
        pages = argv[2]

    parse_elektron_manual(path, pages)
