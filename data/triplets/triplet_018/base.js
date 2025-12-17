import fs from 'fs';
import path from 'path';
const dir = path.join(process.cwd(), 'data');
const file = path.join(dir, 'shipping-rates.json');
export default function handler(req, res) {
  if (req.method !== 'POST') {
    res.statusCode = 405;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: 'Method not allowed' }));
    return;
  }
  const { destination, weight, dimensions } = req.body || {};
  if (!destination || !weight) {
    return res.status(400).json({ error: 'Destination and weight are required' });
  }
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  let existing = [];
  try {
    if (fs.existsSync(file)) {
      const data = fs.readFileSync(file, 'utf8');
      existing = JSON.parse(data);
      if (!Array.isArray(existing)) existing = [];
    }
  } catch (_error) {
    // console.error('Error reading existing rates:', error);
<<<<<<< HEAD
=======

  } catch (error) {
    console.error('Error reading existing rates:', error);
>>>>>>> cursor/fix-errors-and-merge-to-main-8341
=======
>>>>>>> cursor/fix-errors-and-merge-to-main-d3c2
    existing = [];
  }
  
  // Calculate shipping rates based on destination and weight
  const baseRate = 10;
  const weightMultiplier = weight * 0.5;
  const distanceMultiplier = destination === 'US' ? 1 : 1.5;
  const totalRate = Math.round((baseRate + weightMultiplier) * distanceMultiplier * 100) / 100;
  const newRate = {
    id: Date.now().toString(),
    destination,
    weight,
    dimensions,
    rate: totalRate,
    timestamp: new Date().toISOString()
  };
  existing.push(newRate);
  try {
    fs.writeFileSync(file, JSON.stringify(existing, null, 2));
    res.statusCode = 200;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ 
      success: true, 
      rate: totalRate,
      id: newRate.id
    }));
  } catch (_error) {
<<<<<<< HEAD
=======

>>>>>>> cursor/fix-errors-and-merge-to-main-8341
=======
>>>>>>> cursor/fix-errors-and-merge-to-main-d3c2
    // console.error('Error saving shipping rate:', error);
    res.statusCode = 500;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: 'Failed to save rate' }));
  }
}