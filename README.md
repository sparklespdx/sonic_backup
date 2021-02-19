# Moop: fast encrypted backups for large filesystems

### NOTE: This software is pre-alpha and is a work in progress. It may not work at all. USE AT YOUR OWN RISK. Don't use it with important data.

Moop is a client and server for performing file level backups. I am developing Moop because the existing Linux backup software I've used is either highly complex, very slow, missing features I need, or a combination of the three.

Moop's purpose is to do what I need it to do and be highly performant. We gotta go fast. The project focuses on large filesystems with large files.

### Features:
* Easy backup and restore using simple cli tools. (wip)
* Verifies file integrity. (todo)
* End-to-end encryption: all keys are stored with the client and the server cannot decrypt data. (wip)
* Differential backups (todo)
* Extensibility: Accessible Python code base with hooks for extensions. (todo)
* Storage Flexibility: send backups to a local FS, the Moop server, S3-like object storage, or others via extensions. (wip)
* High performance / parallelized encryption, compression and network transport (faster faster faster). (wip)
* Accessible backup format: anyone with the key should be able to recover files without the software.
* Minimal storage of state: no backup server database and minimal caching.

### Architecture
**TODO**: high level overview of client and server architecture

**TODO**: walk through backup and restore process

**TODO**: walk through backup file format specification

**TODO**: talk about file encryption and compression implementation.
