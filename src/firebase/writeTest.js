import { getDatabase, ref, set } from "firebase/database";
import app from "./firebaseConfig.js";

const db = getDatabase(app);

export function writeTestData() {
  set(ref(db, "session"), {
    emotion: "neutral",
    confidence: 0.5,
    difficulty: 1,
    timestamp: Date.now()
  });

  console.log("Test data written to Firebase");
}
