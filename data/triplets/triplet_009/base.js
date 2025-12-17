import fs from 'fs';
import path from 'path';
const dir = path.join(process.cwd(), 'data');
const file = path.join(dir, 'subscribers.json');
export default function handler(req, res) {
  if (req.method !== 'POST') {
    res.statusCode = 405;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: 'Method not allowed' }));
    return;
  }
  const { email, name, preferences } = req.body || {};
  if (!email) {
    res.statusCode = 400;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: 'Email is required' }));
    return;
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
    // console.error('Error reading existing subscribers:', error);
<<<<<<< HEAD
=======

  } catch (error) {
    console.error('Error reading existing subscribers:', error);
>>>>>>> cursor/fix-errors-and-merge-to-main-8341
=======
>>>>>>> cursor/fix-errors-and-merge-to-main-d3c2
    existing = [];
  }
  
  // Check if email already exists
  const existingSubscriber = existing.find(sub => sub.email === email);
  if (existingSubscriber) {
    res.statusCode = 400;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: 'Email already subscribed' }));
    return;
  }
  const newSubscriber = {
    id: Date.now().toString(),
    email,
    name: name || '',
    preferences: preferences || {},
    timestamp: new Date().toISOString(),
    status: 'active'
  };
  existing.push(newSubscriber);
  try {
    fs.writeFileSync(file, JSON.stringify(existing, null, 2));
    res.statusCode = 200;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ 
      success: true, 
      message: 'Successfully subscribed to newsletter',
      id: newSubscriber.id
    }));
  } catch (_error) {
    // console.error('Error saving subscriber:', error);
<<<<<<< HEAD
=======

>>>>>>> cursor/fix-errors-and-merge-to-main-8341
=======
>>>>>>> cursor/fix-errors-and-merge-to-main-d3c2
    res.statusCode = 500;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: 'Failed to save subscription' }));
  }
}