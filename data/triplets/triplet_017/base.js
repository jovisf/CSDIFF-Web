<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> cursor/fix-errors-and-merge-to-main-717a
// Simple email validation function
const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};
async function handler(req, res) {
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
export default function handler(req, res) {
>>>>>>> cursor/fix-errors-and-merge-to-main-3792
=======

export default async function handler(req, res) {

>>>>>>> cursor/fix-errors-and-merge-to-main-529c
=======
>>>>>>> cursor/fix-errors-and-merge-to-main-717a
=======

>>>>>>> cursor/fix-errors-and-merge-to-main-8341
=======

export default async function handler(req, res) {

>>>>>>> cursor/fix-errors-and-merge-to-main-d3c2
=======
// Simple email validation function (currently unused but kept for future use)
// const isValidEmail = (email) => {
//   const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
//   return emailRegex.test(email);
// };

export default async function handler(req, res) {
>>>>>>> cursor/fix-errors-and-merge-to-main-fb5a
  if (req.method !== 'POST') {
    res.statusCode = 405;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: 'Method not allowed' }));
    return;
  }
  try {
    const { email } = req.body || {};
    if (!email) {
      res.statusCode = 400;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({ error: 'Email is required' }));
      return;
    }
    // Simple email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      res.statusCode = 400;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({ error: 'Invalid email format' }));
      return;
    }
    // Save subscription logic here
    // In a real application, you would:
    // 1. Save to your database
    // 2. Add to your email marketing service (Mailchimp, ConvertKit, etc.)
    // 3. Send confirmation email
    console.log('Newsletter subscription:', {
      email: req.body.email,
      timestamp: new Date().toISOString()
    });
<<<<<<< HEAD
<<<<<<< HEAD

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> cursor/fix-errors-and-merge-to-main-3792
=======
    res.statusCode = 200;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ success: true, message: 'Successfully subscribed to newsletter' }));

>>>>>>> cursor/fix-errors-and-merge-to-main-529c
=======
>>>>>>> cursor/fix-errors-and-merge-to-main-717a
=======
>>>>>>> cursor/fix-errors-and-merge-to-main-8341
=======
>>>>>>> cursor/fix-errors-and-merge-to-main-d3c2
=======
>>>>>>> cursor/fix-errors-and-merge-to-main-fb5a
    res.statusCode = 200;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ 
      success: true,
      message: 'Successfully subscribed to newsletter'
    }));
  } catch (error) {
    console.error('Newsletter subscription error:', error);
    res.statusCode = 500;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ 
      error: 'Failed to subscribe to newsletter',
      details: process.env.NODE_ENV === 'development' ? error.message : undefined
    }));
  }
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> cursor/fix-errors-and-merge-to-main-717a
=======
>>>>>>> cursor/fix-errors-and-merge-to-main-d3c2
}

export default handler;
<<<<<<< HEAD
<<<<<<< HEAD
=======
}
>>>>>>> cursor/fix-errors-and-merge-to-main-3792
=======
=======
>>>>>>> cursor/fix-errors-and-merge-to-main-d3c2
}

export default handler;

<<<<<<< HEAD
>>>>>>> cursor/fix-errors-and-merge-to-main-529c
=======
>>>>>>> cursor/fix-errors-and-merge-to-main-717a
=======

>>>>>>> cursor/fix-errors-and-merge-to-main-8341
=======
>>>>>>> cursor/fix-errors-and-merge-to-main-d3c2
=======
}
>>>>>>> cursor/fix-errors-and-merge-to-main-fb5a
