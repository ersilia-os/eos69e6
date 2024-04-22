# Pharmacophore-guided molecular generation

Based on a molecule's pharmacophore, this model generates new molecules de-novo to match the pharmacophore. Internally, pharmacophore hypotheses are generated for a given ligand. A graph neural network encodes spatially distributed chemical features and a transformer decoder generates molecules.

## Identifiers

* EOS model ID: `eos69e6`
* Slug: `pgmg-pharmacophore-generative`

## Characteristics

* Input: `Compound`
* Input Shape: `Single`
* Task: `Generative`
* Output: `Compound`
* Output Type: `String`
* Output Shape: `List`
* Interpretation: Model generates new molecules from input molecule by first creating pharmacophore hypotheses and then constraining generation.

## References

* [Publication](https://www.nature.com/articles/s41467-023-41454-9)
* [Source Code](https://github.com/CSUBioGroup/PGMG)
* Ersilia contributor: [miquelduranfrigola](https://github.com/miquelduranfrigola)

## Ersilia model URLs
* [GitHub](https://github.com/ersilia-os/eos69e6)

## Citation

If you use this model, please cite the [original authors](https://www.nature.com/articles/s41467-023-41454-9) of the model and the [Ersilia Model Hub](https://github.com/ersilia-os/ersilia/blob/master/CITATION.cff).

## License

This package is licensed under a GPL-3.0 license. The model contained within this package is licensed under a MIT license.

Notice: Ersilia grants access to these models 'as is' provided by the original authors, please refer to the original code repository and/or publication if you use the model in your research.

## About Us

The [Ersilia Open Source Initiative](https://ersilia.io) is a Non Profit Organization ([1192266](https://register-of-charities.charitycommission.gov.uk/charity-search/-/charity-details/5170657/full-print)) with the mission is to equip labs, universities and clinics in LMIC with AI/ML tools for infectious disease research.

[Help us](https://www.ersilia.io/donate) achieve our mission!