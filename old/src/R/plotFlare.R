require(ggplot2)

flare <- read.csv("../../data/gj_3685a_lc.csv")
flare$t_mean <- flare$t_mean - flare$t_mean[1]

ggplot(data=flare, aes(x=t_mean,y=flux_bgsub)) +
  geom_area() +
  xlab("Time (s)") +
  ylab("Corrected Flux (ergs/s/cm2/A")
