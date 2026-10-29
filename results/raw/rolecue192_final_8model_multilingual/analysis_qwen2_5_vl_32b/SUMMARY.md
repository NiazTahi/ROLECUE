# Realistic-v2 multilingual pilot

All scores are collapsed across reversed A/B option mappings.

| Model | Task | Language | Order | n | Case accuracy | First-noun agreement | Option consistency |
|---|---|---|---|---:|---:|---:|---:|
| Qwen2.5-VL-32B | joint_match | bn | agent_first | 352 | 99.4% | 99.4% | 100.0% |
| Qwen2.5-VL-32B | joint_match | bn | patient_first | 352 | 94.9% | 5.1% | 96.9% |
| Qwen2.5-VL-32B | joint_match | de | agent_first | 352 | 99.4% | 99.4% | 99.7% |
| Qwen2.5-VL-32B | joint_match | de | patient_first | 352 | 18.8% | 81.2% | 98.6% |
| Qwen2.5-VL-32B | joint_match | en | agent_first | 352 | 98.0% | 98.0% | 99.7% |
| Qwen2.5-VL-32B | joint_match | en | patient_first | 352 | 95.5% | 4.5% | 100.0% |
| Qwen2.5-VL-32B | joint_match | ja | agent_first | 352 | 98.3% | 98.3% | 98.6% |
| Qwen2.5-VL-32B | joint_match | ja | patient_first | 352 | 96.9% | 3.1% | 98.0% |
| Qwen2.5-VL-32B | joint_match | ko | agent_first | 352 | 98.9% | 98.9% | 99.4% |
| Qwen2.5-VL-32B | joint_match | ko | patient_first | 352 | 98.9% | 1.1% | 99.4% |
| Qwen2.5-VL-32B | joint_match | tr | agent_first | 352 | 88.9% | 88.9% | 95.7% |
| Qwen2.5-VL-32B | joint_match | tr | patient_first | 352 | 92.9% | 7.1% | 96.9% |
| Qwen2.5-VL-32B | text_only | bn | agent_first | 352 | 100.0% | 100.0% | 100.0% |
| Qwen2.5-VL-32B | text_only | bn | patient_first | 352 | 100.0% | 0.0% | 100.0% |
| Qwen2.5-VL-32B | text_only | de | agent_first | 352 | 100.0% | 100.0% | 100.0% |
| Qwen2.5-VL-32B | text_only | de | patient_first | 352 | 36.4% | 63.6% | 90.9% |
| Qwen2.5-VL-32B | text_only | en | agent_first | 352 | 100.0% | 100.0% | 100.0% |
| Qwen2.5-VL-32B | text_only | en | patient_first | 352 | 100.0% | 0.0% | 36.4% |
| Qwen2.5-VL-32B | text_only | ja | agent_first | 352 | 100.0% | 100.0% | 100.0% |
| Qwen2.5-VL-32B | text_only | ja | patient_first | 352 | 100.0% | 0.0% | 100.0% |
| Qwen2.5-VL-32B | text_only | ko | agent_first | 352 | 100.0% | 100.0% | 100.0% |
| Qwen2.5-VL-32B | text_only | ko | patient_first | 352 | 100.0% | 0.0% | 100.0% |
| Qwen2.5-VL-32B | text_only | tr | agent_first | 352 | 100.0% | 100.0% | 100.0% |
| Qwen2.5-VL-32B | text_only | tr | patient_first | 352 | 100.0% | 0.0% | 100.0% |

## Joint match by ground-truth status

| Model | Language | Order | True match | n | Case accuracy | First-noun agreement |
|---|---|---|---:|---:|---:|---:|
| Qwen2.5-VL-32B | bn | agent_first | False | 176 | 98.9% | 98.9% |
| Qwen2.5-VL-32B | bn | agent_first | True | 176 | 100.0% | 100.0% |
| Qwen2.5-VL-32B | bn | patient_first | False | 176 | 90.3% | 9.7% |
| Qwen2.5-VL-32B | bn | patient_first | True | 176 | 99.4% | 0.6% |
| Qwen2.5-VL-32B | de | agent_first | False | 176 | 98.9% | 98.9% |
| Qwen2.5-VL-32B | de | agent_first | True | 176 | 100.0% | 100.0% |
| Qwen2.5-VL-32B | de | patient_first | False | 176 | 13.1% | 86.9% |
| Qwen2.5-VL-32B | de | patient_first | True | 176 | 24.4% | 75.6% |
| Qwen2.5-VL-32B | en | agent_first | False | 176 | 96.6% | 96.6% |
| Qwen2.5-VL-32B | en | agent_first | True | 176 | 99.4% | 99.4% |
| Qwen2.5-VL-32B | en | patient_first | False | 176 | 97.7% | 2.3% |
| Qwen2.5-VL-32B | en | patient_first | True | 176 | 93.2% | 6.8% |
| Qwen2.5-VL-32B | ja | agent_first | False | 176 | 98.3% | 98.3% |
| Qwen2.5-VL-32B | ja | agent_first | True | 176 | 98.3% | 98.3% |
| Qwen2.5-VL-32B | ja | patient_first | False | 176 | 95.5% | 4.5% |
| Qwen2.5-VL-32B | ja | patient_first | True | 176 | 98.3% | 1.7% |
| Qwen2.5-VL-32B | ko | agent_first | False | 176 | 97.7% | 97.7% |
| Qwen2.5-VL-32B | ko | agent_first | True | 176 | 100.0% | 100.0% |
| Qwen2.5-VL-32B | ko | patient_first | False | 176 | 98.3% | 1.7% |
| Qwen2.5-VL-32B | ko | patient_first | True | 176 | 99.4% | 0.6% |
| Qwen2.5-VL-32B | tr | agent_first | False | 176 | 80.7% | 80.7% |
| Qwen2.5-VL-32B | tr | agent_first | True | 176 | 97.2% | 97.2% |
| Qwen2.5-VL-32B | tr | patient_first | False | 176 | 87.5% | 12.5% |
| Qwen2.5-VL-32B | tr | patient_first | True | 176 | 98.3% | 1.7% |
