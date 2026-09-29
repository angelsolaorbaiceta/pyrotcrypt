# Pyrotcrypt

A CLI to encrypt and decrypt text using [Caesar's cipher](https://en.wikipedia.org/wiki/Caesar_cipher).
(Don't use it to encrypt secrets, only for fun!)

# Installation

Using uv:

```bash
$ uv tool install pyrotcrypt
```

# Usage

Encrypt text from stdin, using the default 13 rotations:

```bash
$ pyrotcrypt < example.txt
```

Decrypt text from stdin using the `--decrypt` flag:

```bash
$ pyrotcrypt --decrypt < example.encrypted.txt
```

Encrypt and decrypt usign a different number of rotations:

```bash
$ pyrotcrypt --num 10 < example.txt
$ pyrotcrypt --num 10 --decrypt < example.encrypted.txt
```

Encrypt files, writing the ciphertext to stdout:

```bash
$ pyrotcrypt example.txt another_example.txt
```

Encrypt files, writing the ciphertext to files:

```bash
$ pyrotcrypt --write example.txt another_example.txt
```

Writes the result of encrypting _example.txt_ to _example.cipher.rot13.txt_ and _another_example.txt_ to _another_example.cipher.rot13.txt_.

Encrypt from stin to a file called _cipher.rot7.txt_:

```bash
$ pyrotcrypt --num 7 --write < example.txt
```
