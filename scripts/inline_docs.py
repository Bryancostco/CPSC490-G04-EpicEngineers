#!/usr/bin/env python3
"""Copy every specification and design document into proposal section 4 (#141).

Each document in docs/specs/ and docs/design/ is copied, in full, directly
under the proposal paragraph that indexes it, between two HTML comment markers
that GitHub and the Word export both hide. The documents in docs/ stay the
source: edit them, then rerun this script to refresh the copies.

    python scripts/inline_docs.py           # refresh the copies in proposal.md
    python scripts/inline_docs.py --check   # exit 1 if a copy is out of date

What the copy changes, so the proposal and its Word export stay correct:
  * a document's title becomes a "### " heading and its section headings
    become bold paragraphs, because the harness and the Word export treat
    "## " as a new proposal section and the Word template only styles three
    heading levels;
  * each image and its caption share one paragraph, so Word does not print
    the image's alt text as a second caption;
  * quote blocks become normal paragraphs, because the Word export drops quotes;
  * relative links and images are rewritten to work from proposal/;
  * a Mermaid diagram becomes its exported PNG from docs/design/diagrams/ when
    one exists, because Word cannot draw Mermaid;
  * 〈placeholders〉 become "pending", because one 〈 in section 4 makes gate G8
    treat the whole section as an unfilled skeleton;
  * figures are numbered once across the whole of section 4.
"""
from __future__ import annotations  # allow modern type hints on older Pythons

import argparse  # command line flags
import os  # relative path arithmetic
import re  # pattern matching on Markdown
import sys  # exit codes and stderr
from pathlib import Path  # file paths

repo_root = Path(__file__).resolve().parents[1]  # this file lives in scripts/
proposal_path = repo_root / "proposal" / "proposal.md"  # the document being filled in

# Documents in the order they appear in section 4; any other document follows these.
preferred_order = [
    "docs/specs/pnl-calculation.md",  # position matching and PNL specification (#55)
    "docs/specs/trader-ranking.md",  # trader ranking and behavior specification (#54)
    "docs/specs/data-sources.md",  # data source specification (#104), once it exists
    "docs/specs/dashboard-questions.md",  # dashboard client questions (#123)
    "docs/specs/dashboard.md",  # dashboard specification (#125), once it exists
    "docs/design/architecture.md",  # architecture and system context (#56)
    "docs/design/implementation.md",  # prototype layout and build order (#61)
    "docs/design/data-model.md",  # data model and ER diagram (#57)
    "docs/design/data-flow.md",  # level 0 and level 1 data flow (#58)
    "docs/design/pnl-pipeline.md",  # PNL run sequence diagram (#59), once it exists
    "docs/design/dashboard-flow.md",  # dashboard page flow (#60)
]  # end of the preferred order

# Alt text and captions for diagrams that exist only as Mermaid inside a document.
mermaid_figures = {
    "docs/design/architecture.md": (  # Kyle's architecture document
        "Two diagrams side by side. System context: SonarX clients view the dashboard of our analytics system, "
        "which pulls trades from SonarX's Snowflake database and pushes results to the dashboard. High level "
        "architecture: SonarX's Snowflake database feeds pull trades, build positions, compute PNL and rank wallets; "
        "the results are stored and shown in the dashboard.",  # alt text describing the picture
        "System context (left) and high level architecture (right)",  # caption text
    ),  # end of the architecture entry
    "docs/design/implementation.md": (  # Kyle's implementation document
        "Prototype modules: the user reaches the application interface, which calls services, which call database "
        "access, which reads the Snowflake database. Configuration supplies environment variables and connection "
        "settings. Unit tests and integration tests, fed by test fixtures, check the modules.",  # alt text
        "Prototype module diagram",  # caption text
    ),  # end of the implementation entry
}  # end of the Mermaid figure table

