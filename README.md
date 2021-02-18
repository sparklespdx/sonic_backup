# Sonic Backup: fast encrypted backups for large filesystems

### NOTE: This software is a work in progress. It may not work at all. USE AT YOUR OWN RISK.

Sonic Backup is a client and server for performing file level backups. I am developing Sonic Backup because the existing Linux backup software I've used is either highly complex, very slow, missing features I need, or a combination of the three.

Sonic Backup's purpose is to do what I need it to do and be highly performant. We gotta go fast. The project focuses on large filesystems with large files.

### Features:
* Easy backup and restore using simple cli tools. (wip)
* Verifies file integrity. (todo)
* End-to-end encryption: all keys are stored with the client and the server cannot decrypt data. (wip)
* Only writes to the backup when new files appear or when content changes. (todo)
* Extensibility: Accessible Python code base with hooks for extensions. (todo)
* Storage Flexibility: send backups to a local FS, the Sonic Backup server, S3-like object storage, or others via extensions. (wip)
* High performance / parallelized encryption, compression and network transport (faster faster faster). (wip)
* Accessible backup format: anyone with the key should be able to recover files without the software.
* Minimal storage of state: no backup server database and minimal caching.

### Architecture
**TODO**: high level overview of client and server architecture
**TODO**: walk through backup and restore process
**TODO**: walk through backup file format specification
**TODO**: talk about file encryption and compression implementation.

### Notes
Sonic Backup uses a key stored with the client to encrypt and decrypt backup data. If the client system suffers a catastrophe, that key may go missing. **Back up all Sonic Backup client encryption keys in a secure place**.

Sonic Backup values speed over preserving resources on the client. By default, it will use everything it can. **Make sure you tune the resource limits for Sonic Backup to fit your use case.**

Sonic Backup uses raw TCP sockets for network transport by default. This is to address performance concerns and duplicated work with SSH, SSL, and other authenticated/encrypted sockets. More secure transport can be implemented as an extension (and I will probably implement TLS sockets with mutual authentication) but the project does not assume that it is needed. The data being sent is already encrypted in the software. In the author's use case, WireGuard takes care of transport encryption, authentication and authorization. **Make sure that the connection between the client and server is secure before using Sonic Backup.** If you don't know how to make it safe, I recommend against using it.

Sonic Backup also uses a non-cryptographic hashing algorithm (xxHash) for file verification and finding duplicates. This is in the interest of performance. **If you need strong cryptographic hashes to verify your files, do not use Sonic Backup.**.

Sonic Backup has not been thoroughly evaluated for it's reliability or security. It is currently in alpha stage. **Do not use Sonic Backup for important data.**
