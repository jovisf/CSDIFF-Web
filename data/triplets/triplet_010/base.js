import fs from 'fs';
import path from 'path';

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> cursor/fix-errors-and-merge-to-main-3792
=======
// Simple wrapper function to replace withSentry
// const withSentry = (handler) => handler;

>>>>>>> cursor/fix-errors-and-merge-to-main-529c
=======
>>>>>>> cursor/fix-errors-and-merge-to-main-717a
=======
>>>>>>> cursor/fix-errors-and-merge-to-main-8341
=======
>>>>>>> cursor/fix-errors-and-merge-to-main-d3c2
=======
>>>>>>> cursor/fix-errors-and-merge-to-main-fb5a
const dir = path.join(process.cwd(), 'data');
const file = path.join(dir, 'onsite-requests.json');

export default function handler(req, res) {
  if (req.method !== 'POST') {
    res.statusCode = 405;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: 'Method not allowed' }));
    return;
  }
  const { name, email, company, phone, message, location } = req.body || {};
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
  } catch {
    existing = [];
  }
  const newRequest = {
    id: Date.now().toString(),
    name,
    email,
    company,
    phone,
    message,
    location,
    timestamp: new Date().toISOString(),
    status: 'pending'
  };
  existing.push(newRequest);
  try {
    fs.writeFileSync(file, JSON.stringify(existing, null, 2));
    res.statusCode = 200;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ 
      success: true,
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> cursor/fix-errors-and-merge-to-main-3792
=======
      message: 'Onsite request submitted successfully',
>>>>>>> cursor/fix-errors-and-merge-to-main-529c
=======
>>>>>>> cursor/fix-errors-and-merge-to-main-717a
=======

>>>>>>> cursor/fix-errors-and-merge-to-main-8341
=======
      message: 'Onsite request submitted successfully',
>>>>>>> cursor/fix-errors-and-merge-to-main-d3c2
=======
      message: 'Onsite request submitted successfully',
>>>>>>> cursor/fix-errors-and-merge-to-main-fb5a
      id: newRequest.id
    }));
  } catch {
    console.error('Error saving onsite request');
    res.statusCode = 500;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: 'Failed to save request' }));
  }
}