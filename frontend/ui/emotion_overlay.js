 // TRAYAM — frontend/ui/emotion_overlay.js

export class EmotionOverlay {
  constructor(scene) {
    this.text = scene.add.text(10, 40, "Emotion: —", {
      fontFamily: "monospace",
      fontSize: "16px",
      color: "#ffffff"
    }).setDepth(1000);
  }

  update(emotion, confidence) {
    this.text.setText(`Emotion: ${emotion} (${Math.round(confidence * 100)}%)`);
  }
}
