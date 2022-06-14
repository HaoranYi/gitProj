---
marp: true
---

# Stake Reward Computation

---

# Problem

At the start of each epoch, the stake rewards are computed and credited to stake accounts through the following code path - which actually happens on the bank creation time (i.e. bank::new_from_parent) synchronously and block further bank processing.

The problem is that, with the growing number of stake accounts, the reward computation time takes multiple seconds.

To address this issue, a few approaches have been proposed, which is summarized below.

---

# Summary of stake_rewards proposals

- sharding the reward computation and update over multiple slots
- offload reward computation into a background threads and update later when rewards are available
- precompute reward before epoch boundary
- use a reward pool to store rewards, and provide new reward withdraw instruction to let the user withdraw reward later.

---

# Proposed Implementation

- sharding: evenly distributed stake rewards collection over the epoch
- early reward payment when the stake account is accessed before its assigned collection slot

---

# Leader Scheduler
![bg fit left](leader_schedule.svg)
- stake distribution used in epoch leader schedule computation
- snapshot before epoch leader schedule computation
- rewards materialized for next epoch's leader schedule computation

---
# Q/A
