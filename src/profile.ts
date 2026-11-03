export const PROFILE = {
  name: "제빵기능사", slug: "Craftsman-Bakery-CBT",
  rulesVerificationStatus: "pending-official-access",
  exam: { subjects: ["빵류 재료, 제조 및 위생관리"] as const,
    questionCount: 60, durationMinutes: 60, choiceCount: 4, passScore: 60,
    hasSubjectCutoff: false, selectionPolicy: "통합 무작위 학습용 추출, 공식 단원별 분포 아님" },
  storageNamespace: "Craftsman-Bakery-CBT:v1",
} as const;
