# Problem Set 1: The Beaver Cipher

## Introduction

It is 3 a.m. on the Infinite Corridor. Someone has taped a strip of paper to a classroom door:

> `gcuA!`

Underneath is a doodle of a beaver and a note from the Mystery Hunt committee:

> *New cipher this year. Same alphabet, wrapping shift — but the shift is not constant. If you can implement it, you can hide a message. If you can break it, you can find the next puzzle.*

The committee calls it the **Beaver cipher**: a Caesar cipher that occasionally “bumps” its shift, using a secret **magic number**. Your job in this problem set is to implement encryption and decryption, then recover English plaintext **without being told the key**.

Although this handout is long, the information is here to provide you with context, useful examples, and hints, so be sure to read carefully.

## Objectives

- Practice strings, loops, and modular arithmetic
- Implement a cipher as a pair of inverse operations
- Use a dictionary / word list as an objective function for a brute-force search

## Getting Started

Work in this folder. Fill in your name and kerberos at the top of `pset.py`.

Do **not** change the supplied helpers (`collect_file_entries`, `initialize_words`, `is_possessive_word`, `is_word`, etc.). Extra imports are not allowed.

Run the staff tests from this folder:

```bash
python3 test.py
```

You can also try the commented manual checks at the bottom of `pset.py`.

---

## Problem 1: How the Beaver cipher works

You are given an ordered `alphabet` string. Characters in the alphabet wrap around using modular arithmetic (`% len(alphabet)`). Characters **not** in the alphabet — spaces, digits, punctuation the alphabet does not contain — are copied through unchanged.

A Beaver cipher has two key pieces:

1. **`initial_shift`** — how far the first alphabet character is shifted forward.
2. **`magic_number`** — after encrypting a character whose **new index** is a multiple of `magic_number`, increase the shift by 1 for later characters.

Decrypting is the reverse: shift backward, but bump the shift when the **ciphertext character's original index** is a multiple of `magic_number`.

**Example.** With `alphabet = a…zA…Z` (that is, `string.ascii_lowercase + string.ascii_uppercase`), `initial_shift = 2`, and `magic_number = 8`:

- `"easy"` encrypts to `"gcuA"`.

Think of the beaver walking along the message. Most of the time it uses a fixed Caesar shift. Whenever it lands on an alphabet index that is a multiple of the magic number, it gets a little more caffeinated and the shift increases by one.

---

## Problem 2: Character-level Caesar steps

Implement the two helpers that move a **single** character that is already known to be in `alphabet`.

### 2.1) `encrypt_char(char, alphabet, shift)`

Shift `char` forward by `shift` positions in `alphabet`. Wrapping should use `% len(alphabet)`.

### 2.2) `decrypt_char(char, alphabet, shift)`

Shift `char` backward by `shift` positions. Same wraparound rule.

**Manual checks** (with `alphabet = lowercase + uppercase`):

- `decrypt_char("c", alphabet, 2)` should be `"a"`.
- `decrypt_char("a", alphabet, 5)` wraps around the end of the alphabet to `"V"`.

**Hint:** Find the index of `char` in `alphabet`, add or subtract `shift`, then take the character at the wrapped index. You should not special-case lowercase vs. uppercase; the alphabet string already defines the order.

---

## Problem 3: Encrypting and decrypting a whole message

### 3.1) `encrypt(plaintext, alphabet, initial_shift, magic_number)`

Walk the plaintext left to right, keeping a **current** shift that starts at `initial_shift`:

- If the character is in `alphabet`, encrypt it with the **current** shift, then if the **new** index (the ciphertext character’s index) is divisible by `magic_number`, increment the shift.
- Otherwise leave the character unchanged.

### 3.2) `decrypt(ciphertext, alphabet, initial_shift, magic_number)`

Same left-to-right walk, but shift **backward**. The magic-number check uses the ciphertext character’s index **before** decrypting.

Encrypting then decrypting with the same key should recover the original text. That is a good sanity check before you move on.

**Hint:** The bump happens based on an index in `alphabet`, not based on the character’s position in the string. Spaces never bump the shift, because they are not in the alphabet.

---

## Problem 4: Counting English words

The Hunt committee will not give you the key. To guess it, you need a way to score a candidate decryption: **how English does it look?**

### 4.1) `count_words(text)`

Count valid English words using the provided `is_word()`.

- Lowercase the text first.
- Words are chunks of characters **between** the given `separators` (`whitespace`, `- /`, punctuation pauses, and `"`). These constants are already defined in `pset.py`.
- Apostrophes inside a token are part of the word (`don't`, possessives). Hyphens and slashes **split** words (`state-of-the-art` is four candidate tokens).

**Examples:**

- `"hello world"` → `2`
- `'Hello, "World\'s Fair"!'` → `3`

**Hint:** You can walk the string and split whenever you hit a separator, then ask `is_word` about each non-empty token. Remember that `is_word` expects lowercase text with no surrounding punctuation.

---

## Problem 5: Breaking the cipher

The note on the door is only the first of many. You do not know `initial_shift` or `magic_number`. Time to brute-force the beaver.

### 5.1) `break_cipher(ciphertext, alphabet)`

Try possible keys and return the decryption with the **most** `count_words` hits. If several keys tie, any of those plaintexts is fine.

A practical search space:

- `magic_number` from 1 up to a modest bound (tests use small alphabets; trying 1–99 is enough).
- `initial_shift` over `range(len(alphabet))`.

This is brute force — correctness matters more than clever optimization.

**Hint:** For each candidate key, call your `decrypt`, then `count_words`. Keep the plaintext with the best score. You already wrote the hard parts; this function is a nested loop around them.

---

## Suggested order

1. Character encrypt/decrypt and wraparound.
2. Full-string encrypt, then decrypt as the inverse.
3. Word counting on the separator rules.
4. Cipher breaking using (2) and (3).

Use the commented manual tests at the bottom of `pset.py`, then `python3 test.py`.
