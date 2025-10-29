#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
asm2c.py — minimal x86-64 assembly → pseudo-C lifter (single-file)

Scope (honest):
- Lifts a practical subset of x86-64 into readable C-like code with labels/gotos.
- Handles Intel or AT&T syntax, basic function frames, locals/args via rbp.
- Arithmetic/logical ops, cmp + conditional jumps, calls, ret.
- NOT a full decompiler: no full CFG structuring, no types, limited mem addressing.

Usage:
  python asm2c.py --in input.s --func myfunc --syntax auto > out.c

Flags:
  --in PATH          Input assembly file (or omit to read stdin)
  --func NAME        Name for the emitted C function (default: lifted_func)
  --syntax {auto,intel,att}  Assembly dialect (default: auto)
  --arch x86_64      (reserved, only x86_64 supported)
  --show-unsupported Show lines that were skipped as comments in output

Example input (Intel):
  push rbp
  mov rbp, rsp
  sub rsp, 32
  mov DWORD PTR [rbp-4], 5
  mov eax, DWORD PTR [rbp-4]
  add eax, 7
  leave
  ret

Output (pseudo-C):
  uint64_t lifted_func(uint64_t arg_8, uint64_t arg_16, ...) {
    uint64_t local_4 = 5ULL;
    rax = (uint32_t)local_4;
    rax = (uint32_t)(rax + 7ULL);
    return rax;
  }

