 // EMOTION → GAME VALUES MAPPING TABLE
// This is the single source of truth. Never scatter this logic anywhere else.

const EMOTION_MAP = {
  stressed: {
    difficulty: { spawnRate: 3000, enemySpeed: 60 },
    music:      { bpm: 72,  key: 'minor' },
    visual:     { filter: 'warm',    intensity: 0.6 },
    npcTone:    'supportive',
    safeMode:   true
  },
  bored: {
    difficulty: { spawnRate: 500,  enemySpeed: 200 },
    music:      { bpm: 180, key: 'aggressive' },
    visual:     { filter: 'neon',    intensity: 1.0 },
    npcTone:    'taunting',
    safeMode:   false
  },
  angry: {
    difficulty: { spawnRate: 2000, enemySpeed: 100 },
    music:      { bpm: 140, key: 'minor' },
    visual:     { filter: 'red',     intensity: 0.8 },
    npcTone:    'empowering',
    safeMode:   false
  },
  happy: {
    difficulty: { spawnRate: 1500, enemySpeed: 120 },
    music:      { bpm: 120, key: 'major' },
    visual:     { filter: 'vibrant', intensity: 0.7 },
    npcTone:    'adventurous',
    safeMode:   false
  },
  fearful: {
    difficulty: { spawnRate: 5000, enemySpeed: 40 },
    music:      { bpm: 40,  key: 'minor' },
    visual:     { filter: 'dark',    intensity: 0.9 },
    npcTone:    'reassuring',
    safeMode:   true
  },
  sad: {
    difficulty: { spawnRate: 4000, enemySpeed: 50 },
    music:      { bpm: 60,  key: 'minor' },
    visual:     { filter: 'blue',    intensity: 0.6 },
    npcTone:    'compassionate',
    safeMode:   false
  },
  neutral: {
    difficulty: { spawnRate: 1500, enemySpeed: 100 },
    music:      { bpm: 100, key: 'neutral' },
    visual:     { filter: 'none',    intensity: 0.0 },
    npcTone:    'normal',
    safeMode:   false
  }
};
export function mapEmotion(emotion) {
  return EMOTION_MAP[emotion] || EMOTION_MAP.neutral;
}

export default EMOTION_MAP;
