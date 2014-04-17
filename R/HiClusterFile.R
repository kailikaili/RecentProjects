my.gene.dist.old <- function(){

	x <- read.table("prostate_preprocessed.txt")
	num.gene <- dim(x)[1]-1
	num.series <- dim(x)[2]-1
	y <- as.matrix(x[-(num.gene+1),-1])
	gene.mat <- apply(y,2,as.numeric)
	
	gene.mean <- apply(gene.mat,1,mean)
	gene.sd <- apply(gene.mat,1,sd)
	
	similarity.mat <- matrix(data = 0, nrow = num.gene, ncol = num.gene, byrow = FALSE)
	for (i in 2:num.gene)
	{
		if(i%%100 == 0)
		{
			print(i)
		}
		
		for(j in 1:(i-1))
		{
			gene.sim <- 0
			for( k  in 1:num.series)
			{
				gene.sim <- gene.sim + ((gene.mat[i,k]-gene.mean[i])/gene.sd[i]) * ((gene.mat[j,k]-gene.mean[j])/gene.sd[j])
			}
			
			gene.sim <- gene.sim/num.series
			similarity.mat[i,j] <- gene.sim
		}
	}
	
	d.list <- as.dist(similarity.mat)
	 
}



hier.cluster <- function()
{
	
	x <- read.table("prostate_preprocessed.txt")
	num.gene <- dim(x)[1]-1
	num.series <- dim(x)[2]-1
	y <- as.matrix(x[-(num.gene+1),-1])
	gene.mat <- apply(y,2,as.numeric)
	
	log.gene.mat <- log(gene.mat)
	
	sample.dist <- my.gene.dist(t(log.gene.mat))
	sample.hc <- hclust(sample.dist, method="complete")
	plot(sample.hc, main = "Cluster by Sample")
	
	gene.dist <- my.gene.dist(log.gene.mat)
	gene.hc <- hclust(gene.dist, method="complete")
	dev.new()
	plot(gene.hc, hang = -1, main = "Cluster by Gene")
	
	dev.new()
	heatmap(log.gene.mat, Rowv = as.dendrogram(gene.hc), Colv = as.dendrogram(sample.hc), scale="none", main="Heatmap Using Hierarchical Clustering")
	
	dev.new()
	image(log.gene.mat, main="Heatmap of Original Ordering")
	
	
}



my.gene.dist <- function(x){
	
	
	num.gene <- dim(x)[1]
	
	similarity.mat <- matrix(data = 0, nrow = num.gene, ncol = num.gene, byrow = FALSE)

	for (i in 2:num.gene)
	{
		for(j in 1:(i-1))
		{
			similarity.mat[i,j] <- cor(x[i,], x[j,])
		}
	}
	
	d.list <- as.dist(similarity.mat)
	
	return(d.list)
	 
}