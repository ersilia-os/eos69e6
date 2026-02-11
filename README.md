# Pharmacophore-guided molecular generation

Based on a molecules pharmacophore, this model generates new molecules de-novo to match the pharmacophore.
Internally, pharmacophore hypotheses are generated for a given ligand.
A graph neural network encodes spatially distributed chemical features and a transformer decoder generates molecules.

This model was incorporated on 2023-12-01.


## Information
### Identifiers
- **Ersilia Identifier:** `eos69e6`
- **Slug:** `pgmg-pharmacophore`

### Domain
- **Task:** `Sampling`
- **Subtask:** `Generation`
- **Biomedical Area:** `Any`
- **Target Organism:** `Any`
- **Tags:** `Chemical graph model`, `Compound generation`

### Input
- **Input:** `Compound`
- **Input Dimension:** `1`

### Output
- **Output Dimension:** `100`
- **Output Consistency:** `Variable`
- **Interpretation:** New molecules generated based on the pharmacophore

Below are the **Output Columns** of the model:
| Name | Type | Direction | Description |
|------|------|-----------|-------------|
| smiles_0000 | string |  | Generated molecule index 0 using the pharmacophore-guided molecular generation (PGMG) model |
| smiles_0001 | string |  | Generated molecule index 1 using the pharmacophore-guided molecular generation (PGMG) model |
| smiles_0002 | string |  | Generated molecule index 2 using the pharmacophore-guided molecular generation (PGMG) model |
| smiles_0003 | string |  | Generated molecule index 3 using the pharmacophore-guided molecular generation (PGMG) model |
| smiles_0004 | string |  | Generated molecule index 4 using the pharmacophore-guided molecular generation (PGMG) model |
| smiles_0005 | string |  | Generated molecule index 5 using the pharmacophore-guided molecular generation (PGMG) model |
| smiles_0006 | string |  | Generated molecule index 6 using the pharmacophore-guided molecular generation (PGMG) model |
| smiles_0007 | string |  | Generated molecule index 7 using the pharmacophore-guided molecular generation (PGMG) model |
| smiles_0008 | string |  | Generated molecule index 8 using the pharmacophore-guided molecular generation (PGMG) model |
| smiles_0009 | string |  | Generated molecule index 9 using the pharmacophore-guided molecular generation (PGMG) model |

_10 of 1000 columns are shown_
### Source and Deployment
- **Source:** `Local`
- **Source Type:** `External`
- **DockerHub**: [https://hub.docker.com/r/ersiliaos/eos69e6](https://hub.docker.com/r/ersiliaos/eos69e6)
- **Docker Architecture:** `AMD64`
- **S3 Storage**: [https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos69e6.zip](https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos69e6.zip)

### Resource Consumption


### References
- **Source Code**: [https://github.com/CSUBioGroup/PGMG](https://github.com/CSUBioGroup/PGMG)
- **Publication**: [https://www.nature.com/articles/s41467-023-41454-9](https://www.nature.com/articles/s41467-023-41454-9)
- **Publication Type:** `Peer reviewed`
- **Publication Year:** `2023`
- **Ersilia Contributor:** [miquelduranfrigola](https://github.com/miquelduranfrigola)

### License
This package is licensed under a [GPL-3.0](https://github.com/ersilia-os/ersilia/blob/master/LICENSE) license. The model contained within this package is licensed under a [MIT](LICENSE) license.

**Notice**: Ersilia grants access to models _as is_, directly from the original authors, please refer to the original code repository and/or publication if you use the model in your research.


## Use
To use this model locally, you need to have the [Ersilia CLI](https://github.com/ersilia-os/ersilia) installed.
The model can be **fetched** using the following command:
```bash
# fetch model from the Ersilia Model Hub
ersilia fetch eos69e6
```
Then, you can **serve**, **run** and **close** the model as follows:
```bash
# serve the model
ersilia serve eos69e6
# generate an example file
ersilia example -n 3 -f my_input.csv
# run the model
ersilia run -i my_input.csv -o my_output.csv
# close the model
ersilia close
```

## About Ersilia
The [Ersilia Open Source Initiative](https://ersilia.io) is a tech non-profit organization fueling sustainable research in the Global South.
Please [cite](https://github.com/ersilia-os/ersilia/blob/master/CITATION.cff) the Ersilia Model Hub if you've found this model to be useful. Always [let us know](https://github.com/ersilia-os/ersilia/issues) if you experience any issues while trying to run it.
If you want to contribute to our mission, consider [donating](https://www.ersilia.io/donate) to Ersilia!
