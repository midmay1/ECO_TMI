CAS_list <- read.table(file="CAS.txt",header=FALSE, sep="",quote="")
CAS_list <- unique(CAS_list)
NCAS <- nrow(CAS_list)
print(NCAS)
