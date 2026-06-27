// 식약처 영양성분 데이터 전체 받아오기
const SERVICE_KEY = "546daf17e313831463ce22b89f66da60f5bf9af863d969e7344661ec16937901";
const BASE_URL = "https://api.data.go.kr/openapi/tn_pubr_public_health_functional_food_nutrition_info_api";
const PAGE_SIZE = 1000; // 한 번에 1000개씩 받기

async function fetchPage(pageNo) {
  const url = `${BASE_URL}?serviceKey=${SERVICE_KEY}&pageNo=${pageNo}&numOfRows=${PAGE_SIZE}&type=json`;
  const res = await fetch(url);
  const data = await res.json();
  return data.response.body;
}

async function fetchAll() {
  console.log("1페이지 받는 중...");
  const first = await fetchPage(1);
  const total = parseInt(first.totalCount);
  const totalPages = Math.ceil(total / PAGE_SIZE);
  console.log(`전체 ${total}개, ${totalPages}페이지로 나눠 받습니다.`);

  let allItems = [...first.items];

  for (let page = 2; page <= totalPages; page++) {
    console.log(`${page}/${totalPages} 페이지 받는 중...`);
    const data = await fetchPage(page);
    allItems = allItems.concat(data.items);
    await new Promise(r => setTimeout(r, 300)); // 서버 부담 줄이려고 0.3초씩 쉬기
  }

  console.log(`총 ${allItems.length}개 받음. 파일로 저장 중...`);

  const fs = require("fs");
  fs.writeFileSync("nutrition-db.json", JSON.stringify(allItems));

  console.log("완료! nutrition-db.json 파일 생성됨.");
}

fetchAll();