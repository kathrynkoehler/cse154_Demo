// descriptive header comment :^)

"use strict";
const puppeteer = require('puppeteer');
const fs = require('fs').promises;

// full list of beanies and poem links
const SCRAPE_URL = "https://www.angelfire.com/ar/bbcollector/poems.html";

async function main() {
  await scrape();
};

// /**
//  * Downloads images from the web to local directory based on url.
//  * @param url - the source url of the image
//  * @param destination - the local directory path to save the image to
//  */
async function screenshot(filename) {
  let browser;
  try {
    browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.setViewport({width: 100, height: 100});
    let url = `https://www.angelfire.com/ar/bbcollector/images/${filename.split("/").pop()}`;
    await page.goto(url);
    await page.screenshot({"path": filename});
    await browser.close();
  } catch (err) {
    console.log(err);
    await browser.close();
  }
}

/**
 * Scrapes data from the web and saves to a local json file.
 */
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
      await new Promise(resolve => setTimeout(resolve, 100));
      // second run: get the image and poem from each sub-page
      await page.goto(baby['url']);
      // pass screenshot in as parameter so it's within scope
      baby.details = await page.evaluate(async () => {
        let image = document.querySelector('center > img')?.src.trim() ?? "";
        let data;
        // check if image exists
        if (image != "") {
          // split on the '/'; the last index holds our image filename
          let dest = image.split('/').pop().trim();
          let poem = document.querySelector('center > h3 > b')?.innerHTML.replace(/<br>/g, " ").replace(/\\"/g, "'") ?? "";
          // set our nested data to the relative path of the image and the associated poem
          data = {
            'img': `img/${dest}`,
            'poem': poem.trim()
          };
        } else {
          data = {
            'img': "No image found",
            'poem': poem.trim()
          };
        }

        return data;
      });
    }

    // get images
    for (const baby of beanieData) {
      console.log(`Screenshot ${baby['name']} at url: ${baby['details']['img']}...`);
      // Interval between sub-page requests
      await new Promise(resolve => setTimeout(resolve, 250));
      // screenshot each beanie baby image
      screenshot(baby['details']['img']);
    };

    // write objects to json file, to be parsed into csv
    await fs.writeFile('data/beanieData.json', JSON.stringify(beanieData, null, 2));
  } catch (error) {
    console.error(error);
  } finally {
    if (browser) {
      await browser.close();
    }
    console.log("/!\\ Done /!\\");
  }
}

main();