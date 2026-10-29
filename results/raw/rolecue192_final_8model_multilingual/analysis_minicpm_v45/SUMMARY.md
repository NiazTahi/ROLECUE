# Realistic-v2 multilingual pilot

All scores are collapsed across reversed A/B option mappings.

| Model | Task | Language | Order | n | Case accuracy | First-noun agreement | Option consistency |
|---|---|---|---|---:|---:|---:|---:|
| MiniCPM-V-4.5 | joint_match | bn | agent_first | 352 | 89.5% | 89.5% | 91.5% |
| MiniCPM-V-4.5 | joint_match | bn | patient_first | 352 | 10.8% | 70.5% | 81.2% |
| MiniCPM-V-4.5 | joint_match | de | agent_first | 352 | 98.3% | 98.3% | 98.6% |
| MiniCPM-V-4.5 | joint_match | de | patient_first | 352 | 6.8% | 86.6% | 93.5% |
| MiniCPM-V-4.5 | joint_match | en | agent_first | 352 | 99.7% | 99.7% | 100.0% |
| MiniCPM-V-4.5 | joint_match | en | patient_first | 352 | 95.2% | 1.1% | 96.3% |
| MiniCPM-V-4.5 | joint_match | ja | agent_first | 352 | 100.0% | 100.0% | 100.0% |
| MiniCPM-V-4.5 | joint_match | ja | patient_first | 352 | 76.1% | 9.1% | 85.2% |
| MiniCPM-V-4.5 | joint_match | ko | agent_first | 352 | 98.6% | 98.6% | 98.6% |
| MiniCPM-V-4.5 | joint_match | ko | patient_first | 352 | 72.2% | 12.5% | 84.7% |
| MiniCPM-V-4.5 | joint_match | tr | agent_first | 352 | 96.0% | 96.0% | 96.0% |
| MiniCPM-V-4.5 | joint_match | tr | patient_first | 352 | 6.0% | 85.8% | 91.8% |
| MiniCPM-V-4.5 | text_only | bn | agent_first | 352 | 95.7% | 95.7% | 95.7% |
| MiniCPM-V-4.5 | text_only | bn | patient_first | 352 | 12.5% | 52.6% | 65.1% |
| MiniCPM-V-4.5 | text_only | de | agent_first | 352 | 100.0% | 100.0% | 100.0% |
| MiniCPM-V-4.5 | text_only | de | patient_first | 352 | 15.6% | 58.2% | 73.9% |
| MiniCPM-V-4.5 | text_only | en | agent_first | 352 | 100.0% | 100.0% | 100.0% |
| MiniCPM-V-4.5 | text_only | en | patient_first | 352 | 11.4% | 28.7% | 40.1% |
| MiniCPM-V-4.5 | text_only | ja | agent_first | 352 | 93.2% | 93.2% | 93.2% |
| MiniCPM-V-4.5 | text_only | ja | patient_first | 352 | 41.8% | 0.0% | 41.8% |
| MiniCPM-V-4.5 | text_only | ko | agent_first | 352 | 92.3% | 92.3% | 92.3% |
| MiniCPM-V-4.5 | text_only | ko | patient_first | 352 | 41.5% | 0.9% | 42.3% |
| MiniCPM-V-4.5 | text_only | tr | agent_first | 352 | 100.0% | 100.0% | 100.0% |
| MiniCPM-V-4.5 | text_only | tr | patient_first | 352 | 1.4% | 54.8% | 56.2% |

## Joint match by ground-truth status

| Model | Language | Order | True match | n | Case accuracy | First-noun agreement |
|---|---|---|---:|---:|---:|---:|
| MiniCPM-V-4.5 | bn | agent_first | False | 176 | 79.0% | 79.0% |
| MiniCPM-V-4.5 | bn | agent_first | True | 176 | 100.0% | 100.0% |
| MiniCPM-V-4.5 | bn | patient_first | False | 176 | 0.0% | 100.0% |
| MiniCPM-V-4.5 | bn | patient_first | True | 176 | 21.6% | 40.9% |
| MiniCPM-V-4.5 | de | agent_first | False | 176 | 96.6% | 96.6% |
| MiniCPM-V-4.5 | de | agent_first | True | 176 | 100.0% | 100.0% |
| MiniCPM-V-4.5 | de | patient_first | False | 176 | 12.5% | 80.7% |
| MiniCPM-V-4.5 | de | patient_first | True | 176 | 1.1% | 92.6% |
| MiniCPM-V-4.5 | en | agent_first | False | 176 | 99.4% | 99.4% |
| MiniCPM-V-4.5 | en | agent_first | True | 176 | 100.0% | 100.0% |
| MiniCPM-V-4.5 | en | patient_first | False | 176 | 90.9% | 2.3% |
| MiniCPM-V-4.5 | en | patient_first | True | 176 | 99.4% | 0.0% |
| MiniCPM-V-4.5 | ja | agent_first | False | 176 | 100.0% | 100.0% |
| MiniCPM-V-4.5 | ja | agent_first | True | 176 | 100.0% | 100.0% |
| MiniCPM-V-4.5 | ja | patient_first | False | 176 | 52.3% | 18.2% |
| MiniCPM-V-4.5 | ja | patient_first | True | 176 | 100.0% | 0.0% |
| MiniCPM-V-4.5 | ko | agent_first | False | 176 | 97.2% | 97.2% |
| MiniCPM-V-4.5 | ko | agent_first | True | 176 | 100.0% | 100.0% |
| MiniCPM-V-4.5 | ko | patient_first | False | 176 | 50.6% | 23.9% |
| MiniCPM-V-4.5 | ko | patient_first | True | 176 | 93.8% | 1.1% |
| MiniCPM-V-4.5 | tr | agent_first | False | 176 | 97.7% | 97.7% |
| MiniCPM-V-4.5 | tr | agent_first | True | 176 | 94.3% | 94.3% |
| MiniCPM-V-4.5 | tr | patient_first | False | 176 | 10.8% | 76.7% |
| MiniCPM-V-4.5 | tr | patient_first | True | 176 | 1.1% | 94.9% |
