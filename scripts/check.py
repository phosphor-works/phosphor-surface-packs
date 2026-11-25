#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Phosphor Works Team
# SPDX-License-Identifier: LGPL-2.1-or-later
"""Structural checks on the packs, with the standard library only.

Every pack directory holds a metadata.json that parses, whose id is the
directory's name and whose shader files exist. Every #include names a file
in the pack or in packs/shared. Every shader carries an SPDX copyright and
an LGPL-2.1-or-later or GPL-3.0-or-later licence identifier, joined with
AND to a permissive upstream licence where the file incorporates one.

What a pack's GLSL compiles to, and whether its parameters match its
shader, is checked by the applications that draw the packs, against the
commit they pin (PlasmaZones' plasmazones-shader-validate).
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "packs"
SHARED = ROOT / "shared"
# A file that incorporates permissive upstream code names both licences,
# e.g. "LGPL-2.1-or-later AND BSD-3-Clause".
LICENCES = {"LGPL-2.1-or-later", "GPL-3.0-or-later"}
UPSTREAM_LICENCES = {"BSD-3-Clause", "MIT"}
SHADER_SUFFIXES = {".frag", ".vert", ".glsl"}
INCLUDE = re.compile(r"^\s*#include\s+[<\"]([^>\"]+)[>\"]", re.MULTILINE)


def main() -> int:
    problems = []

    def problem(path: Path, message: str) -> None:
        problems.append(f"{path.relative_to(ROOT.parent)}: {message}")

    packs = sorted(p for p in ROOT.iterdir() if p.is_dir() and p != SHARED)
    if not packs:
        problem(ROOT, "no packs found")
    for pack in packs:
        meta_path = pack / "metadata.json"
        if not meta_path.is_file():
            problem(pack, "no metadata.json")
            continue
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            problem(meta_path, f"does not parse: {error}")
            continue
        if meta.get("id") != pack.name:
            problem(meta_path, f"id is {meta.get('id')!r}, not the directory name {pack.name!r}")
        shaders = [meta.get("fragmentShader")]
        if "vertexShader" in meta:
            shaders.append(meta["vertexShader"])
        shaders += [s for s in meta.get("bufferShaders", []) if not s.startswith("builtin:")]
        for shader in shaders:
            if not isinstance(shader, str) or not (pack / shader).is_file():
                problem(meta_path, f"names shader {shader!r}, which is not in the pack")

    for shader in sorted(p for p in ROOT.rglob("*") if p.suffix in SHADER_SUFFIXES):
        text = shader.read_text(encoding="utf-8")
        head = text.splitlines()[:10]
        if not any(line.startswith("// SPDX-FileCopyrightText: ") for line in head):
            problem(shader, "no SPDX-FileCopyrightText line in its header")
        # REUSE-IgnoreStart
        tag = "// SPDX-License-Identifier:"
        # REUSE-IgnoreEnd
        ids = [line[len(tag):].strip() for line in head if line.startswith(tag)]
        parts = ids[0].split(" AND ") if len(ids) == 1 else []
        if not parts or parts[0] not in LICENCES or not set(parts[1:]) <= UPSTREAM_LICENCES:
            problem(shader, f"licence identifier {ids or 'missing'}, expected one of {sorted(LICENCES)}")
        for name in INCLUDE.findall(text):
            if not (shader.parent / name).is_file() and not (SHARED / name).is_file():
                problem(shader, f"includes {name}, which is neither beside it nor in packs/shared")

    for line in problems:
        print(line)
    print(f"{len(packs)} packs checked, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
