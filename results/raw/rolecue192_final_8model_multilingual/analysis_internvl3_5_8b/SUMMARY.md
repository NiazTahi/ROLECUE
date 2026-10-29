# Realistic-v2 multilingual pilot

All scores are collapsed across reversed A/B option mappings.

| Model | Task | Language | Order | n | Case accuracy | First-noun agreement | Option consistency |
|---|---|---|---|---:|---:|---:|---:|
| InternVL3.5-8B | joint_match | bn | agent_first | 352 | 56.5% | 56.5% | 91.8% |
| InternVL3.5-8B | joint_match | bn | patient_first | 352 | 55.7% | 44.3% | 89.5% |
| InternVL3.5-8B | joint_match | de | agent_first | 352 | 96.3% | 96.3% | 96.9% |
| InternVL3.5-8B | joint_match | de | patient_first | 352 | 59.4% | 40.6% | 77.6% |
| InternVL3.5-8B | joint_match | en | agent_first | 352 | 97.7% | 97.7% | 93.2% |
| InternVL3.5-8B | joint_match | en | patient_first | 352 | 93.5% | 6.5% | 92.3% |
| InternVL3.5-8B | joint_match | ja | agent_first | 352 | 81.8% | 81.8% | 92.6% |
| InternVL3.5-8B | joint_match | ja | patient_first | 352 | 54.5% | 45.5% | 86.4% |
| InternVL3.5-8B | joint_match | ko | agent_first | 352 | 89.5% | 89.5% | 85.8% |
| InternVL3.5-8B | joint_match | ko | patient_first | 352 | 68.2% | 31.8% | 86.1% |
| InternVL3.5-8B | joint_match | tr | agent_first | 352 | 56.2% | 56.2% | 77.6% |
| InternVL3.5-8B | joint_match | tr | patient_first | 352 | 46.6% | 53.4% | 83.2% |
| InternVL3.5-8B | text_only | bn | agent_first | 352 | 100.0% | 100.0% | 95.5% |
| InternVL3.5-8B | text_only | bn | patient_first | 352 | 45.5% | 54.5% | 63.6% |
| InternVL3.5-8B | text_only | de | agent_first | 352 | 100.0% | 100.0% | 100.0% |
| InternVL3.5-8B | text_only | de | patient_first | 352 | 59.1% | 40.9% | 22.7% |
| InternVL3.5-8B | text_only | en | agent_first | 352 | 100.0% | 100.0% | 100.0% |
| InternVL3.5-8B | text_only | en | patient_first | 352 | 36.4% | 63.6% | 27.3% |
| InternVL3.5-8B | text_only | ja | agent_first | 352 | 100.0% | 100.0% | 95.5% |
| InternVL3.5-8B | text_only | ja | patient_first | 352 | 100.0% | 0.0% | 100.0% |
| InternVL3.5-8B | text_only | ko | agent_first | 352 | 100.0% | 100.0% | 100.0% |
| InternVL3.5-8B | text_only | ko | patient_first | 352 | 95.5% | 4.5% | 18.2% |
| InternVL3.5-8B | text_only | tr | agent_first | 352 | 100.0% | 100.0% | 100.0% |
| InternVL3.5-8B | text_only | tr | patient_first | 352 | 54.5% | 45.5% | 18.2% |

## Joint match by ground-truth status

| Model | Language | Order | True match | n | Case accuracy | First-noun agreement |
|---|---|---|---:|---:|---:|---:|
| InternVL3.5-8B | bn | agent_first | False | 176 | 13.1% | 13.1% |
| InternVL3.5-8B | bn | agent_first | True | 176 | 100.0% | 100.0% |
| InternVL3.5-8B | bn | patient_first | False | 176 | 11.9% | 88.1% |
| InternVL3.5-8B | bn | patient_first | True | 176 | 99.4% | 0.6% |
| InternVL3.5-8B | de | agent_first | False | 176 | 93.8% | 93.8% |
| InternVL3.5-8B | de | agent_first | True | 176 | 98.9% | 98.9% |
| InternVL3.5-8B | de | patient_first | False | 176 | 67.6% | 32.4% |
| InternVL3.5-8B | de | patient_first | True | 176 | 51.1% | 48.9% |
| InternVL3.5-8B | en | agent_first | False | 176 | 95.5% | 95.5% |
| InternVL3.5-8B | en | agent_first | True | 176 | 100.0% | 100.0% |
| InternVL3.5-8B | en | patient_first | False | 176 | 88.1% | 11.9% |
| InternVL3.5-8B | en | patient_first | True | 176 | 98.9% | 1.1% |
| InternVL3.5-8B | ja | agent_first | False | 176 | 64.2% | 64.2% |
| InternVL3.5-8B | ja | agent_first | True | 176 | 99.4% | 99.4% |
| InternVL3.5-8B | ja | patient_first | False | 176 | 9.7% | 90.3% |
| InternVL3.5-8B | ja | patient_first | True | 176 | 99.4% | 0.6% |
| InternVL3.5-8B | ko | agent_first | False | 176 | 80.1% | 80.1% |
| InternVL3.5-8B | ko | agent_first | True | 176 | 98.9% | 98.9% |
| InternVL3.5-8B | ko | patient_first | False | 176 | 39.2% | 60.8% |
| InternVL3.5-8B | ko | patient_first | True | 176 | 97.2% | 2.8% |
| InternVL3.5-8B | tr | agent_first | False | 176 | 15.3% | 15.3% |
| InternVL3.5-8B | tr | agent_first | True | 176 | 97.2% | 97.2% |
| InternVL3.5-8B | tr | patient_first | False | 176 | 4.5% | 95.5% |
| InternVL3.5-8B | tr | patient_first | True | 176 | 88.6% | 11.4% |
