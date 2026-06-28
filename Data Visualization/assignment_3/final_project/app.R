library(shiny)
library(plotly)
library(readxl)
library(tidyverse)

ui <- fluidPage(
  titlePanel("Gender Pay Gap Analysis"),
  tabsetPanel(
    tabPanel("Gender PayGap by States",
             plotlyOutput("gender_pay_gap_plot", height = "400px")),
    tabPanel("Earnings by Industry",
             sidebarLayout(
               sidebarPanel(
                 checkboxGroupInput("selected_industries", "Select Industries:", 
                                    choices = NULL,
                                    selected = c("Industry A", "Industry B", "Industry C", "Industry D"))
               ),
               mainPanel(
                 plotlyOutput("industry_earnings_plot", height = "800px")
               )
             )),
    tabPanel("Hourly Earnings by Occupation",
             plotlyOutput("professions_plot", height = "800px")
    )
  )
)


# Server
server <- function(input, output, session) {
  
  # Plot 1
  data <- read_excel("gender_paygap.xlsx")
  
  
  data$dates <- as.Date(data$dates, format = "%Y-%m-%d")
  
 
  data$state <- as.factor(data$state)
  
 
  data$gap <- round(data$gap, 1)
  
  # Render Plotly plot
  output$gender_pay_gap_plot <- renderPlotly({
    plot_ly(data, x = ~dates, y = ~gap, color = ~state, type = 'scatter', mode = 'lines') %>%
      layout(
        title = "Gender Pay Gap in Australia 2012-2023",
        xaxis = list(title = "Year", tickformat = "%Y", tickmode = "linear", tick0 = min(data$dates), dtick = "M12"),
        yaxis = list(title = "% Gap"),
        showlegend = TRUE,
        hovermode = "x"
      )
  })
  
  # plot 2
  industries <- read_csv("earnings_by_industries.csv")
  
  # Wrap long industry names
  industries$industry_wrapped <- str_wrap(industries$industry, width = 25)

  
  # Update checkboxGroupInput choices based on the industry data
  observe({
    updateCheckboxGroupInput(session, "selected_industries", choices = unique(industries$industry), 
                             selected = c("Mining", "Construction", "Retail trade", 
                                          "Education & training", "Information media & telecommunications"))
  })
  
  # Render Plotly bar chart
  output$industry_earnings_plot <- renderPlotly({
    req(input$selected_industries)  
    
    filtered_data <- industries %>% filter(industry %in% input$selected_industries)
    
    plot_ly(filtered_data, y = ~industry_wrapped, x = ~weekly_earnings, 
            color = ~gender, type = 'bar', barmode = 'group',
            marker = list(line = list(width = 2))) %>%
      layout(
        title = "Weekly Earnings by Industry and Gender",
        xaxis = list(title = "Weekly Earnings in AUD"),
        yaxis = list(title = ""),  # Remove y-axis label
        showlegend = TRUE,
        bargap = 0.4,       # Increase the gap between individual bars
        bargroupgap = 0.5,  # Increase the gap between groups of bars
        margin = list(l = 200, r = 50, b = 50, t = 50, pad = 10),  # Adjust margins for better spacing
        height = 600  # Increase the plot height
      )
  })
  
  # plot 3
  occupations <- read_csv("profession.csv")
  occupations$Professions<- as.factor(occupations$Professions) 
  occupations$Professions_wrapped <- str_wrap(occupations$Professions, width = 8)
  # Render Plotly bar chart - Professions
  output$professions_plot <- renderPlotly({
    plot_ly(occupations, x = ~Professions_wrapped, y = ~Males, name = "Male", type = 'bar', marker = list(color = '#8DA0CB')) %>%
      add_trace(y = ~Females, name = "Female", marker = list(color = '#66C2A5')) %>%
      layout(
        title = "Hourly Earnings by Occupation",
        xaxis = list(title = "Occupations"),
        yaxis = list(title = "Hourly Earnings"),
        barmode = 'group',
        legend = list(
          title = "Gender",  # Legend title
          orientation = "h",  # Horizontal legend orientation
          x = 0, y = -0.3  # Adjust legend position
        ),
        margin = list(l = 100, r = 50, b = 100, t = 50, pad = 10),  # Adjust margins
        height = 500  # Set plot height
      )
  })
}

# Run the application
shinyApp(ui = ui, server = server)
