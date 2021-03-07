# YuGiOhBot: Title and Text Function

Build status: [![Continuous integration Actions Status](https://github.com/YuGiOhBot3000/yugiohbot-function-title-text/workflows/CI/badge.svg)](https://github.com/YuGiOhBot3000/yugiohbot-function-title-text/actions)

This project sets up the card title and effect text for the YuGiOhBot.

## What it does
Using a pre-trained Machine Learning model, this function chooses a type of card to make and generates new text based on that model.
It will then package this information up into a HTTP request and tell [the cloud run service](https://github.com/YuGiOhBot3000/yugiohbot-cloud-run-card-generator) to create a card.