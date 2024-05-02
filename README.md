# RentalRadar

RentalRadar is a tool developed when me and a few friends wanted to move to West Hartford and were looking for apartments. We found that apartments were snatched up as soon as they were posted, so I built a tool that would notify us when new apartments were posted.

## How it works

RentalRadar is a web scraper that scrapes apartments from apartments.com and sends an email notification when a new apartment is posted. The scraper runs every day and checks for new apartments. If a new apartment is found, it sends an email notification to the user.

## How to use

1. Clone the repository

```bash
git clone
```

2. Install the dependencies

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add the following variables

```bash
email=
password=
```

4. Run the scraper
```bash
python src.py
```

## Future improvements

- Add more websites to scrape from
- Add a front-end to the scraper
- Add a database to store the apartments
- Add a feature to filter apartments based on user preferences
- Add a feature to send notifications to the user when the price of an apartment drops
- Add a feature to send notifications to the user when a new apartment is posted in a specific area