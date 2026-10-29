# Realistic-v2 multilingual pilot

All scores are collapsed across reversed A/B option mappings.

| Model | Task | Language | Order | n | Case accuracy | First-noun agreement | Option consistency |
|---|---|---|---|---:|---:|---:|---:|
| GPT-5.6-Luna | joint_match | bn | agent_first | 384 | 93.5% | 93.5% | 96.4% |
| GPT-5.6-Luna | joint_match | bn | patient_first | 384 | 91.7% | 3.1% | 94.8% |
| GPT-5.6-Luna | joint_match | de | agent_first | 192 | 86.5% | 86.5% | 90.6% |
| GPT-5.6-Luna | joint_match | de | patient_first | 192 | 86.5% | 4.7% | 91.1% |
| GPT-5.6-Luna | joint_match | en | agent_first | 384 | 93.0% | 93.0% | 97.7% |
| GPT-5.6-Luna | joint_match | en | patient_first | 384 | 95.8% | 1.3% | 97.1% |
| GPT-5.6-Luna | joint_match | ja | agent_first | 192 | 91.1% | 91.1% | 94.8% |
| GPT-5.6-Luna | joint_match | ja | patient_first | 192 | 89.1% | 2.6% | 91.7% |
| GPT-5.6-Luna | joint_match | ko | agent_first | 384 | 93.8% | 93.8% | 95.8% |
| GPT-5.6-Luna | joint_match | ko | patient_first | 384 | 93.5% | 2.1% | 95.6% |
| GPT-5.6-Luna | joint_match | tr | agent_first | 192 | 82.3% | 82.3% | 89.1% |
| GPT-5.6-Luna | joint_match | tr | patient_first | 192 | 83.9% | 8.3% | 92.2% |
| GPT-5.6-Luna | text_only | bn | agent_first | 384 | 99.7% | 99.7% | 99.7% |
| GPT-5.6-Luna | text_only | bn | patient_first | 384 | 79.7% | 0.0% | 79.7% |
| GPT-5.6-Luna | text_only | de | agent_first | 192 | 100.0% | 100.0% | 100.0% |
| GPT-5.6-Luna | text_only | de | patient_first | 192 | 78.1% | 0.0% | 78.1% |
| GPT-5.6-Luna | text_only | en | agent_first | 384 | 91.4% | 91.4% | 91.4% |
| GPT-5.6-Luna | text_only | en | patient_first | 384 | 54.9% | 0.0% | 54.9% |
| GPT-5.6-Luna | text_only | ja | agent_first | 192 | 76.6% | 76.6% | 76.6% |
| GPT-5.6-Luna | text_only | ja | patient_first | 192 | 99.0% | 0.0% | 99.0% |
| GPT-5.6-Luna | text_only | ko | agent_first | 384 | 95.8% | 95.8% | 95.8% |
| GPT-5.6-Luna | text_only | ko | patient_first | 384 | 86.7% | 0.0% | 86.7% |
| GPT-5.6-Luna | text_only | tr | agent_first | 192 | 87.0% | 87.0% | 87.0% |
| GPT-5.6-Luna | text_only | tr | patient_first | 192 | 85.9% | 0.0% | 85.9% |

## Joint match by ground-truth status

| Model | Language | Order | True match | n | Case accuracy | First-noun agreement |
|---|---|---|---:|---:|---:|---:|
| GPT-5.6-Luna | bn | agent_first | False | 192 | 95.8% | 95.8% |
| GPT-5.6-Luna | bn | agent_first | True | 192 | 91.1% | 91.1% |
| GPT-5.6-Luna | bn | patient_first | False | 192 | 88.5% | 4.2% |
| GPT-5.6-Luna | bn | patient_first | True | 192 | 94.8% | 2.1% |
| GPT-5.6-Luna | de | agent_first | False | 96 | 79.2% | 79.2% |
| GPT-5.6-Luna | de | agent_first | True | 96 | 93.8% | 93.8% |
| GPT-5.6-Luna | de | patient_first | False | 96 | 81.2% | 4.2% |
| GPT-5.6-Luna | de | patient_first | True | 96 | 91.7% | 5.2% |
| GPT-5.6-Luna | en | agent_first | False | 192 | 90.1% | 90.1% |
| GPT-5.6-Luna | en | agent_first | True | 192 | 95.8% | 95.8% |
| GPT-5.6-Luna | en | patient_first | False | 192 | 93.8% | 2.6% |
| GPT-5.6-Luna | en | patient_first | True | 192 | 97.9% | 0.0% |
| GPT-5.6-Luna | ja | agent_first | False | 96 | 88.5% | 88.5% |
| GPT-5.6-Luna | ja | agent_first | True | 96 | 93.8% | 93.8% |
| GPT-5.6-Luna | ja | patient_first | False | 96 | 83.3% | 5.2% |
| GPT-5.6-Luna | ja | patient_first | True | 96 | 94.8% | 0.0% |
| GPT-5.6-Luna | ko | agent_first | False | 192 | 96.4% | 96.4% |
| GPT-5.6-Luna | ko | agent_first | True | 192 | 91.1% | 91.1% |
| GPT-5.6-Luna | ko | patient_first | False | 192 | 91.7% | 3.1% |
| GPT-5.6-Luna | ko | patient_first | True | 192 | 95.3% | 1.0% |
| GPT-5.6-Luna | tr | agent_first | False | 96 | 74.0% | 74.0% |
| GPT-5.6-Luna | tr | agent_first | True | 96 | 90.6% | 90.6% |
| GPT-5.6-Luna | tr | patient_first | False | 96 | 74.0% | 13.5% |
| GPT-5.6-Luna | tr | patient_first | True | 96 | 93.8% | 3.1% |
