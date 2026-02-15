export const sessionSchema = {
  currentEmotion: "neutral",
  confidence: 0,
  gameState: {
    difficulty: 1,
    enemySpawnRate: 1,
    musicBPM: 100
  },
  timestamp: Date.now()
};
