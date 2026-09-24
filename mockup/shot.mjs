import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const b = await chromium.launch();
const p = await b.newPage({ viewport:{width:1240,height:1060}, deviceScaleFactor:2 });
await p.goto('file://'+process.cwd()+'/mock.html'); await p.evaluate(async()=>{await Promise.all(['300','500','700','800'].map(w=>document.fonts.load(w+' 20px Inter')));await document.fonts.load('900 20px "Noto Sans JP"');await document.fonts.ready}); await p.waitForTimeout(800);
await p.screenshot({path:'mockup_compare.png'});
const fr = await p.$$('.frame');
await fr[0].screenshot({path:'mockup_A_minimal.png'}); await fr[1].screenshot({path:'mockup_B_sporty.png'});
await b.close();
