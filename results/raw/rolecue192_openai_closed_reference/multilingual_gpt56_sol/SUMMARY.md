# Realistic-v2 multilingual pilot

All scores are collapsed across reversed A/B option mappings.

| Model | Task | Language | Order | n | Case accuracy | First-noun agreement | Option consistency |
|---|---|---|---|---:|---:|---:|---:|
| GPT-5.6-Sol | joint_match | bn | agent_first | 384 | 95.8% | 95.8% | 100.0% |
| GPT-5.6-Sol | joint_match | bn | patient_first | 384 | 95.8% | 4.2% | 100.0% |
| GPT-5.6-Sol | joint_match | de | agent_first | 192 | 99.5% | 99.5% | 99.5% |
| GPT-5.6-Sol | joint_match | de | patient_first | 192 | 100.0% | 0.0% | 100.0% |
| GPT-5.6-Sol | joint_match | en | agent_first | 384 | 100.0% | 100.0% | 100.0% |
| GPT-5.6-Sol | joint_match | en | patient_first | 384 | 100.0% | 0.0% | 100.0% |
| GPT-5.6-Sol | joint_match | ja | agent_first | 192 | 99.0% | 99.0% | 99.0% |
| GPT-5.6-Sol | joint_match | ja | patient_first | 192 | 100.0% | 0.0% | 100.0% |
| GPT-5.6-Sol | joint_match | ko | agent_first | 384 | 95.3% | 95.3% | 98.7% |
| GPT-5.6-Sol | joint_match | ko | patient_first | 384 | 95.8% | 2.1% | 97.9% |
| GPT-5.6-Sol | joint_match | tr | agent_first | 192 | 98.4% | 98.4% | 99.0% |
| GPT-5.6-Sol | joint_match | tr | patient_first | 192 | 95.3% | 0.5% | 95.8% |
| GPT-5.6-Sol | text_only | bn | agent_first | 384 | 79.4% | 79.4% | 79.4% |
| GPT-5.6-Sol | text_only | bn | patient_first | 384 | 96.4% | 0.0% | 96.4% |
| GPT-5.6-Sol | text_only | de | agent_first | 192 | 76.6% | 76.6% | 76.6% |
| GPT-5.6-Sol | text_only | de | patient_first | 192 | 99.5% | 0.0% | 99.5% |
| GPT-5.6-Sol | text_only | en | agent_first | 384 | 51.6% | 51.6% | 51.6% |
| GPT-5.6-Sol | text_only | en | patient_first | 384 | 64.8% | 0.0% | 64.8% |
| GPT-5.6-Sol | text_only | ja | agent_first | 192 | 93.2% | 93.2% | 93.2% |
| GPT-5.6-Sol | text_only | ja | patient_first | 192 | 96.4% | 0.0% | 96.4% |
| GPT-5.6-Sol | text_only | ko | agent_first | 384 | 79.2% | 79.2% | 79.2% |
| GPT-5.6-Sol | text_only | ko | patient_first | 384 | 98.7% | 0.0% | 98.7% |
| GPT-5.6-Sol | text_only | tr | agent_first | 192 | 94.3% | 94.3% | 94.3% |
| GPT-5.6-Sol | text_only | tr | patient_first | 192 | 76.6% | 0.0% | 76.6% |

## Joint match by ground-truth status

| Model | Language | Order | True match | n | Case accuracy | First-noun agreement |
|---|---|---|---:|---:|---:|---:|
| GPT-5.6-Sol | bn | agent_first | False | 192 | 100.0% | 100.0% |
| GPT-5.6-Sol | bn | agent_first | True | 192 | 91.7% | 91.7% |
| GPT-5.6-Sol | bn | patient_first | False | 192 | 100.0% | 0.0% |
| GPT-5.6-Sol | bn | patient_first | True | 192 | 91.7% | 8.3% |
| GPT-5.6-Sol | de | agent_first | False | 96 | 100.0% | 100.0% |
| GPT-5.6-Sol | de | agent_first | True | 96 | 99.0% | 99.0% |
| GPT-5.6-Sol | de | patient_first | False | 96 | 100.0% | 0.0% |
| GPT-5.6-Sol | de | patient_first | True | 96 | 100.0% | 0.0% |
| GPT-5.6-Sol | en | agent_first | False | 192 | 100.0% | 100.0% |
| GPT-5.6-Sol | en | agent_first | True | 192 | 100.0% | 100.0% |
| GPT-5.6-Sol | en | patient_first | False | 192 | 100.0% | 0.0% |
| GPT-5.6-Sol | en | patient_first | True | 192 | 100.0% | 0.0% |
| GPT-5.6-Sol | ja | agent_first | False | 96 | 100.0% | 100.0% |
| GPT-5.6-Sol | ja | agent_first | True | 96 | 97.9% | 97.9% |
| GPT-5.6-Sol | ja | patient_first | False | 96 | 100.0% | 0.0% |
| GPT-5.6-Sol | ja | patient_first | True | 96 | 100.0% | 0.0% |
| GPT-5.6-Sol | ko | agent_first | False | 192 | 100.0% | 100.0% |
| GPT-5.6-Sol | ko | agent_first | True | 192 | 90.6% | 90.6% |
| GPT-5.6-Sol | ko | patient_first | False | 192 | 99.0% | 1.0% |
| GPT-5.6-Sol | ko | patient_first | True | 192 | 92.7% | 3.1% |
| GPT-5.6-Sol | tr | agent_first | False | 96 | 100.0% | 100.0% |
| GPT-5.6-Sol | tr | agent_first | True | 96 | 96.9% | 96.9% |
| GPT-5.6-Sol | tr | patient_first | False | 96 | 94.8% | 1.0% |
| GPT-5.6-Sol | tr | patient_first | True | 96 | 95.8% | 0.0% |
