const puppeteer = require("puppeteer");

const SITE = process.env.SITE || 'http://localhost:443';
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || '<YOU DONT KNOW THIS>'

const sleep = async s => new Promise(resolve => setTimeout(resolve, 1000 * s));

const visit = async url => {
	let browser
	try {
		browser = await puppeteer.launch({
			args: ["--disable-gpu", "--no-sandbox", "--js-flags=--noexpose_wasm", "--ignore-certificate-errors"],
			executablePath: "/usr/bin/chromium-browser",
		});
		const context = await browser.createIncognitoBrowserContext();
		const page = await context.newPage();
		
		await page.goto(SITE);
		await page.waitForTimeout(1000);

		await page.type('#username', 'admin');
		await page.type('#password', ADMIN_PASSWORD);
		await page.click('#btn')
		await page.waitForTimeout(1000);

		page.goto(url);
		await page.waitForTimeout(10000);

		await browser.close();

	} catch (e) {
		console.log(e);
	} finally {
		if (browser) await browser.close();
	}
}

module.exports = visit
