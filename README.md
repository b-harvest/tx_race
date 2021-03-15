# tx_race

### serial

- pre-sign tx sequential broadcasting, retry loop for current sequence ~ +3
  - `python3 generate.py` generate send msg for pre-sign
  - sign
  - `python3 broadcast.py` start broadcasting
- 3 broadcaset methods (block, sysn, async) * nodes * Current sequence ~ + 2 

### realtime
- If an increase in the balance is detected by unbonding sign the current sequence ~ +4 tx and send it or send it online. (need to always allow for keyring)
- 3 broadcaset methods (block, sysn, async) * nodes * Current sequence ~ + 2 
- `python3 realtime.py` start checking balance