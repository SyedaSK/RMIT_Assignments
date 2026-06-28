library(readxl)
library(ggplot2)
library(plotly)
library(tidyverse)


data <- read_excel("gender_paygap.xlsx")
industries <- read_csv("earnings_by_industries.csv")
industries$industry_wrapped <- str_wrap(industries$industry, width = 20)

data$dates <- as.Date(data$dates,format = "%Y-%m-%d")
data$state <- as.factor(data$state)
data$gap <- round(data$gap, 1)


p1 <- plot_ly(data, x = ~dates, y = ~gap, color = ~state, type = 'scatter', mode = 'lines') %>%
  layout(
    title = "Gender Pay Gap in Australia 2012-2023",
    xaxis = list(title = "Year", tickformat = "%Y", tickmode = "linear", tick0 = min(data$dates), dtick = "M12"),
    yaxis = list(title = "% Gap"),
    showlegend = TRUE,
    hovermode = "x"
  )
p1

# Render Plotly bar chart
output$industry_earnings_plot <- renderPlotly({
  plot_ly(industries, y = ~industry_wrapped, x = ~weekly_earnings, color = ~gender, type = 'bar', barmode = 'group') %>%
    layout(
      title = "Weekly Earnings by Industry and Gender",
      xaxis = list(title = "Industry"),
      yaxis = list(title = "Weekly Earnings"),
      showlegend = TRUE
    )
})

