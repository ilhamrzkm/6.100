# Problem Set 1 — Beaver Cipher

Implement a variant of a Caesar cipher (the **Beaver cipher**) and then break it without knowing the key.

Run tests from this folder:

```bash
python3 test.py
```

Fill in your name/kerberos at the top of `pset.py`. Do not change the supplied helpers (`is_word`, etc.). Extra imports are not allowed.

## The cipher

You are given an ordered `alphabet` string. Characters in the alphabet wrap around using modular arithmetic. Characters **not** in the alphabet are copied through unchanged.

A Beaver cipher has two key pieces:

1. **`initial_shift`** — how far the first alphabet character is shifted forward.
2. **`magic_number`** — after encrypting a character whose **new index** is a multiple of `magic_number`, increase the shift by 1 for later characters.

Decrypting is the reverse: shift backward, but bump the shift when the **ciphertext character's original index** is a multiple of `magic_number`.

Example with `alphabet = a…zA…Z`, `initial_shift = 2`, `magic_number = 8`:

- `"easy"` encrypts to `"gcuA"`.

## Functions to implement

### `encrypt_char` / `decrypt_char`

Shift a single character that is known to be in `alphabet`. Wrapping should use `% len(alphabet)`.

Manual check: `decrypt_char("c", lowercase+uppercase, 2)` should be `"a"`. `decrypt_char("a", …, 5)` wraps to `"V"`.

### `encrypt(plaintext, alphabet, initial_shift, magic_number)`

Walk the plaintext left to right:

- If the character is in `alphabet`, encrypt it with the **current** shift, then if the new index is divisible by `magic_number`, increment the shift.
- Otherwise leave it unchanged (spaces, digits not in the alphabet, etc.).

### `decrypt(ciphertext, alphabet, initial_shift, magic_number)`

Same walk, but shift backward. The magic-number check uses the ciphertext character's index **before** decrypting.

Encrypting then decrypting with the same key should recover the original text.

### `count_words(text)`

Count valid English words using the provided `is_word()`.

- Lowercase the text first.
- Words are chunks of characters **between** the given `separators` (`whitespace`, `- /`, punctuation pauses, and `"`).
- Apostrophes inside a token are part of the word (`don't`, possessives). Hyphens and slashes split words (`state-of-the-art` is four words).

Examples: `"hello world"` → 2; `'Hello, "World\'s Fair"!'` → 3.

### `break_cipher(ciphertext, alphabet)`

Try possible keys and return the decryption with the **most** `count_words` hits. If several tie, any of them is fine.

A practical search space:

- `magic_number` from 1 up to a modest bound (tests use small alphabets; trying 1–99 is enough).
- `initial_shift` over `range(len(alphabet))`.

This is brute force — correctness matters more than clever optimization.

## Suggested order

1. Character encrypt/decrypt and wraparound.
2. Full-string encrypt, then decrypt as the inverse.
3. Word counting on the separator rules.
4. Cipher breaking using (2) and (3).

Use the commented manual tests at the bottom of `pset.py`, then `python3 test.py`.
