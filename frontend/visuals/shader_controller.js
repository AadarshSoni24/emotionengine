 // TRAYAM — frontend/visuals/shader_controller.js

export class ShaderController {
  constructor(scene) {
    this.scene = scene;

    this.overlay = scene.add.rectangle(
      0, 0, 800, 600, 0x000000, 0
    ).setOrigin(0).setDepth(999);
  }

  apply(mapped) {
    if (!mapped) return;

    if (mapped.valence === "negative") {
      this.overlay.setFillStyle(0xff0000, 0.15);
    } else if (mapped.valence === "positive") {
      this.overlay.setFillStyle(0x00ffcc, 0.1);
    } else {
      this.overlay.setFillStyle(0x000000, 0);
    }
  }
}

