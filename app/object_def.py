from pydantic import BaseModel, validator, Field
from typing import List, Union
import re


class OffTarget(BaseModel):
    chromosome: Union[str, int]
    start: int
    end: int
    strand: str = None
    id: int = Field(None, title="id")
    sequence: str = Field(None, title="sequence")

    @validator("chromosome", allow_reuse=True)
    def val_chromosome(cls, v):
        if not v.replace("_", "").isalnum():
            raise ValueError("Chrom can not contain special char")
        return v

    @validator("end", allow_reuse=True)
    def val_end(cls, v, values):
        assert isinstance(v, int)
        if "start" in values and v < values["start"]:
            raise ValueError("End need to be larger then start")
        return v

    @validator("strand", allow_reuse=True)
    def val_strand(cls, v):
        assert v in ["+", "-"]
        return v

    @validator("sequence")
    def val_seq(cls, v):
        if v:
            if not re.fullmatch(r"^[AaGcTtCcUu]*$", v):
                raise ValueError("Got invalid string for site. Only A, T, U, C and G are allowed")
            if not len(v) < 24:
                raise ValueError("seq can not be longer then 24")
        return v


class Site(BaseModel):
    """
    Site for on-target search
    """

    sequence: str  # include sequences and pam
    mismatch: int = 4

    @validator("sequence", allow_reuse=True)
    def val_site(cls, v):
        if not re.fullmatch(r"^[AaGgTtCcUu]*$", v):
            raise ValueError("Got invalid string for site. Only A, T, U, C and G are allowed")
        return v

    @validator("mismatch", allow_reuse=True)
    def val_mismatch(cls, v):
        if v > 20:
            raise ValueError("Number is greater then 20. Only number Between 0 to 20 are allowed")
        if v < 0:
            raise ValueError("Number is less then 0. Only number Between 0 to 20 are allowed")
        return v


class SitesList(BaseModel):
    """
    List of Sites
    """

    # pattern: str = "NNNNNNNNNNNNNNNNNNNNNGG"
    pam: str = "NGG"
    downstream: bool = True
    pattern_dna_bulge: int = 0
    pattern_rna_bulge: int = 0
    search_tools: List[str] = ["flashfry"]
    sites: List[Site]

    @validator("pam", allow_reuse=True)
    def val_pattern(cls, v):
        if not re.fullmatch(r"[AGTCRYSWKMBDHVN]*$", v):
            raise ValueError("Not a valid pattern. Please refer for Cas-Offinder documentation")
        return v

    @validator("pattern_dna_bulge", "pattern_rna_bulge", allow_reuse=True)
    def val_bulge(cls, v):
        if v > 20:
            raise ValueError("Number is greater then 20. Only number Between 0 to 20 are allowed")
        if v < 0:
            raise ValueError("Number is less then 0. Only number Between 0 to 20 are allowed")
        return v


class OffTargetList(BaseModel):
    off_targets: List[OffTarget]