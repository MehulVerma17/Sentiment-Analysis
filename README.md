# Sentiment Analysis of YouTube Comments

This project is a web application built with Flask that scrapes comments from a YouTube video and performs a sentiment analysis. It visualizes the sentiments (positive, negative, neutral) of the comments in a bar chart and doughnut chart.

## Features

- Scrapes comments from a specified YouTube video.
- Analyzes the sentiment of each comment.
- Displays the sentiment distribution in a bar and doughnut chart.
- Lists the comments with pagination.

## Technologies Used

- Python
- Flask
- `googleapiclient` for YouTube API interaction
- `python-dotenv` for managing environment variables
- HTML, Bootstrap for front-end
- JavaScript, Chart.js for visualization

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.7 or later
- `pip` (Python package manager)
- Python-dotenv
- Flask
- google-api-python-client
- emoji
- vaderSentiment
