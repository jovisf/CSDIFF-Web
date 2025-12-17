export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.statusCode = 405;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: 'Method not allowed' }));
    return;
  }
  try {
    const { name, email, phone, details, country, service } = req.body || {};
    if (!name || !email || !phone || !details) {
      res.statusCode = 400;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({ error: 'Name, email, phone, and details are required' }));
      return;
    }
    // Process quote submission logic here
    // In a real application, you would:
    // 1. Save to your database
    // 2. Send notification to your sales team
    // 3. Send confirmation email to the customer
    // 4. Integrate with your CRM
    const quoteData = {
      name,
      email,
      phone,
      details,
      country: country || 'Not specified',
      service: service || 'General inquiry',
      timestamp: new Date().toISOString(),
      status: 'pending'
    };
    // // console.log('Quote request received:', quoteData);
<<<<<<< HEAD
=======

>>>>>>> cursor/fix-errors-and-merge-to-main-8341
=======
>>>>>>> cursor/fix-errors-and-merge-to-main-d3c2
    res.statusCode = 200;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ 
      success: true, 
      message: 'Quote request submitted successfully',
      quoteId: `quote_${Date.now()}`,
      data: quoteData
    }));
  } catch (_error) {
    // console.error('Quote submission error:', error);
<<<<<<< HEAD
=======
  } catch (error) {
    console.error('Quote submission error:', error);
>>>>>>> cursor/fix-errors-and-merge-to-main-8341
=======
>>>>>>> cursor/fix-errors-and-merge-to-main-d3c2
    res.statusCode = 500;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: 'Internal server error' }));
  }
}
}