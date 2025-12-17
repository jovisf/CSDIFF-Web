const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.statusCode = 405;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: 'Method not allowed' }));
    return;
  }

  try {
    const { amount, currency = 'usd' } = req.body;

    if (!amount) {
      res.statusCode = 400;
      res.end(JSON.stringify({ error: 'Amount is required' }));
      return;
    }

    const paymentIntent = await stripe.paymentIntents.create({
      amount: Math.round(amount * 100), // Convert to cents
      currency,
    });

    res.statusCode = 200;
    res.end(JSON.stringify({ clientSecret: paymentIntent.client_secret }));

  } catch (error) {
    console.error('Stripe payment intent error:', error);
    res.statusCode = 500;
    res.end(JSON.stringify({ error: 'Internal server error' }));
  }
}

