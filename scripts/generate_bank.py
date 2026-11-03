"""Deterministic authored bakery exercises. Decimal generation, independent TS validation.
No scraped questions, source years or sessions. No random generation.
"""
from decimal import Decimal as D, ROUND_HALF_UP
from pathlib import Path
import json, csv, hashlib
ROOT=Path(__file__).resolve().parents[1]
SOURCE='https://github.com/YunSangYeong/Craftsman-Bakery-CBT/blob/main/docs/question-review.md'
SUBJECT='빵류 재료, 제조 및 위생관리'
def base(id,topic,question,choices,answer,explanation):
 return dict(id=id,subject=SUBJECT,topic=topic,question=question,choices=choices,answer=answer,explanation=explanation,difficulty='하',year=None,session=None,type='original',sourceUrl=SOURCE,verificationStatus='reviewed',reviewNote='AI 자체 작성·내부 문장 검토. 외부 교재·기출 원문 인용 없음. 외부 전문가 검수 및 공식 출제기준 대조 미실시.',version='main',rights='자체 제작 학습자료 · CC BY 4.0 · Craftsman-Bakery-CBT contributors 표기 및 변경 표시. 외부 자료의 권리는 포함하지 않음.')
bank=[]
for n,line in enumerate((ROOT/'scripts/concepts.tsv').read_text().splitlines(),1):
 topic,q,a,b,c,d,ex=line.split('|')
 choices=[a,b,c,d]; offset=n%4; choices=choices[offset:]+choices[:offset]
 bank.append(base(f'BAK-C-{n:03}',topic,q,choices,choices.index(a)+1,ex))
