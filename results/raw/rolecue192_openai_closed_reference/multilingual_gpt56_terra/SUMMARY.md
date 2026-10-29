# Realistic-v2 multilingual pilot

All scores are collapsed across reversed A/B option mappings.

| Model | Task | Language | Order | n | Case accuracy | First-noun agreement | Option consistency |
|---|---|---|---|---:|---:|---:|---:|
| GPT-5.6-Terra | joint_match | bn | agent_first | 384 | 88.8% | 88.8% | 91.7% |
| GPT-5.6-Terra | joint_match | bn | patient_first | 384 | 95.1% | 1.3% | 96.4% |
| GPT-5.6-Terra | joint_match | de | agent_first | 192 | 96.9% | 96.9% | 96.9% |
| GPT-5.6-Terra | joint_match | de | patient_first | 192 | 95.8% | 1.6% | 97.4% |
| GPT-5.6-Terra | joint_match | en | agent_first | 384 | 99.7% | 99.7% | 99.7% |
| GPT-5.6-Terra | joint_match | en | patient_first | 384 | 99.7% | 0.0% | 99.7% |
| GPT-5.6-Terra | joint_match | ja | agent_first | 192 | 96.9% | 96.9% | 96.9% |
| GPT-5.6-Terra | joint_match | ja | patient_first | 192 | 94.8% | 0.0% | 94.8% |
| GPT-5.6-Terra | joint_match | ko | agent_first | 384 | 95.8% | 95.8% | 96.6% |
| GPT-5.6-Terra | joint_match | ko | patient_first | 384 | 87.5% | 1.6% | 89.1% |
| GPT-5.6-Terra | joint_match | tr | agent_first | 192 | 93.2% | 93.2% | 94.8% |
| GPT-5.6-Terra | joint_match | tr | patient_first | 192 | 89.1% | 2.1% | 91.1% |
| GPT-5.6-Terra | text_only | bn | agent_first | 384 | 100.0% | 100.0% | 100.0% |
| GPT-5.6-Terra | text_only | bn | patient_first | 384 | 93.5% | 0.0% | 93.5% |
| GPT-5.6-Terra | text_only | de | agent_first | 192 | 100.0% | 100.0% | 100.0% |
| GPT-5.6-Terra | text_only | de | patient_first | 192 | 95.8% | 0.0% | 95.8% |
| GPT-5.6-Terra | text_only | en | agent_first | 384 | 100.0% | 100.0% | 100.0% |
| GPT-5.6-Terra | text_only | en | patient_first | 384 | 65.9% | 0.0% | 65.9% |
| GPT-5.6-Terra | text_only | ja | agent_first | 192 | 100.0% | 100.0% | 100.0% |
| GPT-5.6-Terra | text_only | ja | patient_first | 192 | 75.5% | 0.0% | 75.5% |
| GPT-5.6-Terra | text_only | ko | agent_first | 384 | 98.4% | 98.4% | 98.4% |
| GPT-5.6-Terra | text_only | ko | patient_first | 384 | 89.6% | 0.0% | 89.6% |
| GPT-5.6-Terra | text_only | tr | agent_first | 192 | 100.0% | 100.0% | 100.0% |
| GPT-5.6-Terra | text_only | tr | patient_first | 192 | 77.1% | 0.0% | 77.1% |

## Joint match by ground-truth status

| Model | Language | Order | True match | n | Case accuracy | First-noun agreement |
|---|---|---|---:|---:|---:|---:|
| GPT-5.6-Terra | bn | agent_first | False | 192 | 85.4% | 85.4% |
| GPT-5.6-Terra | bn | agent_first | True | 192 | 92.2% | 92.2% |
| GPT-5.6-Terra | bn | patient_first | False | 192 | 97.9% | 0.0% |
| GPT-5.6-Terra | bn | patient_first | True | 192 | 92.2% | 2.6% |
| GPT-5.6-Terra | de | agent_first | False | 96 | 96.9% | 96.9% |
| GPT-5.6-Terra | de | agent_first | True | 96 | 96.9% | 96.9% |
| GPT-5.6-Terra | de | patient_first | False | 96 | 99.0% | 0.0% |
| GPT-5.6-Terra | de | patient_first | True | 96 | 92.7% | 3.1% |
| GPT-5.6-Terra | en | agent_first | False | 192 | 99.5% | 99.5% |
| GPT-5.6-Terra | en | agent_first | True | 192 | 100.0% | 100.0% |
| GPT-5.6-Terra | en | patient_first | False | 192 | 100.0% | 0.0% |
| GPT-5.6-Terra | en | patient_first | True | 192 | 99.5% | 0.0% |
| GPT-5.6-Terra | ja | agent_first | False | 96 | 94.8% | 94.8% |
| GPT-5.6-Terra | ja | agent_first | True | 96 | 99.0% | 99.0% |
| GPT-5.6-Terra | ja | patient_first | False | 96 | 89.6% | 0.0% |
| GPT-5.6-Terra | ja | patient_first | True | 96 | 100.0% | 0.0% |
| GPT-5.6-Terra | ko | agent_first | False | 192 | 99.5% | 99.5% |
| GPT-5.6-Terra | ko | agent_first | True | 192 | 92.2% | 92.2% |
| GPT-5.6-Terra | ko | patient_first | False | 192 | 82.8% | 2.1% |
| GPT-5.6-Terra | ko | patient_first | True | 192 | 92.2% | 1.0% |
| GPT-5.6-Terra | tr | agent_first | False | 96 | 90.6% | 90.6% |
| GPT-5.6-Terra | tr | agent_first | True | 96 | 95.8% | 95.8% |
| GPT-5.6-Terra | tr | patient_first | False | 96 | 78.1% | 4.2% |
| GPT-5.6-Terra | tr | patient_first | True | 96 | 100.0% | 0.0% |
