# vim: syntax highlight 
#   set filetype=r
#
#
# A simple shiny webapp

library(shiny)
library(ggplot2)
library(dplyr)

bcl <- read.csv("bcl-data.csv", stringsAsFactors = FALSE)

ui <- fluidPage(
  titlePanel("BC Liquor Store prices"),
  sidebarLayout(
    sidebarPanel(
      sliderInput("priceInput", "Price", 0, 100, c(25, 40), pre = "$"),
      radioButtons("typeInput", "Product type",
                  choices = c("BEER", "REFRESHMENT", "SPIRITS", "WINE"),
                  selected = "WINE"),
      #selectInput("countryInput", "Country",
      #            choices = c("CANADA", "FRANCE", "ITALY"))
      uiOutput("countryOutput")
    ),
    mainPanel(
      plotOutput("coolplot"),
      br(), br(),
      tableOutput("results")
    )
  )
)

server <- function(input, output, session) {
  filtered <- reactive({
    if (is.null(input$countryInput)) {
        return (NULL)
    }
    bcl %>%
    filter(Price >= input$priceInput[1],
           Price <= input$priceInput[2],
           Type == input$typeInput,
           Country == input$countryInput
    )
  })

  output$countryOutput <- renderUI({
    selectInput("countryInput", "Country",
                sort(unique(bcl$Country)),
                selected = "CANADA")
  })

  output$coolplot <- renderPlot({
   # filtered <-
   #   bcl %>%
   #   filter(Price >= input$priceInput[1],
   #          Price <= input$priceInput[2],
   #          Type == input$typeInput,
   #          Country == input$countryInput
   #   )
    ggplot(filtered(), aes(Alcohol_Content)) +
      geom_histogram()
  })

  output$results <- renderTable({
   # filtered <-
   #   bcl %>%
   #   filter(Price >= input$priceInput[1],
   #          Price <= input$priceInput[2],
   #          Type == input$typeInput,
   #          Country == input$countryInput
   #   )
   filtered()
 })
}

shinyApp(ui = ui, server = server)
