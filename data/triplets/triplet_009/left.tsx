'use client';
import { useSearchParams } from 'next/navigation';
import { useRef } from 'react';
import { createPortal } from 'react-dom';
import CartModal from '../../ui/modals/CartModal';

export default function Portal() {
  const ref = useRef(document.body);
  const searchParams = useSearchParams();
  const modal = searchParams.get('cart');

  return modal && ref.current ? createPortal(<CartModal />, ref.current) : null;
}
