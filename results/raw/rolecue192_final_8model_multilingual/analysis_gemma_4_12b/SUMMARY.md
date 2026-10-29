# Realistic-v2 multilingual pilot

All scores are collapsed across reversed A/B option mappings.

| Model | Task | Language | Order | n | Case accuracy | First-noun agreement | Option consistency |
|---|---|---|---|---:|---:|---:|---:|
| Gemma-4-12B-it | joint_match | bn | agent_first | 384 | 94.0% | 94.0% | 99.0% |
| Gemma-4-12B-it | joint_match | bn | patient_first | 384 | 94.0% | 6.0% | 98.7% |
| Gemma-4-12B-it | joint_match | de | agent_first | 384 | 94.8% | 94.8% | 99.2% |
| Gemma-4-12B-it | joint_match | de | patient_first | 384 | 68.8% | 31.2% | 94.8% |
| Gemma-4-12B-it | joint_match | en | agent_first | 384 | 96.1% | 96.1% | 99.2% |
| Gemma-4-12B-it | joint_match | en | patient_first | 384 | 93.8% | 6.2% | 92.7% |
| Gemma-4-12B-it | joint_match | ja | agent_first | 384 | 93.2% | 93.2% | 96.4% |
| Gemma-4-12B-it | joint_match | ja | patient_first | 384 | 93.2% | 6.8% | 93.5% |
| Gemma-4-12B-it | joint_match | ko | agent_first | 384 | 92.7% | 92.7% | 97.7% |
| Gemma-4-12B-it | joint_match | ko | patient_first | 384 | 94.3% | 5.7% | 96.1% |
| Gemma-4-12B-it | joint_match | tr | agent_first | 384 | 94.3% | 94.3% | 98.7% |
| Gemma-4-12B-it | joint_match | tr | patient_first | 384 | 94.0% | 6.0% | 97.7% |
| Gemma-4-12B-it | text_only | bn | agent_first | 384 | 100.0% | 100.0% | 100.0% |
| Gemma-4-12B-it | text_only | bn | patient_first | 384 | 100.0% | 0.0% | 100.0% |
| Gemma-4-12B-it | text_only | de | agent_first | 384 | 100.0% | 100.0% | 100.0% |
| Gemma-4-12B-it | text_only | de | patient_first | 384 | 87.5% | 12.5% | 95.8% |
| Gemma-4-12B-it | text_only | en | agent_first | 384 | 100.0% | 100.0% | 100.0% |
| Gemma-4-12B-it | text_only | en | patient_first | 384 | 87.5% | 12.5% | 25.0% |
| Gemma-4-12B-it | text_only | ja | agent_first | 384 | 54.2% | 54.2% | 58.3% |
| Gemma-4-12B-it | text_only | ja | patient_first | 384 | 70.8% | 29.2% | 75.0% |
| Gemma-4-12B-it | text_only | ko | agent_first | 384 | 100.0% | 100.0% | 100.0% |
| Gemma-4-12B-it | text_only | ko | patient_first | 384 | 100.0% | 0.0% | 100.0% |
| Gemma-4-12B-it | text_only | tr | agent_first | 384 | 100.0% | 100.0% | 100.0% |
| Gemma-4-12B-it | text_only | tr | patient_first | 384 | 100.0% | 0.0% | 100.0% |

## Joint match by ground-truth status

| Model | Language | Order | True match | n | Case accuracy | First-noun agreement |
|---|---|---|---:|---:|---:|---:|
| Gemma-4-12B-it | bn | agent_first | False | 192 | 100.0% | 100.0% |
| Gemma-4-12B-it | bn | agent_first | True | 192 | 88.0% | 88.0% |
| Gemma-4-12B-it | bn | patient_first | False | 192 | 99.5% | 0.5% |
| Gemma-4-12B-it | bn | patient_first | True | 192 | 88.5% | 11.5% |
| Gemma-4-12B-it | de | agent_first | False | 192 | 100.0% | 100.0% |
| Gemma-4-12B-it | de | agent_first | True | 192 | 89.6% | 89.6% |
| Gemma-4-12B-it | de | patient_first | False | 192 | 88.5% | 11.5% |
| Gemma-4-12B-it | de | patient_first | True | 192 | 49.0% | 51.0% |
| Gemma-4-12B-it | en | agent_first | False | 192 | 100.0% | 100.0% |
| Gemma-4-12B-it | en | agent_first | True | 192 | 92.2% | 92.2% |
| Gemma-4-12B-it | en | patient_first | False | 192 | 95.3% | 4.7% |
| Gemma-4-12B-it | en | patient_first | True | 192 | 92.2% | 7.8% |
| Gemma-4-12B-it | ja | agent_first | False | 192 | 96.9% | 96.9% |
| Gemma-4-12B-it | ja | agent_first | True | 192 | 89.6% | 89.6% |
| Gemma-4-12B-it | ja | patient_first | False | 192 | 94.8% | 5.2% |
| Gemma-4-12B-it | ja | patient_first | True | 192 | 91.7% | 8.3% |
| Gemma-4-12B-it | ko | agent_first | False | 192 | 99.5% | 99.5% |
| Gemma-4-12B-it | ko | agent_first | True | 192 | 85.9% | 85.9% |
| Gemma-4-12B-it | ko | patient_first | False | 192 | 95.8% | 4.2% |
| Gemma-4-12B-it | ko | patient_first | True | 192 | 92.7% | 7.3% |
| Gemma-4-12B-it | tr | agent_first | False | 192 | 100.0% | 100.0% |
| Gemma-4-12B-it | tr | agent_first | True | 192 | 88.5% | 88.5% |
| Gemma-4-12B-it | tr | patient_first | False | 192 | 96.4% | 3.6% |
| Gemma-4-12B-it | tr | patient_first | True | 192 | 91.7% | 8.3% |
