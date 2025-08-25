import os, random

# Default alphabet: space + lowercase letters (tweak as you wish)
DEFAULT_ALPHABET = "      abcdefghijklmnopqrstuvwxyz"

def build_kmp(pattern: str):
    """Precompute longest prefix-suffix (lps) table for KMP."""
    lps = [0]*len(pattern)
    i = 1
    length = 0
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length-1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_next_state(c, pattern, lps, state):
    """Advance the KMP automaton by char c; return new state (match length)."""
    while state > 0 and c != pattern[state]:
        state = lps[state-1]
    if c == pattern[state]:
        state += 1
    return state

def simulate_monkeys(
    outfile="monkey.txt",
    target=None,                          # string or None
    alphabet=DEFAULT_ALPHABET,
    batch_size=1_000_000,                 # chars per write (tune to your machine)
    report_every=5_000_000,               # progress print frequency
    seed=None,
    resume=True,
):
    """
    Streams random text to `outfile`. If `target` is set, stops when found.
    Returns a dict with stats (total_chars, found, position).
    """
    if seed is not None:
        random.seed(seed)

    # Prep target search if provided
    if target is not None:
        pat = target
        lps = build_kmp(pat)
        state = 0
        m = len(pat)
    else:
        pat = None
        lps = None
        state = 0
        m = 0

    total_chars = 0
    start_offset = 0

    # Open file for append; create if missing
    os.makedirs(os.path.dirname(outfile) or ".", exist_ok=True)
    mode = "ab"  # write bytes for speed
    f_exists = os.path.exists(outfile)

    # If resuming and target mode: warm up KMP with the last m-1 chars
    if resume and f_exists and pat:
        with open(outfile, "rb") as r:
            # Only need the last m-1 chars to set stream state correctly
            if m > 1:
                r.seek(0, os.SEEK_END)
                tail_len = min(m-1, r.tell())
                r.seek(-tail_len, os.SEEK_END)
                tail = r.read(tail_len).decode("utf-8", errors="ignore")
                # Feed tail into KMP to restore state
                for ch in tail:
                    state = kmp_next_state(ch, pat, lps, state)

            # Count existing chars for reporting
            r.seek(0, os.SEEK_END)
            start_offset = r.tell()

    with open(outfile, mode) as w:
        # Main loop
        while True:
            # Generate a batch
            batch_chars = [random.choice(alphabet) for _ in range(batch_size)]

            # If searching, scan as we “stream”
            if pat:
                for i, ch in enumerate(batch_chars, 1):
                    state = kmp_next_state(ch, pat, lps, state)
                    total_chars += 1
                    # Found full match
                    if state == m:
                        # Write up to and including this char
                        to_write = "".join(batch_chars[:i])
                        w.write(to_write.encode("utf-8"))
                        w.flush()
                        pos = start_offset + (total_chars)
                        return {
                            "outfile": outfile,
                            "total_chars_written_this_run": total_chars,
                            "file_size_bytes_end": start_offset + total_chars,
                            "found": True,
                            "match_end_position_1based": pos,
                            "target": target,
                            "alphabet_size": len(alphabet),
                        }

                    # Periodic progress report
                    if (start_offset + total_chars) % report_every == 0:
                        print(f"Wrote {(start_offset + total_chars):,} chars so far...")

                # If we got here, no match in this batch—write whole batch
                w.write("".join(batch_chars).encode("utf-8"))

            else:
                # No target: just blast batches
                w.write("".join(batch_chars).encode("utf-8"))
                total_chars += batch_size
                if (start_offset + total_chars) % report_every == 0:
                    print(f"Wrote {(start_offset + total_chars):,} chars so far...")

            # Optional: ensure data hits disk occasionally (safer, slightly slower)
            # os.fsync(w.fileno())

# ------------------------------
# Quick helpers / examples
# ------------------------------

def expected_chars_to_hit(target_len, alphabet_size):
    """
    Expected characters until first appearance ≈ alphabet_size**target_len (geometric),
    more precisely ~ A^n + n - 1 in a naive model (overlaps ignored).
    """
    return alphabet_size ** target_len

if __name__ == "__main__":
    # Example 1: stop when the phrase appears (lowercase & spaces)
    stats = simulate_monkeys(outfile="monkey.txt",
                             target="taaaaaa",
                             alphabet=DEFAULT_ALPHABET,
                             batch_size=1_000_000,
                             report_every=5_000_000,
                             seed=42,
                             resume=True)
    print(stats)

    # Example 2: just write forever (Ctrl+C to stop)
    # simulate_monkeys(outfile="monkey_infinite.txt",
    #                  target=None,
    #                  batch_size=1_000_000,
    #                  report_every=10_000_000)
    #