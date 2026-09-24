// Renders transparent 1920x1080 PNG overlays from a project config
// usage: node make_overlays.mjs projects/XX.json OUT_DIR
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const out = process.argv[3];
fs.mkdirSync(out, { recursive: true });
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
await p.goto('file://' + process.cwd() + '/overlay.html');
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
const shot = async (id, fn, arg, path) => {
  await p.evaluate(([id, fn, arg]) => {
    document.querySelectorAll('.layer').forEach(l => l.style.display = 'none');
    document.getElementById(id).style.display = 'block';
    new Function('arg', fn)(arg);
  }, [id, fn, arg]);
  // Noto Sans JP ships as unicode-range subsets: load the ones this text needs
  await p.evaluate(async () => {
    const txt = document.body.innerText;
    for (const f of ['700 40px "Noto Sans JP"', '900 40px "Noto Sans JP"', '500 40px Inter', '700 40px Inter']) await document.fonts.load(f, txt);
    await document.fonts.ready;
  });
  await p.screenshot({ path, omitBackground: true });
};
await shot('grad', '', null, `${out}/grad.png`);
for (const [i, t] of cfg.titles.entries())
  await shot('ttl', "for (const k of ['no','jp','en']) document.getElementById(k).textContent = arg[k]; document.getElementById('jp').style.fontSize = (arg.size || 81) + 'px';", t, `${out}/title_${i}.png`);
for (const [i, t] of cfg.telops.entries())
  await shot('tel', "document.getElementById('telop').innerHTML = arg;",
    esc(t.text).replace(/\[(.+?)\]/g, '<em>$1</em>'), `${out}/telop_${String(i).padStart(2, '0')}.png`);
await b.close();
