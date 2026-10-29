# Realistic-v2 multilingual pilot

All scores are collapsed across reversed A/B option mappings.

| Model | Task | Language | Order | n | Case accuracy | First-noun agreement | Option consistency |
|---|---|---|---|---:|---:|---:|---:|
| InternVL3.5-38B | joint_match | bn | agent_first | 384 | 93.0% | 93.0% | 97.1% |
| InternVL3.5-38B | joint_match | bn | patient_first | 384 | 90.1% | 9.9% | 94.8% |
| InternVL3.5-38B | joint_match | de | agent_first | 384 | 95.8% | 95.8% | 97.4% |
| InternVL3.5-38B | joint_match | de | patient_first | 384 | 96.9% | 3.1% | 95.3% |
| InternVL3.5-38B | joint_match | en | agent_first | 384 | 95.1% | 95.1% | 97.9% |
| InternVL3.5-38B | joint_match | en | patient_first | 384 | 97.1% | 2.9% | 95.6% |
| InternVL3.5-38B | joint_match | ja | agent_first | 384 | 95.3% | 95.3% | 98.2% |
| InternVL3.5-38B | joint_match | ja | patient_first | 384 | 96.1% | 3.9% | 98.2% |
| InternVL3.5-38B | joint_match | ko | agent_first | 384 | 94.5% | 94.5% | 97.9% |
| InternVL3.5-38B | joint_match | ko | patient_first | 384 | 98.2% | 1.8% | 96.6% |
| InternVL3.5-38B | joint_match | tr | agent_first | 384 | 89.3% | 89.3% | 94.5% |
| InternVL3.5-38B | joint_match | tr | patient_first | 384 | 95.3% | 4.7% | 95.1% |
| InternVL3.5-38B | text_only | bn | agent_first | 384 | 100.0% | 100.0% | 100.0% |
| InternVL3.5-38B | text_only | bn | patient_first | 384 | 100.0% | 0.0% | 37.5% |
| InternVL3.5-38B | text_only | de | agent_first | 384 | 100.0% | 100.0% | 100.0% |
| InternVL3.5-38B | text_only | de | patient_first | 384 | 100.0% | 0.0% | 18.8% |
| InternVL3.5-38B | text_only | en | agent_first | 384 | 100.0% | 100.0% | 100.0% |
| InternVL3.5-38B | text_only | en | patient_first | 384 | 100.0% | 0.0% | 0.0% |
| InternVL3.5-38B | text_only | ja | agent_first | 384 | 100.0% | 100.0% | 100.0% |
| InternVL3.5-38B | text_only | ja | patient_first | 384 | 100.0% | 0.0% | 87.5% |
| InternVL3.5-38B | text_only | ko | agent_first | 384 | 100.0% | 100.0% | 100.0% |
| InternVL3.5-38B | text_only | ko | patient_first | 384 | 100.0% | 0.0% | 41.7% |
| InternVL3.5-38B | text_only | tr | agent_first | 384 | 100.0% | 100.0% | 100.0% |
| InternVL3.5-38B | text_only | tr | patient_first | 384 | 100.0% | 0.0% | 4.2% |

## Joint match by ground-truth status

| Model | Language | Order | True match | n | Case accuracy | First-noun agreement |
|---|---|---|---:|---:|---:|---:|
| InternVL3.5-38B | bn | agent_first | False | 192 | 85.9% | 85.9% |
| InternVL3.5-38B | bn | agent_first | True | 192 | 100.0% | 100.0% |
| InternVL3.5-38B | bn | patient_first | False | 192 | 82.8% | 17.2% |
| InternVL3.5-38B | bn | patient_first | True | 192 | 97.4% | 2.6% |
| InternVL3.5-38B | de | agent_first | False | 192 | 91.7% | 91.7% |
| InternVL3.5-38B | de | agent_first | True | 192 | 100.0% | 100.0% |
| InternVL3.5-38B | de | patient_first | False | 192 | 96.4% | 3.6% |
| InternVL3.5-38B | de | patient_first | True | 192 | 97.4% | 2.6% |
| InternVL3.5-38B | en | agent_first | False | 192 | 91.1% | 91.1% |
| InternVL3.5-38B | en | agent_first | True | 192 | 99.0% | 99.0% |
| InternVL3.5-38B | en | patient_first | False | 192 | 100.0% | 0.0% |
| InternVL3.5-38B | en | patient_first | True | 192 | 94.3% | 5.7% |
| InternVL3.5-38B | ja | agent_first | False | 192 | 90.6% | 90.6% |
| InternVL3.5-38B | ja | agent_first | True | 192 | 100.0% | 100.0% |
| InternVL3.5-38B | ja | patient_first | False | 192 | 92.2% | 7.8% |
| InternVL3.5-38B | ja | patient_first | True | 192 | 100.0% | 0.0% |
| InternVL3.5-38B | ko | agent_first | False | 192 | 91.7% | 91.7% |
| InternVL3.5-38B | ko | agent_first | True | 192 | 97.4% | 97.4% |
| InternVL3.5-38B | ko | patient_first | False | 192 | 96.4% | 3.6% |
| InternVL3.5-38B | ko | patient_first | True | 192 | 100.0% | 0.0% |
| InternVL3.5-38B | tr | agent_first | False | 192 | 82.8% | 82.8% |
| InternVL3.5-38B | tr | agent_first | True | 192 | 95.8% | 95.8% |
| InternVL3.5-38B | tr | patient_first | False | 192 | 96.9% | 3.1% |
| InternVL3.5-38B | tr | patient_first | True | 192 | 93.8% | 6.2% |
