const fs = require("fs");
const items = JSON.parse(fs.readFileSync("nutrition-db.json", "utf8"));

function search(keyword) {
  return items.filter(item => item.foodNm.includes(keyword));
}

const results = search("마그네슘");
console.log(`"마그네슘" 검색 결과: ${results.length}개`);
results.slice(0, 5).forEach(r => console.log("-", r.foodNm));