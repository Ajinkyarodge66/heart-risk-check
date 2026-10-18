// ---- Model maths (runs fully on the device) ----
function rawScore(M, x) {
  const z = x.map((v, i) => (v - M.mean1[i]) / M.scale1[i]);
  let logit = M.intercept;
  for (let k = 0; k < M.powers.length; k++) {
    const pw = M.powers[k];
    let t = 1;
    for (let j = 0; j < pw.length; j++) if (pw[j]) t *= pw[j] === 1 ? z[j] : Math.pow(z[j], pw[j]);
    logit += M.coef[k] * (t - M.mean2[k]) / M.scale2[k];
  }
  return 1 / (1 + Math.exp(-logit));
}
// values: object keyed by feature name; null for HighBP / HighChol means "not sure"
function scorePerson(M, values) {
  const F = M.features;
  const unknown = ["HighBP", "HighChol"].filter(f => values[f] === null || values[f] === undefined);
  let combos = [{ w: 1, v: Object.assign({}, values) }];
  for (const f of unknown) {
    const prev = M.mean1[F.indexOf(f)];
    combos = combos.flatMap(c => [
      { w: c.w * prev, v: Object.assign({}, c.v, { [f]: 1 }) },
      { w: c.w * (1 - prev), v: Object.assign({}, c.v, { [f]: 0 }) }]);
  }
  let s = 0;
  for (const c of combos) s += c.w * rawScore(M, F.map(f => c.v[f]));
  s = Math.min(Math.max(s, 1e-6), 1 - 1e-6);
  // balanced class weights behave like a 50/50 prior: shift odds back to the real prevalence
  const odds = s / (1 - s) * M.base_rate / (1 - M.base_rate);
  const prob = odds / (1 + odds);
  let lo = 0, hi = M.quantiles.length - 1;
  while (lo < hi) { const mid = (lo + hi) >> 1; if (M.quantiles[mid] < s) lo = mid + 1; else hi = mid; }
  const pct = Math.round(lo / (M.quantiles.length - 1) * 100);
  return { score: s, prob, pct };
}
// linear-model contributions (log-odds, relative to an average respondent)
function contributions(M, values) {
  return M.features.map((f, i) => {
    let v = values[f];
    if (v === null || v === undefined) v = M.ex_mean[i];
    return { f, c: M.ex_coef[i] * (v - M.ex_mean[i]) / M.ex_scale[i] };
  });
}
if (typeof module !== "undefined") module.exports = { rawScore, scorePerson, contributions };
