// Checks the JavaScript model gives the same answers as scikit-learn.  Run: node web/test_parity.js
const fs = require("fs"), path = require("path");
const { rawScore } = require("./core.js");
const root = path.join(__dirname, "..");
const M = JSON.parse(fs.readFileSync(path.join(root, "model/model_global.json")));
const rows = fs.readFileSync(path.join(root, "model/parity_sample.csv"), "utf8").trim().split("\n");
const head = rows[0].split(",");
let worst = 0;
for (const line of rows.slice(1)) {
  const v = line.split(",").map(Number), o = {};
  head.forEach((k, i) => (o[k] = v[i]));
  worst = Math.max(worst, Math.abs(rawScore(M, M.features.map(f => o[f])) - o.p));
}
console.log(worst < 1e-9 ? "PASS" : "FAIL", "max difference:", worst);
process.exit(worst < 1e-9 ? 0 : 1);
