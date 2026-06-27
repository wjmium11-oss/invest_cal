const fs = require("fs");
const items = JSON.parse(fs.readFileSync("nutrition-db.json", "utf8"));

// 필요한 것만 골라서 가볍게 만들기
const trimmed = items
  .filter(item => item.foodNm) // 이름 없는 것 제외
  .map(item => ({
    name: item.foodNm,
    ca: parseFloat(item.ca) || 0,      // 칼슘
    fe: parseFloat(item.fe) || 0,      // 철
    vitaRae: parseFloat(item.vitaRae) || 0, // 비타민A
    thia: parseFloat(item.thia) || 0,  // 비타민B1
    ribf: parseFloat(item.ribf) || 0,  // 비타민B2
    nia: parseFloat(item.nia) || 0,    // 나이아신
    vitc: parseFloat(item.vitc) || 0,  // 비타민C
    vitd: parseFloat(item.vitd) || 0   // 비타민D
  }));

fs.writeFileSync("nutrition-search.json", JSON.stringify(trimmed));
console.log(`${trimmed.length}개 정리 완료`);