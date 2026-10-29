# Realistic-v2 multilingual pilot

All scores are collapsed across reversed A/B option mappings.

| Model | Task | Language | Order | n | Case accuracy | First-noun agreement | Option consistency |
|---|---|---|---|---:|---:|---:|---:|
| Qwen3-VL-32B | joint_match | bn | agent_first | 384 | 99.0% | 99.0% | 100.0% |
| Qwen3-VL-32B | joint_match | bn | patient_first | 384 | 98.7% | 1.3% | 99.7% |
| Qwen3-VL-32B | joint_match | de | agent_first | 384 | 99.0% | 99.0% | 100.0% |
| Qwen3-VL-32B | joint_match | de | patient_first | 384 | 98.7% | 1.3% | 99.5% |
| Qwen3-VL-32B | joint_match | en | agent_first | 384 | 99.0% | 99.0% | 99.5% |
| Qwen3-VL-32B | joint_match | en | patient_first | 384 | 97.9% | 2.1% | 99.7% |
| Qwen3-VL-32B | joint_match | ja | agent_first | 384 | 99.0% | 99.0% | 98.7% |
| Qwen3-VL-32B | joint_match | ja | patient_first | 384 | 98.7% | 1.3% | 99.7% |
| Qwen3-VL-32B | joint_match | ko | agent_first | 384 | 98.7% | 98.7% | 99.0% |
| Qwen3-VL-32B | joint_match | ko | patient_first | 384 | 94.8% | 5.2% | 99.5% |
| Qwen3-VL-32B | joint_match | tr | agent_first | 384 | 97.7% | 97.7% | 98.2% |
| Qwen3-VL-32B | joint_match | tr | patient_first | 384 | 99.0% | 1.0% | 100.0% |
| Qwen3-VL-32B | text_only | bn | agent_first | 384 | 100.0% | 100.0% | 100.0% |
| Qwen3-VL-32B | text_only | bn | patient_first | 384 | 100.0% | 0.0% | 20.8% |
| Qwen3-VL-32B | text_only | de | agent_first | 384 | 100.0% | 100.0% | 100.0% |
| Qwen3-VL-32B | text_only | de | patient_first | 384 | 100.0% | 0.0% | 100.0% |
| Qwen3-VL-32B | text_only | en | agent_first | 384 | 100.0% | 100.0% | 100.0% |
| Qwen3-VL-32B | text_only | en | patient_first | 384 | 100.0% | 0.0% | 41.7% |
| Qwen3-VL-32B | text_only | ja | agent_first | 384 | 100.0% | 100.0% | 100.0% |
| Qwen3-VL-32B | text_only | ja | patient_first | 384 | 100.0% | 0.0% | 91.7% |
| Qwen3-VL-32B | text_only | ko | agent_first | 384 | 100.0% | 100.0% | 100.0% |
| Qwen3-VL-32B | text_only | ko | patient_first | 384 | 100.0% | 0.0% | 100.0% |
| Qwen3-VL-32B | text_only | tr | agent_first | 384 | 100.0% | 100.0% | 100.0% |
| Qwen3-VL-32B | text_only | tr | patient_first | 384 | 100.0% | 0.0% | 66.7% |

## Joint match by ground-truth status

| Model | Language | Order | True match | n | Case accuracy | First-noun agreement |
|---|---|---|---:|---:|---:|---:|
| Qwen3-VL-32B | bn | agent_first | False | 192 | 100.0% | 100.0% |
| Qwen3-VL-32B | bn | agent_first | True | 192 | 97.9% | 97.9% |
| Qwen3-VL-32B | bn | patient_first | False | 192 | 100.0% | 0.0% |
| Qwen3-VL-32B | bn | patient_first | True | 192 | 97.4% | 2.6% |
| Qwen3-VL-32B | de | agent_first | False | 192 | 100.0% | 100.0% |
| Qwen3-VL-32B | de | agent_first | True | 192 | 97.9% | 97.9% |
| Qwen3-VL-32B | de | patient_first | False | 192 | 100.0% | 0.0% |
| Qwen3-VL-32B | de | patient_first | True | 192 | 97.4% | 2.6% |
| Qwen3-VL-32B | en | agent_first | False | 192 | 100.0% | 100.0% |
| Qwen3-VL-32B | en | agent_first | True | 192 | 97.9% | 97.9% |
| Qwen3-VL-32B | en | patient_first | False | 192 | 100.0% | 0.0% |
| Qwen3-VL-32B | en | patient_first | True | 192 | 95.8% | 4.2% |
| Qwen3-VL-32B | ja | agent_first | False | 192 | 100.0% | 100.0% |
| Qwen3-VL-32B | ja | agent_first | True | 192 | 97.9% | 97.9% |
| Qwen3-VL-32B | ja | patient_first | False | 192 | 100.0% | 0.0% |
| Qwen3-VL-32B | ja | patient_first | True | 192 | 97.4% | 2.6% |
| Qwen3-VL-32B | ko | agent_first | False | 192 | 99.5% | 99.5% |
| Qwen3-VL-32B | ko | agent_first | True | 192 | 97.9% | 97.9% |
| Qwen3-VL-32B | ko | patient_first | False | 192 | 100.0% | 0.0% |
| Qwen3-VL-32B | ko | patient_first | True | 192 | 89.6% | 10.4% |
| Qwen3-VL-32B | tr | agent_first | False | 192 | 97.4% | 97.4% |
| Qwen3-VL-32B | tr | agent_first | True | 192 | 97.9% | 97.9% |
| Qwen3-VL-32B | tr | patient_first | False | 192 | 100.0% | 0.0% |
| Qwen3-VL-32B | tr | patient_first | True | 192 | 97.9% | 2.1% |
