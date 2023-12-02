// descriptive header comment :^)

"use strict";
const puppeteer = require('puppeteer');
const fs = require('fs').promises;

// full list of beanies and poem links
const SCRAPE_URL = "https://www.angelfire.com/ar/bbcollector/poems.html";

async function main() {
  await scrape();
};

async function scrape() {
  let browser;
  let beanieData;

  try {
    browser = await puppeteer.launch();
    const page = await browser.newPage();
    page.setDefaultNavigationTimeout(2 * 60 * 1000);

    console.log("/!\\ Starting scrape /!\\");
    await page.goto(SCRAPE_URL);

    // first run: gets teh name and url of subpage from main page list
    beanieData = await page.evaluate(() => {
      const beanieBabyArray = Array.from(document.querySelectorAll('li'));
      return beanieBabyArray.map( beanie => {
        const  url = 'https:' + beanie.querySelector('a').getAttribute('href');
        const name = beanie.querySelector('a').textContent.trim();
        return {
          "name": name,
          "url": url
        };
      });
    });

    // Scrapes beanie baby's subpages
    for (const baby of beanieData) {
      console.log(`Starting ${baby['name']} at url: ${baby['url']}...`);

      // Interval between subpage requests
      await new Promise(resolve => setTimeout(resolve, 250));
      await page.goto(baby['url']);
      // second run: get the image and poem from each subpage
      baby.details = await page.evaluate(() => {
        let data = {
          'img': document.querySelector('center > img')?.src.trim() ?? "",
          'poem': document.querySelector('center > h3 > b')?.innerHTML.replace(/<br>/g, " ").replace(/\\"/g, "'") ?? ""
        };
        return data;
      });
    };

    // write objects to json file, to be parsed into csv
    fs.writeFile('data/beanieData.json', JSON.stringify(beanieData, null, 2));
  } catch (error) {
    console.error(error);
  } finally {
    if (browser) {
      await browser.close();
    }
    console.log("/!\\ Done /!\\")
  }
}

main();