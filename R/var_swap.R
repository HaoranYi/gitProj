
vega <- function(S0=100, K=100, r=0.05, d=0.05, tau=1, vol=0.1)
{
    d_1  <- (log(S0/K)+((r-d)+vol^2/2)*tau)/(vol*sqrt(tau));
    S0*sqrt(tau)*(1/sqrt(2*pi)*exp(-d_1^2/2))*exp(-d*tau)
}

vegaK <- function(K, t)
{
    sapply(t, function(x){vega(S0=50:200, K=K, tau=x)/K^2})
}

my3d_plot <- function(mat, xl="", yl="", zl="", FUN=persp3d, add=FALSE,
                      bgcol="slatergray", col=NULL, aspect=!add)
{
    require(rgl);
    x <- 1:nrow(mat);
    y <- 1:ncol(mat)
    if(!add)
    {
        open3d();
        material3d(color=bgcol)
    }
    if(is.null(col))
    {
        colorlut <- heat.colors(ncol(mat),alpha=0)
        col <- rev(rep(colorlut,each=nrow(mat)))
    }
    FUN(x, y, mat, col = col, alpha=1, back="points", axes = TRUE,
        box = TRUE,front="lines",xlab=xl, ylab=yl, zlab=zl,
        aspect=aspect, add=add)
}

mat <- lapply(seq(60,180,15),
              vegaK,
              t=seq(1,0,length=20))
mat$sum <- Reduce("+", mat)
my3d_plot(mat$sum, col="grey", aspect=c(4, 3, 1), bgcol="white")
sapply(mat[1:9],my3d_plot, add=TRUE, col="green")

