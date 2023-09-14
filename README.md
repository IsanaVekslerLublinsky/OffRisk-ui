# OffRisk UI
OffRisk UI is running with the server OffRisk, and both need to be on the same network
To create the network:
~~~
docker network create off-risk-net
~~~



## gRNA input page

![grna_page_explanatory](https://github.com/gili311/OffRisk-ui/assets/17099695/ba1d9af8-023a-478b-9459-32d2bb42afce)

### Server and Databases section
1. Navigation: This section provides a navigation tool in the form of a navbar to access various tools within the off-risk-ui.
2. Server Configuration: Users have the option to specify a server name. 
   - If you intend to use the Docker version of the off-risk-server, it should be kept local.
   - Alternatively, you can create a custom server.
3. A list of databases that can be used for annotations is provided.</br>
Supported databases include: ["GENCODE", "MirGeneDB", "ReMapEPD", "EnhancerAtlas 2.0", "Pfam", "TargetScan 8.0", "OMIM", "HumanTF 3.0", "Protein Atlas", "RBP", "COSMIC"].
### Search Tool Section
4. Search tool for detecting off-targets. Supported search tools include:
   - FlashFry - Allows 20nts sequence length with NGG pam downstream only. without bulges.
   the FlashFry output will also provide score for the guid in the output section.
   - Cas-Offinder
   - CRISPRitz
### gRNA Section
In this section you configure the gRNA sequence to search for potential targets in the genome.
this section allow two types of search. Single search **or** Batch search.
#### Single search
5. The gRNA pam, (NGG, NNN, TTTN, etc.)

   Following codes are supported (as described in [Cas-Offinder repository](https://github.com/snugel/cas-offinder/tree/2.4.1) ):

<div align="center">

|   A   |    C   |   G   |   T   |
|:-----:|:------:|:-----:|:-----:|
|Adenine|Cytosine|Guanine|Thymine|

|   R  |   Y  |   S  |   W  |   K  |   M  |
|:----:|:----:|:----:|:----:|:----:|:----:|
|A or G|C or T|G or C|A or T|G or T|A or C|

|     B     |     D     |     H     |     V     |   N    |
|:---------:|:---------:|:---------:|:---------:|:------:|
|C or G or T|A or G or T|A or C or T|A or C or G|any base|

</div>

6. Where the guid is located
   - Downstream - At the end of the sequence
   - Upstream - At the beginning of the sequence
7. The amount of the DNA bugles
8. The amount of the RNA bugles
9. The gRNA Sequence
10. The maximum number of mismatches allowed.

#### Batch search
11. The off-risk-ui allow to use a Batch search to search for multiple gRNA targets.
to allow it a json file need to be provided describing the search parameters.
more details about the json file can be found in the off-risk-server github.


for example:
```json
{
  "request_id": 456,
  "pam": "NGG",
  "downstream": true,
  "pattern_dna_bulge": 0,
  "pattern_rna_bulge": 0,
  "sites": [
    {
      "sequence": "GGAGAATGACGAGTGGACCC",
      "mismatch": 4
    },
    {
      "sequence": "CACCCGATCCACTGGGGAGC",
      "mismatch": 3
    }
  ],
  "db_list": ["all"],
  "search_tools": ["crispritz"]
}
```

12. Run button
    
## Off-target page

![off_target_page_explanatory](https://github.com/gili311/OffRisk-ui/assets/17099695/e22dc7e4-d376-4690-aa18-f526e6e0df17)

### Server and Databases section
1. Navbar to navigate between off-risk-ui tools
2. Server name input:
   - For using the docker version of the off-risk-server keep it local
   - The off-risk-ui also provide a custom server option in case you decided to create one.
3. A list of supported databases to search in for annotations.
Supported databases include: ["GENCODE", "MirGeneDB", "ReMapEPD", "EnhancerAtlas 2.0", "Pfam", "TargetScan 8.0", "OMIM", "HumanTF 3.0", "Protein Atlas", "RBP", "COSMIC"].
### gRNA Section
In this section you configure the gRNA sequences to annotate in the genome.
this section allow two types inputs.

4. Tsv file where each row contains the bellow details about the guid target sequence:
   - 1st column for the **chromosome** of the target sequence
   - 2nd column for the **start** location of the target sequence
   - 3rd column for the **end** location of the target sequence
   - 4th column for the **strand** of the target sequence

   for example:

<div align="center">

| <!-- -->    | <!-- -->     | <!-- -->     | <!-- -->   |
|:-----------:|:------------:|:------------:|:----------:|
|      1      |   4888228    |   4888251    |     -      |
|      2      |   38211467   |   38211490   |     +      |
|     20      |   21476782   |   21476805   |     +      |
|     14      |   22547572   |   22547595   |     -      |
|      X      |  152319010   |  152319033   |     +      |
|     10      |   21110550   |   21110573   |     -      |

</div>

5. Free text file where each row contains the bellow details about the guid target sequence, seperated by space:
   - 1st column for the **chromosome** of the target sequence
   - 2nd column for the **start** location of the target sequence
   - 3rd column for the **end** location of the target sequence
   - 4th column for the **strand** of the target sequence
      
   for example:
     
    ```
      1 4888228 4888251 - 
      2 38211467 38211490 +
      20 21476782 21476805 +
      14 22547572 22547595 -
      X 152319010 152319033 + 
      10 21110550 21110573 -
    ```


6. Run button



### Output section

For both the **gRNA input page** and the **Off-target page**, once the search tools have completed their operation, tables containing information regarding the off-targets will be displayed below.</br>
*Sample output instances are accessible within the example folder within this repository for reference.*


#### FlashFry Score Summary
In case FlashFry included in the search tool a score table with the following scoring algorithms, *doench2014ontarget, doench2016cfd, dangerous, hsu2013, minot*,  will be displayed as well.
more information about FlashFry scoring can be found in [FlashFry repository](https://github.com/mckennalab/FlashFry/wiki/Site-scoring#scoring-methods).


#### Off-targets Summary

An overview encompassing the off-targets and their corresponding annotations retrieved from the databases.

- **(column 1) - Off Target ID**: A unique identifier or reference for the off-target site being analyzed. This could be a numerical or alphanumeric identifier.
- **(column 2) - crRNA**: Short for "CRISPR RNA," it represents the guide RNA sequence used in a CRISPR-Cas9 gene editing experiment. This sequence guides the Cas9 protein to the target DNA.
- **(column 3) - DNA**: The DNA sequence that is the subject of the study or analysis. It could be the target DNA that the crRNA is designed to bind to or modify.
- **(column 4) - Chromosome**: The specific chromosome on which the DNA sequence is located.
- **(column 5) - Start**: The starting position or coordinate of the DNA sequence on the specified chromosome.
- **(column 6) - End**: The ending position or coordinate of the DNA sequence on the specified chromosome.
- **(column 7) - Strand**: Indicates whether the DNA sequence is on the forward (+) or reverse (-) strand of the chromosome.
- **(column 8) - Mismatches**: The number of mismatches or differences between the crRNA and the target DNA sequence. Mismatches can affect the efficiency of CRISPR-Cas9 editing.
- **(column 9) - Gene Type**: Describes the type of gene associated with the target DNA sequence, such as protein-coding gene, non-coding RNA, etc.
- **(column 10) - Feature**: Specific features or functional elements associated with the target DNA sequence, such as exons, introns, promoters, enhancers, etc.
- **(column 11-29) - Databases annotations**: These columns provide information related to the gene or genomic region's functional characteristics, associations with phenotypic traits, inheritance patterns, cancer involvement, protein domains, miRNA interactions, transcription factor sources, expression data, RNA-binding proteins.
- **(column 30) - Risk score**:score based on the genomic feature or region it hits (coding/non-coding/regulatory) and the function associated with the feature.

#### Target Risk Score Summary

A more comprehensive summary is provided exclusively for targets with elevated risk potential, as determined by the annotation results from various databases.

- **(column 1) - Off Target ID**: A unique identifier or reference for the off-target site being analyzed. This could be a numerical or alphanumeric identifier.
- **(column 2) - crRNA**: Short for "CRISPR RNA," it represents the guide RNA sequence used in a CRISPR-Cas9 gene editing experiment. This sequence guides the Cas9 protein to the target DNA.
- **(column 3) - DNA**: The DNA sequence that is the subject of the study or analysis. It could be the target DNA that the crRNA is designed to bind to or modify.
- **(column 4) - Chromosome**: The specific chromosome on which the DNA sequence is located.
- **(column 5) - Start**: The starting position or coordinate of the DNA sequence on the specified chromosome.
- **(column 6) - End**: The ending position or coordinate of the DNA sequence on the specified chromosome.
- **(column 7) - Strand**: Indicates whether the DNA sequence is on the forward (+) or reverse (-) strand of the chromosome.
- **(column 8) - Mismatches**: The number of mismatches or differences between the crRNA and the target DNA sequence. Mismatches can affect the efficiency of CRISPR-Cas9 editing.
- **(column 9) - Gene Type**: Describes the type of gene associated with the target DNA sequence, such as protein-coding gene, non-coding RNA, etc.
- **(column 10) - Feature**: Specific features or functional elements associated with the target DNA sequence, such as exons, introns, promoters, enhancers, etc.
- **(column 11-26) - Databases annotations**:
- **(column 27) - Risk score**:score based on the genomic feature or region it hits (coding/non-coding/regulatory) and the function associated with the feature.

#### Detailed biological information

Comprehensive details pertaining to each off-target, along with their respective annotations across various databases, are available for reference.

To view illustrative output examples, kindly navigate to the dedicated "examples" page.
