# Backpack: fast encrypted backups for large filesystems

### NOTE: This software is a work in progress. It may not work at all. USE AT YOUR OWN RISK.

Backpack is a client and server for performing file level backups. I developed Backpack because the Linux backup software I've used is either highly complex, very slow, missing features I need, or a combination of the three.

Backpack's purpose is to do what I need it to do and be highly performant. We gotta go fast. The project focuses on large filesystems with large files.

### Features: (WIP)
* Easy backup and restore using simple cli tools.
* Verifies file integrity.
* End-to-end encryption: all keys are stored with the client and the server cannot decrypt data.
* Only writes to the backup when new files appear or when content changes.
* Extensibility: Accessible Python code base with hooks for extensions.
* Storage Flexibility: send backups to a local FS, the Backpack server, S3-like object storage, or others via extensions.
* High performance / parallelized encryption, compression and network transport (faster faster faster).
* Accessible backup format: anyone with the key should be able to recover files without the software.
* Minimal storage of state: no backup server database and minimal caching.

### Architecture
**TODO**: high level overview of client and server architecture
**TODO**: walk through backup and restore process
**TODO**: walk through backup file format specification
**TODO**: talk about file encryption and compression implementation.

### Notes
Backpack uses a key stored with the client to encrypt and decrypt backup data. If the client system suffers a catastrophe, that key may go missing. **Back up all Backpack client encryption keys in a secure place**.

Backpack values speed over preserving resources on the client. By default, it will use everything it can. **Make sure you tune the resource limits for Backpack to fit your use case**.

Backpack uses raw TCP sockets for network transport by default. This is to address performance concerns and duplicated work with SSH, SSL, and other authenticated/encrypted sockets. More secure transport can be implemented as an extension (and I will probably implement TLS sockets with mutual authentication) but the project does not assume that it is needed. The data being sent is already encrypted client-side and verified when received. In the author's use case, WireGuard takes care of transport encryption, authentication and authorization. **Make sure that your network transport security is addressed before using Backpack**. If you don't know how to make it safe, I recommend against using it.

Backpack also uses a non-cryptographic hashing algorithm (xxHash) for file verification and finding duplicates. This is in the interest of performance. **If you need strong cryptographic hashes to verify your files, do not use Backpack**.

Backpack has not been thoroughly evaluated for it's reliability or security. It is currently in alpha stage. **Do not use Backpack for important data, unless you like to live on the bleeding edge.**
