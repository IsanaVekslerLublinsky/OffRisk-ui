import os

SET_PAGE_CONFIG = False
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).rstrip("/")

# DB_NAME_LIST = ["gencode", "mirgene", "remapepd", "enhanceratlas", "pfam", "targetscan",
#                 "omim", "humantf", "protein_atlas", "rbp", "cosmic"]

DB_NAME_LIST = {"gencode": "GENCODE", "mirgene": "MirGeneDB", "remapepd": "ReMapEPD",
                      "enhanceratlas" : "EnhancerAtlas 2.0", "pfam": "Pfam", "targetscan": "TargetScan 8.0",
                      "omim": "OMIM", "humantf": "HumanTF 3.0", "protein_atlas": "Protein Atlas", "rbp": "RBP",
                      "cosmic": "COSMIC"}



TOOLS_NAME_LIST = {"flashfry": "FlashFry", "cas_offinder": "Cas-OFFinder", "crispritz": "CRISPRitz"}

# images
LOGO_PATH = f"{BASE_DIR}/images/logo.png"
CIRCULAR_GRAPH_PNG_PATH = f"{BASE_DIR}/images/circular_graph.png"

# Log
LOG_PATH = f"{BASE_DIR}/log/off-risk-ui.log"

# Scripts
CIRCULAR_GRAPH_SCRIPT_PATH = f"{BASE_DIR}/scripts/circular_graph.R"

# Files
OFF_TARGET_CSV = f"{BASE_DIR}/output/off_target.csv"

SERVER_MAP = {
    "Local":
        {
            "url": "http://off-risk-server",
            "port": 80
        }
}

HELP_STRING_MAP = {
    "GENCODE": "Gene features in human based on biological evidence.\n"
               "Release version 42. Genome version GRCh38.p13, GRCh38/hg38",
    "MirGene": "Database of microRNA genes that have been validated and annotated.\n"
               "Release Version 2.1. Genome version GRCh38/hg38",
    "ReMapEPD": "ReMap is a database of transcriptional regulators from DNA-binding experiments.\n "
                "EPD ia a databse of transcription initiation sites of eukaryotic genes promoter.\n"
                "ReMap: 2022, release number 4, EPD: coding - version 6, non-coding - version 1. "
                "Genome version GRCh38/hg38",
    "EnhancerAtlas": "Enhancers databse, distal cis-regulatory elements that activate the "
                     "transcription of their target genes.\n"
                     "Release version 2.0. Genome version GRCh37/hg19 (converted in this database to GRCh38/hg38)",
    "Pfam": "Database of protein families and domains.\n"
            "Genome version GRCh38/hg38",
    "TargetScan": "Database for predicted microRNA targets in mammals.\n"
                  "Release version 8.0. Genome version GRCh37/hg19",
    "OMIM": "A comprehensive, authoritative compendium of human genes and genetic phenotypes.\n "
            "Downloaded on December 24, 2020",
    "HumanTF": "Database with information on animal transcription factors (TFs) and cofactors.\n"
               "Release version 3.0",
    "Protein Atlas": "Database which shows the distribution of the proteins across all major tissues and organs "
                     "in the human body.\n"
                     "Release version 21.1",
    "RBP": "Data set of RNA elements in the human genome that are recognized by RNA-binding proteins (RBPs)",
    "COSMIC": "Database for the available information about the effects of somatic mutations across the range of"
              " human cancers.\n"
              "Release version 96, 31st May 2022",

}

FULL_NAME_MAP = {
    "GENCODE": "GENCODE",
    "MirGene": "MirGeneDB",
    "ReMapEPD": "ReMap and Eukaryotic Promoter Database",
    "EnhancerAtlas": "EnhancerAtlas",
    "Pfam": "Pfam Protein Domains",
    "TargetScan": "TargetScan",
    "OMIM": "Online Mendelian Inheritance in Man",
    "HumanTF": "Human transcription factors",
    "Protein Atlas": "The Human Protein Atlas",
    "RBP": "RNA binding proteins",
    "COSMIC": "COSMIC"

}

