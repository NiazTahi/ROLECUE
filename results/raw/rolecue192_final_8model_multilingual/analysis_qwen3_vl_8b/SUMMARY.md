# Realistic-v2 multilingual pilot

All scores are collapsed across reversed A/B option mappings.

| Model | Task | Language | Order | n | Case accuracy | First-noun agreement | Option consistency |
|---|---|---|---|---:|---:|---:|---:|
| Qwen3-VL-8B | joint_match | bn | agent_first | 384 | 77.3% | 77.3% | 80.5% |
| Qwen3-VL-8B | joint_match | bn | patient_first | 384 | 55.2% | 44.8% | 56.2% |
| Qwen3-VL-8B | joint_match | de | agent_first | 384 | 94.5% | 94.5% | 93.5% |
| Qwen3-VL-8B | joint_match | de | patient_first | 384 | 79.2% | 20.8% | 84.1% |
| Qwen3-VL-8B | joint_match | en | agent_first | 384 | 86.5% | 86.5% | 82.6% |
| Qwen3-VL-8B | joint_match | en | patient_first | 384 | 90.6% | 9.4% | 85.7% |
| Qwen3-VL-8B | joint_match | ja | agent_first | 384 | 63.3% | 63.3% | 76.0% |
| Qwen3-VL-8B | joint_match | ja | patient_first | 384 | 79.4% | 20.6% | 51.3% |
| Qwen3-VL-8B | joint_match | ko | agent_first | 384 | 78.9% | 78.9% | 70.8% |
| Qwen3-VL-8B | joint_match | ko | patient_first | 384 | 72.7% | 27.3% | 58.6% |
| Qwen3-VL-8B | joint_match | tr | agent_first | 384 | 71.1% | 71.1% | 77.6% |
| Qwen3-VL-8B | joint_match | tr | patient_first | 384 | 65.1% | 34.9% | 52.3% |
| Qwen3-VL-8B | text_only | bn | agent_first | 384 | 100.0% | 100.0% | 100.0% |
| Qwen3-VL-8B | text_only | bn | patient_first | 384 | 45.8% | 54.2% | 4.2% |
| Qwen3-VL-8B | text_only | de | agent_first | 384 | 100.0% | 100.0% | 100.0% |
| Qwen3-VL-8B | text_only | de | patient_first | 384 | 87.5% | 12.5% | 87.5% |
| Qwen3-VL-8B | text_only | en | agent_first | 384 | 100.0% | 100.0% | 100.0% |
| Qwen3-VL-8B | text_only | en | patient_first | 384 | 16.7% | 83.3% | 45.8% |
| Qwen3-VL-8B | text_only | ja | agent_first | 384 | 100.0% | 100.0% | 100.0% |
| Qwen3-VL-8B | text_only | ja | patient_first | 384 | 100.0% | 0.0% | 45.8% |
| Qwen3-VL-8B | text_only | ko | agent_first | 384 | 100.0% | 100.0% | 100.0% |
| Qwen3-VL-8B | text_only | ko | patient_first | 384 | 100.0% | 0.0% | 33.3% |
| Qwen3-VL-8B | text_only | tr | agent_first | 384 | 100.0% | 100.0% | 100.0% |
| Qwen3-VL-8B | text_only | tr | patient_first | 384 | 100.0% | 0.0% | 75.0% |

## Joint match by ground-truth status

| Model | Language | Order | True match | n | Case accuracy | First-noun agreement |
|---|---|---|---:|---:|---:|---:|
| Qwen3-VL-8B | bn | agent_first | False | 192 | 56.8% | 56.8% |
| Qwen3-VL-8B | bn | agent_first | True | 192 | 97.9% | 97.9% |
| Qwen3-VL-8B | bn | patient_first | False | 192 | 22.4% | 77.6% |
| Qwen3-VL-8B | bn | patient_first | True | 192 | 88.0% | 12.0% |
| Qwen3-VL-8B | de | agent_first | False | 192 | 93.2% | 93.2% |
| Qwen3-VL-8B | de | agent_first | True | 192 | 95.8% | 95.8% |
| Qwen3-VL-8B | de | patient_first | False | 192 | 76.0% | 24.0% |
| Qwen3-VL-8B | de | patient_first | True | 192 | 82.3% | 17.7% |
| Qwen3-VL-8B | en | agent_first | False | 192 | 74.5% | 74.5% |
| Qwen3-VL-8B | en | agent_first | True | 192 | 98.4% | 98.4% |
| Qwen3-VL-8B | en | patient_first | False | 192 | 84.9% | 15.1% |
| Qwen3-VL-8B | en | patient_first | True | 192 | 96.4% | 3.6% |
| Qwen3-VL-8B | ja | agent_first | False | 192 | 29.2% | 29.2% |
| Qwen3-VL-8B | ja | agent_first | True | 192 | 97.4% | 97.4% |
| Qwen3-VL-8B | ja | patient_first | False | 192 | 63.5% | 36.5% |
| Qwen3-VL-8B | ja | patient_first | True | 192 | 95.3% | 4.7% |
| Qwen3-VL-8B | ko | agent_first | False | 192 | 62.0% | 62.0% |
| Qwen3-VL-8B | ko | agent_first | True | 192 | 95.8% | 95.8% |
| Qwen3-VL-8B | ko | patient_first | False | 192 | 50.5% | 49.5% |
| Qwen3-VL-8B | ko | patient_first | True | 192 | 94.8% | 5.2% |
| Qwen3-VL-8B | tr | agent_first | False | 192 | 46.4% | 46.4% |
| Qwen3-VL-8B | tr | agent_first | True | 192 | 95.8% | 95.8% |
| Qwen3-VL-8B | tr | patient_first | False | 192 | 41.7% | 58.3% |
| Qwen3-VL-8B | tr | patient_first | True | 192 | 88.5% | 11.5% |
