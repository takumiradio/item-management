// Renders transparent 1920x1080 PNG overlays from telops.json
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
const cfg = JSON.parse(fs.readFileSync('telops.json', 'utf8'));
const out = process.argv[2] || 'overlays';
fs.mkdirSync(out, { recursive: true });
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
await p.goto('file://' + process.cwd() + '/overlay.html');
await p.evaluate(async () => {
  for (const f of ['700 20px Inter', '900 20px "Noto Sans JP"', '700 20px "Noto Sans JP"']) await document.fonts.load(f, '腕立て伏せ手幅ABC');
  await document.fonts.ready;
});
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
const show = async (id, fn, arg) => {
  await p.evaluate(([id, fn, arg]) => {
    document.querySelectorAll('.layer').forEach(l => l.style.display = 'none');
    document.getElementById(id).style.display = 'block';
    new Function('arg', fn)(arg);
  }, [id, fn, arg]);
  // Google Fonts splits Noto Sans JP into unicode-range subsets: load the ones this text needs
  await p.evaluate(async () => {
    const txt = document.body.innerText;
    for (const w of ['700', '900']) await document.fonts.load(`${w} 40px "Noto Sans JP"`, txt);
    await document.fonts.ready;
  });
  await p.waitForLoadState('networkidle');
};
await show('base', "for (const k of ['no','jp','en']) document.getElementById(k).textContent = arg[k];", cfg.title);
await p.screenshot({ path: `${out}/base.png`, omitBackground: true });
for (const [i, t] of cfg.telops.entries()) {
  const html = esc(t.text).replace(/\[(.+?)\]/g, '<em>$1</em>');
  await show('tel', "document.getElementById('telop').innerHTML = arg;", html);
  await p.screenshot({ path: `${out}/telop_${String(i).padStart(2, '0')}.png`, omitBackground: true });
}
await b.close();