begin_marker = "<!-- inline:begin {path} (copied by scripts/inline_docs.py: edit {path}, then rerun the script) -->"  # opens a copy
end_marker = "<!-- inline:end {path} -->"  # closes a copy
any_marker_re = re.compile(r"^<!-- inline:(begin|end) (\S+)")  # recognises either marker
fence_re = re.compile(r"^\s{0,3}(```|~~~)")  # opens or closes a fenced code block
heading_re = re.compile(r"^(#{1,6})(\s+.*)$")  # a Markdown heading line
quote_re = re.compile(r"^\s{0,3}>\s?")  # the start of a quote block line
link_re = re.compile(r"(!?\[[^\]]*\])\(([^)\s]+)(\s+\"[^\"]*\")?\)")  # a Markdown link or image
placeholder_re = re.compile(r"〈[^〉]*〉")  # a 〈placeholder〉 left in a template table
caption_re = re.compile(r"^\*Figure (\d+)\b")  # a figure caption line in this repo's style
figure_ref_re = re.compile(r"\bFigure (\d+)\b")  # any mention of a figure number


def find_documents() -> list[str]:
    """Return every team specification and design document, preferred order first."""
    found = set()  # repository relative paths of the documents
    for folder in ("docs/specs", "docs/design"):  # the two folders gate G9 indexes
        for path in (repo_root / folder).glob("*.md"):  # every Markdown file in it
            if path.name.startswith("example-") or path.stem.isupper():  # course examples and DIAGRAMS.md
                continue  # not team deliverables
            found.add(path.relative_to(repo_root).as_posix())  # keep the document
    ordered = [path for path in preferred_order if path in found]  # known documents in reading order
    ordered += sorted(found - set(ordered))  # anything new goes at the end
    return ordered  # the documents to copy


def rewrite_link(match: re.Match, document_dir: Path) -> str:
    """Point a relative link or image at the same file, seen from proposal/."""
    label, target, title = match.group(1), match.group(2), match.group(3) or ""  # the link's parts
    if re.match(r"^(https?:|mailto:|#)", target):  # absolute links and anchors need no change
        return match.group(0)  # leave it as written
    file_part, _, anchor = target.partition("#")  # keep any anchor after the file
    absolute = (document_dir / file_part).resolve()  # where the link points on disk
    relative = os.path.relpath(absolute, proposal_path.parent).replace(os.sep, "/")  # the same file from proposal/
    return f"{label}({relative}{'#' + anchor if anchor else ''}{title})"  # the rewritten link


def mermaid_to_image(document: str, block_number: int) -> list[str] | None:
    """Return image and caption lines for a document's Mermaid block, or None if no export exists."""
    stem = Path(document).stem  # file name without .md
    suffix = "" if block_number == 1 else f"-{block_number}"  # first block is stem.png, later ones stem-2.png
    image = repo_root / "docs" / "design" / "diagrams" / f"{stem}{suffix}.png"  # where the export lives
    source = image.with_suffix(".mmd")  # its editable source
    if not image.exists():  # nothing exported yet
        return None  # keep the Mermaid block
    alt, caption = mermaid_figures.get(document, (f"Diagram from {document}", f"Diagram from {document}"))  # words for it
    image_link = os.path.relpath(image, proposal_path.parent).replace(os.sep, "/")  # image path from proposal/
    source_link = os.path.relpath(source, proposal_path.parent).replace(os.sep, "/")  # source path from proposal/
    return [  # an image paragraph and a caption paragraph, in the repo's figure style
        f"![{alt}]({image_link})",  # the picture
        "",  # paragraph break
        f"*Figure 1 — {caption}. Editable source: [`{source.name}`]({source_link}).*",  # renumbered later
    ]  # end of the replacement


