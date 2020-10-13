setwd("~/Documents/ECO")
T_data <- read.table("./tests.txt",sep="|", header=TRUE,fill=TRUE,quote="")
C_data <- read.table("./chemical_carriers.txt",sep="|", header=TRUE,fill=TRUE,quote="")

result <- read.table(file="./results.txt",header=TRUE,fill=TRUE, sep="|",quote="")
species <- read.table(file="./validation/species.txt",header=TRUE,fill=TRUE, sep="|",quote="")
result_yes <- subset(result, endpoint=="LC50" | endpoint=="LC50*" | endpoint=="EC50" | endpoint=="EC50*" )
head(species)
head(result_yes)

subset(T_data, test_id==result_yes[1,2])[1,18]

CAS <- vector()
CN <- vector()
LN <- vector()
Nresult <- nrow(result_yes)
for(i in 1:Nresult) {
  CAS <- c(CAS,subset(T_data, test_id==result_yes[i,2])[1,3])
  spc_id <- subset(T_data, test_id==result_yes[i,2])[1,18]
  CN <- c(CN, subset(species, species_number==spc_id)[1,2])
  LN <- c(LN, subset(species, species_number==spc_id)[1,3])
}

head(cbind(CAS,CN,LN,result_yes))
