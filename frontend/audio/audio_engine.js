 // TRAYAM — frontend/audio/audio_engine.js



export class AudioEngine {
  constructor() {
    this.synth = new Tone.Synth().toDestination();
  }

  async start() {
    await Tone.start();
    console.log("Audio started");
  }

  react(mapped) {
    if (!mapped) return;

    if (mapped.intensity === "high") {
      this.synth.triggerAttackRelease("C5", "8n");
    } else if (mapped.intensity === "low") {
      this.synth.triggerAttackRelease("C3", "8n");
    } else {
      this.synth.triggerAttackRelease("C4", "8n");
    }
  }
}

