const withErrorLogging = (handler) => {
  return async (req, res) => {
    try {
      await handler(req, res);
    } catch (error) {
      console.error('API Error:', error);
      res.statusCode = 500;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({ error: 'Internal server error' }));
    }
  };
};

async function handler(req, res) {
<<<<<<< HEAD
=======

export default function handler(req, res) {
>>>>>>> cursor/fix-errors-and-merge-to-main-8341
=======
>>>>>>> cursor/fix-errors-and-merge-to-main-d3c2
  if (req.method !== 'POST') {
    res.statusCode = 405;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: 'Method not allowed' }));
    return;
  }
<<<<<<< HEAD
<<<<<<< HEAD

  const { amount, currency = 'usd' } = req.body || {};

  if (!amount) {
    res.statusCode = 400;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: 'Amount is required' }));
    return;
  }

  try {
=======

  try {
    const { amount = 100, currency = 'usd' } = req.body || {};
    
>>>>>>> cursor/fix-errors-and-merge-to-main-8341
=======
  try {
    const { amount, currency = 'usd' } = req.body || {};
    if (!amount) {
      res.statusCode = 400;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({ error: 'Amount is required' }));
      return;
    }
>>>>>>> cursor/fix-errors-and-merge-to-main-d3c2
    // Mock payment intent creation
    const paymentIntent = {
      id: `pi_${Date.now()}`,
      amount: Math.round(amount * 100), // Convert to cents
      currency,
      status: 'requires_payment_method',
      created: Math.floor(Date.now() / 1000)
<<<<<<< HEAD
=======
      status: 'requires_payment_method'
>>>>>>> cursor/fix-errors-and-merge-to-main-8341
=======
>>>>>>> cursor/fix-errors-and-merge-to-main-d3c2
    };
    
    res.statusCode = 200;
<<<<<<< HEAD
<<<<<<< HEAD
    res.json({ paymentIntent });
<<<<<<< HEAD
  } catch (error) {
=======
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ paymentIntent }));
  } catch (error) {
    console.error('Payment intent creation error:', error);
>>>>>>> cursor/fix-errors-and-merge-to-main-8341
=======
    res.json({ paymentIntent });
  } catch (_error) {
>>>>>>> cursor/fix-errors-and-merge-to-main-d3c2
=======
  } catch (_error) {
>>>>>>> cursor/fix-errors-and-merge-to-main-fb5a
    res.statusCode = 500;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: 'Failed to create payment intent' }));
  }
}

<<<<<<< HEAD
export default withErrorLogging(handler);
<<<<<<< HEAD
=======
>>>>>>> cursor/fix-errors-and-merge-to-main-8341
=======
>>>>>>> cursor/fix-errors-and-merge-to-main-d3c2
