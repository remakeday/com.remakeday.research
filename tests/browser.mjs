// Run with Node 20: node --experimental-websocket tests/browser.mjs
// Uses the real site and a local headless Chrome; no browser test dependency.
import assert from 'node:assert/strict';
import {mkdir, writeFile} from 'node:fs/promises';

const origin = 'http://127.0.0.1:4173';
const debug = 'http://127.0.0.1:9223';
const target = await fetch(`${debug}/json/new?about:blank`, {method: 'PUT'}).then(r => r.json());
const socket = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((resolve, reject) => { socket.onopen = resolve; socket.onerror = reject; });
let serial = 0;
const pending = new Map();
const exceptions = [];
const logs = [];
socket.onmessage = ({data}) => {
  const packet = JSON.parse(data);
  if (packet.method === 'Log.entryAdded') logs.push(packet.params.entry);
  if (packet.method === 'Runtime.exceptionThrown') exceptions.push(packet.params.exceptionDetails.text);
  if (!packet.id) return;
  const call = pending.get(packet.id);
  if (!call) return;
  pending.delete(packet.id); clearTimeout(call.timer);
  packet.error ? call.reject(new Error(JSON.stringify(packet.error))) : call.resolve(packet.result);
};
function send(method, params = {}) {
  return new Promise((resolve, reject) => {
    const id = ++serial;
    const timer = setTimeout(() => { pending.delete(id); reject(new Error(`Timeout: ${method}`)); }, 15000);
    pending.set(id, {resolve, reject, timer});
    socket.send(JSON.stringify({id, method, params}));
  });
}
async function evaluate(expression) {
  const result = await send('Runtime.evaluate', {expression, returnByValue: true, awaitPromise: true});
  if (result.exceptionDetails) throw new Error(JSON.stringify(result.exceptionDetails));
  return result.result.value;
}
async function until(expression) {
  for (let n = 0; n < 50; n++) {
    if (await evaluate(expression)) return;
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  throw new Error(`Condition not reached: ${expression}`);
}
async function viewport(width, height) {
  await send('Emulation.setDeviceMetricsOverride', {width, height, deviceScaleFactor: 1, mobile: width < 600});
}
async function navigate(path) {
  await send('Page.navigate', {url: origin + path});
  await until(`location.pathname === new URL(${JSON.stringify(origin + path)}).pathname && document.readyState === 'complete' && document.querySelector('.paper') !== null`);
}
async function shot(name, height = 1800) {
  await send('Runtime.evaluate', {expression: 'window.scrollTo(0,0)'});
  const metrics = await send('Page.getLayoutMetrics');
  const size = metrics.cssContentSize;
  const {data} = await send('Page.captureScreenshot', {format: 'png', captureBeyondViewport: true, clip: {x: 0, y: 0, width: size.width, height: Math.min(size.height, height), scale: 1}});
  await mkdir('/tmp/research-ui-shots', {recursive: true});
  await writeFile(`/tmp/research-ui-shots/${name}.png`, Buffer.from(data, 'base64'));
}
let passed = 0;
async function check(name, action) { await action(); passed++; console.log(`PASS ${name}`); }
try {
  await send('Page.enable'); await send('Runtime.enable'); await send('Log.enable');
  await send('Network.enable'); await send('Network.setCacheDisabled', {cacheDisabled: true});
  await send('Emulation.setScriptExecutionDisabled', {value: false});
  await viewport(390, 844);
  await navigate('/');
  if (process.argv.includes('--screenshots-only')) {
    for (const width of [390, 1440]) {
      await viewport(width, width === 390 ? 844 : 1080);
      for (const [path, name] of [['/', 'home'], ['/experiments/model-selection/', 'model-selection'], ['/experiments/human-observations/', 'human-observations'], ['/prereg/', 'prereg']]) {
        await navigate(path); await shot(`${name}-${width}`);
      }
    }
  } else {
    await check('mobile menu exposes its state and closes with Escape', async () => {
      await evaluate(`document.querySelector('[data-menu-toggle]').click()`);
      assert.equal(await evaluate(`document.querySelector('[data-menu-toggle]').getAttribute('aria-expanded')`), 'true');
      assert.equal(await evaluate(`getComputedStyle(document.querySelector('#mobile-navigation')).display`), 'block');
      await send('Input.dispatchKeyEvent', {type: 'keyDown', key: 'Escape', code: 'Escape'});
      assert.equal(await evaluate(`document.querySelector('[data-menu-toggle]').getAttribute('aria-expanded')`), 'false');
      assert.equal(await evaluate(`document.activeElement.matches('[data-menu-toggle]')`), true);
    });
    await check('source link reveals the original article', async () => {
      await evaluate(`document.querySelector('a[href="#original-record"]').click()`);
      await until(`document.querySelector('#original-record').open`);
    });
    await check('old deep link reveals its original heading', async () => {
      await navigate('/#abstract');
      await until(`document.querySelector('#original-record').open`);
      assert.equal(await evaluate(`document.querySelector('#abstract').getClientRects().length > 0`), true);
    });
    await check('glossary link reveals definitions', async () => {
      await viewport(1440, 1080); await navigate('/');
      await evaluate(`document.querySelector('.rail-glossary').click()`);
      await until(`document.querySelector('#reading-glossary').open`);
    });
    await check('page outlines resolve to visible sections', async () => {
      await navigate('/experiments/model-selection/');
      assert.ok(await evaluate(`document.querySelectorAll('[data-outline-links] a').length > 10`));
      assert.equal(await evaluate(`Array.from(document.querySelectorAll('[data-outline-links] a')).every(a => document.getElementById(decodeURIComponent(a.hash.slice(1))))`), true);
    });
    await check('local CSS and JavaScript URLs carry the current build version', async () => {
      await navigate('/');
      const assets = await evaluate(`({css:document.querySelector('link[href*="/assets/css/style.css"]').href,js:document.querySelector('script[src*="/assets/js/app.js"]').src})`);
      assert.match(assets.css, /\/assets\/css\/style\.css\?v=\d+$/);
      assert.match(assets.js, /\/assets\/js\/app\.js\?v=\d+$/);
    });
    await check('model metrics expose accessible exact values', async () => {
      await viewport(1440, 1080); await navigate('/experiments/model-selection/');
      const rows = await evaluate(`Array.from(document.querySelectorAll('.metric-row')).map(row => { const meter=row.querySelector('meter'); const label=row.querySelector(':scope > strong').textContent.trim(); const exact=row.querySelector('.metric-bar b').textContent.trim(); return {label,exact,value:meter.value,max:meter.max,aria:meter.getAttribute('aria-label')}; })`);
      assert.equal(rows.length, 6);
      assert.equal(rows.every(row => row.exact === `${row.value}/${row.max}`), true);
      assert.equal(rows.every(row => row.aria && row.aria.includes(row.label) && row.aria.includes(row.exact)), true);
    });
    for (const width of [320, 390, 768, 1440]) {
      await viewport(width, 1000);
      for (const path of ['/', '/experiments/model-selection/', '/experiments/human-observations/', '/testbed/', '/prereg/', '/limitations/']) {
        await navigate(path);
        await check(`no page overflow: ${width}px ${path}`, async () => {
          const measure = await evaluate(`({inner:innerWidth, scroll:document.documentElement.scrollWidth})`);
          assert.ok(measure.scroll <= measure.inner + 1, JSON.stringify(measure));
        });
        if ([320, 390, 1440].includes(width) && ['/', '/experiments/model-selection/', '/experiments/human-observations/'].includes(path)) await shot(`${path === '/' ? 'home' : path.split('/')[2]}-${width}`);
      }
    }
    await check('no-JS navigation and original text remain available', async () => {
      await send('Emulation.setScriptExecutionDisabled', {value: true}); await viewport(390, 844); await navigate('/');
      assert.equal(await evaluate(`getComputedStyle(document.querySelector('#mobile-navigation')).display`), 'block');
      assert.ok(await evaluate(`document.querySelector('[data-original-content]').textContent.length > 1000`));
      const visibility = await evaluate(`(() => { const header = document.querySelector('.site-header'); const main = document.querySelector('main'); window.scrollTo(0, main.offsetTop + 16); const rect = main.getBoundingClientRect(); return {position:getComputedStyle(header).position, visible:rect.top < innerHeight && rect.bottom > 0}; })()`);
      assert.equal(visibility.position, 'static');
      assert.equal(visibility.visible, true);
      await send('Emulation.setScriptExecutionDisabled', {value: false});
    });
    await check('print exposes the full original text', async () => {
      await navigate('/'); await send('Emulation.setEmulatedMedia', {media: 'print'});
      assert.equal(await evaluate(`document.querySelector('#abstract').checkVisibility()`), true);
      await send('Emulation.setEmulatedMedia', {media: ''});
    });
    await check('no runtime errors', async () => assert.deepEqual(exceptions, []));
  }
  console.log(`${passed} browser checks passed. Screenshots: /tmp/research-ui-shots`);
} finally {
  socket.close(); await fetch(`${debug}/json/close/${target.id}`);
}
