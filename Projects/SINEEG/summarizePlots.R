

res <- read.mat('Results_Infants_included_decode_within_SVM_03-Aug-2022_70912.mat')


DA <- res$results$DA[[1]]
times <- res$results$times

y = apply(DA,c(1,2),'mean')
rowMeans(y)

