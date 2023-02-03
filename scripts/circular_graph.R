    #
    #   Draw human chromosome ideogram and and off target from csv file. name are the off-target ID:
    #   This script will create the image in the project image folder. Need to be run from this project foldre
    #   app or script

    #   1.  Connectors
    #   2.  Gene lables

    #   Load RCircos package
    #   _________________________________________________________________
    #   xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    if (!require("RCircos")) install.packages("RCircos")
    if (!require("rjson")) install.packages("rjson")
    library(RCircos);
	library(tools)
	library("rjson")

	args = commandArgs(trailingOnly=TRUE)
    input_json = fromJSON(args)
    print("Loading library")


    #   Load human cytoband data and change the cyto color to be the same (grey)
    #   _________________________________________________________________
    #   xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    data(UCSC.HG38.Human.CytoBandIdeogram);
    hg38.cyto <- UCSC.HG38.Human.CytoBandIdeogram;
	hg38.cyto["Stain"] <- "gvar";

    #   Setup RCircos core components:
    #   _________________________________________________________________
    #   xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    RCircos.Set.Core.Components(cyto.info=hg38.cyto, chr.exclude=NULL,
                tracks.inside=0, tracks.outside=0);



    #   Open the graphic device (here a pdf file)
    #   _________________________________________________________________
    #   xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    message("Open graphic device and start plot ...\n");
    setwd("../")
	file_path_pdf <- input_json[["png_path"]]
    png(file=file_path_pdf, height=8, width=8, unit="in",
          type="cairo", res=300);

    RCircos.Set.Plot.Area();
    #title("Off-target location");

    #   Draw chromosome ideogram
    #   _________________________________________________________________
    #   xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    message("Draw chromosome ideogram ...\n");
    RCircos.Chromosome.Ideogram.Plot();

    #   Connectors in first track and gene names in the second track.
    #   _________________________________________________________________
    #   xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    message("Add Gene and connector tracks ...\n");
	file_path_csv <- input_json[["csv_path"]]
	data_csv = read.csv(file_path_csv, sep = '\t')
    RCircos.Gene.Connector.Plot(genomic.data=data_csv,
               track.num=1, side="in");
    RCircos.Gene.Name.Plot(gene.data=data_csv, name.col=5,
                track.num=2, side="in");


    #   Close the graphic device and clear memory
    #   _________________________________________________________________
    #   xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    dev.off();
    message("R Circos Demo Done ...\n\n");