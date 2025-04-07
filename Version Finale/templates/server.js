const express = require("express");
const axios = require("axios");
const cors = require("cors");
const FormData = require("form-data");

const app = express();
app.use(cors());
app.use(express.json());

const STABILITY_API_KEY = "sk-xtvVV4bT5SAKKWRIIeL1IZHxxnOUcFKjYXfmcCSZaX9n8zBn"
app.post("/generate-music", async (req, res) => {
  try {
    if (!req.body.prompt) {
      return res.status(400).json({ error: "Le prompt est requis" });
    }

    console.log("Tentative de génération avec le prompt:", req.body.prompt);

    // Création du payload en FormData
    const formData = new FormData();
    formData.append("prompt", req.body.prompt);
    formData.append("output_format", "mp3");
    formData.append("duration", 30);
    formData.append("steps", 30);

    // Envoi de la requête avec axios.postForm
    const response = await axios.post(
      "https://api.stability.ai/v2beta/audio/stable-audio-2/text-to-audio",
      formData,
      {
        validateStatus: undefined,
        responseType: "arraybuffer",
        headers: {
          Authorization: `Bearer ${STABILITY_API_KEY}`,
          Accept: "audio/*",
        },
      }
    );

    if (response.status !== 200) {
      throw new Error(`${response.status}: ${response.data.toString()}`);
    }

    res.set("Content-Type", "audio/mp3");
    res.send(response.data);

  } catch (error) {
    console.error("Erreur complète:", error.message);
    res.status(500).json({ error: "Erreur lors de la génération", details: error.message });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Serveur démarré sur http://localhost:${PORT}`));
