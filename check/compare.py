import icdiff
import pexpect
import sys

from dataclasses import dataclass
from pathlib import Path

@dataclass
class Options:
    # Facade data class for argparse options
    is_git_diff: bool = False
    labels: str = ""
    no_headers: bool = False
    head: int = 0
    matcher: str = ""
    no_bold: bool = False
    color_map: str = ""
    whole_file: bool = False
    output_encoding: str = "utf-8"
    unified: int = 5
    strip_trailing_cr: bool = True


def run(path, class_name):
    result = []
    try:
        absurdle = pexpect.spawn(f"java {class_name}.java", timeout=3)
        with open(path) as f:
            for line in f.readlines():
                absurdle.expect_exact("> ")
                result.append(absurdle.before.decode("utf-8"))
                result.append("> ")
                absurdle.send(line)
        absurdle.expect_exact(pexpect.EOF)
    except (pexpect.TIMEOUT, pexpect.EOF):
        pass
    finally:
        result.append(absurdle.before.decode("utf-8"))
        return "".join(result)


if __name__ == "__main__":
    options = Options()
    icdiff.set_cols_option(options)
    cd = icdiff.ConsoleDiff(
        cols=options.cols,
        strip_trailing_cr=options.strip_trailing_cr
    )

    def diff(expected, actual, expected_header, actual_header):
        printed_lines = 0
        for line in cd.make_table(
                expected.splitlines(), actual.splitlines(),
                expected_header, actual_header,
                context=(not options.whole_file),
                numlines=int(options.unified)
            ):
            icdiff.codec_print(line, options)
            sys.stdout.flush()
            printed_lines += 1
        return printed_lines != 1

    err = 0
    for p in sorted(Path("dict2").glob("*.input")):
        with open(p.with_suffix(".expected")) as f:
            if diff(f.read(), run(p.with_suffix(".input"), "AbsurdleMainDict2"),
                    p.with_suffix(".expected"), p.with_suffix(".actual")):
                err = 1

    for p in sorted(Path("dict1").glob("*.input")):
        with open(p.with_suffix(".expected")) as f:
            if diff(f.read(), run(p.with_suffix(".input"), "AbsurdleMainDict1"),
                    p.with_suffix(".expected"), p.with_suffix(".actual")):
                err = 1

    sys.exit(err)
