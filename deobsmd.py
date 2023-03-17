from __future__ import annotations
import argparse
from dataclasses import dataclass
import re


def remove_comments(text: str) -> str:
    """Rremove obsidian comments (`%%comment text%%`) from text"""
    while (start := text.find(r"%%")) != -1 and (
        end := text.find(r"%%", start + 2)
    ) != -1:
        end += 2
        comment = text[start:end]
        assert comment.startswith(r"%%")
        assert comment.endswith(r"%%")

        text = text.replace(comment, "")

    return text


def strip_excessive_newlines(text: str) -> str:
    """Remove too many newlines from the text: leave at most 2 consecutive newlines"""
    return re.sub(r"\n[\n\s]+\n", "\n\n", text)  # .replace("\u200B", "")


@dataclass(frozen=True, slots=True)
class Args:
    """Console line arguments passed to the script"""
    input_filename: str
    output_filename: str

    @classmethod
    def parse(cls) -> Args:
        """Parse console line arguments"""
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "input_filename", help="filename markdown to be deobsidianized"
        )
        parser.add_argument(
            "-o",
            "--output_filename",
            help="ouptut filename for the result",
            required=False,
        )
        parsed = vars(parser.parse_args())
        assert parsed["input_filename"].endswith(".md")
        if parsed["output_filename"] is None:
            parsed["output_filename"] = "_" + parsed["input_filename"]
        elif not parsed["output_filename"].endswith(".md"):
            parsed["output_filename"] += ".md"
        return cls(**parsed)


FUNCS = [remove_comments, strip_excessive_newlines]


def main() -> None:
    args = Args.parse()
    with open(args.input_filename, "r", encoding="utf-8") as f:
        text = f.read()
    for func in FUNCS:
        text = func(text)
    with open(args.output_filename, "w", encoding="utf-8") as f:
        f.write(text)


if __name__ == "__main__":
    main()
