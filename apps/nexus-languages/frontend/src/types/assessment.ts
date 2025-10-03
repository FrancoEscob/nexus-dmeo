export type AssessmentScores = {
  overall: number;
  accuracy: number;
  fluency: number;
  completeness: number;
  prosody: number;
};

export type WordTiming = { start: number; end: number };

export type WordResult = { text: string; accuracy: number; timing?: WordTiming };

export type FeedbackCard = { title: string; body: string; type: "tip" | "info" | "warning" };

export type AssessmentResponse = {
  scores: AssessmentScores;
  words: WordResult[];
  feedback: FeedbackCard[];
  metadata: { engine: string; duration_ms?: number | null; locale?: string | null };
};