def transform_document(document: str) -> str:
    """Return the document's text, adjusted to sit inside proposal section 4."""
    path = repo_root / document  # the source file
    lines = path.read_text(encoding="utf-8").splitlines()  # its lines
    output: list[str] = []  # the transformed lines
    in_fence = False  # inside a fenced code block
    mermaid_lines: list[str] | None = None  # collected Mermaid block, when inside one
    mermaid_count = 0  # Mermaid blocks seen so far in this document
    for line in lines:  # walk the document once
        if mermaid_lines is not None:  # inside a Mermaid block
            if fence_re.match(line):  # its closing fence
                mermaid_count += 1  # count the block
                image_lines = mermaid_to_image(document, mermaid_count)  # its exported picture, if any
                output += image_lines if image_lines else ["```mermaid", *mermaid_lines, "```"]  # picture or the original block
                mermaid_lines = None  # leave the block
            else:  # a line of the diagram
                mermaid_lines.append(line)  # keep it in case there is no export
            continue  # nothing else to do for this line
        if fence_re.match(line):  # opening or closing an ordinary fence
            if not in_fence and line.strip().lstrip("`~").strip().lower().startswith("mermaid"):  # a Mermaid fence opens
                mermaid_lines = []  # start collecting the diagram
                continue  # the fence line itself is not copied
            in_fence = not in_fence  # toggle code block state
            output.append(line)  # copy the fence line unchanged
            continue  # next line
        if in_fence:  # code inside a fence is copied exactly
            output.append(line)  # copy it
            continue  # next line
        heading = heading_re.match(line)  # is this a heading?
        if heading:  # the Word template only styles three heading levels
            level, title = len(heading.group(1)), heading.group(2).strip()  # old level and its text
            if level == 1:  # the document's own title
                line = "### " + title  # a bold, unnumbered heading in Word, below "## 4."
            elif level == 2:  # the document's sections
                line = f"**{title}**"  # a bold paragraph, visible in Word and on GitHub
            else:  # deeper sections
                line = f"***{title}***"  # a bold italic paragraph
        line = quote_re.sub("", line)  # quote blocks become normal text
        line = link_re.sub(lambda match: rewrite_link(match, path.parent), line)  # fix relative links
        line = placeholder_re.sub("pending", line)  # no 〈placeholders〉 inside section 4
        output.append(line.rstrip())  # keep the line without trailing spaces
    return join_figures("\n".join(output).strip("\n"))  # the whole document as one string


def join_figures(text: str) -> str:
    """Put each image and its caption in one paragraph, so Word does not print the alt text as a second caption."""
    image_then_caption = re.compile(r"^(!\[[^\]]*\]\([^)]*\))\n\n(\*Figure \d+\b)", re.M)  # an image paragraph, then a caption paragraph
    return image_then_caption.sub(lambda m: f"{m.group(1)}\\\n{m.group(2)}", text)  # a hard line break joins them


def section_four_bounds(lines: list[str]) -> tuple[int, int]:
    """Return the first and one past the last line index of proposal section 4."""
    start = next(i for i, line in enumerate(lines) if re.match(r"^##\s+4\.?\s", line))  # the "## 4." heading
    end = next((i for i in range(start + 1, len(lines)) if re.match(r"^##\s", lines[i])), len(lines))  # the next section
    return start, end  # section 4 runs from start up to end


def strip_old_copies(lines: list[str]) -> list[str]:
    """Remove every previous copy, markers included, leaving the hand written text."""
    kept: list[str] = []  # lines outside any copy
    inside = False  # inside a copy
    for line in lines:  # walk section 4
        marker = any_marker_re.match(line)  # is this a marker line?
        if marker and marker.group(1) == "begin":  # a copy starts
            inside = True  # skip until its end marker
            if kept and kept[-1] == "":  # drop the blank line that separated it
                kept.pop()  # remove the separator
            continue  # skip the marker itself
        if marker and marker.group(1) == "end":  # the copy ends
            inside = False  # back to hand written text
            continue  # skip the marker itself
        if not inside:  # hand written text
            kept.append(line)  # keep it
    return kept  # section 4 without copies


def index_entry_end(lines: list[str], document: str) -> int | None:
    """Return the line index just past the hand written entry that indexes a document, or None."""
    link = f"](../{document})"  # how section 4 links the document
    starts = [i for i, line in enumerate(lines) if link in line]  # lines that link it
    if not starts:  # the document is not indexed yet
        return None  # nothing to attach the copy to
    position = starts[0]  # its index paragraph
    for i in range(position + 1, len(lines)):  # look for where this entry stops
        line = lines[i]  # the line being checked
        starts_new_entry = re.search(r"\]\(\.\./docs/(specs|design)/[^)]+\.md\)", line) and (i == 0 or lines[i - 1] == "")  # another document's index paragraph
        if starts_new_entry or line.startswith("#"):  # the next entry or the next heading
            end = i  # the entry stops before it
            while end > position and lines[end - 1] == "":  # step back over blank lines
                end -= 1  # the entry's last text line is just above
            return end  # insert the copy here
    return len(lines)  # the entry runs to the end of the section


