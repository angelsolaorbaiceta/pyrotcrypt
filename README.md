# Pyrotcrypt

A CLI to encrypt and decrypt text using [Caesar's cipher](https://en.wikipedia.org/wiki/Caesar_cipher).
(Don't use it to encrypt secrets, only for fun!)

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
