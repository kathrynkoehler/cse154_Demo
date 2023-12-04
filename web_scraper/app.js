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

    // first run: gets the name and url of sub-pages from main page list
    await page.goto(SCRAPE_URL);
    beanieData = await page.evaluate(() => {
      // Get all beanie baby elements
      const beanieBabyArray = Array.from(document.querySelectorAll('   li   '));
      // Loop over each beanie element
      return beanieBabyArray.map( beanie => {
        const url = 'https:' + beanie.querySelector('   a   ').getAttribute('href');
        const name = beanie.querySelector('   a   ').textContent.trim();
        // Return JSON entry
        return {
          "name": name,
          "url": url
        };
      });
    });

    // Scrapes beanie baby's sub-pages
    for (const baby of beanieData) {
      console.log(`Starting ${baby['name']} at url: ${baby['url']}...`);
      // Interval between sub-page requests
      await new Promise(resolve => setTimeout(resolve, 250));
      // second run: get the image and poem from each sub-page
      await page.goto(baby['url']);
      baby.details = await page.evaluate(() => {
        let image = document.querySelector('center > img')?.src.trim() ?? "";
        let data;

        // check if image exists
        if (image != "") {
          // split on the '/'; the last index holds our image filename
          let pieces = image.split('/');
          let imageDest = `img/${pieces[-1]}`;
          // download image to our /img folder
          downloadImage(image, imageDest);
          // set our nested data to the relative path of the image and the associated poem
          data = {
            'img': imageDest,
            'poem': document.querySelector('center > h3 > b')?.innerHTML.replace(/<br>/g, " ").replace(/\\"/g, "'") ?? ""
          };
        } else {
          data = {
            'img': "No image found",
            'poem': document.querySelector('center > h3 > b')?.innerHTML.replace(/<br>/g, " ").replace(/\\"/g, "'") ?? ""
          };
        }

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
    console.log("/!\\ Done /!\\");
  }
}

async function downloadImage(url, destination) {
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to download image from ${url}. Status: ${response.status}`);
  }

  const buffer = await response.buffer();
  fs.writeFile(destination, buffer);
}

main();