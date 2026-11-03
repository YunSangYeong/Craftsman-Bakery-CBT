import { describe, expect, it } from 'vitest';
import { BASE_BANK as bank, fingerprint, validateQuestion } from '../src/model';
// Independent numeric path: JS IEEE-754 arithmetic versus Python Decimal generation.
const evaluate: Record<string, (v:number[])=>number> = {
 ingredient:([f,p])=> f/100*p,
 hydration:([f,w])=> w*100/f,
 flour:([w,p])=> w/(p/100),
 dough:([f,w,o])=>f+f*w/100+f*o/100,
 scale:([f,old,count])=>f/old*count,
 divide:([mass,count])=>mass/count,
 baked:([mass,p])=>mass-mass*p/100,
 lossRate:([before,after])=>100-100*after/before,
 requiredDough:([after,p])=>after/(1-p/100),
 usable:([mass,p])=>mass*(1-p/100),
 yeast:([mass,factor])=>mass/factor,
 solution:([mass,p])=>mass*p/100,
 addedWater:([f,p,liquid,water])=>(f*p-liquid*water)/100,
 eggWater:([mass,p])=>mass*p/100,
 fat:([mass,p])=>mass*p/100,
 capacity:([pans,each,runs])=>each*runs*pans,
 energy:([power,minutes])=>minutes/60*power,
 cost:([price,grams])=>grams/1000*price,
 elapsed:(v)=>v.reduce((sum,x)=>sum+x,0),
 volume:([volume,mass])=>volume/mass,
};
function rounded(x:number) {return Math.round((x+Number.EPSILON*Math.max(1,Math.abs(x)))*100)/100;}
describe('제빵 자체 제작 은행의 등록·중복·권리·검토 범위',()=>{
 it('실제 기본 등록은 내부 검토 1000개, 개념 80·변형 920이며 기출 연도를 만들지 않는다',()=>{
  expect(bank).toHaveLength(1000);
  expect(new Set(bank.map(q=>q.id)).size).toBe(1000);
  expect(new Set(bank.map(fingerprint)).size).toBe(1000);
  expect(bank.filter(q=>!q.family)).toHaveLength(80);
  expect(bank.filter(q=>q.family)).toHaveLength(920);
  expect(new Set(bank.filter(q=>q.family).map(q=>q.family)).size).toBe(20);
  for(const q of bank){
   expect(()=>validateQuestion(q)).not.toThrow();
   expect(q.type).toBe('original');expect(q.year).toBeNull();expect(q.session).toBeNull();
   expect(q.verificationStatus).toBe('reviewed');expect(q.rights).toContain('CC BY 4.0');
   expect(q.explanation.length).toBeGreaterThan(30);
   expect(q.reviewNote).toContain('외부 전문가');
  }
 });
 it('각 family의 조건 조합은 46개이며 학습 다양성 수와 변형 수를 구분한다',()=>{
  for(const family of new Set(bank.filter(q=>q.family).map(q=>q.family))){
   const items=bank.filter(q=>q.family===family);
   expect(items).toHaveLength(46);
   expect(new Set(items.map(q=>JSON.stringify(q.calculation?.values))).size).toBe(46);
  }
 });
 for(const q of bank.filter(q=>q.calculation)) it(`독립 수치·단위·정답 검증 ${q.id}`,()=>{
  const c=q.calculation!;
  const value=evaluate[c.kind](c.values);
  expect(Number.isFinite(value)).toBe(true);
  expect(rounded(value)).toBeCloseTo(c.result,8);
  expect(c.result).toBeGreaterThan(0);
  expect(q.choices[q.answer-1]).toBe(`${c.result} ${c.unit}`);
  // Parse all options: exactly one numerically equivalent answer, not just unique strings.
  expect(q.choices.filter(choice=>Number(choice.split(' ')[0])===c.result)).toHaveLength(1);
  for(const choice of q.choices) expect(choice.endsWith(` ${c.unit}`)).toBe(true);
  expect(q.explanation).toContain(`${c.result} ${c.unit}`);
 });
});
