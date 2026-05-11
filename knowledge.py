import os


def load_docs():

    docs_dir = "docs"

    all_docs = []

    if not os.path.exists(docs_dir):
        return ""

    for filename in os.listdir(docs_dir):

        path = os.path.join(
            docs_dir,
            filename
        )

        if not os.path.isfile(path):
            continue

        try:

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as f:

                content = f.read()

                all_docs.append(
                    f"""
FILE: {filename}

{content}
"""
                )

        except Exception as e:

            print(
                f"failed to load {filename}: {e}"
            )

    return "\n\n".join(all_docs)