COLUMNS_NAME_MAP = {
    "GENCODE": {"off_target_id": "OFF Target (OT) Id", "ot_chromosome": "OT Chromosome", "ot_start": "OT Start",
                "ot_end": "OT End", "gene_ensembl_id": "Gene Ensembl Id", "gene_symbol": "Gene Symbol",
                "segment": "Feature (F)", "start": "F Start", "end": "F End", "strand": "F Strand",
                "gene_type": "Gene Type", "transcript_ensembl_id": "Transcript Ensembl Id",
                "transcript_type": "Transcript Type", "transcript_symbol": "Transcript Symbol",
                "protein_id": "Protein Id", "exon_number": "Exon Number", "exon_id": "Exon Id"},
    "MirGene": {"off_target_id": "OFF Target (OT) Id", "ot_chromosome": "OT Chromosome", "ot_start": "OT Start",
                "ot_end": "OT End", "start": "MiRNA start", "end": "MiRNA end", "mir_symbol": "MiRNA symbol",
                "strand": "MiRNA strand"},
    "ReMapEPD": {"off_target_id": "OFF Target (OT) Id", "ot_chromosome": "OT Chromosome", "ot_start": "OT Start",
                 "ot_end": "OT End", "gene_ensembl_id": "Gene with Promoter (ENSG)",
                 "start": "Binding Site (BS) Start", "end": "BS End", "strand": "BS Strand",
                 "remap": "Binding Factor (Biotype)", "epd_coding": "EPD Coding/Non-Coding (1/0)",
                 "epd_gene_symbol": "Epd Gene Symbol"},
    "EnhancerAtlas": {"off_target_id": "OFF Target (OT) Id", "ot_chromosome": "OT Chromosome", "ot_start": "OT Start",
                      "ot_end": "OT End", "enhancer_gene_score": "Enh-Gene Score", "gene_ensembl_id": "Gene Ensembl Id",
                      "gene_symbol": "Gene Symbol", "gene_start": "Gene Start", "enh_start": "Enh Start",
                      "enh_stop": "Enh Stop", "tissue": "Tissue"},
    "Pfam": {"off_target_id": "OFF Target (OT) Id", "ot_chromosome": "OT Chromosome", "ot_start": "OT Start",
             "ot_end": "OT End", "start": "Domain start", "end": "Domain End", "gene_ensembl_id": "Gene Ensembl Id",
             "gene_symbol": "Gene Symbol", "pfam_domain_name": "Pfam Domain Name"},
    "TargetScan": {"off_target_id": "OFF Target (OT) Id", "ot_chromosome": "OT Chromosome", "ot_start": "OT Start",
                   "ot_end": "OT End", "gene_ensembl_id": "Gene Ensembl Id", "gene_symbol": "Gene Symbol",
                   "mir_symbol": "MiRNA Symbol"},
    "OMIM": {"off_target_id": "OFF Target (OT) Id", "gene_ensembl_id": "Gene Ensembl Id", "gene_symbol": "Gene Symbol",
             "omim_id": "OMIM ID", "disease_related": "Phenotype", "inheritance_model": "Inheritance Model"},
    "HumanTF": {"off_target_id": "OFF Target (OT) Id", "gene_ensembl_id": "Gene Ensembl Id",
                "gene_symbol": "Gene Symbol",  "HumanTF_source": "HumanTF source"},
    "Protein Atlas": {"gene_ensembl_id": "Gene Ensembl Id", "gene_symbol": "Gene Symbol"},
    "RBP": {"off_target_id": "OFF Target (OT) Id", "gene_ensembl_id": "Gene Ensembl Id",
            "gene_symbol": "Gene Symbol"},
    "COSMIC": {"off_target_id": "OFF Target (OT) Id", "gene_ensembl_id": "Gene Ensembl Id",
               "gene_symbol": "Gene Symbol", "Name": "Gene Name"},
    "OFF_TARGET": {"off_target_id": "Off Target ID", "cr_rna": "crRNA", "dna": "DNA", "chromosome": "Chromosome",
                   "start": "Start", "end": "End",
                   # "score": "Score", "strand": "Strand", "attributes": "attributes", "segment": "Feature",
                   # "strand": "Strand", "mismatch": "Mismatches", "sequence": "Sequence", "segment": "Feature",
                   "strand": "Strand", "mismatch": "Mismatches", "gene_type": "Gene Type", "segment": "Feature",
                   "gene_ensembl_id": "Gene Ensembl Id", "gene_symbol": "Gene Symbol",
                   "disease_related": "OMIM Phenotype",
                   "inheritance_model": "OMIM Inheritance Model",
                   "cancer_related": "Role in Cancer",
                   "mir_gene": "MiRNA gene", "pfam_protein_domains": "Pfam Protein Domains", "targetscan": "TargetScan",
                   "HumanTF_source": "HumanTF Source", "expression_information": "Expression Information",
                   "rbp_gene_ensembl_id": "Rbp Gene",
                   "remap_epd_gene_ensembl_id": "Promoter of Gene (ENSG)",
                   "remap_epd_disease_related": "Gene(Promoter) Phenotype",
                   "remap_epd_inheritance_model": "Gene(Promoter) Inheritance model",
                   "remap_epd_cancer_related": "Gene(Promoter) Role in Cancer",
                   "enhancer_atlas_gene_ensembl_id": "Enhancer of Gene (ENSG)",
                   "enhancer_atlas_disease_related": "Gene(Enhancer) Phenotype",
                   "enhancer_atlas_inheritance_model": "Gene(Enhancer) Inheritance Model",
                   "enhancer_atlas_cancer_related": "Gene(Enhancer) Role in Cancer",
                   "risk_score": "Risk_Score"},

    "RISK_TARGET": {"off_target_id": "Off Target ID", "cr_rna": "crRNA", "dna": "DNA", "chromosome": "Chromosome",
                   "start": "Start", "end": "End",
                   "strand": "Strand", "mismatch": "Mismatches", "gencode_gene_type": "Gene Type", "gencode_segment": "Feature",
                   "gencode_gene_ensembl_id": "Gene Ensembl Id", "gencode_gene_symbol": "Gene Symbol",
                   "gencode_omim_disease_related": "OMIM Phenotype",
                   "gencode_omim_inheritance_model": "OMIM Inheritance Model",
                   "gencode_cosmic_role_in_cancer": "Role in Cancer",
                   "remapepd_gene_ensembl_id": "Promoter of Gene (ENSG)",
                   "remapepd_epd_gene_symbol": "Gene(Promoter) Symbol",
                   "remapepd_omim_disease_related": "Gene(Promoter) Phenotype",
                   "remapepd_omim_inheritance_model": "Gene(Promoter) Inheritance model",
                   "remapepd_cosmic_role_in_cancer": "Gene(Promoter) Role in Cancer",
                   "enhanceratlas_gene_ensembl_id": "Enhancer of Gene (ENSG)",
                   "enhanceratlas_gene_symbol": "Gene(Enhancer) Symbol",
                   "enhanceratlas_omim_disease_related": "Gene(Enhancer) Phenotype",
                   "enhanceratlas_omim_inheritance_model": "Gene(Enhancer) Inheritance Model",
                   "enhanceratlas_cosmic_role_in_cancer": "Gene(Enhancer) Role in Cancer",
                   "risk_score": "Risk_Score"
                }

}

ON_TARGET_JSON_EXAMPLE = """{
  "sites": [
    {
      "sequence": "CTTAAGAATACGCGTAGTCGAGG",
    },
    {
      "sequence": "ATGTCTGGTAAGACGCCCATCGG",
    }
  ]
}"""

ON_TARGET_UPLOAD_HELP = f"Need to be json file with the structure of SitesList pydantic object. For example:\n" \
                        f"{ON_TARGET_JSON_EXAMPLE}"

OFF_TARGET_TEXT_HELP = "Need to be tab delimiters, each row with chromosome name, start, end and strand. " \
                       "For example:\n" \
                       "1	116905	116928	+\n" \
                       "1	293471	293494	+\n" \
                       "1	472912	472935	+\n" \
                       "1	707890	707913	+\n" \
                       "Chromosome name need to be in format"
