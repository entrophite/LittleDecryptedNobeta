# LittleDecryptedNobeta

Game save/achievement progress viewer and editor for the game Little Witch Nobeta.

Online site: [https://entrophite.github.io/LittleDecryptedNobeta/](https://entrophite.github.io/LittleDecryptedNobeta/)

## Synopsis

Apparently the devs added game save encryption upon the 1.0 release, since the old save editor I can find on github no longer works. No worry! Here is the save data editor to decrypt and re-encrypt the game save data, as well as the achievement progress in System.dat. Happy editing!

Reversed from and tested with steam version 1.0.5 (patch note 2022-12-21).

This project uses aes.js (source: [https://github.com/ricmoo/aes-js/blob/master/index.js](https://github.com/ricmoo/aes-js/blob/master/index.js)) for AES ciphers.