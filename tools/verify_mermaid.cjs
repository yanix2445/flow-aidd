// Requires Playwright via normal Node resolution, or FLOW_PLAYWRIGHT_MODULE.
// An existing browser can be selected with FLOW_BROWSER_EXECUTABLE.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const {chromium} = require(process.env.FLOW_PLAYWRIGHT_MODULE || 'playwright');

(async () => {
  const root = path.resolve(__dirname,'../skills/flow-aidd/references');
  const model = JSON.parse(fs.readFileSync(path.join(root,'workflow.json'),'utf8'));
  const files = ['00-prerequis.mmd',...model.sequences.map(sequence => sequence.id+'.mmd')];
  const browser = await chromium.launch({headless:true,...(process.env.FLOW_BROWSER_EXECUTABLE ? {executablePath:process.env.FLOW_BROWSER_EXECUTABLE} : {})});
  const out = process.env.FLOW_RENDER_DIR || fs.mkdtempSync(path.join(os.tmpdir(),'flow-aidd-mermaid-'));
  fs.mkdirSync(out,{recursive:true});
  try {
    const page = await browser.newPage({viewport:{width:1280,height:6000}});
    await page.setContent('<html lang="fr"><meta charset="utf-8"><body></body></html>');
    await page.addScriptTag({url:'https://cdn.jsdelivr.net/npm/mermaid@10.9.5/dist/mermaid.min.js'});
    await page.evaluate(() => mermaid.initialize({startOnLoad:false,securityLevel:'strict',suppressErrorRendering:true}));
    for (const [index,file] of files.entries()) {
      const source = fs.readFileSync(path.join(root,'mermaid',file),'utf8');
      assert(source.startsWith('---\ntitle:'));
      assert(!source.includes('\\n') && !source.includes('<br'));
      const {svg} = await page.evaluate(async ({source,index}) => {
        await mermaid.parse(source);
        return await mermaid.render('SequenceDiagram'+index,source);
      },{source,index});
      fs.writeFileSync(path.join(out,file.replace('.mmd','.svg')),svg);
      if (['S00.mmd','S91.mmd'].includes(file)) {
        await page.evaluate(svg => {document.body.innerHTML=svg;},svg);
        await page.locator('svg').first().screenshot({path:path.join(out,file.replace('.mmd','.png'))});
      }
    }
    console.log(`PASS : ${files.length} schémas parsés et rendus avec Mermaid 10.9.5 ; sources dérivées du modèle courant.`);
    console.log(`Rendus hors du dépôt : ${out}`);
  } finally {
    await browser.close();
  }
})().catch(error => {console.error(error);process.exitCode=1;});
