events = read.csv("../../data/Gezari2013_table4.csv")

events <- events[events$Class == "Mdw",]

write.csv(events,"../../data/gezari_clean.csv")
