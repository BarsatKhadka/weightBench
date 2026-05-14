# %% [markdown]
# # First SVD on a real LoRA checkpoint
#
# Goal: see your own LoRA's singular value spectrum. One layer, one number, one plot.
# This is the smallest possible "I touched my own data with SVD" exercise.
#
# Open this file in VS Code, then click the "Run Cell" link above each `# %%` block
# (or press Shift+Enter). VS Code will start a Jupyter kernel automatically.
#
# Prerequisites: `pip install numpy safetensors matplotlib` in your local Python env.

# %%
import numpy as np
from safetensors.torch import load_file
from pathlib import Path
import matplotlib.pyplot as plt

# Adjust if your local path is different
ADAPTERS = Path(__file__).resolve().parents[1] / "adapters" / "hellaswag_seed0"
print(f"looking for adapters under: {ADAPTERS}")
print(f"exists: {ADAPTERS.exists()}")

# %% [markdown]
# ## Cell 1 — Inventory: what's in one checkpoint?

# %%
ckpt = ADAPTERS / "checkpoint-2000" / "adapter_model.safetensors"
sd = load_file(str(ckpt))

print(f"total tensors in this checkpoint: {len(sd)}")
print()
print("first 8 keys with shapes:")
for k in list(sd.keys())[:8]:
    print(f"  {k}  shape={tuple(sd[k].shape)}")

# %% [markdown]
# Observations to register:
# - `lora_A.weight` is `(16, in_dim)` — the down-projection
# - `lora_B.weight` is `(out_dim, 16)` — the up-projection
# - Their product `B @ A` is `(out_dim, in_dim)` — same shape as the original weight,
#   but constrained to rank ≤ 16

# %% [markdown]
# ## Cell 2 — Pick one layer, build ΔW, SVD it

# %%
# Try different layers later. Layer 14 q_proj is a reasonable starting point (mid-network attention).
B_key = "base_model.model.model.layers.14.self_attn.q_proj.lora_B.weight"
A_key = "base_model.model.model.layers.14.self_attn.q_proj.lora_A.weight"

B = sd[B_key].numpy().astype("float32")
A = sd[A_key].numpy().astype("float32")
dW = B @ A

print(f"B: {B.shape}")
print(f"A: {A.shape}")
print(f"dW = B @ A: {dW.shape}  (but rank ≤ {min(B.shape[1], A.shape[0])})")

# %%
# THE moment: SVD on real LoRA data
U, s, Vt = np.linalg.svd(dW, full_matrices=False)
print(f"U: {U.shape}    s: {s.shape}    Vt: {Vt.shape}")
print()
print("first 20 singular values:")
print(s[:20])
print()
print(f"ratio s[0] / s[15]: {s[0] / s[15]:.2f}")
print(f"singular values 16+ (should be ~0):")
print(s[16:25])

# %% [markdown]
# ## Cell 3 — Plot the spectrum

# %%
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].plot(np.arange(len(s)), s, "o-")
axes[0].set_xlabel("singular value index")
axes[0].set_ylabel("magnitude")
axes[0].set_title(f"All {len(s)} singular values of ΔW (layer 14 q_proj)")
axes[0].set_xlim(0, 30)
axes[0].grid(True, alpha=0.3)

axes[1].semilogy(np.arange(len(s)), s + 1e-10, "o-")
axes[1].set_xlabel("singular value index")
axes[1].set_ylabel("magnitude (log scale)")
axes[1].set_title("Same, log-y — the rank-16 cutoff becomes obvious")
axes[1].set_xlim(0, 30)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# %% [markdown]
# Look at the log-y plot. You should see a sharp drop after index 15:
# the first 16 are real, the rest are floating-point noise (~1e-7).
# That's the rank-16 constraint of LoRA visible in your own data.

# %% [markdown]
# ## Cell 4 — How did the spectrum evolve from step 50 to step 2000?

# %%
ckpt_early = ADAPTERS / "checkpoint-50" / "adapter_model.safetensors"
sd_early = load_file(str(ckpt_early))

B_e = sd_early[B_key].numpy().astype("float32")
A_e = sd_early[A_key].numpy().astype("float32")
dW_e = B_e @ A_e
_, s_e, _ = np.linalg.svd(dW_e, full_matrices=False)

print("singular values at step 50:")
print(s_e[:16])
print()
print("singular values at step 2000:")
print(s[:16])
print()
print("ratio step2000 / step50 per index:")
print(s[:16] / s_e[:16])

# %%
plt.figure(figsize=(8, 5))
plt.plot(np.arange(16), s_e[:16], "o-", label="step 50 (early)")
plt.plot(np.arange(16), s[:16], "o-", label="step 2000 (final)")
plt.xlabel("singular value index")
plt.ylabel("magnitude")
plt.title("How the spectrum grew over training (layer 14 q_proj)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# %% [markdown]
# ## Questions to answer by eye:
#
# 1. Did all 16 singular values grow uniformly, or did the top ones grow much more?
# 2. Is there a "gap" in the final spectrum — a clear drop separating big and small? If yes,
#    *that's the effective rank* the layer ended up using.
# 3. What's `||dW||_F` at step 2000 vs step 50? (`np.sqrt((s**2).sum())` — the Frobenius norm.)

# %%
print(f"||dW||_F at step 50:   {np.sqrt((s_e**2).sum()):.4f}")
print(f"||dW||_F at step 2000: {np.sqrt((s**2).sum()):.4f}")
print(f"growth factor: {np.sqrt((s**2).sum()) / np.sqrt((s_e**2).sum()):.2f}x")

# %% [markdown]
# ## Next steps (later sessions, not now)
#
# - Try other layers (layer 0, layer 27, MLP modules) — does the pattern differ?
# - Compare layer 14 q_proj across different seeds (seed 0 vs seed 1) — same shape?
# - Plot the singular-value trajectory across ALL 40 checkpoints — that's the σ-shrink test.
#
# Don't do all of these tonight. Just look at the four cells above and let it sink in.
