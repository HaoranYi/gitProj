library(RODBC)
library(httr)
library(ggplot2)
library(jsonlite)
library(dplyr)
library(lubridate)
library(tidyr)

DB_ENTERPRISE <- c('DALDATA1,1433', 'Enterprise')
DB_SHREDS <- c('DALDATA5,1633', 'Vendor')
SHREDDER_FILTER_THRESHOLD <- 0.1

# establish new sql connection with logging
# conn.vec - c(server name, database name)
sql.connect <- function(conn.vec){
    # due to problems installing RODBC on linux, use RJDBC library
    if(.Platform$OS.type == 'unix'){
        require(RJDBC)
        drv <- JDBC('com.microsoft.sqlserver.jdbc.SQLServerDriver', '/etc/sqljdbc_4.1/enu/sqljdbc4.jar', identifier.quote="'")
        conn.str <- sprintf('jdbc:sqlserver://%s;databaseName=%s', gsub(',', ':', conn.vec[[1]]), conn.vec[[2]])
        #loginfo('Opening new database connection: %s', conn.str)
        conn.obj <- dbConnect(drv, conn.str, 'EM_UNIX', 'Ecuador2')
    } else {
        require(RODBC)
        conn.str <- paste("DRIVER={SQL Server};SERVER=",
                          conn.vec[[1]], ";DATABASE=", conn.vec[[2]], ";", sep="")
        #loginfo("Opening new database connection: %s", conn.str)
        conn.obj <- odbcDriverConnect(conn.str)
    }
    return(conn.obj)
}

# close sql connection with logging
sql.close <- function(conn.obj){
    # due to problems installing RODBC on linux, use RJDBC library
    if(.Platform$OS.type == 'unix'){
        require(RJDBC)
        dbDisconnect(conn.obj)
    } else {
        require(RODBC)
        odbcClose(conn.obj)
    }
    #loginfo("Closed database connection")
}


substituteParameters <- function(template, map){
    output <- template
    for(lab in names(map)){
        output <- gsub(lab, gsub("\\\\", "/", map[[lab]]), output)
    }
    return(output)
}

getYMDString <- function(d)
{
    sprintf("%d%02d%02d", year(d), month(d), day(d))
}

getEMBondDetail <- function(instrumentName) 
{
    dbConnection <- sql.connect(DB_ENTERPRISE)
    on.exit(sql.close(dbConnection))
    template <- 
        "SELECT * 
         FROM vwIssuerUniverseEMHistorical
         WHERE Instrument = '<INSTRUMENT>'"
    
    map <- list('<INSTRUMENT>'= instrumentName)
    query <- substituteParameters(template, map)
    print(query)
    r <- sqlQuery(dbConnection, query)
    #sql.close(dbConnection)
    r
}

getRateCurveDetail <- function(curveName)
{
    dbConnection <- sql.connect(DB_ENTERPRISE)
    on.exit(sql.close(dbConnection))
    template <- 
        "SELECT i.InstrumentID, i.Name as Instrument, p.Value as BLP
            FROM tbInstrument i
	        LEFT OUTER join vwParameters p on i.InstrumentID = p.ObjectId and p.ParamName = 'BLP'
            WHERE i.Name ='<CURVE_NAME>'
"
    
    map <- list('<CURVE_NAME>'= curveName)
    query <- substituteParameters(template, map)
    print(query)
    r <- sqlQuery(dbConnection, query)
    #sql.close(dbConnection)
    r
    
}

getHbkHistoricalData <- function(instrumentId, stringsAsFactors=FALSE, as.is=FALSE)
{
    dbConnection <- sql.connect(DB_ENTERPRISE)
    on.exit(sql.close(dbConnection))

    template <- 
        "SELECT cast(hip.PriceDate as DATE) as Date, inst.Name, inst.InstrumentID Instrument, COALESCE((bid+ask)/2, Last) Value, hip.*, v.Name as Vendor
         FROM tbHistInstPrice (NOLOCK) hip 
         JOIN vwInstrument (NOLOCK) inst on hip.InstrumentId = inst.InstrumentID
         LEFT OUTER JOIN tbVendor(NOLOCK) v on hip.VendorId = v.ID	
         WHERE isbest=1 and inst.InstrumentID = <INSTRUMENTID>"
  
    map <- list('<INSTRUMENTID>'= instrumentId)
    query <- substituteParameters(template, map)
    print(query)
  
    result <- sqlQuery(dbConnection, query)

    #sql.close(dbConnection)
    
    result$Date <- as.Date(result$Date)
    result$Value <- as.numeric(result$Value)
    result$Last <- as.numeric(result$Last)
    result$Vendor <- as.factor(result$Vendor)
    result
}