def renumber_figures(lines: list[str]) -> list[str]:
    """Number figures once across section 4, keeping each copy's references consistent."""
    segments: list[list[str]] = [[]]  # hand written text and copies, in order
    for line in lines:  # split section 4 at every marker
        marker = any_marker_re.match(line)  # is this a marker line?
        if marker and marker.group(1) == "begin":  # a copy starts a new segment
            segments.append([line])  # the copy's segment
        elif marker and marker.group(1) == "end":  # a copy ends its segment
            segments[-1].append(line)  # close the copy's segment
            segments.append([])  # hand written text follows
        else:  # an ordinary line
            segments[-1].append(line)  # add it to the current segment
    next_number = 1  # the next figure number in the proposal
    result: list[str] = []  # the renumbered section
    for segment in segments:  # each segment has its own local numbering
        mapping: dict[str, str] = {}  # local figure number to proposal figure number
        for line in segment:  # find the captions in order
            caption = caption_re.match(line)  # a caption line?
            if caption and caption.group(1) not in mapping:  # first caption with this number
                mapping[caption.group(1)] = str(next_number)  # give it the next proposal number
                next_number += 1  # move the counter on
        result += [figure_ref_re.sub(lambda m: f"Figure {mapping.get(m.group(1), m.group(1))}", line) for line in segment]  # apply the mapping
    return result  # section 4 with proposal wide figure numbers


def build_proposal(text: str) -> tuple[str, list[str]]:
    """Return the proposal with fresh copies, and the documents that could not be placed."""
    lines = text.split("\n")  # the proposal's lines
    start, end = section_four_bounds(lines)  # where section 4 is
    section = strip_old_copies(lines[start:end])  # section 4 without old copies
    skipped: list[str] = []  # documents with no index paragraph
    positions: list[tuple[int, str]] = []  # where each copy goes, found on the hand written text only
    for document in find_documents():  # every document, in reading order
        position = index_entry_end(section, document)  # where its copy goes
        if position is None:  # not indexed in section 4 yet
            skipped.append(document)  # report it
            continue  # nothing to attach to
        positions.append((position, document))  # remember the spot
    for position, document in sorted(positions, reverse=True):  # insert bottom up so earlier spots stay valid
        copy = [  # the copy, wrapped in markers and blank lines
            "",  # separate it from the entry above
            begin_marker.format(path=document),  # opening marker
            "",  # blank line after the marker
            transform_document(document),  # the document itself
            "",  # blank line before the marker
            end_marker.format(path=document),  # closing marker
        ]  # end of the copy
        section[position:position] = "\n".join(copy).split("\n")  # insert it after the entry
    section = renumber_figures(section)  # one figure numbering for the section
    section = join_figures("\n".join(section)).split("\n")  # captions sit with their images in hand written text too
    return "\n".join(lines[:start] + section + lines[end:]), skipped  # the rebuilt proposal


def main() -> int:
    """Refresh the copies, or check that they are current with --check."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])  # one line help
    parser.add_argument("--check", action="store_true", help="exit 1 if proposal.md is out of date")  # the check flag
    arguments = parser.parse_args()  # read the flags
    current = proposal_path.read_text(encoding="utf-8")  # the proposal as it is
    rebuilt, skipped = build_proposal(current)  # the proposal as it should be
    for document in skipped:  # documents section 4 does not index
        print(f"not copied: {document} has no index paragraph in proposal section 4 yet", file=sys.stderr)  # say so
    if arguments.check:  # only report
        if rebuilt != current:  # a copy is stale or missing
            print("proposal/proposal.md is out of date: run python scripts/inline_docs.py", file=sys.stderr)  # how to fix
            return 1  # fail
        print("proposal/proposal.md copies are current")  # all good
        return 0  # pass
    if rebuilt != current:  # something changed
        proposal_path.write_text(rebuilt, encoding="utf-8")  # save the new proposal
        print("proposal/proposal.md updated")  # report
    else:  # nothing to do
        print("proposal/proposal.md already current")  # report
    return 0  # success


if __name__ == "__main__":  # run as a script
    sys.exit(main())  # pass the exit code to the shell
