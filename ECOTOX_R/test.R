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

#head(test)
CAS_list <- vector()
for (i in 1:length(test_list) ) {
  tid <- test_list[i]
  #print(tid)
  CAS_list <- c(CAS_list, test[which(test$test_id == tid),3])
  #print(test[which(test$test_id == tid),3])
}
#head(chem_yes)
CAS_list <- sort( unique(CAS_list) )
NCAS <- length(CAS_list)
print(NCAS)

