import { test, expect, type Page } from '@playwright/test';
async function open(page:Page) {
 await page.getByRole('button',{name:'메뉴 열기'}).click();
 await expect(page.locator('.sidebar')).toHaveClass(/open/);
 await page.waitForTimeout(400);
}
async function atViewport(page:Page,selector:string) {
 await expect.poll(async()=>{
  const box=await page.locator(selector).boundingBox();
  return !!box && box.y >= 0 && box.y+box.height <= page.viewportSize()!.height+1;
 }).toBe(true);
}
for(const size of [{width:390,height:480},{width:740,height:360}]) {
 test(`작은 높이 메뉴 실제 휠 왕복·하단 백업·상단 선택 ${size.width}x${size.height}`,async({page})=>{
  await page.setViewportSize(size);await page.goto('');await open(page);
  const menu=page.locator('.sidebar');
  expect(await menu.evaluate(el=>el.scrollHeight>el.clientHeight)).toBe(true);
  await page.mouse.move(160,size.height/2);await page.mouse.wheel(0,1400);
  await expect.poll(()=>menu.evaluate(el=>el.scrollTop)).toBeGreaterThan(0);
  await atViewport(page,'.sidebar-bottom button:last-of-type');
  const download=page.waitForEvent('download');
  await page.getByRole('button',{name:'학습 기록 백업',exact:true}).click();
  expect((await download).suggestedFilename()).toBe('bakery-study-backup.json');
  await page.getByRole('button',{name:'데이터 초기화',exact:true}).click();
  await expect(page.getByRole('dialog')).toBeVisible();
  await page.getByRole('button',{name:'돌아가기',exact:true}).click();
  await page.mouse.move(160,size.height/2);await page.mouse.wheel(0,-1600);
  await expect.poll(()=>menu.evaluate(el=>el.scrollTop)).toBe(0);
  await atViewport(page,'nav button:first-child');
  await page.getByRole('navigation').getByRole('button',{name:'학습 대시보드',exact:true}).click();
  await expect(menu).not.toHaveClass(/open/);
  await expect(page.getByRole('heading',{name:'제빵기능사 필기 CBT',exact:true})).toBeVisible();
 });
 test(`모바일 터치 스와이프 왕복 ${size.width}x${size.height}`,async({page,context,browserName},info)=>{
  test.skip(info.project.name!=='mobile'||browserName!=='chromium','Chromium 모바일 CDP 터치 에뮬레이션 전용');
  await page.setViewportSize(size);await page.goto('');await open(page);
  const menu=page.locator('.sidebar');const session=await context.newCDPSession(page);
  async function swipe(from:number,to:number) {
   await session.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:145,y:from}]});
   for(let i=1;i<=16;i++){
    await session.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:145,y:from+(to-from)*i/16}]});
    await page.waitForTimeout(20);
   }
   await session.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
   await page.waitForTimeout(250);
  }
  for(let i=0;i<5;i++)await swipe(size.height-70,75);
  await expect.poll(()=>menu.evaluate(el=>el.scrollTop)).toBeGreaterThan(0);
  await atViewport(page,'.sidebar-bottom button:last-of-type');
  await page.getByRole('button',{name:'데이터 초기화',exact:true}).tap();
  await expect(page.getByRole('dialog')).toBeVisible();
  await page.getByRole('button',{name:'돌아가기',exact:true}).tap();
  for(let i=0;i<5;i++)await swipe(75,size.height-70);
  await expect.poll(()=>menu.evaluate(el=>el.scrollTop)).toBe(0);
  await atViewport(page,'nav button:first-child');
  await page.getByRole('navigation').getByRole('button',{name:'학습 대시보드',exact:true}).tap();
  await expect(menu).not.toHaveClass(/open/);
 });
}
test('글자 확대·높이 변화·상단 배너 없음',async({page})=>{
 await page.setViewportSize({width:390,height:480});await page.goto('');
 await page.addStyleTag({content:'.sidebar {font-size:150%} .sidebar nav button {font-size:1.2em}'});
 await open(page);await page.mouse.move(145,250);await page.mouse.wheel(0,1700);
 await atViewport(page,'.sidebar-bottom button:last-of-type');
 await page.setViewportSize({width:390,height:360});
 await page.mouse.wheel(0,1700);await page.waitForTimeout(200);
 await atViewport(page,'.sidebar-bottom button:last-of-type');
 await page.mouse.wheel(0,-2000);
 await expect.poll(()=>page.locator('.sidebar').evaluate(el=>el.scrollTop)).toBe(0);
 await page.getByRole('navigation').getByRole('button',{name:'학습 대시보드',exact:true}).click();
 await expect(page.locator('.criteria-note')).toHaveCount(0);
 await expect(page.getByLabel('학습 기준')).toHaveCount(0);
});
test('화면별 가로 넘침·상단 안내 없음·메인 시각 검토 자료',async({page},info)=>{
 await page.goto('');
 await expect(page.locator('.criteria-note')).toHaveCount(0);
 await page.screenshot({path:`test-results/${info.project.name}-dashboard.png`,fullPage:true});
 for(const name of ['실전 모의시험','랜덤 문제풀이','오답노트','북마크','학습 통계','문제은행 관리']){
  if(await page.getByRole('button',{name:'메뉴 열기'}).isVisible())await open(page);
  await page.getByRole('navigation').getByRole('button',{name,exact:true}).click();
  await expect(page.locator('.criteria-note')).toHaveCount(0);
  await expect(page.locator('main .notice').filter({hasText:/비공식|검증 대기|잠정 규칙|출제기준 대조/})).toHaveCount(0);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 }
 await page.locator('.source-details summary').click();
 await expect(page.locator('.source-details')).toContainText('공식 규칙 확인 상태: 미확인');
 await page.screenshot({path:`test-results/${info.project.name}-sources.png`,fullPage:true});
});
