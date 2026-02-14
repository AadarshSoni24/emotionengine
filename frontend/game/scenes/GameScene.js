 // TRAYAM — frontend/game/scenes/GameScene.js

import { connectWebSocket } from "../../ws_client.js";
import { mapEmotion } from "../../emotion_mapper.js";
import { EmotionOverlay } from "../../ui/emotion_overlay.js";
import { AudioEngine } from "../../audio/audio_engine.js";
import { ShaderController } from "../../visuals/shader_controller.js";
import { NarrativeOverlay } from "../../ui/narrative_overlay.js";




const CONFIG = {
  playerSpeed: 200,
  enemySpeed: 60,
  spawnRateMs: 1500,
  playerSize: 30,
  enemySize: 25,
  maxHealth: 100
};

export default class GameScene extends Phaser.Scene {
  constructor() {
    super("GameScene");
  }

  create() {

    this.enemySpeedMultiplier = 1.0;
    this.overlay = new EmotionOverlay(this);
    this.audioEngine = new AudioEngine();
    this.shader = new ShaderController(this);
    this.input.once("pointerdown", async () => {
      await this.audioEngine.start();
    });
    this.narrative = new NarrativeOverlay(this);
    window.addEventListener("narrative", (e) => {
      this.narrative.show(e.detail.dialogue);
    });
    window.addEventListener("safe_mode", () => {
  this.physics.pause();
  this.add.text(400, 300, "SAFE MODE", {
    fontSize: "32px",
    color: "#ff4444"
  }).setOrigin(0.5).setDepth(2000);
});

    // Player
    this.player = this.add.rectangle(400, 300, CONFIG.playerSize, CONFIG.playerSize, 0x00ffcc);
    this.physics.add.existing(this.player);

    // Enemies group
    this.enemies = this.physics.add.group();

    // Health
    this.health = CONFIG.maxHealth;

    // Health bar
    this.healthBarBg = this.add.rectangle(100, 20, 200, 20, 0x333333).setOrigin(0, 0.5);
    this.healthBar = this.add.rectangle(100, 20, 200, 20, 0x00ff00).setOrigin(0, 0.5);

    // Controls
    this.cursors = this.input.keyboard.createCursorKeys();
    this.keys = this.input.keyboard.addKeys("W,A,S,D");

    // Spawn enemies loop
    this.time.addEvent({
      delay: CONFIG.spawnRateMs,
      loop: true,
      callback: this.spawnEnemy,
      callbackScope: this
    });

    // Collision
    this.physics.add.overlap(this.player, this.enemies, this.hitPlayer, null, this);

    //websocket
    connectWebSocket((emotionData) => {
      const mapped = mapEmotion(emotionData.emotion);
      this.applyEmotion(mapped);
      this.overlay.update(emotionData.emotion, emotionData.confidence);
      this.audioEngine.react(mapped);
      this.shader.apply(mapped);
    });

  }

  spawnEnemy() {
    const x = Phaser.Math.Between(0, 800);
    const y = Phaser.Math.Between(0, 600);

    const enemy = this.add.rectangle(x, y, CONFIG.enemySize, CONFIG.enemySize, 0xff5555);
    this.physics.add.existing(enemy);

    this.enemies.add(enemy);
  }

  hitPlayer(player, enemy) {
    enemy.destroy();
    this.health -= 5;
    this.updateHealthBar();
  }

  updateHealthBar() {
    const width = 200 * (this.health / CONFIG.maxHealth);
    this.healthBar.width = width;
  }
  applyEmotion(mapped) {
  // Example tuning — adjust only CONFIG‑driven values
  if (!mapped) return;

  if (mapped.intensity === "high") {
    this.enemySpeedMultiplier = 1.4;
  } else if (mapped.intensity === "low") {
    this.enemySpeedMultiplier = 0.8;
  } else {
    this.enemySpeedMultiplier = 1.0;
  }
}


  update() {
    const body = this.player.body;
    body.setVelocity(0);

    // Movement
    if (this.cursors.left.isDown || this.keys.A.isDown) {
      body.setVelocityX(-CONFIG.playerSpeed);
    }
    if (this.cursors.right.isDown || this.keys.D.isDown) {
      body.setVelocityX(CONFIG.playerSpeed);
    }
    if (this.cursors.up.isDown || this.keys.W.isDown) {
      body.setVelocityY(-CONFIG.playerSpeed);
    }
    if (this.cursors.down.isDown || this.keys.S.isDown) {
      body.setVelocityY(CONFIG.playerSpeed);
    }

    // Enemy chase
    this.enemies.getChildren().forEach(enemy => {
      const angle = Phaser.Math.Angle.Between(
        enemy.x,
        enemy.y,
        this.player.x,
        this.player.y
      );

      enemy.body.setVelocity(
  Math.cos(angle) * CONFIG.enemySpeed * this.enemySpeedMultiplier,
  Math.sin(angle) * CONFIG.enemySpeed * this.enemySpeedMultiplier

      );
    });
  }
}
