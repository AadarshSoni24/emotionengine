export class NarrativeOverlay {
  constructor(scene) {
    this.text = scene.add.text(400, 560, "", {
      fontFamily: "serif",
      fontSize: "18px",
      color: "#ffffff",
      wordWrap: { width: 700 }
    }).setOrigin(0.5).setDepth(1000);
  }

  show(dialogue) {
    this.text.setText(dialogue);

    setTimeout(() => {
      this.text.setText("");
    }, 5000);
  }
}
