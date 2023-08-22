import cloudinary from 'cloudinary';

// Configure Cloudinary
cloudinary.v2.config({
  cloud_name: process.env.NEXT_PUBLIC_CLOUDINARY_CLOUDNAME,
  api_key: process.env.NEXT_PUBLIC_CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET,
  secure: true,
});

// Save the api_secret in a separate variable
const apiSecret = cloudinary.v2.config().api_secret;

export async function getSignature() {
  const timestamp = Math.floor(Date.now() / 1000); // Use seconds since epoch
  const folder = 'next';

  const signature = cloudinary.utils.api_sign_request(
    {
      timestamp,
      folder,
    },
    apiSecret
  );

  return { timestamp, signature };
}

export async function saveToDatabase({ public_id, version, signature }) {
  // Verify the data
  const expectedSignature = cloudinary.utils.api_sign_request(
    { public_id, version },
    apiSecret
  );

  if (expectedSignature === signature) {
    // Safe to write to the database
    console.log({ public_id });
  }
}
