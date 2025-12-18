import { Endpoints } from '@/app/api/types';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const res = await fetch(
      `${process.env.API_URL}${Endpoints.beer}/${body.id}/${Endpoints.rating}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ratingValue: body.value }),
      },
    );
    if (!res.ok) {
      throw new Error('Failed to fetch data');
    }

    console.log('res', await res.json());

    return NextResponse.json({ message: 'succsess' });
  } catch (error) {
    console.log(`Something went wrong: ${error}`);
    throw new Error();
  }
}
