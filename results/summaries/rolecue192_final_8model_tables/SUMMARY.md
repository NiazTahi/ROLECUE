# ROLECUE-192 final 8-model tables

## Visual gate

| Model | Primary set | Images | Acc. | Chasing | Gate |
|---|---|---:|---:|---:|---|
| Qwen3-VL-8B | full | 192 | 99.0% | 87.5% | pass |
| Gemma-4-12B-it | full | 192 | 100.0% | 100.0% | pass |
| InternVL3.5-8B | no-chasing | 192 | 91.7% | 6.2% | no-chasing |
| LLaVA-OneVision-7B | no-chasing | 192 | 96.4% | 56.2% | no-chasing |
| MiniCPM-V-4.5 | no-chasing | 192 | 96.4% | 56.2% | no-chasing |
| Qwen2.5-VL-32B | no-chasing | 192 | 97.9% | 81.2% | no-chasing |
| Qwen3-VL-32B | full | 192 | 99.5% | 93.8% | pass |
| InternVL3.5-38B | full | 192 | 100.0% | 100.0% | pass |

## Patient-first joint accuracy

| Model | Set | de | ja | tr | en | ko | bn |
|---|---|---:|---:|---:|---:|---:|---:|
| Qwen3-VL-8B | full | 79.2% | 79.4% | 65.1% | 90.6% | 72.7% | 55.2% |
| Gemma-4-12B-it | full | 68.8% | 93.2% | 94.0% | 93.8% | 94.3% | 94.0% |
| InternVL3.5-8B | no-chasing | 59.4% | 54.5% | 46.6% | 93.5% | 68.2% | 55.7% |
| LLaVA-OneVision-7B | no-chasing | 50.3% | 50.0% | 50.0% | 71.9% | 50.0% | 50.0% |
| MiniCPM-V-4.5 | no-chasing | 6.8% | 76.1% | 6.0% | 95.2% | 72.2% | 10.8% |
| Qwen2.5-VL-32B | no-chasing | 18.8% | 96.9% | 92.9% | 95.5% | 98.9% | 94.9% |
| Qwen3-VL-32B | full | 98.7% | 98.7% | 99.0% | 97.9% | 94.8% | 98.7% |
| InternVL3.5-38B | full | 96.9% | 96.1% | 95.3% | 97.1% | 98.2% | 90.1% |

## Patient-first text-only accuracy

| Model | Set | de | ja | tr | en | ko | bn |
|---|---|---:|---:|---:|---:|---:|---:|
| Qwen3-VL-8B | full | 87.5% | 100.0% | 100.0% | 16.7% | 100.0% | 45.8% |
| Gemma-4-12B-it | full | 87.5% | 70.8% | 100.0% | 87.5% | 100.0% | 100.0% |
| InternVL3.5-8B | no-chasing | 59.1% | 100.0% | 54.5% | 36.4% | 95.5% | 45.5% |
| LLaVA-OneVision-7B | no-chasing | 45.5% | 95.5% | 36.4% | 77.3% | 90.9% | 54.5% |
| MiniCPM-V-4.5 | no-chasing | 15.6% | 41.8% | 1.4% | 11.4% | 41.5% | 12.5% |
| Qwen2.5-VL-32B | no-chasing | 36.4% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| Qwen3-VL-32B | full | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| InternVL3.5-38B | full | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
