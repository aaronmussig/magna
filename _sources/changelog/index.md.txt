## [3.0.1](https://github.com/aaronmussig/magna/compare/v3.0.0...v3.0.1) (2022-05-10)


### Bug Fixes

* **ncbi.web.get_ncbi_assembly_id:** Ensure that the correct ID is returned. ([a2d88f5](https://github.com/aaronmussig/magna/commit/a2d88f55be49d26f1657d0b89808ecbdb9a9b5a2))

# [3.0.0](https://github.com/aaronmussig/magna/compare/v2.8.0...v3.0.0) (2022-05-10)


### Features

* **3.0.0:** Docs / Refactor / NCBI / CLI ([71df0e5](https://github.com/aaronmussig/magna/commit/71df0e5245a3956763a28ea832971c136a90f264))


### BREAKING CHANGES

* **3.0.0:** Refactored util.io -> util.web

# [2.8.0](https://github.com/aaronmussig/magna/compare/v2.7.1...v2.8.0) (2022-05-07)


### Features

* **PFAM/TIGRFAM:** Add TopHit file. ([eff81d2](https://github.com/aaronmussig/magna/commit/eff81d26f8f4490ac8db11e319444b05d68c973b))

## [2.7.1](https://github.com/aaronmussig/magna/compare/v2.7.0...v2.7.1) (2022-05-05)


### Bug Fixes

* **PFAM/TIGRFAM:** Adjust columns in tophit file, fix data type. ([c63fc52](https://github.com/aaronmussig/magna/commit/c63fc52b08a37dc3a9618a8d7254e4c292dada4a))

# [2.7.0](https://github.com/aaronmussig/magna/compare/v2.6.2...v2.7.0) (2022-05-04)


### Bug Fixes

* **util.pandas.optimise_df:** Remove error if integer data type cannot be matched. ([34daffd](https://github.com/aaronmussig/magna/commit/34daffd62321f182ed47f6916f7aee0123094e69))


### Features

* **PFAM/TIGRFAM:** Include a set containing markers at specific releases. ([62387d7](https://github.com/aaronmussig/magna/commit/62387d7f91919f199e79fada2a333572773df5a9))

## [2.6.2](https://github.com/aaronmussig/magna/compare/v2.6.1...v2.6.2) (2022-04-17)


### Bug Fixes

* **util.pandas.optimise_df:** Stricter processing for float data types. ([3f4aadb](https://github.com/aaronmussig/magna/commit/3f4aadb0223db133471b916179afb26af3f91837))

## [2.6.1](https://github.com/aaronmussig/magna/compare/v2.6.0...v2.6.1) (2022-04-17)


### Bug Fixes

* **util.pandas.optimise_df:** Stricter processing for unsigned data types. ([64063ff](https://github.com/aaronmussig/magna/commit/64063ff41b1a20163501d144e3ab6cbe87b295e3))

# [2.6.0](https://github.com/aaronmussig/magna/compare/v2.5.1...v2.6.0) (2022-04-15)


### Features

* **util.pandas:** Add optimise_df to reduce dataframe size. ([706baff](https://github.com/aaronmussig/magna/commit/706bafff248f6a6ad708cee546f9bbffa61897ed))

## [2.5.1](https://github.com/aaronmussig/magna/compare/v2.5.0...v2.5.1) (2022-04-11)


### Bug Fixes

* **tree:** Force rd=False. ([67087e6](https://github.com/aaronmussig/magna/commit/67087e60cb1f030364c2aea328671b802ad813ca))

# [2.5.0](https://github.com/aaronmussig/magna/compare/v2.4.1...v2.5.0) (2022-04-11)


### Features

* **tree:** Add distance matrix to newick conversion method. ([9146bbb](https://github.com/aaronmussig/magna/commit/9146bbbcb13151b1860d19c2a17591a07da070ef))

## [2.4.1](https://github.com/aaronmussig/magna/compare/v2.4.0...v2.4.1) (2022-03-29)


### Bug Fixes

* **gunc:** Fixed path to feather for concatenated assignment file. ([5f48c1b](https://github.com/aaronmussig/magna/commit/5f48c1b18ebe7a452307a2d1bdcce5afc035a920))

# [2.4.0](https://github.com/aaronmussig/magna/compare/v2.3.0...v2.4.0) (2022-03-29)


### Features

* **gtdb markers:** Added sets of BAC120/AR53/AR122 markers. ([30e66c3](https://github.com/aaronmussig/magna/commit/30e66c313b1dcb2073d8a35489c24b5279952c28))
* **gunc:** Add method to parse contig_assignments file. ([625c597](https://github.com/aaronmussig/magna/commit/625c59766488d16d48eeae10ed1e236bc78abdeb))
* **pfam/tigrfam:** Add PFAM/TIGRFAM output parsers. ([35c0755](https://github.com/aaronmussig/magna/commit/35c0755cecf602bc5ea4d66299e943bcc2befaf9))

# [2.3.0](https://github.com/aaronmussig/magna/compare/v2.2.0...v2.3.0) (2022-03-29)


### Features

* **diamond:** Added diamond file handler. ([6dd18a5](https://github.com/aaronmussig/magna/commit/6dd18a59ff95df6de5210e4d5150734f76ad194b))

# [2.2.0](https://github.com/aaronmussig/magna/compare/v2.1.1...v2.2.0) (2022-03-17)


### Features

* **gunc:** Updated GUNC paths. ([8306b31](https://github.com/aaronmussig/magna/commit/8306b318f7a5db7ce21e6ac3b091e270c2d433c0))

## [2.1.1](https://github.com/aaronmussig/magna/compare/v2.1.0...v2.1.1) (2022-03-11)


### Bug Fixes

* **gunc:** TSV extension instead of feather for gunc file. ([5d0e84f](https://github.com/aaronmussig/magna/commit/5d0e84fb1e9bd783e3e5e0bbca4506af887c5a80))

# [2.1.0](https://github.com/aaronmussig/magna/compare/v2.0.0...v2.1.0) (2022-03-11)


### Features

* **io:** Added copy_file, and move_file. ([dd9f776](https://github.com/aaronmussig/magna/commit/dd9f77630dadfa5c5ec09f9e757e2d934d12b011))


# [2.0.0](https://github.com/aaronmussig/magna/compare/v1.4.0...v2.0.0) (2022-03-10)


### Bug Fixes

* **GTDB Tree:** Added option to force underscores. ([8c87e70](https://github.com/aaronmussig/magna/commit/8c87e70c8243d5ef4fda710d9fecd380ba3b5760))


### Features

* **GUNC:** Added GTDB R95 dataset methods. ([aff82f6](https://github.com/aaronmussig/magna/commit/aff82f65eca0a4224a36bb647598ba1c4915ecd5))
* Refactored code, added CI for docs. ([e891e84](https://github.com/aaronmussig/magna/commit/e891e84045e30a00037dcfed9a1e818a5aab13d1))


### BREAKING CHANGES

* Re-organised folder structure.

# [1.4.0](https://github.com/aaronmussig/magna/compare/v1.3.0...v1.4.0) (2022-02-18)


### Features

* **gtdb:** Added GTDB trees. ([08ba91c](https://github.com/aaronmussig/magna/commit/08ba91ce793b23603fcc863651901a65f05ba8fa))

# [1.3.0](https://github.com/aaronmussig/magna/compare/v1.2.0...v1.3.0) (2022-02-17)


### Features

* **gunc:** Updated GUNC dataset for MAXCss ([ffaf645](https://github.com/aaronmussig/magna/commit/ffaf645f7564dce73b9f5bbec389934a286be1b8))

# [1.2.0](https://github.com/aaronmussig/magna/compare/v1.1.0...v1.2.0) (2022-02-16)


### Features

* **accession:** Add canonical_gid function. ([95067ca](https://github.com/aaronmussig/magna/commit/95067ca2b09fa4506915ea1d214ce203df571fe4))

# [1.1.0](https://github.com/aaronmussig/magna/compare/v1.0.3...v1.1.0) (2022-02-16)


### Features

* **GTDB:** Add R202 and Genome. ([31e5bc3](https://github.com/aaronmussig/magna/commit/31e5bc361a0c2839adac97cb41deb89998907611))

## [1.0.3](https://github.com/aaronmussig/magna/compare/v1.0.2...v1.0.3) (2022-02-02)


### Bug Fixes

* **datasets:** Reduced the gunc dataset to just RefSeq/GenBank genomes. ([d432765](https://github.com/aaronmussig/magna/commit/d43276556658ffae56d756b2c5e629d3efe46e9b))

## [1.0.2](https://github.com/aaronmussig/magna/compare/v1.0.1...v1.0.2) (2022-02-02)


### Bug Fixes

* **datasets:** Updated the GTDB R95 bac source. ([d74eccf](https://github.com/aaronmussig/magna/commit/d74eccf03e949c8798df9b0a09f23f3d76ebfc56))

## [1.0.1](https://github.com/aaronmussig/magna/compare/v1.0.0...v1.0.1) (2022-02-02)


### Performance Improvements

* **dataset:** Updated GTDB/GUNC to use feather file format. ([90fe0fd](https://github.com/aaronmussig/magna/commit/90fe0fdcfab3021002d51005d6d4c77b73018043))

# 1.0.0 (2022-02-02)


### Features

* **dataset:** Added GTDBR95 metadata, and GUNC data. ([1755414](https://github.com/aaronmussig/magna/commit/17554142b6b2a29f1b5899f31f014f8fb0c28428))

# 1.0.0 (2021-11-08)


### Features

* Trigger release ([6435c4f](https://github.com/aaronmussig/magna/commit/6435c4ff9d21192ae3dfff20023e9a996423da2b))
