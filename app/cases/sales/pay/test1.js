const puppeteer = require('puppeteer');
function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms))
}
(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('https://www.baidu.com/');
  await page.screenshot({path: '4.png'});
  await browser.close();
  await sleep(10000)
})();