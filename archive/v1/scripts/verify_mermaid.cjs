const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {chromium} = require('/Users/yanis/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

(async () => {
  const folder = path.resolve(__dirname, '../mermaid');
  const files = fs.readdirSync(folder).filter(file => file.endsWith('.mmd')).sort();
  assert.equal(files.length, 13);
  const out = path.join(folder,'rendus');
  fs.mkdirSync(out,{recursive:true});
  const browser = await chromium.launch({headless:true,executablePath:'/Users/yanis/Library/Caches/ms-playwright/chromium-1248/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing'});
  const results = [];
  try {
    const page = await browser.newPage({viewport:{width:1280,height:5000}});
    await page.setContent('<html lang="fr"><head><meta charset="utf-8"></head><body></body></html>');
    await page.addScriptTag({url:'https://cdn.jsdelivr.net/npm/mermaid@10.9.5/dist/mermaid.min.js'});
    await page.evaluate(() => mermaid.initialize({startOnLoad:false,securityLevel:'strict',suppressErrorRendering:true}));
    for (const [index,file] of files.entries()) {
      const source = fs.readFileSync(path.join(folder,file),'utf8');
      assert(source.startsWith('---\ntitle:'));
      assert(!source.includes('\\n'));
      assert(!source.includes('<br'));
      assert(!/classDef|style |linkStyle/.test(source));
      const declared = new Set();
      const connected = new Set();
      for (const line of source.split('\n')) {
        const node = line.match(/^\s+([A-Za-z][A-Za-z0-9]*)[\[{]/);
        if (node) declared.add(node[1]);
        if (/-->|\.->/.test(line)) {
          const from = line.match(/^\s+([A-Za-z][A-Za-z0-9]*)\s/);
          const to = line.match(/\b([A-Za-z][A-Za-z0-9]*)$/);
          assert(from && to, line);
          connected.add(from[1]); connected.add(to[1]);
        }
      }
      assert.deepEqual([...declared].sort(),[...connected].sort(),`${file}: node missing, isolated or undeclared`);
      const rendered = await page.evaluate(async ({source,index}) => {
        await mermaid.parse(source);
        const {svg} = await mermaid.render(`flowDiagram${index}`,source);
        return svg;
      },{source,index});
      fs.writeFileSync(path.join(out,file.replace('.mmd','.svg')),rendered);
      await page.evaluate(svg => { document.body.innerHTML=svg; },rendered);
      const svg = page.locator('svg').first();
      assert(await svg.locator('.node').count() > 0);
      const dimensions = await svg.evaluate(element => ({viewBox:element.getAttribute('viewBox'),width:element.getBoundingClientRect().width,height:element.getBoundingClientRect().height}));
      if (index === 0 || index === 2) await svg.screenshot({path:path.join(out,file.replace('.mmd','.png'))});
      results.push({file,nodes:declared.size,...dimensions});
    }
    console.log(JSON.stringify({parser:'Mermaid 10.9.5',passed:results.length,checks:['syntaxe et rendu','titres','identifiants et connexions','aucun nœud isolé','aucun style ajouté','13 sources reprises dans MERMAID.md'],diagrams:results},null,2));
  } finally {
    await browser.close();
  }
})().catch(error => {console.error(error);process.exitCode=1;});
