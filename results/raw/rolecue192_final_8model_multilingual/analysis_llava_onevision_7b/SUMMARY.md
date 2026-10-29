# Realistic-v2 multilingual pilot

All scores are collapsed across reversed A/B option mappings.

| Model | Task | Language | Order | n | Case accuracy | First-noun agreement | Option consistency |
|---|---|---|---|---:|---:|---:|---:|
| LLaVA-OneVision-7B | joint_match | bn | agent_first | 352 | 50.0% | 50.0% | 99.4% |
| LLaVA-OneVision-7B | joint_match | bn | patient_first | 352 | 50.0% | 50.0% | 100.0% |
| LLaVA-OneVision-7B | joint_match | de | agent_first | 352 | 64.8% | 64.8% | 91.5% |
| LLaVA-OneVision-7B | joint_match | de | patient_first | 352 | 50.3% | 49.7% | 96.3% |
| LLaVA-OneVision-7B | joint_match | en | agent_first | 352 | 81.5% | 81.5% | 99.1% |
| LLaVA-OneVision-7B | joint_match | en | patient_first | 352 | 71.9% | 28.1% | 94.3% |
| LLaVA-OneVision-7B | joint_match | ja | agent_first | 352 | 50.0% | 50.0% | 100.0% |
| LLaVA-OneVision-7B | joint_match | ja | patient_first | 352 | 50.0% | 50.0% | 99.7% |
| LLaVA-OneVision-7B | joint_match | ko | agent_first | 352 | 50.0% | 50.0% | 100.0% |
| LLaVA-OneVision-7B | joint_match | ko | patient_first | 352 | 50.0% | 50.0% | 99.7% |
| LLaVA-OneVision-7B | joint_match | tr | agent_first | 352 | 50.0% | 50.0% | 100.0% |
| LLaVA-OneVision-7B | joint_match | tr | patient_first | 352 | 50.0% | 50.0% | 100.0% |
| LLaVA-OneVision-7B | text_only | bn | agent_first | 352 | 100.0% | 100.0% | 100.0% |
| LLaVA-OneVision-7B | text_only | bn | patient_first | 352 | 54.5% | 45.5% | 0.0% |
| LLaVA-OneVision-7B | text_only | de | agent_first | 352 | 100.0% | 100.0% | 100.0% |
| LLaVA-OneVision-7B | text_only | de | patient_first | 352 | 45.5% | 54.5% | 68.2% |
| LLaVA-OneVision-7B | text_only | en | agent_first | 352 | 100.0% | 100.0% | 100.0% |
| LLaVA-OneVision-7B | text_only | en | patient_first | 352 | 77.3% | 22.7% | 72.7% |
| LLaVA-OneVision-7B | text_only | ja | agent_first | 352 | 100.0% | 100.0% | 100.0% |
| LLaVA-OneVision-7B | text_only | ja | patient_first | 352 | 95.5% | 4.5% | 13.6% |
| LLaVA-OneVision-7B | text_only | ko | agent_first | 352 | 100.0% | 100.0% | 100.0% |
| LLaVA-OneVision-7B | text_only | ko | patient_first | 352 | 90.9% | 9.1% | 36.4% |
| LLaVA-OneVision-7B | text_only | tr | agent_first | 352 | 100.0% | 100.0% | 100.0% |
| LLaVA-OneVision-7B | text_only | tr | patient_first | 352 | 36.4% | 63.6% | 54.5% |

## Joint match by ground-truth status

| Model | Language | Order | True match | n | Case accuracy | First-noun agreement |
|---|---|---|---:|---:|---:|---:|
| LLaVA-OneVision-7B | bn | agent_first | False | 176 | 0.0% | 0.0% |
| LLaVA-OneVision-7B | bn | agent_first | True | 176 | 100.0% | 100.0% |
| LLaVA-OneVision-7B | bn | patient_first | False | 176 | 0.0% | 100.0% |
| LLaVA-OneVision-7B | bn | patient_first | True | 176 | 100.0% | 0.0% |
| LLaVA-OneVision-7B | de | agent_first | False | 176 | 29.5% | 29.5% |
| LLaVA-OneVision-7B | de | agent_first | True | 176 | 100.0% | 100.0% |
| LLaVA-OneVision-7B | de | patient_first | False | 176 | 3.4% | 96.6% |
| LLaVA-OneVision-7B | de | patient_first | True | 176 | 97.2% | 2.8% |
| LLaVA-OneVision-7B | en | agent_first | False | 176 | 63.1% | 63.1% |
| LLaVA-OneVision-7B | en | agent_first | True | 176 | 100.0% | 100.0% |
| LLaVA-OneVision-7B | en | patient_first | False | 176 | 43.8% | 56.2% |
| LLaVA-OneVision-7B | en | patient_first | True | 176 | 100.0% | 0.0% |
| LLaVA-OneVision-7B | ja | agent_first | False | 176 | 0.0% | 0.0% |
| LLaVA-OneVision-7B | ja | agent_first | True | 176 | 100.0% | 100.0% |
| LLaVA-OneVision-7B | ja | patient_first | False | 176 | 0.0% | 100.0% |
| LLaVA-OneVision-7B | ja | patient_first | True | 176 | 100.0% | 0.0% |
| LLaVA-OneVision-7B | ko | agent_first | False | 176 | 0.0% | 0.0% |
| LLaVA-OneVision-7B | ko | agent_first | True | 176 | 100.0% | 100.0% |
| LLaVA-OneVision-7B | ko | patient_first | False | 176 | 0.0% | 100.0% |
| LLaVA-OneVision-7B | ko | patient_first | True | 176 | 100.0% | 0.0% |
| LLaVA-OneVision-7B | tr | agent_first | False | 176 | 0.0% | 0.0% |
| LLaVA-OneVision-7B | tr | agent_first | True | 176 | 100.0% | 100.0% |
| LLaVA-OneVision-7B | tr | patient_first | False | 176 | 0.0% | 100.0% |
| LLaVA-OneVision-7B | tr | patient_first | True | 176 | 100.0% | 0.0% |
