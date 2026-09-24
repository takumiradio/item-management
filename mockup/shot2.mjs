import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const b = await chromium.launch();
const p = await b.newPage({ viewport:{width:1280,height:720}, deviceScaleFactor:1.5 });
await p.goto('file://'+process.cwd()+'/real.html');
await p.evaluate(async()=>{await Promise.all(['300','500','700','800'].map(w=>document.fonts.load(w+' 20px Inter')));await document.fonts.load('900 20px "Noto Sans JP"');await document.fonts.load('700 20px "Noto Sans JP"');await document.fonts.ready});
await p.waitForTimeout(500);
for (const id of ['A','B']) await (await p.$('#'+id)).screenshot({path:'real_'+id+'.png'});
await b.close();
