import { ApiEndpoints, Endpoints } from '@/app/api/types';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  const body = await request.json();
  const res = await fetch(
    `${ApiEndpoints.rating}/${body.id}/${Endpoints.rating}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ratingValue: body.value }),
    },
  );
  if (!res.ok) {
    throw new Error('Failed to fetch data');
  }

  return NextResponse.json({ message: 'succsess' });
}