getHistoricalDataFromTerminalServiceUrl <- function(blp, startDate, endDate)
{
    map <- list('<START>'= getYMDString(as.Date(startDate)),
                '<END>' = getYMDString(as.Date(endDate)),
                '<BLP>' = blp)
    
    urlTemplate <- 'http://dalbmcbbg1:8080/bbterminalservice/gethistory?blp=<BLP>&startdate=<START>&enddate=<END>&fields=PX_LAST,PX_BID,PX_ASK'
    url <- URLencode(substituteParameters(urlTemplate, map))
    url
}

getHistoricalDataFromTerminalService <- function(blp, startDate, endDate)
{
    url <- getHistoricalDataFromTerminalServiceUrl(blp, startDate, endDate)
    print(url)
    r <- GET(url)
    parsedJson <- fromJSON(content(r, "text"))
    d <- data.frame(parsedJson$data)
    priceColumn <- grep('.*PX_LAST', colnames(d))
    bidColumn <- grep('.*PX_BID', colnames(d))
    askColumn <- grep('.*PX_ASK', colnames(d))
    dateColumn <- grep('.*date', colnames(d))
    result <- d[, c(dateColumn, priceColumn, bidColumn, askColumn)]
    colnames(result) <- c('Date', 'BBGPrice', 'BBGBID', 'BBGASK')

    result$Date <- as.Date(result$Date)
    result$BBGPrice <- as.numeric(result$BBGPrice)
    result
}

getMessageOneShreds <- function(instrument)
{
    dbConnection <- sql.connect(DB_SHREDS)
    on.exit(sql.close(dbConnection))
    
    template <- 
        "select s.*
        from Vendor.dbo.tbBbgRunsMgrBonds s with (NoLock)
        Where s.ISIN = '<ISIN>'"
    
    map <- list('<ISIN>'= instrument$ISIN)
    query <- substituteParameters(template, map)
    print(query)
    result <- sqlQuery(dbConnection, query)
    result
}

getTraxData <- function(instrument)
{
    dbConnection <- sql.connect(DB_ENTERPRISE)
    on.exit(sql.close(dbConnection))
    
    template <- 
        "select t.*
        from vendor.dbo.tbTraxVolumeDaily t with (NoLock)
        Where t.ISIN = '<ISIN>'"
    
    map <- list('<ISIN>'= instrument$ISIN)
    query <- substituteParameters(template, map)
    print(query)
    result <- sqlQuery(dbConnection, query)
    result
}

getCombinedHistoricalData <- function(instrument)
{
    d <- c()
    d$hbk <- getHbkHistoricalData(instrument$InstrumentId)    
    d$bgn <- getHistoricalDataFromTerminalService(instrument$BLP, '1990-01-01', '2017-07-18')
    d$shreds <- getMessageOneShreds(instrument)
    d$trax <- getTraxData(instrument)
    d
}


