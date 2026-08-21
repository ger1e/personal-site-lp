#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

START = "/* cat-hero-max:start */"
END = "/* cat-hero-max:end */"
BLOCK = f"""{START}
/* Managed responsive override: promote the existing embedded cat without touching its image payload. */
.cat-card{{width:min(470px,39vw);min-width:320px;aspect-ratio:4/5;right:clamp(18px,3.4vw,42px);bottom:clamp(18px,3.4vw,36px);box-shadow:0 24px 72px rgba(0,0,0,.46),0 0 62px rgba(89,255,155,.09)}}
.content{{max-width:675px}}
.spotify{{width:min(490px,100%)}}
@media(max-width:1040px){{.hero-card{{padding-bottom:480px}}.cat-card{{width:min(440px,84vw);min-width:0}}}}
@media(max-width:620px){{.hero-card{{padding-bottom:440px}}.cat-card{{left:16px;right:16px;width:auto;aspect-ratio:4/5}}}}
{END}"""


def transform(html: str) -> str:
    managed = re.compile(r"\n?" + re.escape(START) + r".*?" + re.escape(END) + r"\n?", re.S)
    cleaned = managed.sub("\n", html, count=1)
    if "</style>" not in cleaned:
        raise ValueError("index.html is missing </style>")
    return cleaned.replace("</style>", f"\n{BLOCK}\n</style>", 1)


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote the existing rotund cat to the primary visual hero")
    parser.add_argument("--path", default="index.html")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    path = Path(args.path)
    updated = transform(path.read_text(encoding="utf-8"))
    if args.write:
        path.write_text(updated, encoding="utf-8")
    else:
        print(updated)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