for family in range(1,21):
 for n in range(1,47):
  # Values and all arithmetic are Decimal; no binary rounding in generator.
  a=D(800+n*20); b=D(50+n%11); c=D(100+n*5)
  if family==1:
   kind='ingredient';v=[a,b];r=a*b/100;unit='g';topic='배합 계산';q=f'밀가루 {a} g에 대해 설탕을 베이커스 퍼센트 {b}%로 넣는다. 필요한 설탕 질량은?';formula=f'재료 질량 = 밀가루 × 백분율 ÷ 100 = {a} × {b} ÷ 100'
  elif family==2:
   kind='hydration';v=[a,c];r=c/a*100;unit='%';topic='배합 계산';q=f'밀가루 {a} g과 물 {c} g만으로 반죽한다. 물의 베이커스 퍼센트는?';formula=f'물 비율 = 물 ÷ 밀가루 × 100 = {c} ÷ {a} × 100'
  elif family==3:
   kind='flour';v=[a,b];r=a*100/b;unit='g';topic='배합 계산';q=f'물 {a} g이 밀가루 질량의 {b}%인 배합에서 필요한 밀가루 질량은?';formula=f'밀가루 = 물 × 100 ÷ 물 비율 = {a} × 100 ÷ {b}'
  elif family==4:
   kind='dough';v=[a,b,D(8)];r=a*(100+b+8)/100;unit='g';topic='배합 계산';q=f'밀가루 {a} g, 물 {b}%, 기타 재료 합계 8%인 배합이다. 모든 %는 밀가루 기준이며 손실은 없다. 총 반죽 질량은?';formula=f'총 반죽 = 밀가루 × (100 + 물 비율 + 기타 비율) ÷ 100 = {a} × (100 + {b} + 8) ÷ 100'
  elif family==5:
   kind='scale';v=[a,D(12),D(15+n)];r=a*v[2]/12;unit='g';topic='생산 계산';q=f'{12}개 생산 배합의 밀가루가 {a} g이다. 동일 크기 {v[2]}개 생산에 필요한 밀가루는? 손실은 무시한다.';formula=f'확대 질량 = 원래 질량 × 목표 수량 ÷ 원래 수량 = {a} × {v[2]} ÷ 12'
  elif family==6:
   kind='divide';v=[a,D(10+n)];r=a/v[1];unit='g';topic='생산 계산';q=f'반죽 {a} g을 손실 없이 같은 질량 {v[1]}개로 분할한다. 한 개의 반죽 질량은?';formula=f'한 개 질량 = 총 반죽 ÷ 개수 = {a} ÷ {v[1]}'
  elif family==7:
   kind='baked';v=[a,D(8+n%8)];r=a*(100-v[1])/100;unit='g';topic='굽기 손실 계산';q=f'굽기 전 반죽 {a} g의 질량 손실률이 {v[1]}%이다. 정해진 냉각 시점의 빵 질량은?';formula=f'굽기 후 질량 = 굽기 전 질량 × (100 − 손실률) ÷ 100 = {a} × (100 − {v[1]}) ÷ 100'
  elif family==8:
   kind='lossRate';v=[a,a-D(40+n)];r=(v[0]-v[1])/v[0]*100;unit='%';topic='굽기 손실 계산';q=f'굽기 전 반죽 {a} g, 정해진 냉각 시점의 빵 {v[1]} g이다. 굽기 전 질량 기준 손실률은?';formula=f'손실률 = (전 질량 − 후 질량) ÷ 전 질량 × 100 = ({a} − {v[1]}) ÷ {a} × 100'
  elif family==9:
   kind='requiredDough';v=[a,D(10+n%6)];r=a*100/(100-v[1]);unit='g';topic='굽기 손실 계산';q=f'냉각 후 빵 {a} g을 얻고 싶다. 굽기 전 질량 기준 손실률이 {v[1]}%일 때 필요한 반죽 질량은?';formula=f'필요 반죽 = 목표 빵 질량 × 100 ÷ (100 − 손실률) = {a} × 100 ÷ (100 − {v[1]})'
  elif family==10:
   kind='usable';v=[a,D(3+n%7)];r=a*(100-v[1])/100;unit='g';topic='생산 계산';q=f'필링 원료 {a} g에서 손질 손실이 원료 질량의 {v[1]}% 발생했다. 사용할 수 있는 질량은?';formula=f'가용 질량 = 원료 × (100 − 손질 손실률) ÷ 100 = {a} × (100 − {v[1]}) ÷ 100'
  elif family==11:
   kind='yeast';v=[D(30+n),D(3)];r=v[0]/v[1];unit='g';topic='배합 계산';q=f'제품 지침에서 생효모 3 g을 인스턴트 효모 1 g으로 환산하도록 정했다. 생효모 {v[0]} g을 대체할 인스턴트 효모는? 이 문제의 지침에 한한다.';formula=f'대체 효모 = 생효모 질량 ÷ 주어진 환산계수 = {v[0]} ÷ 3. 실제 제품에서는 제조사의 지침을 확인한다'
  elif family==12:
   kind='solution';v=[a,D(2+n%9)];r=a*v[1]/100;unit='g';topic='배합 계산';q=f'소금물 총 질량 {a} g에서 소금의 질량분율이 {v[1]}%이다. 소금 질량은? 베이커스 퍼센트가 아니다.';formula=f'소금 = 용액 총 질량 × 질량분율 ÷ 100 = {a} × {v[1]} ÷ 100'
  elif family==13:
   kind='addedWater';v=[a,D(60),c,D(80)];r=a*D('0.60')-c*D('0.80');unit='g';topic='수분 보정 계산';q=f'밀가루 {a} g에 총 수분을 밀가루의 60%로 맞춘다. 수분 함량이 질량 기준 80%인 액상 재료 {c} g을 넣는다. 다른 수분원이 없을 때 추가할 물은?';formula=f'추가 물 = 목표 수분 − 액상 재료의 수분 = {a} × 60 ÷ 100 − {c} × 80 ÷ 100'
  elif family==14:
   kind='eggWater';v=[c,D(75)];r=c*D('0.75');unit='g';topic='수분 보정 계산';q=f'이 배합 계산에서는 전란의 수분 함량을 질량 기준 75%로 가정한다. 전란 {c} g에 들어 있는 수분은? 실제 재료는 성분표를 확인한다.';formula=f'수분 질량 = 전란 질량 × 주어진 수분율 ÷ 100 = {c} × 75 ÷ 100'
  elif family==15:
   kind='fat';v=[c,D(82)];r=c*D('0.82');unit='g';topic='배합 계산';q=f'성분표에서 지방 함량이 질량 기준 82%인 버터 {c} g을 사용한다. 버터로 공급되는 지방 질량은?';formula=f'지방 질량 = 버터 질량 × 표시 지방 비율 ÷ 100 = {c} × 82 ÷ 100'
  elif family==16:
   kind='capacity';v=[D(4+n),D(12),D(3)];r=v[0]*v[1]*v[2];unit='개';topic='생산 계산';q=f'한 번에 팬 {v[0]}장, 팬당 빵 12개를 굽는다. 동일 조건으로 3번 구웠고 불량이 없으면 총 생산 수량은?';formula=f'총 생산 = 팬 수 × 팬당 개수 × 굽기 횟수 = {v[0]} × 12 × 3'
  elif family==17:
   kind='energy';v=[D(2+n%5),D(20+n)];r=v[0]*v[1]/60;unit='kWh';topic='설비 계산';q=f'소비 전력이 일정하게 {v[0]} kW인 설비를 {v[1]}분 사용했다. 대기 전력 등은 무시한다. 소비 전력량은?';formula=f'전력량 = 전력 × 시간(h), 60분 = 1시간이므로 {v[0]} × {v[1]} ÷ 60'
  elif family==18:
   kind='cost';v=[D(1000+n*50),c];r=v[0]*v[1]/1000;unit='원';topic='원가 계산';q=f'1 kg에 {v[0]}원인 밀가루를 {c} g 사용했다. 단순 재료비는? 세금·폐기·부대비용은 고려하지 않는다.';formula=f'재료비 = kg당 가격 × 사용 g ÷ 1000 = {v[0]} × {c} ÷ 1000'
  elif family==19:
   kind='elapsed';v=[D(25+n),D(8+n%5),D(35+n)];r=sum(v);unit='분';topic='공정 시간 계산';q=f'1차 발효 {v[0]}분, 중간 휴지 {v[1]}분, 2차 발효 {v[2]}분을 순서대로 진행한다. 다른 공정 시간은 제외할 때 세 단계의 합계 시간은?';formula=f'총 시간 = 1차 + 휴지 + 2차 = {v[0]} + {v[1]} + {v[2]}'
  else:
   kind='volume';v=[D(600+n*20),D(150+n*2)];r=v[0]/v[1];unit='mL/g';topic='품질 계산';q=f'빵 부피가 {v[0]} mL, 질량이 {v[1]} g이다. 단위 질량당 부피인 비체적은?';formula=f'비체적 = 부피 ÷ 질량 = {v[0]} ÷ {v[1]}'
  rounded=r.quantize(D('0.01'),rounding=ROUND_HALF_UP)
  def fmt(x):return format(x.normalize(),'f')
  step=max(D('1'),(rounded*D('0.10')).quantize(D('0.01'),rounding=ROUND_HALF_UP))
  options=[rounded,rounded+step,rounded+step*2,rounded+step*3]
  offset=n%4;options=options[offset:]+options[:offset]
  choices=[f'{fmt(x)} {unit}' for x in options]
  # Korean explanation, including explicit unit and rounding policy.
  ex=f'{formula}. 계산 결과는 {fmt(rounded)} {unit}이다. 단위는 {unit}이며, 계산 중에는 반올림하지 않고 최종 결과만 소수 둘째 자리까지 일반 반올림한다.'
  q+=' 최종 결과는 소수 둘째 자리까지 일반 반올림한다(불필요한 0 생략).'
  item=base(f'BAK-N-{family:02}-{n:03}',topic,q,choices,options.index(rounded)+1,ex)
  item.update(family=f'BAK-F{family:02}',calculation=dict(kind=kind,values=[float(x) for x in v],result=float(rounded),unit=unit,precision=2))
  item['reviewNote']='자체 제작 계산 조건 변형. 명시된 가정·식·단위·보기·해설을 내부 검토. Python Decimal 생성과 별도 TypeScript 공식으로 재계산. 실제 시험 분포나 제품별 권장 배합이 아님. 외부 전문가 검수·공식 출제기준 대조 미실시.'
  bank.append(item)
assert len(bank)==1000
ids={x['id'] for x in bank}; assert len(ids)==1000
fingerprints={''.join((x['question']+'|'+ '|'.join(sorted(x['choices']))).split()) for x in bank}; assert len(fingerprints)==1000
out=ROOT/'src/data/questions.json';out.write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n')
# Import examples are local pending questions, not counted in the base bank.
example={**bank[0],'id':'LOCAL-EXAMPLE','verificationStatus':'pending'}
example['question']='[로컬 등록 예시] '+bank[0]['question']
(ROOT/'public/templates/questions.json').write_text(json.dumps([example],ensure_ascii=False,indent=2)+'\n')
flat={k:v for k,v in example.items() if k!='choices'}
flat.update({f'choice{i+1}':v for i,v in enumerate(example['choices'])})
with (ROOT/'public/templates/questions.csv').open('w',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=list(flat),lineterminator="\n");writer.writeheader();writer.writerow(flat)
print('registered:',len(bank),'concepts: 80; numeric variants: 920; families: 20')
print('sha256:',hashlib.sha256(out.read_bytes()).hexdigest())
