test <- read.table(file="tests.txt",header=TRUE,fill=TRUE, sep="|",quote="")
result <- read.table(file="results.txt",header=TRUE,fill=TRUE, sep="|",quote="")
#dose_response <- read.table(file="dose_responses.txt",header=TRUE,fill=TRUE, sep="|",quote="")
#dose_response_link <- read.table(file="dose_response_links.txt",header=TRUE,fill=TRUE, sep="|",quote="")
#head(dose_response)
#head(result)
#head(dose_response_link)
result_yes <- subset(result, endpoint=="LC50" | endpoint=="LC50*" | endpoint=="EC50" | endpoint=="EC50*" )
#head(test_yes)
Nresults <- nrow(result_yes)
test_list = sort( unique(result_yes[,2]) )
chem <- read.table(file="chemical_carriers.txt",header=TRUE,fill=TRUE, sep="|",quote="")

chem_yes <- vector()
for (tid in test_list){
  chem_yes <- rbind(chem_yes, subset(chem, test_id == tid)[,3])
}
head(chem_yes)

