import { Resend } from "resend";

// Direct API key 
const resend = new Resend("re_D9vz8WuA_3nPVvhKTLzM7nLQVGsukn1ts");

export const sendConfirmationEmail = async (to, name) => {
  try {
    const response = await resend.emails.send({
      from: "Herb AI 🌿 <onboarding@resend.dev>", // default sender (works immediately)
      to: [to],
      subject: "Your Contribution has been received 🌿",
      html: `
        <p>Dear ${name || "Contributor"},</p>

        <p>
          Thank you for your herb contribution! We truly appreciate you
          taking the time to share it with us.
        </p>

        <p>
          Our team will carefully review your submission and once approved,
          add it to our herb library.
        </p>

        <p>
          Thanks again for contributing to our growing herb community.
        </p>

        <br/>

        <p>
          Best regards,<br/>
          Herb AI Team 🌿
        </p>
      `,
    });

    console.log("✅ Email sent:", response);
  } catch (error) {
    console.error("❌ Email error:", error);
    throw error; // IMPORTANT: keeps your "must send email" requirement
  }
};