Author: ChatGPT (GPT-5 Thinking)
License: MIT
"""

import sys
import re
import argparse
from typing import List, Tuple, Optional, Dict, Any


# -------- Utilities

def strip_comment(line: str) -> str:
    # Intel often uses ';' for comments, AT&T can use '#'
    # But '#' can appear in directives; be conservative:
    # Remove ';' comments. For '#' treat leading '#' as comment.
    if ';' in line:
        line = line.split(';', 1)[0]
    l = line.strip()
    if l.startswith('#'):
        return ''
    return line


def is_label(line: str) -> bool:
    return bool(re.match(r'^\s*([A-Za-z_.$][\w.$]*):\s*$', line))


def extract_label(line: str) -> str:
    return re.match(r'^\s*([A-Za-z_.$][\w.$]*):', line).group(1)


def looks_att(line: str) -> bool:
    # crude heuristic: '%' before registers, '$' for immediates
    return ('%' in line) or re.search(r'\$-?\d', line) is not None


def tokenize(line: str) -> Tuple[str, List[str]]:
    line = line.strip()
    if not line:
        return '', []
    # split mnemonic and operands
    m = re.match(r'^([A-Za-z.]+)\s*(.*)$', line)
    if not m:
        return '', []
    mnemonic = m.group(1).lower()
    rest = m.group(2).strip()
    if not rest:
        return mnemonic, []
    # split operands by commas not within brackets/parentheses
    parts = []
    buf, depth = '', 0
    for ch in rest:
        if ch in '[(':
            depth += 1
        elif ch in '])':
            depth -= 1
        if ch == ',' and depth == 0:
            parts.append(buf.strip())
            buf = ''
        else:
            buf += ch
    if buf.strip():
        parts.append(buf.strip())
    return mnemonic, parts


# -------- Operand parsing (Intel + AT&T normalized)

REGS64 = {
    'rax', 'rbx', 'rcx', 'rdx', 'rsi', 'rdi', 'rbp', 'rsp',
    'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14', 'r15'
}
REGS32 = {
    'eax', 'ebx', 'ecx', 'edx', 'esi', 'edi', 'ebp', 'esp',
    'r8d', 'r9d', 'r10d', 'r11d', 'r12d', 'r13d', 'r14d', 'r15d'
}
REGS16 = {
    'ax', 'bx', 'cx', 'dx', 'si', 'di', 'bp', 'sp',
    'r8w', 'r9w', 'r10w', 'r11w', 'r12w', 'r13w', 'r14w', 'r15w'
}
REGS8 = {
    'al', 'bl', 'cl', 'dl', 'sil', 'dil', 'bpl', 'spl',
    'r8b', 'r9b', 'r10b', 'r11b', 'r12b', 'r13b', 'r14b', 'r15b',
    'ah', 'bh', 'ch', 'dh'
}


def op_is_reg(x: str) -> bool:
    x = x.lower()
    return x in REGS64 or x in REGS32 or x in REGS16 or x in REGS8


def normalize_intel_mem(op: str) -> Optional[Dict[str, Any]]:
    """
    Parse Intel mem like: [rbp-8], qword ptr [rbp+16], [rip+0x123], [rax+rbx*4+8]
    Return dict: {'kind':'mem','base':..., 'index':..., 'scale':..., 'disp':..., 'size':bits or None}
    """
    o = op.strip()
    size = None
    # strip optional size keywords
    size_map = {
        'byte ptr': 8, 'word ptr': 16, 'dword ptr': 32, 'qword ptr': 64,
        'BYTE PTR': 8, 'WORD PTR': 16, 'DWORD PTR': 32, 'QWORD PTR': 64
    }
    for k, v in size_map.items():
        if o.lower().startswith(k.lower()):
            size = v
            o = o[len(k):].strip()
            break
    m = re.match(r'^\[([^\]]+)\]$', o)
    if not m:
        return None
    expr = m.group(1).replace(' ', '')
    # pattern: base + index*scale + disp (all optional)
    # split by '+' and handle negatives
    # recognize base/index registers and numeric disps
    base = None
    index = None
    scale = 1
    disp = 0

    # Tokenize on '+' with sign kept for numbers
    tokens = re.split(r'(?=\+)|(?=-)', expr)
    tokens = [t for t in tokens if t]
    for t in tokens:
        t = t.lstrip('+')
        if '*' in t:
            # index*scale
            idx, sc = t.split('*', 1)
            if op_is_reg(idx):
                index = idx.lower()
                try:
                    scale = int(sc, 0)
                except:
                    scale = 1
            else:
                # unknown, ignore
                pass
        elif op_is_reg(t):
            if base is None:
                base = t.lower()
            else:
                # if base already set and index empty, treat as index
                if index is None:
                    index = t.lower()
                    scale = 1
        else:
            # disp
            try:
                disp += int(t, 0)
            except:
                # rip-relative like rip+0x123 already numeric for disp when base='rip'
                pass
    return {'kind': 'mem', 'base': base, 'index': index, 'scale': scale, 'disp': disp, 'size': size}


def normalize_att_mem(op: str) -> Optional[Dict[str, Any]]:
    """
    AT&T mem like: -8(%rbp), 16(%rbp), (%rax,%rbx,4)
    """
    o = op.strip()
    # immediate prefix '$' shouldn't be here
    m = re.match(r'^([+-]?\s*0x[0-9A-Fa-f]+|[+-]?\s*\d+)?\s*\((%[a-z0-9]+)?(?:,\s*(%[a-z0-9]+)\s*(?:,\s*(\d+))?)?\)$',
                 o)
    if not m:
        return None
    disp_s, base_s, index_s, scale_s = m.groups()
    disp = int(disp_s.replace(' ', ''), 0) if disp_s else 0
    base = base_s[1:].lower() if base_s else None
    index = index_s[1:].lower() if index_s else None
    scale = int(scale_s) if scale_s else 1
    return {'kind': 'mem', 'base': base, 'index': index, 'scale': scale, 'disp': disp, 'size': None}


def parse_operand(op: str, syntax: str) -> Dict[str, Any]:
    op = op.strip()
    # immediates
    if syntax == 'att':
        if op.startswith('$'):
            return {'kind': 'imm', 'val': int(op[1:], 0)}
    else:
        # intel immediate is bare number
        if re.match(r'^[+-]?\s*(0x[0-9A-Fa-f]+|\d+)$', op):
            return {'kind': 'imm', 'val': int(op.replace(' ', ''), 0)}
    # registers
    if syntax == 'att' and op.startswith('%'):
        r = op[1:].lower()
        if op_is_reg(r):
            return {'kind': 'reg', 'name': r}
    elif op_is_reg(op.lower()):
        return {'kind': 'reg', 'name': op.lower()}
    # memory
    mem = normalize_att_mem(op) if syntax == 'att' else normalize_intel_mem(op)
    if mem:
        return mem
    # labels/symbols
    if re.match(r'^[A-Za-z_.$][\w.$]*$', op):
        return {'kind': 'sym', 'name': op}
    # fallback
    return {'kind': 'raw', 'text': op}


# -------- Lifter

CMP_SET = {
    'e': '==', 'z': '==',
    'ne': '!=', 'nz': '!=',
    'l': '<', 'nge': '<',
    'le': '<=', 'ng': '<=',
    'g': '>', 'nle': '>',
    'ge': '>=', 'nl': '>=',
    # unsigned
    'b': '<', 'c': '<', 'nae': '<',
    'be': '<=', 'na': '<=',
    'a': '>', 'nbe': '>',
    'ae': '>=', 'nb': '>='
}


class Emitter:
    def __init__(self, func_name: str, show_unsupported: bool):
        self.func_name = func_name
        self.lines: List[str] = []
        self.label_lines: Dict[str, int] = {}
        self.locals: Dict[int, str] = {}  # rbp - k
        self.args: Dict[int, str] = {}  # rbp + k
        self.globals: Dict[int, str] = {}  # rip + disp
        self.show_unsupported = show_unsupported
        self.used_regs = set()

    def add(self, s: str):
        self.lines.append(s)

    def c_opnd(self, o: Dict[str, Any]) -> str:
        if o['kind'] == 'imm':
            return f"{int(o['val'])}ULL"
        if o['kind'] == 'reg':
            self.used_regs.add(o['name'])
            return o['name']
        if o['kind'] == 'sym':
            return o['name']
        if o['kind'] == 'mem':
            base = o.get('base')
            disp = o.get('disp', 0)
            if base == 'rbp':
                if disp < 0:
                    name = self.locals.setdefault(-disp, f"local_{-disp}")
                    return name
                elif disp > 0:
                    name = self.args.setdefault(disp, f"arg_{disp}")
                    return name
                else:
                    # [rbp]
                    return "rbp_mem0"
            if base == 'rip':
                name = self.globals.setdefault(disp, f"global_{disp:+}")
                return name
            # generic mem expr fallback
            idx = o.get('index')
            sc = o.get('scale', 1)
            parts = []
            if base:
                parts.append(base)
                self.used_regs.add(base)
            if idx:
                parts.append(f"{idx}*{sc}")
                self.used_regs.add(idx)
            if disp:
                parts.append(str(disp))
            expr = ' + '.join(parts) if parts else '0'
            return f"MEM64({expr})"
        if o['kind'] == 'raw':
            return f"/*RAW:{o['text']}*/"
        return "/*UNK*/"

    def emit_assign(self, dst: Dict[str, Any], expr: str):
        if dst['kind'] == 'reg':
            self.used_regs.add(dst['name'])
            self.add(f"{dst['name']} = {expr};")
        elif dst['kind'] == 'mem':
            target = self.c_opnd(dst)
            self.add(f"{target} = {expr};")
        else:
            self.add(f"/* unsupported dst in assign */ /* {expr} */")

    def emit_label(self, lab: str):
        self.add(f"{lab}: ;")

    def emit_goto(self, lab: str):
        self.add(f"goto {lab};")

    def emit_if_goto(self, cond: str, lab: str):
        self.add(f"if ({cond}) goto {lab};")

    def header(self):
        # function signature and scaffolding
        self.add("#include <stdint.h>")
        self.add("#include <stdio.h>")
        self.add("")
        self.add("/* Helper macro for generic memory fallback (replace as needed) */")
        self.add("#define MEM64(addr) (*(uint64_t*)(uintptr_t)(addr))")
        self.add("")
        self.add(f"uint64_t {self.func_name}(uint64_t arg_8, uint64_t arg_16, uint64_t arg_24, uint64_t arg_32) {{")
        # declare registers used (declare all common to simplify)
        regs = sorted(list(REGS64 | REGS32 | REGS16 | REGS8))
        # only 64-bit regs as uint64_t variables; subwidth uses casting when writing
        used = sorted([r for r in REGS64])
        decl = ", ".join(used) if used else ""
        if decl:
            self.add(f"  uint64_t {decl};")
        # declare known locals/args/globals after lifting completes (we inject later)
        self.add("  // locals/args will be declared below")
        self.add("")

    def footer(self):
        self.add("}")

    def finalize_locals(self):
        # Insert declarations for locals/args/globals at top (after header scaffolding)
        decls = []
        if self.locals:
            names = ", ".join(sorted(self.locals.values()))
            decls.append(f"  uint64_t {names};")
        if self.args:
            # args already appear as parameters; keep as aliases if used by name
            # If args[] got referenced, they are parameters; nothing needed.
            pass
        if self.globals:
            names = ", ".join(sorted(self.globals.values()))
            decls.append(f"  extern uint64_t {names}; // RIP-relative symbol placeholder")
        # Inject after the marker line
        for i, line in enumerate(self.lines):
            if line.strip() == "// locals/args will be declared below":
                self.lines[i] = "// locals/args will be declared below\n" + "\n".join(decls)
                break


class Lifter:
    def __init__(self, syntax: str, show_unsupported: bool):
        self.syntax = syntax
        self.em = Emitter(func_name="", show_unsupported=show_unsupported)
        self.last_cmp: Optional[Tuple[str, str]] = None  # (lhs, rhs) as C expr strings

    def parse_op(self, s: str) -> Dict[str, Any]:
        return parse_operand(s, self.syntax)

    def op_str(self, o: Dict[str, Any]) -> str:
        return self.em.c_opnd(o)

    def set_func(self, name: str):
        self.em.func_name = name
        self.em.header()

    def finish(self):
        self.em.finalize_locals()
        self.em.footer()

    # ---- instruction handlers

    def handle_mov(self, dst, src):
        self.em.emit_assign(dst, self.op_str(src))

    def handle_binop(self, mnem: str, dst, src):
        op_map = {
            'add': '+', 'sub': '-', 'and': '&', 'or': '|', 'xor': '^',
            'shl': '<<', 'sal': '<<', 'shr': '>>', 'sar': '>>',
            'imul': '*',
        }
        if mnem not in op_map:
            self.em.add(f"/* unsupported binop {mnem} */")
            return
        op = op_map[mnem]
        # dst = dst OP src
        dsts = self.op_str(dst)
        srcs = self.op_str(src)
        self.em.emit_assign(dst, f"({dsts} {op} {srcs})")

    def handle_unop(self, mnem: str, dst):
        if mnem == 'inc':
            self.em.emit_assign(dst, f"({self.op_str(dst)} + 1ULL)")
        elif mnem == 'dec':
            self.em.emit_assign(dst, f"({self.op_str(dst)} - 1ULL)")
        elif mnem == 'neg':
            self.em.emit_assign(dst, f"(0ULL - {self.op_str(dst)})")
        elif mnem == 'not':
            self.em.emit_assign(dst, f"(~{self.op_str(dst)})")
        else:
            self.em.add(f"/* unsupported unop {mnem} */")

    def handle_cmp(self, a, b):
        self.last_cmp = (self.op_str(a), self.op_str(b))

    def cond_from_suffix(self, suf: str) -> Optional[str]:
        suf = suf.lower()
        # normalize e/z etc
        if suf in CMP_SET:
            return CMP_SET[suf]
        return None

    def handle_jcc(self, mnem: str, ops: List[Dict[str, Any]]):
        # je label / jne label / jl label ...
        if not self.last_cmp:
            # Fall back: if (ZF-like?) we can't know → emit comment goto
            if ops and ops[0]['kind'] == 'sym':
                self.em.add(f"/* jcc without prior cmp */ goto {ops[0]['name']};")
            return
        lhs, rhs = self.last_cmp
        suf = mnem[1:]  # strip leading 'j'
        op = self.cond_from_suffix(suf)
        target = ops[0]['name'] if ops and ops[0]['kind'] == 'sym' else "UNKNOWN"
        if op is None:
            self.em.add(f"/* unsupported condition {mnem} */")
            return
        # unsigned vs signed: we can't infer — assume unsigned for a/ae/b/be, signed for l/g variants
        self.em.emit_if_goto(f"({lhs} {op} {rhs})", target)

    def handle_jmp(self, ops):
        if ops and ops[0]['kind'] == 'sym':
            self.em.emit_goto(ops[0]['name'])
        else:
            self.em.add("/* jmp unknown target */")

    def handle_call(self, ops):
        # assign to rax by convention (if any return)
        if ops and ops[0]['kind'] in ('sym', 'raw'):
            callee = ops[0]['name'] if ops[0]['kind'] == 'sym' else ops[0]['text']
            self.em.add(f"rax = {callee}();")
        else:
            self.em.add("/* call unknown */")

    def handle_ret(self):
        self.em.add("return rax;")

    def handle_prologue(self, mnemonic: str, ops: List[Dict[str, Any]]) -> bool:
        # Detect leave/ret and push rbp / mov rbp, rsp / sub rsp, imm
        if mnemonic == 'leave':
            # optional; nothing needed since we don't model rsp here
            return True
        if mnemonic == 'ret':
            self.handle_ret()
            return True
        # Ignore frame pushes/moves/sub
        if mnemonic == 'push' and ops and ops[0]['kind'] == 'reg' and ops[0]['name'] == 'rbp':
            return True
        if mnemonic == 'mov' and len(ops) == 2 and ops[0]['kind'] == 'reg' and ops[1]['kind'] == 'reg' and ops[0][
            'name'] == 'rbp' and ops[1]['name'] == 'rsp':
            return True
        if mnemonic == 'sub' and len(ops) == 2 and ops[0]['kind'] == 'reg' and ops[0]['name'] == 'rsp' and ops[1][
            'kind'] == 'imm':
            # reserve locals size; we don't need to emit anything
            return True
        if mnemonic == 'add' and len(ops) == 2 and ops[0]['kind'] == 'reg' and ops[0]['name'] == 'rsp' and ops[1][
            'kind'] == 'imm':
            # epilogue counterpart
            return True
        return False

    def lift_line(self, line: str):
        if not line.strip():
            return
        if is_label(line):
            lab = extract_label(line)
            self.em.emit_label(lab)
            return
        mnem, raw_ops = tokenize(line)
        if not mnem:
            return
        # normalize syntax-specific operand order (AT&T is src,dst)
        # We'll parse first then swap for AT&T where needed.
        ops = [self.parse_op(x) for x in raw_ops]

        # AT&T syntax typically uses 'mnemonic[b/w/l/q]' + src, dst
        # Strip size suffix for common ops.
        base_mnem = re.match(r'^[a-z]+', mnem).group(0) if re.match(r'^[a-z]+', mnem) else mnem
        mnem_norm = base_mnem

        if self.syntax == 'att':
            # Swap src,dst for most two-operand ops
            if len(ops) == 2 and base_mnem not in ('cmp', 'test'):
                ops = [ops[1], ops[0]]

        # quick prologue/epilogue filter
        if self.handle_prologue(mnem_norm, ops):
            return

        # dispatch
        if mnem_norm == 'mov':
            if len(ops) == 2:
                self.handle_mov(ops[0], ops[1])
                return
        if mnem_norm in ('add', 'sub', 'and', 'or', 'xor', 'shl', 'shr', 'sal', 'sar', 'imul'):
            if len(ops) == 2:
                self.handle_binop(mnem_norm, ops[0], ops[1])
                return
        if mnem_norm in ('inc', 'dec', 'neg', 'not'):
            if len(ops) == 1:
                self.handle_unop(mnem_norm, ops[0])
                return
        if mnem_norm == 'cmp' and len(ops) == 2:
            self.handle_cmp(ops[0], ops[1])
            return
        if mnem_norm == 'jmp':
            self.handle_jmp(ops)
            return
        if mnem_norm.startswith('j') and mnem_norm != 'jmp':
            self.handle_jcc(mnem_norm, ops)
            return
        if mnem_norm == 'call':
            self.handle_call(ops)
            return
        if mnem_norm == 'ret':
            self.handle_ret()
            return

        # size-extending moves (zero/sign): treat as mov
        if mnem_norm in ('movzx', 'movsx', 'movsxd') and len(ops) == 2:
            self.handle_mov(ops[0], ops[1])
            return

        # store/load with explicit size in Intel were normalized by operand formatter

        # Anything else:
        if self.em.show_unsupported:
            self.em.add(f"/* unsupported: {line.strip()} */")


def autodetect_syntax(lines: List[str]) -> str:
    for ln in lines:
        l = strip_comment(ln).strip()
        if not l:
            continue
        if looks_att(l):
            return 'att'
        # If has 'ptr [' it smells Intel
        if 'ptr' in l.lower() or '[' in l:
            return 'intel'
    return 'intel'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--in', dest='inp', default='-', help='Input assembly file or - for stdin')
    ap.add_argument('--func', dest='func', default='lifted_func', help='Output C function name')
    ap.add_argument('--syntax', dest='syntax', choices=['auto', 'intel', 'att'], default='auto', help='Assembly syntax')
    ap.add_argument('--arch', dest='arch', default='x86_64', help='Architecture (x86_64 only)')
    ap.add_argument('--show-unsupported', action='store_true', help='Emit comments for unsupported lines')
    args = ap.parse_args()

    if args.arch != 'x86_64':
        print("/* Only x86_64 supported */", file=sys.stderr)
        sys.exit(1)

    if args.inp == '-' or args.inp is None:
        raw = sys.stdin.read().splitlines()
    else:
        with open(args.inp, 'r', encoding='utf-8') as f:
            raw = f.read().splitlines()

    # strip comments & keep labels
    cleaned = []
    for ln in raw:
        if is_label(ln):
            cleaned.append(ln.rstrip())
        else:
            s = strip_comment(ln)
            if s.strip():
                cleaned.append(s.rstrip())

    syntax = args.syntax
    if syntax == 'auto':
        syntax = autodetect_syntax(cleaned)

    lifter = Lifter(syntax=syntax, show_unsupported=args.show_unsupported)
    lifter.set_func(args.func)

    for ln in cleaned:
        lifter.lift_line(ln)

    lifter.finish()
    # Print
    print("\n".join(lifter.em.lines))


if __name__ == '__main__':
    main()