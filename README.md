# tx_race

### serial

- pre-sign tx sequential broadcasting, retry loop for current sequence ~ +3
  - generate, sign txs
    - `python3 generate.py` generate send msg for pre-sign by using keyring
    - `python3 generate_passphrase.py` generate send msg for pre-sign by file backend with passphrase ( need to recover key as file `gaiad keys add test --recover --keyring-backend file` )
  - start broadcast before 1 miniute when you need
    - `python3 broadcast.py` start broadcasting
- 3 broadcaset methods (block, sysn, async) * nodes * Current sequence ~ + 2 

### realtime
- If an increase in the balance is detected by unbonding sign the current sequence ~ +4 tx and send it or send it online. (need to always allow for keyring)
- 3 broadcaset methods (block, sysn, async) * nodes * Current sequence ~ + 2 
- start realtime 10 minutes in advance, it can be a good insurance as a two-track
- `python3 realtime.py` start checking balance


### notice
- We highly recommended test on testnet before use
- It may fail, it may not work, it may be buggy, and it does not guarantee success.