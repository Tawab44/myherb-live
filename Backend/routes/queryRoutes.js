import express from "express";
import Query from "../models/Query.js";
import { sendConfirmationEmail } from "../utils/sendEmail.js";

const router = express.Router();

/* POST Query (N IMG) */
router.post("/", async (req, res) => {
  try {
    const query = new Query({
      commonName: req.body.commonName,
      scientificName: req.body.scientificName,
      partUsed: req.body.partUsed,
      properties: req.body.properties,
      source: req.body.source,
      missingStatus: req.body.missingStatus,
      notes: req.body.notes,
      contributorName: req.body.contributorName,
      email: req.body.email,
      permission: req.body.permission,
      imageUrl: null, //  n image 
    });

    await query.save();

    await sendConfirmationEmail(
      req.body.email,
      req.body.contributorName
    );

    res.status(201).json({
      message: "Submission successful 🌿 Email sent!",
    });

  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Submission failed" });
  }
});

export default router;