getPricePlotData <- function(d, sources) 
{
    plot_data <- data.frame()
    if ('HBK' %in% sources)
    {
        hbk <- d$hbk %>% 
            mutate(data_source='HBK', date=as.Date(PriceDate), vendor=Vendor) %>% 
            select(date, data_source, vendor, price=Value) %>% 
            gather(key=value_type, value=value, factor_key=TRUE, price, -date) %>% 
            as_tibble()
        plot_data <- bind_rows(plot_data, hbk)
    }
    
    if ('BGN' %in% sources)
    {
        bgn <- d$bgn %>% 
            select(date=Date, price=BBGPrice) %>% 
            mutate(data_source='BGN', vendor='Unknown') %>% 
            gather(key=value_type, value=value, factor_key=TRUE, price, -date) %>% 
            as_tibble()
        plot_data <- bind_rows(plot_data, bgn)
    }
    
    if ('Shreds' %in% sources)
    {
        shreds <- d$shreds %>% 
            mutate(date=as.Date(EVENT_TIME), data_source='Shreds', vendor=LAST_SENDERS_FIRM, bid=BID, ask=ASK, mid=(BID+ASK)/2) %>% 
            select(date, data_source, vendor, bid, ask, mid) %>% 
            gather(key=value_type, value=value, factor_key=TRUE, bid, ask, mid, -date) %>% 
            filter(!is.na(value)) %>%
            as_tibble()
        plot_data <- bind_rows(plot_data, shreds)
    }
    
    # TODO: supppress factor warnings
    plot_data$data_source <- as.factor(plot_data$data_source)
    plot_data$vendor <- as.factor(plot_data$vendor)
    plot_data$value_type <- as.factor(plot_data$value_type)
    plot_data
}

pick <- function(condition){
    function(d) d %>% filter_(condition)
}

getCombinedPriceGraph <- function(d, instrument, sources=c('HBK', 'BGN', 'Shreds'))
{
    plot_data <- getPricePlotData(d, sources)
    
    g <- ggplot(plot_data, aes(x=date, y=value))
    g <- g + theme_light()
    if ('HBK' %in% sources) {
        g <- g + geom_point(data=pick(~data_source=='HBK'), aes(color=vendor), size=3, alpha=0.2)
    } 
    if ('BGN' %in% sources) {
        g <- g + geom_line(data=pick(~data_source=='BGN'), size=.5)
    } 

    if ('Shreds' %in% sources) {
        selector <- function(d) { filter(d, data_source == 'Shreds') %>% filter(value_type == 'mid') }
        g <- g + geom_point(data=selector, aes(y=value, color=vendor), alpha=0.2)
    }
    
    title <- sprintf("%s - prices from ", instrument$Instrument, paste(sources, collapse=', '))
    subtitle <- sprintf("Number of points: HBK=%d, BGN=%d, Shreds=%d", nrow(d$bgn), nrow(d$hbk), nrow(d$shreds))
    g <- g + ggtitle(title, subtitle)
    g
}

getPriceAndVolumeGraph <- function(d, instrument)
{
    hbk_data <- getPricePlotData(d, c('HBK'))
    bgn_data <- getPricePlotData(d, c('BGN'))
    shreds_data <- getPricePlotData(d, c('Shreds'))

    filtered_shreds <-shreds_data %>%
        #remove bid/ask
        filter(value_type != 'ask' & value_type != 'bid') %>% 
        #join with bgn
        full_join(bgn, by='date') %>% 
        # calc diff % from bgn
        mutate(diff=(value.x - value.y)/value.y) %>% 
        # apply filter
        filter(abs(diff) < SHREDDER_FILTER_THRESHOLD) %>% 
        # select relevant columns
        select(date,data_source=data_source.x, vendor=vendor.x, value_type=value_type.x, value=value.x) %>% 
        as_tibble()

    trax_data <- d$trax %>%
        mutate(date=as.Date(PeriodDate), data_source='Trax', vendor='Trax', trades=ActualTradeCount, volume_usd=VolumeUSD) %>%
        select(date, data_source, vendor, trades, volume_usd) %>%
        filter(!grepl('<', trades) && !grepl('<', volume_usd)) %>%
        gather(key=value_type, value=value, factor_key=TRUE, trades, volume_usd, -date) %>%
        mutate(value=as.numeric(value)) %>%
        filter(!is.na(value)) %>%
        as_tibble()

    plot_data <- bind_rows(hbk_data, bgn_data, filtered_shreds, trax_data) %>% 
        mutate(data_source=factor(data_source), vendor=as.factor(vendor), value_type = factor(value_type))%>%
        as_tibble()
    
    g <- ggplot(plot_data, aes(x=date)) + theme_light() + guides(color=FALSE)
    
    #HBK data
    g <- g + geom_point(data=pick(~data_source == 'HBK'), aes(y=value, color=vendor))
    #BGN line
    g <- g + geom_line(data=pick(~data_source == 'BGN'), aes(y=value))

    #Shreds 
    g <- g + geom_point(data=pick(~data_source == 'Shreds'), aes(y=value, color=vendor))
    
    # Trax Volume and trades
    g <- g + geom_line(data=pick(~value_type=='volume_usd'), aes(y=value))
    g <- g + geom_line(data=pick(~value_type=='trades'), aes(y=value))

    
    facet_labels <- list(sprintf('Shredder Mid Price (Filtered to %d%% of BGN)', floor(100 * SHREDDER_FILTER_THRESHOLD)), 
                         'HBK and BGN Prices', 
                         'TRAX Trades', 
                         'TRAX Volume (USD)'
                     )
    labeller <- function(v) { return(facet_labels) }
    g <- g + facet_wrap(~value_type, ncol=1, scales='free_y', labeller = as_labeller(labeller))

    title <- sprintf("%s - Composite view", instrument$Instrument)
    subtitle <- sprintf("Number of rows: HBK=%d, BGN=%d, Shreds=%d, Trax=%d", nrow(d$bgn), nrow(d$hbk), nrow(d$shreds), nrow(d$trax))
    g <- g + ggtitle(title, subtitle) + labs(y="")
    g
}


