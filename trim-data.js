const fs = require("fs");
const items = JSON.parse(fs.readFileSync("nutrition-db.json", "utf8"));

function parseTimes(s){
  const n = parseInt(String(s).replace(/[^0-9]/g, ""));
  return (!n || n < 1) ? 1 : n;
}

const trimmed = items
  .filter(item => item.foodNm)
  .map(item => ({
    name: item.foodNm,
    times: parseTimes(item.onetmIntkNmtm), // 권장 횟수 (기본값으로만 씀, 곱하지 않음)
    ca:      parseFloat(item.ca) || 0,      // 1회분량 그대로
    fe:      parseFloat(item.fe) || 0,
    vitaRae: parseFloat(item.vitaRae) || 0,
    thia:    parseFloat(item.thia) || 0,
    ribf:    parseFloat(item.ribf) || 0,
    nia:     parseFloat(item.nia) || 0,
    vitc:    parseFloat(item.vitc) || 0,
    vitd:    parseFloat(item.vitd) || 0
  }));

fs.writeFileSync("nutrition-search.json", JSON.stringify(trimmed));
console.log(`${trimmed.length}개 정리 완료`);