getBgnDiff <- function(d)
{
    c()
}


getBgnDiffGraph <- function(df, instrument)
{
    g <- ggplot(df, aes(x=Date))
    g <- g + theme_light()   
    g <- g + geom_point(aes(y=diff, color=Vendor),size=3, alpha=0.2)
    g <- g + ggtitle(sprintf("%s - Difference of BBG and Enterprise prices", instrument$Instrument))
    g
}

getBgnDiffHistorgram <- function(df, instrument)
{
    g <- ggplot(data=df, aes(df$diff))
    g <- g + theme_light()   
    g <- g + geom_histogram(aes(alpha=0.3))
    title <- sprintf("%s - Histogram of difference between BBG and Enterprise prices", instrument$Instrument)
    subtitle <- sprintf("Mean = %8.3f, SD=%8.3f", mean(df$diff, na.rm=TRUE), sd(df$diff, na.rm=TRUE))
    g <- g + ggtitle(title, subtitle)
    g <- g + guides(fill=FALSE)
    g
}



sanitizeInstrumentName <- function(instrument)
{
    s <- gsub('%', '-', instrument$Instrument)
    s <- gsub('/', '-', s)
    s
}

saveEMBondGraphs <- function(instrumentName)
{
    instrument <- getEMBondDetail(instrumentName)
    prefix <- sanitizeInstrumentName(instrument)

    d <- getCombinedHistoricalData(instrument)
    
    g1 <- getCombinedPriceGraph(d, instrument, c('HBK', 'BGN'))
    ggsave(sprintf("%s-HBK+BGN.png", prefix), g1, width = 12, height = 8, units = "in")

    g2 <- getCombinedPriceGraph(d, instrument, c('Shreds', 'BGN'))
    ggsave(sprintf("%s-Shreds+BGN.png", prefix), g2, width = 12, height = 8, units = "in")
    

    #diff <- getBBGDiff(d)
    #g2 <- getBgnDiffGraph(df, instrument)
    #ggsave(sprintf("%s-diff.png", prefix), g2, width = 12, height = 8, units = "in")

    #g3 <- getBgnDiffHistorgram(df, instrument)
    #ggsave(sprintf("%s-hist.png", prefix), g3, width = 12, height = 8, units = "in")
    
}

#TODO: verify
saveRateCurveGraphs <- function(instrumentName)
{
    instrument <- getRateCurveDetail(instrumentName)
    df <- getCombinedHistoricalData(instrument)
    df$diff <- df$BBGPrice - df$Value
    
    g1 <- getCombinedGraph(df, instrument)
    
    prefix <- sanitizeInstrumentName(instrument)
    
    ggsave(sprintf("%s-HBK+BGN.png", prefix), g1, width = 12, height = 8, units = "in")
    
    g2 <- getBgnDiffGraph(df, instrument)
    ggsave(sprintf("%s-diff.png", prefix), g2, width = 12, height = 8, units = "in")
    
    g3 <- getBgnDiffHistorgram(df, instrument)
    ggsave(sprintf("%s-hist.png", prefix), g3, width = 12, height = 8, units = "in")
}

